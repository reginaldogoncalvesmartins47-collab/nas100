#!/usr/bin/env python3
"""Banco local (SQLite) do calendario economico. Uso: python scripts/calendar_db.py <comando> [...]

Comandos:
  init                              cria o banco
  upsert ARQUIVO.json               grava/atualiza eventos (lista de objetos)
  upsert-news ARQUIVO.json          grava noticias (exige data/hora de publicacao)
  window                            mostra a janela de informacao de agora
  brief [--date D]                  briefing do dia: feriados, calendario, eventos extras, noticias, planos, pendencias
  upsert-holidays ARQ.json          feriados (pais, nome, fechado/cedo, fonte)
  upsert-extra ARQ.json             eventos fora do calendario (cupulas, discursos) - exige published_at com fuso
  add-plan --theme T --correlated A,B --position TXT [--event-id N|--extra-id N|--event-time ISO]   plano de posicionamento ANTECIPADO
  close-plan --id N --status concluido|invalidado   encerra plano
  themes                            temas e ativos correlacionados (rules.json)
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
CREATE TABLE IF NOT EXISTS holidays (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL, country TEXT NOT NULL, name TEXT NOT NULL, closed INTEGER DEFAULT 1, early_close TEXT,
  affects_nas TEXT, notes TEXT, source TEXT NOT NULL, tier INTEGER, captured_at TEXT,
  UNIQUE(date, country, name)
);
CREATE TABLE IF NOT EXISTS extra_events (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL, time_brt TEXT, title TEXT NOT NULL, type TEXT, participants TEXT,
  status TEXT DEFAULT 'anunciado', expected_impact TEXT, published_at TEXT NOT NULL,
  source TEXT NOT NULL, tier INTEGER, verified_by TEXT, notes TEXT, captured_at TEXT,
  UNIQUE(date, title)
);
CREATE TABLE IF NOT EXISTS plans (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL, theme TEXT NOT NULL, ref_table TEXT, ref_id INTEGER, correlated TEXT NOT NULL,
  scenario_up TEXT, scenario_down TEXT, position_note TEXT NOT NULL, event_time TEXT, lead_minutes INTEGER,
  anticipated INTEGER, status TEXT DEFAULT 'ativo', created_at TEXT, updated_at TEXT, closed_note TEXT
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

def need(d, keys, what):
    miss = [k for k in keys if not d.get(k)]
    if miss: sys.exit(f"REJEITADO ({what}): faltam {', '.join(miss)} -> {d}")

def cmd_upsert_holidays(con, a):
    items = json.load(open(a.file, encoding="utf-8"))
    for h in items:
        need(h, ["date", "country", "name", "source"], "feriado")
        con.execute("""INSERT INTO holidays(date,country,name,closed,early_close,affects_nas,notes,source,tier,captured_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(date,country,name) DO UPDATE SET closed=excluded.closed, early_close=excluded.early_close,
                       affects_nas=excluded.affects_nas, notes=excluded.notes, source=excluded.source, tier=excluded.tier""",
                    (h["date"], h["country"], h["name"], h.get("closed", 1), h.get("early_close"), h.get("affects_nas"),
                     h.get("notes"), h["source"], h.get("tier"), now()))
    con.commit(); print(f"{len(items)} feriado(s) gravado(s)")

def cmd_upsert_extra(con, a):
    items = json.load(open(a.file, encoding="utf-8"))
    for e in items:
        need(e, ["date", "title", "source", "published_at"], "evento fora do calendario")
        try: ts = parse_ts(e["published_at"])
        except Exception: sys.exit(f"REJEITADO (published_at sem data/hora com fuso): {e['title']}")
        con.execute("""INSERT INTO extra_events(date,time_brt,title,type,participants,status,expected_impact,published_at,
                       source,tier,verified_by,notes,captured_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(date,title) DO UPDATE SET time_brt=COALESCE(excluded.time_brt,time_brt),
                       status=excluded.status, expected_impact=COALESCE(excluded.expected_impact,expected_impact),
                       verified_by=COALESCE(excluded.verified_by,verified_by), notes=COALESCE(excluded.notes,notes)""",
                    (e["date"], e.get("time_brt"), e["title"], e.get("type"), e.get("participants"), e.get("status", "anunciado"),
                     e.get("expected_impact"), ts.isoformat(timespec="minutes"), e["source"], e.get("tier"),
                     e.get("verified_by"), e.get("notes"), now()))
    con.commit(); print(f"{len(items)} evento(s) fora do calendario gravado(s)")

def row_time(date, hhmm):
    return parse_ts(f"{date}T{hhmm}:00-03:00") if hhmm else None

def cmd_add_plan(con, a):
    n = now_brt(); date = a.date or n.strftime("%Y-%m-%d"); ev_time = None
    if a.event_id:
        r = con.execute("SELECT date,time_brt FROM events WHERE id=?", (a.event_id,)).fetchone()
        if not r: sys.exit("event-id nao existe")
        ev_time = row_time(r["date"], r["time_brt"]); ref = ("events", a.event_id)
    elif a.extra_id:
        r = con.execute("SELECT date,time_brt FROM extra_events WHERE id=?", (a.extra_id,)).fetchone()
        if not r: sys.exit("extra-id nao existe")
        ev_time = row_time(r["date"], r["time_brt"]); ref = ("extra_events", a.extra_id)
    else:
        ref = (None, None)
    if a.event_time: ev_time = parse_ts(a.event_time)
    lead = anticipated = None
    if ev_time:
        lead = int((ev_time - n).total_seconds() // 60); anticipated = 1 if lead > 0 else 0
        if not anticipated: print("AVISO: plano TARDIO (o evento ja ocorreu). Regra: nao operar perseguindo a noticia.")
    con.execute("""INSERT INTO plans(date,theme,ref_table,ref_id,correlated,scenario_up,scenario_down,position_note,event_time,
                   lead_minutes,anticipated,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (date, a.theme, ref[0], ref[1], a.correlated, a.up, a.down, a.position,
                 ev_time.isoformat(timespec="minutes") if ev_time else None, lead, anticipated, now(), now()))
    con.commit(); print("plano gravado, id", con.execute("SELECT last_insert_rowid()").fetchone()[0])

def cmd_close_plan(con, a):
    con.execute("UPDATE plans SET status=?, closed_note=?, updated_at=? WHERE id=?", (a.status, a.note, now(), a.id))
    con.commit(); print("ok")

def cmd_themes(con, a):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules.json")
    t = json.load(open(path, encoding="utf-8")).get("theme_correlations", {})
    print("Temas e ativos correlacionados (hipoteses a calibrar):")
    for k, v in t.items():
        if not k.startswith("_"): print(f"- {k}: {', '.join(v)}")

def cmd_brief(con, a):
    n = now_brt(); d = a.date or n.strftime("%Y-%m-%d")
    print(f"=== BRIEFING DO DIA {d} | agora {n:%H:%M} BRT ===")
    days = [(datetime.fromisoformat(d) + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    hol = con.execute(f"SELECT * FROM holidays WHERE date IN ({','.join('?'*3)}) ORDER BY date", days).fetchall()
    print("\n[Feriados hoje e nos proximos 2 dias]")
    for h in hol:
        print(f"  {h['date']} {h['country']}: {h['name']} ({'fechado' if h['closed'] else 'aberto'}"
              f"{', fecha cedo ' + h['early_close'] if h['early_close'] else ''}) fonte={h['source']}")
    if not hol: print("  nenhum gravado (se o levantamento de feriados nao foi feito, FAZER antes de operar)")
    print("\n[Calendario (2+ estrelas)]")
    plan_ref = {(r["ref_table"], r["ref_id"]) for r in con.execute("SELECT ref_table,ref_id FROM plans WHERE status!='invalidado' AND COALESCE(anticipated,1)!=0")}
    evs = con.execute("SELECT * FROM events WHERE date=? AND COALESCE(stars,0)>=2 AND relevant_nas=1 ORDER BY time_brt", (d,)).fetchall()
    for e in evs:
        flag = "  <-- SEM PLANO" if (e["stars"] or 0) >= 3 and ("events", e["id"]) not in plan_ref else ""
        print(f"  [{e['id']}] {e['time_brt']} {'*'*(e['stars'] or 0)} {e['event']} | atual={e['actual']} proj={e['forecast']}{flag}")
    if not evs: print("  nenhum gravado (calendario nao capturado = sem sinal)")
    print("\n[Eventos fora do calendario oficial]")
    ex = con.execute("SELECT * FROM extra_events WHERE date=? AND status!='cancelado' ORDER BY time_brt", (d,)).fetchall()
    for e in ex:
        flag = "  <-- SEM PLANO" if ("extra_events", e["id"]) not in plan_ref else ""
        print(f"  [{e['id']}] {e['time_brt'] or 'hora n/d'} {e['title']} ({e['type']}; {e['status']}) fonte={e['source']}{flag}")
    if not ex: print("  nenhum gravado")
    print("\n[Noticias dentro da janela]")
    cmd_news(con, argparse.Namespace(hours=None, max_tier=2))
    print("\n[Planos de posicionamento ativos]")
    pl = con.execute("SELECT * FROM plans WHERE status='ativo' AND date=? ORDER BY event_time", (d,)).fetchall()
    for p in pl:
        warn = "  <-- TARDIO: nao operar pela noticia" if p["anticipated"] == 0 else ""
        print(f"  [{p['id']}] {p['theme']} | correlacionados: {p['correlated']} | {p['position_note']}{warn}")
    if not pl: print("  nenhum plano ativo")

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
    sub.add_parser("themes")
    bf = sub.add_parser("brief"); bf.add_argument("--date")
    hl = sub.add_parser("upsert-holidays"); hl.add_argument("file")
    ue = sub.add_parser("upsert-extra"); ue.add_argument("file")
    ap = sub.add_parser("add-plan")
    ap.add_argument("--date"); ap.add_argument("--theme", required=True); ap.add_argument("--correlated", required=True)
    ap.add_argument("--up"); ap.add_argument("--down"); ap.add_argument("--position", required=True)
    ap.add_argument("--event-id", type=int); ap.add_argument("--extra-id", type=int); ap.add_argument("--event-time")
    cp = sub.add_parser("close-plan"); cp.add_argument("--id", type=int, required=True)
    cp.add_argument("--status", choices=["concluido", "invalidado"], required=True); cp.add_argument("--note")
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
     "window": cmd_window, "themes": cmd_themes, "brief": cmd_brief, "upsert-holidays": cmd_upsert_holidays,
     "upsert-extra": cmd_upsert_extra, "add-plan": cmd_add_plan, "close-plan": cmd_close_plan, "upsert-news": cmd_upsert_news, "news": cmd_news,
     "set-actual": cmd_set_actual, "add-reaction": cmd_add_reaction}[a.cmd](con, a)

if __name__ == "__main__":
    main()
