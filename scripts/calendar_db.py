#!/usr/bin/env python3
"""Banco local (SQLite) do calendario economico. Uso: python scripts/calendar_db.py <comando> [...]

Comandos:
  init                              cria o banco
  upsert ARQUIVO.json               grava/atualiza eventos (lista de objetos)
  upsert-news ARQUIVO.json          grava noticias (exige data/hora de publicacao)
  window                            mostra a janela de informacao de agora
  news [--hours N] [--max-tier 2]   lista noticias DENTRO da janela (padrao) por nivel de fonte
  today [--date AAAA-MM-DD] [--min-stars N]   lista eventos do dia
  set-actual --date D --time HH:MM --event NOME --actual VALOR   grava o realizado e calcula a surpresa
  add-reaction --date D --time HH:MM --event NOME --before P --m5 P --m15 P --m60 P   reacao do NAS100 ao evento
Banco padrao: data/calendario.db (variavel CAL_DB ou --db para mudar). Fonte dos dados: Investing (via extensao).
"""
import argparse, json, os, re, sqlite3, sys
from datetime import datetime, timedelta, timezone

DB_DEFAULT = os.environ.get("CAL_DB", os.path.join(os.path.dirname(__file__), "..", "data", "calendario.db"))
SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL, time_brt TEXT NOT NULL, country TEXT NOT NULL, event TEXT NOT NULL,
  stars INTEGER, category TEXT, actual TEXT, forecast TEXT, previous TEXT, preview TEXT,
  surprise REAL, relevant_nas INTEGER DEFAULT 1, notes TEXT,
  source TEXT DEFAULT 'investing', captured_at TEXT, updated_at TEXT,
  UNIQUE(date, time_brt, country, event)
);
CREATE TABLE IF NOT EXISTS news (
  id INTEGER PRIMARY KEY,
  published_at TEXT NOT NULL, captured_at TEXT, headline TEXT NOT NULL, source TEXT NOT NULL, tier INTEGER,
  url TEXT, category TEXT, impact_nas TEXT, confidence TEXT, persistence TEXT, verified_by TEXT, notes TEXT,
  UNIQUE(source, headline, published_at)
);
CREATE TABLE IF NOT EXISTS reactions (
  event_id INTEGER PRIMARY KEY REFERENCES events(id),
  nas_before REAL, nas_5m REAL, nas_15m REAL, nas_60m REAL, recorded_at TEXT
);
"""

def num(v):
    """'3,4%' -> 3.4 ; '-132,60B' -> -132.6 ; vazio -> None"""
    if v is None: return None
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(v).replace("−", "-"))
    return float(m.group(0).replace(",", ".")) if m else None

def surprise(actual, forecast):
    a, f = num(actual), num(forecast)
    return None if a is None or f is None else round(a - f, 4)

def connect(path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    con = sqlite3.connect(path); con.row_factory = sqlite3.Row
    con.executescript(SCHEMA); return con

def now(): return datetime.now().isoformat(timespec="seconds")

def cmd_upsert(con, a):
    events = json.load(open(a.file, encoding="utf-8"))
    for e in events:
        s = surprise(e.get("actual"), e.get("forecast"))
        con.execute("""INSERT INTO events(date,time_brt,country,event,stars,category,actual,forecast,previous,preview,
                       surprise,relevant_nas,notes,source,captured_at,updated_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(date,time_brt,country,event) DO UPDATE SET
                       stars=excluded.stars, category=COALESCE(excluded.category,category),
                       actual=COALESCE(excluded.actual,actual), forecast=COALESCE(excluded.forecast,forecast),
                       previous=COALESCE(excluded.previous,previous), preview=COALESCE(excluded.preview,preview),
                       surprise=COALESCE(excluded.surprise,surprise), updated_at=excluded.updated_at""",
                    (e["date"], e["time_brt"], e.get("country", "US"), e["event"], e.get("stars"), e.get("category"),
                     e.get("actual"), e.get("forecast"), e.get("previous"), e.get("preview"), s,
                     e.get("relevant_nas", 1), e.get("notes"), e.get("source", "investing"), now(), now()))
    con.commit(); print(f"{len(events)} evento(s) gravado(s)")

def cmd_today(con, a):
    d = a.date or datetime.now().strftime("%Y-%m-%d")
    rows = con.execute("SELECT * FROM events WHERE date=? AND COALESCE(stars,0)>=? AND relevant_nas=1 ORDER BY time_brt",
                       (d, a.min_stars)).fetchall()
    if not rows: print(f"Sem eventos gravados para {d} (calendario nao capturado?). Regra: sem calendario, sem sinal."); return
    print(f"Calendario {d} (BRT)  estrelas>={a.min_stars}")
    for r in rows:
        print(f"{r['time_brt']} {r['country']} {'*'*(r['stars'] or 0):<3} {r['event']} | atual={r['actual']} proj={r['forecast']} ant={r['previous']} surpresa={r['surprise']}")

BRT = timezone(timedelta(hours=-3))  # Brasilia: sem horario de verao desde 2019 (evita depender de banco de fusos no Windows)

def now_brt():
    v = os.environ.get("CAL_NOW")  # so para testes: CAL_NOW=2026-09-28T10:00:00-03:00
    return datetime.fromisoformat(v).astimezone(BRT) if v else datetime.now(BRT)

def parse_ts(s):
    dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("data/hora sem fuso")
    return dt.astimezone(BRT)

def window_start(n):
    """Dom/Seg (e sab): desde sexta 16:00 BRT. Ter-Sex: ultimas 24 h."""
    wd = n.weekday()  # seg=0 ... dom=6
    if wd in (5, 6, 0):
        back = {0: 3, 6: 2, 5: 1}[wd]
        return (n - timedelta(days=back)).replace(hour=16, minute=0, second=0, microsecond=0), "desde sexta-feira 16:00 BRT"
    return n - timedelta(hours=24), "ultimas 24 horas"

def cmd_window(con, a):
    n = now_brt(); start, label = window_start(n)
    print(f"Agora: {n:%Y-%m-%d %H:%M} BRT | janela: {label} | inicio: {start:%Y-%m-%d %H:%M} BRT")

def cmd_upsert_news(con, a):
    n = now_brt(); start, _ = window_start(n)
    items = json.load(open(a.file, encoding="utf-8"))
    for it in items:
        try:
            ts = parse_ts(it.get("published_at"))
        except Exception:
            sys.exit(f"REJEITADA (sem data/hora com fuso): {it.get('headline')}")
        if ts < start:
            print(f"aviso: fora da janela ({ts:%Y-%m-%d %H:%M} BRT), gravada so como historico: {it['headline']}")
        con.execute("""INSERT OR IGNORE INTO news(published_at,captured_at,headline,source,tier,url,category,impact_nas,
                       confidence,persistence,verified_by,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (ts.isoformat(timespec="minutes"), now(), it["headline"], it["source"], it.get("tier"), it.get("url"),
                     it.get("category"), it.get("impact_nas"), it.get("confidence"), it.get("persistence"),
                     it.get("verified_by"), it.get("notes")))
    con.commit(); print(f"{len(items)} noticia(s) processada(s)")

def cmd_news(con, a):
    n = now_brt()
    start, label = (n - timedelta(hours=a.hours), f"ultimas {a.hours} h") if a.hours else window_start(n)
    rows = [r for r in con.execute("SELECT * FROM news WHERE COALESCE(tier,9)<=?", (a.max_tier,)).fetchall()
            if parse_ts(r["published_at"]) >= start]
    rows.sort(key=lambda r: parse_ts(r["published_at"]), reverse=True)
    print(f"Janela: {label} (inicio {start:%Y-%m-%d %H:%M} BRT; agora {n:%Y-%m-%d %H:%M})")
    if not rows:
        print("Nenhuma noticia DENTRO da janela. Nao usar noticia mais antiga. Sem noticias capturadas = sem sinal."); return
    for r in rows:
        ts = parse_ts(r["published_at"]); age = (n - ts).total_seconds() / 3600
        print(f"{ts:%Y-%m-%d %H:%M} BRT (ha {age:.1f} h) T{r['tier']} [{r['category']}] {r['impact_nas']}/{r['confidence']}/{r['persistence']} "
              f"{r['headline']} ({r['source']}; 2a fonte: {r['verified_by']})")

def find(con, a):
    r = con.execute("SELECT id FROM events WHERE date=? AND time_brt=? AND event=?", (a.date, a.time, a.event)).fetchone()
    if not r: sys.exit("evento nao encontrado")
    return r["id"]

def cmd_set_actual(con, a):
    eid = find(con, a)
    f = con.execute("SELECT forecast FROM events WHERE id=?", (eid,)).fetchone()["forecast"]
    con.execute("UPDATE events SET actual=?, surprise=?, updated_at=? WHERE id=?", (a.actual, surprise(a.actual, f), now(), eid))
    con.commit(); print("ok")

def cmd_add_reaction(con, a):
    eid = find(con, a)
    con.execute("INSERT OR REPLACE INTO reactions VALUES(?,?,?,?,?,?)", (eid, a.before, a.m5, a.m15, a.m60, now()))
    con.commit(); print("ok")

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--db", default=DB_DEFAULT)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    u = sub.add_parser("upsert"); u.add_argument("file")
    sub.add_parser("window")
    un = sub.add_parser("upsert-news"); un.add_argument("file")
    nw = sub.add_parser("news"); nw.add_argument("--hours", type=int, default=None); nw.add_argument("--max-tier", type=int, default=2)
    t = sub.add_parser("today"); t.add_argument("--date"); t.add_argument("--min-stars", type=int, default=2)
    for name in ("set-actual", "add-reaction"):
        s = sub.add_parser(name)
        for k in ("date", "time", "event"): s.add_argument("--" + k, required=True)
        if name == "set-actual": s.add_argument("--actual", required=True)
        else:
            s.add_argument("--before", type=float, required=True)
            for k in ("m5", "m15", "m60"): s.add_argument("--" + k, type=float)
    a = p.parse_args(); con = connect(a.db)
    {"init": lambda c, x: print("banco pronto:", os.path.abspath(a.db)), "upsert": cmd_upsert, "today": cmd_today,
     "window": cmd_window, "upsert-news": cmd_upsert_news, "news": cmd_news,
     "set-actual": cmd_set_actual, "add-reaction": cmd_add_reaction}[a.cmd](con, a)

if __name__ == "__main__":
    main()
