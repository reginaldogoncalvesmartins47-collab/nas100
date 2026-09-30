#!/usr/bin/env python3
"""Banco local (SQLite) do calendario economico. Uso: python scripts/calendar_db.py <comando> [...]

Comandos:
  init                              cria o banco
  upsert ARQUIVO.json               grava/atualiza eventos (lista de objetos)
  today [--date AAAA-MM-DD] [--min-stars N]   lista eventos do dia
  set-actual --date D --time HH:MM --event NOME --actual VALOR   grava o realizado e calcula a surpresa
  add-reaction --date D --time HH:MM --event NOME --before P --m5 P --m15 P --m60 P   reacao do NAS100 ao evento
Banco padrao: data/calendario.db (variavel CAL_DB ou --db para mudar). Fonte dos dados: Investing (via extensao).
"""
import argparse, json, os, re, sqlite3, sys
from datetime import datetime

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
     "set-actual": cmd_set_actual, "add-reaction": cmd_add_reaction}[a.cmd](con, a)

if __name__ == "__main__":
    main()
