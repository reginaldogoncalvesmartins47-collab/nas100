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
  add-plan --stance compra|venda --theme T --correlated A,B --position TXT [--event-id N|--extra-id N|--event-time ISO]   plano de posicionamento ANTECIPADO
  close-plan --id N --status concluido|invalidado   encerra plano
  open-trade --mode treino|real --side compra|venda --entry E --stop S --risk-usd R [--target1 --target2 --zone-low L --zone-high H (regiao de oferta/demanda-alvo) --size --region-score --bias --plan-id --notes]
                                    registra entrada. Limites de capital valem SEMPRE; no treino o gate nao bloqueia (so registra); no real bloqueia
  update-trade --id N --high H --low L [--be-moved]   atualiza maxima/minima desde a ultima vez (mede quanto o trade andou a favor: MFE)
  close-trade --id N --exit-price P --reason stop|alvo1|alvo2|breakeven|trailing|invalidacao|tempo|evento|manual|fim_dia   fecha e calcula R
  path --id N --price P --quality forte|fraca|lateral|revertendo --pairs sim|parcial|nao [--o O --h H --l L --c C (ultimo candle fechado: detecta o pavio sozinho) | --wick superior|inferior --wick-where zona|caminho] [--note]   leitura do CAMINHO ate a regiao-alvo
  wick --open O --high H --low L --close C [--atr A]   mede os pavios de um candle (auxilio; decisao e visual)
  tune --param P --value V --reason TXT --evidence-kind trades|exemplos --evidence-n N [--mode treino|real]
                                    o Claude ajusta um parametro PERMITIDO, com evidencia minima, um de cada vez, com historico (real exige aprovacao da usuaria)
  tune-history                      historico de ajustes
  tune-revert --id N                desfaz um ajuste
  bias [--set alta|baixa|neutro --reason TXT]   vies do dia (mostra o atual; o choque o marca como VENCIDO)
  shock --o O --h H --l L --c C --atr A [--prev-close PC --atr-gap AH --h1 H2 --l1 L2]   detecta gap, vela enorme e FVG; abre CHOQUE e vence o vies
  shock-diagnose --id N --category C --cause TXT --confidence alta|media|baixa --bias-after alta|baixa|neutro   diagnostico rapido do choque
  entry-check --zone-type demanda|oferta --zone-low L --zone-high H --o O --h H --l L --c C --atr A [--score S --bias B --target-low --target-high --risk-usd --usd-per-point --min-lot]
                                    GATILHO de entrada em M5: toque na regiao + rejeicao de pavio a favor + fechou sem romper; calcula stop, alvo, RR e lote
  ready                             veredito em portugues simples: ja da para ir para a conta real? (criterios do treino)
  stats [--mode treino|real]        acerto, R medio, MFE, quanto devolveu, por motivo de saida e por estado do gate
  themes                            temas e ativos correlacionados (rules.json)
  add-read --pair P --tf H1|H4|D1 --trend T --why TXT --implication I --confidence C --invalidation TXT   leitura RACIOCINADA de um par (micro nao aceito)
  reads [--pair P]                  ultima leitura de cada par/tf, com idade
  mark-checked --name calendar|holidays|extra_events|news [--note]   registra que verificou (inclusive 'nada relevante')
  gate                              semaforo: LIBERADO ou BLOQUEADO com a LISTA de pendencias a concluir (sem trava de horario)
  since                             ultima checagem de noticias: buscar so o que saiu depois (incremental)
  add-sentiment --source S --metric M --reading risk_on|risk_off|neutro|misto [--value V --data-date AAAA-MM-DD --note N]   sentimento do mercado (Finviz e outras)
  renew-read --pair P --tf TF --note TXT   renova leitura quando NADA mudou (sem reescrever)
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
  anticipated INTEGER, status TEXT DEFAULT 'ativo', created_at TEXT, updated_at TEXT, closed_note TEXT, stance TEXT
);
CREATE TABLE IF NOT EXISTS sentiment_reads (
  id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, source TEXT NOT NULL, metric TEXT NOT NULL, value TEXT,
  reading TEXT NOT NULL, note TEXT
);
CREATE TABLE IF NOT EXISTS pair_reads (
  id INTEGER PRIMARY KEY,
  created_at TEXT NOT NULL, pair TEXT NOT NULL, tf TEXT NOT NULL, trend TEXT, structure TEXT,
  why TEXT NOT NULL, news_id INTEGER, implication TEXT NOT NULL, divergence TEXT,
  confidence TEXT, invalidation TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS checks (
  id INTEGER PRIMARY KEY, date TEXT NOT NULL, name TEXT NOT NULL, checked_at TEXT NOT NULL, note TEXT
);
CREATE TABLE IF NOT EXISTS trades (
  id INTEGER PRIMARY KEY, mode TEXT NOT NULL, opened_at TEXT NOT NULL, closed_at TEXT, side TEXT NOT NULL,
  entry REAL NOT NULL, stop REAL NOT NULL, target1 REAL, target2 REAL, size REAL, risk_usd REAL,
  region_score REAL, bias TEXT, plan_id INTEGER, gate_ok INTEGER, gate_pending TEXT,
  exit_price REAL, exit_reason TEXT, result_usd REAL, result_r REAL, mfe_r REAL DEFAULT 0, mae_r REAL DEFAULT 0,
  be_moved INTEGER DEFAULT 0, notes TEXT, target_zone_low REAL, target_zone_high REAL
);
CREATE TABLE IF NOT EXISTS trade_path (
  id INTEGER PRIMARY KEY, trade_id INTEGER NOT NULL REFERENCES trades(id), at TEXT NOT NULL, price REAL NOT NULL,
  quality TEXT NOT NULL, pairs_confirm TEXT NOT NULL, note TEXT, wick_side TEXT, wick_where TEXT
);
CREATE TABLE IF NOT EXISTS param_changes (
  id INTEGER PRIMARY KEY, at TEXT NOT NULL, param TEXT NOT NULL, old_value TEXT, new_value TEXT, reason TEXT NOT NULL,
  evidence_kind TEXT NOT NULL, evidence_n INTEGER NOT NULL, mode TEXT NOT NULL, reverted INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS bias_log (
  id INTEGER PRIMARY KEY, at TEXT NOT NULL, bias TEXT NOT NULL, reason TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS shocks (
  id INTEGER PRIMARY KEY, detected_at TEXT NOT NULL, kinds TEXT NOT NULL, gap_pts REAL, gap_atr REAL, range_atr REAL,
  direction TEXT, fvg_low REAL, fvg_high REAL, fvg_dir TEXT, status TEXT DEFAULT 'aberto',
  category TEXT, cause TEXT, confidence TEXT, diagnosed_at TEXT, notes TEXT
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
    con.executescript(SCHEMA)
    for ddl in ("ALTER TABLE plans ADD COLUMN stance TEXT", "ALTER TABLE trades ADD COLUMN target_zone_low REAL",
                "ALTER TABLE trades ADD COLUMN target_zone_high REAL",
                "ALTER TABLE trade_path ADD COLUMN wick_side TEXT", "ALTER TABLE trade_path ADD COLUMN wick_where TEXT"):  # bancos criados antes
        try: con.execute(ddl)
        except sqlite3.OperationalError: pass
    return con

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
                   lead_minutes,anticipated,created_at,updated_at,stance) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (date, a.theme, ref[0], ref[1], a.correlated, a.up, a.down, a.position,
                 ev_time.isoformat(timespec="minutes") if ev_time else None, lead, anticipated, now(), now(), a.stance))
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
    plan_ref = {(r["ref_table"], r["ref_id"]) for r in con.execute("SELECT ref_table,ref_id FROM plans WHERE status!='invalidado' AND COALESCE(anticipated,1)!=0 AND stance IS NOT NULL")}
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
        print(f"  [{p['id']}] {(p['stance'] or 'SEM DIRECAO').upper()} | {p['theme']} | correlacionados: {p['correlated']} | {p['position_note']}{warn}")
    if not pl: print("  nenhum plano ativo")

def rules_path():
    return os.environ.get("RULES_PATH") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rules.json")

def load_rules():
    try: return json.load(open(rules_path(), encoding="utf-8"))
    except Exception: return {}

def get_path(d, path):
    for k in path: d = d[k]
    return d

def set_path(d, path, v):
    for k in path[:-1]: d = d[k]
    d[path[-1]] = v

def wick_cfg():
    c = load_rules().get("exit_management", {}).get("path_monitoring", {})
    return c.get("wick_min_range_pct", 0.5), c.get("wick_min_body_multiple", 2)

def cmd_add_read(con, a):
    if a.tf not in ("H1", "H4", "D1"):
        sys.exit("REJEITADO: timeframe micro nao conta como base do macro. Use H1, H4 ou D1.")
    if a.implication == "conflito" and not a.divergence:
        sys.exit("REJEITADO: implicacao 'conflito' exige --divergence explicando a divergencia.")
    req = load_rules().get("gate_3_pairs", {}).get("required", [])
    if req and a.pair not in req: print(f"aviso: {a.pair} nao esta na lista obrigatoria {req}")
    con.execute("""INSERT INTO pair_reads(created_at,pair,tf,trend,structure,why,news_id,implication,divergence,confidence,invalidation)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (now_brt().isoformat(timespec="seconds"), a.pair, a.tf, a.trend, a.structure, a.why, a.news_id,
                 a.implication, a.divergence, a.confidence, a.invalidation))
    con.commit(); print("leitura gravada")

def cmd_reads(con, a):
    n = now_brt()
    rows = con.execute("SELECT * FROM pair_reads ORDER BY created_at DESC").fetchall()
    seen = set()
    for r in rows:
        k = (r["pair"], r["tf"])
        if k in seen or (a.pair and r["pair"] != a.pair): continue
        seen.add(k); age = int((n - parse_ts(r["created_at"])).total_seconds() // 60)
        print(f"{r['pair']:<6} {r['tf']} (ha {age} min) trend={r['trend']} -> {r['implication']} [{r['confidence']}] | por que: {r['why']} | invalida: {r['invalidation']}"
              + (f" | divergencia: {r['divergence']}" if r["divergence"] else ""))
    if not seen: print("nenhuma leitura de pares gravada")

def cmd_mark_checked(con, a):
    n = now_brt()
    con.execute("INSERT INTO checks(date,name,checked_at,note) VALUES(?,?,?,?)",
                (n.strftime("%Y-%m-%d"), a.name, n.isoformat(timespec="seconds"), a.note))
    con.commit(); print("verificacao registrada:", a.name)

def cmd_add_sentiment(con, a):
    note = a.note
    if a.data_date:
        age = (now_brt().date() - datetime.fromisoformat(a.data_date).date()).days
        note = f"{note + ' | ' if note else ''}dado de {a.data_date} (defasagem {age} dias)"
    con.execute("INSERT INTO sentiment_reads(created_at,source,metric,value,reading,note) VALUES(?,?,?,?,?,?)",
                (now_brt().isoformat(timespec="seconds"), a.source, a.metric, a.value, a.reading, note))
    con.commit(); print("sentimento gravado" + (f" (defasagem {age} dias)" if a.data_date else ""))

def cmd_renew_read(con, a):
    r = con.execute("SELECT * FROM pair_reads WHERE pair=? AND tf=? ORDER BY created_at DESC", (a.pair, a.tf)).fetchone()
    if not r: sys.exit("nao ha leitura anterior desse par/tf: use add-read")
    n = now_brt()
    con.execute("""INSERT INTO pair_reads(created_at,pair,tf,trend,structure,why,news_id,implication,divergence,confidence,invalidation)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (n.isoformat(timespec="seconds"), r["pair"], r["tf"], r["trend"], r["structure"],
                 f"{r['why']} [renovada {n:%H:%M}: {a.note}]", r["news_id"], r["implication"], r["divergence"],
                 r["confidence"], r["invalidation"]))
    con.commit(); print("leitura renovada (nada mudou):", a.pair, a.tf)

def cmd_since(con, a):
    n = now_brt(); start, label = window_start(n)
    c = con.execute("SELECT checked_at FROM checks WHERE name='news' ORDER BY checked_at DESC").fetchone()
    if c and parse_ts(c["checked_at"]) >= start:
        print(f"Ultima checagem de noticias: {parse_ts(c['checked_at']):%Y-%m-%d %H:%M} BRT. Buscar SO o publicado depois disso; nao rever o que ja esta no banco.")
    else:
        print(f"Sem checagem de noticias dentro da janela ({label}). Buscar desde {start:%Y-%m-%d %H:%M} BRT.")

def gate_eval(con):
    n = now_brt(); d = n.strftime("%Y-%m-%d"); R = load_rules()
    cfg = R.get("gate_3_pairs", {}); fresh = cfg.get("fresh_minutes", {"H1": 60, "H4": 240})
    min_src = R.get("gate_4_sentiment", {}).get("min_sources", 2)
    news_warn = R.get("gate_1_news", {}).get("incremental_warn_minutes", 60)
    todo, warn = [], []
    for sh in con.execute("SELECT * FROM shocks WHERE status='aberto' ORDER BY detected_at"):
        todo.append((f"CHOQUE ABERTO #{sh['id']} ({sh['kinds']}): diagnosticar o que esta acontecendo PRIMEIRO, rapido", f"shock-diagnose --id {sh['id']} --category ... --cause ... --confidence ... --bias-after alta|baixa|neutro"))
    bl = con.execute("SELECT * FROM bias_log ORDER BY at DESC, id DESC").fetchone()
    if not bl or not parse_ts(bl["at"]).strftime("%Y-%m-%d") == d:
        todo.append(("vies do dia nao definido hoje", "definir pela macro do dia: bias --set alta|baixa|neutro --reason TXT"))
    elif bl["bias"] == "vencido":
        todo.append(("VIES VENCIDO (choque/noticia): reavaliar e redefinir", "bias --set alta|baixa|neutro --reason TXT (ou shock-diagnose)"))
    def checked_today(name): return con.execute("SELECT checked_at FROM checks WHERE date=? AND name=? ORDER BY checked_at DESC", (d, name)).fetchone()
    nev = con.execute("SELECT COUNT(*) c FROM events WHERE date=? AND COALESCE(stars,0)>=2", (d,)).fetchone()["c"]
    if not nev and not checked_today("calendar"):
        todo.append(("calendario de hoje nao capturado (gate 0)", "ler o Investing pela extensao -> upsert ARQ.json (ou mark-checked --name calendar se nao houver evento relevante)"))
    if not checked_today("holidays"):
        todo.append(("feriados globais nao verificados hoje (gate 2)", "levantar feriados (hoje e 2 dias) -> upsert-holidays; depois mark-checked --name holidays"))
    if not checked_today("extra_events"):
        todo.append(("eventos fora do calendario nao verificados hoje (gate 2)", "buscar cupulas/reunioes/discursos -> upsert-extra; depois mark-checked --name extra_events"))
    c = checked_today("news")
    if not c:
        todo.append(("noticias de hoje ainda nao verificadas (gate 1)", "buscar a janela inteira (rode `since`) -> upsert-news; depois mark-checked --name news"))
    else:
        age = (n - parse_ts(c["checked_at"])).total_seconds() / 60
        if age > news_warn: warn.append(f"ultima checagem de noticias ha {int(age)} min: fazer checagem INCREMENTAL (rode `since`); nao rever o que ja esta no banco")
    ctx_only = [x.lower() for x in R.get("gate_4_sentiment", {}).get("context_only", [])]
    srcs = len({r["source"] for r in con.execute("SELECT source FROM sentiment_reads WHERE created_at LIKE ?", (d + "%",))
                if not any(c in r["source"].lower() for c in ctx_only)})
    if srcs < min_src:
        todo.append((f"sentimento do mercado: {srcs} fonte(s) do dia (semanais como COT/AAII nao contam), minimo {min_src} (gate 4)", "ler Finviz e outras fontes (ver docs/sentimento.md) -> add-sentiment --source S --metric M --reading risk_on|risk_off|neutro|misto"))
    plan_ref = {(r["ref_table"], r["ref_id"]) for r in con.execute("SELECT ref_table,ref_id FROM plans WHERE status!='invalidado' AND COALESCE(anticipated,1)!=0 AND stance IS NOT NULL")}
    for e in con.execute("SELECT * FROM events WHERE date=? AND COALESCE(stars,0)>=3", (d,)):
        if ("events", e["id"]) not in plan_ref:
            t = row_time(e["date"], e["time_brt"])
            if t and t > n: todo.append((f"posicionamento antes do evento: falta plano com DIRECAO (compra/venda) para {e['event']} ({e['time_brt']} BRT)", f"add-plan --event-id {e['id']} --stance compra|venda --theme T --correlated A,B --position TXT"))
            else: warn.append(f"evento 3 estrelas sem plano antecipado: {e['event']} (ja ocorreu: nao da para antecipar)")
    for e in con.execute("SELECT * FROM extra_events WHERE date=? AND status!='cancelado'", (d,)):
        if ("extra_events", e["id"]) not in plan_ref:
            t = row_time(e["date"], e["time_brt"])
            if not t or t > n: todo.append((f"posicionamento antes do evento: falta plano com DIRECAO para {e['title']}", f"add-plan --extra-id {e['id']} --stance compra|venda --theme T --correlated A,B --position TXT"))
            else: warn.append(f"evento fora do calendario sem plano antecipado: {e['title']} (ja ocorreu)")
    for pair in cfg.get("required", ["VIX", "Brent", "US10Y", "ES", "DXY"]):
        for tf in cfg.get("timeframes_required", ["H1", "H4"]):
            r = con.execute("SELECT * FROM pair_reads WHERE pair=? AND tf=? ORDER BY created_at DESC", (pair, tf)).fetchone()
            if not r: todo.append((f"sem leitura de {pair} em {tf} (gate 3)", f"add-read --pair {pair} --tf {tf} ... (raciocinar: por que, implicacao, invalidacao)")); continue
            age = (n - parse_ts(r["created_at"])).total_seconds() / 60
            if age > fresh.get(tf, 60): todo.append((f"leitura de {pair} {tf} com {int(age)} min (validade {fresh.get(tf, 60)})", f"ver se algo MUDOU: se nao, renew-read --pair {pair} --tf {tf} --note TXT; se sim, add-read"))
    return todo, warn, n

def cmd_gate(con, a):
    todo, warn, n = gate_eval(con)
    print(f"=== GATE {n:%Y-%m-%d %H:%M} BRT ===")
    if todo:
        print("BLOQUEADO. PRIORIDADE: concluir as pendencias abaixo, na ordem. Nao parar e nao pedir permissao para fazer o dever de casa;\nso perguntar a usuaria o que apenas ela sabe.")
        for i, (m, h) in enumerate(todo, 1): print(f" {i}. {m}\n    como: {h}")
    else: print("LIBERADO para analisar entrada (nao e sinal: regiao, reacao e risco ainda precisam passar).")
    for w in warn: print("  aviso:", w)
    sys.exit(1 if todo else 0)

def risk_cfg():
    r = load_rules().get("risk", {})
    return r.get("per_trade_usd_max"), r.get("daily_loss_usd"), r.get("kill_total_usd", 10.0)  # None = a usuaria ainda nao definiu

def cmd_open_trade(con, a):
    per, daily, kill = risk_cfg(); n = now_brt(); d = n.strftime("%Y-%m-%d"); dist = abs(a.entry - a.stop)
    if dist <= 0 or (a.side == "compra" and a.stop >= a.entry) or (a.side == "venda" and a.stop <= a.entry):
        sys.exit("REJEITADO: stop invalido (obrigatorio e do lado certo). Nunca entrar sem stop.")
    if (a.zone_low is None) != (a.zone_high is None): sys.exit("REJEITADO: informe --zone-low e --zone-high juntos")
    if a.zone_low is not None and ((a.side == "compra" and a.zone_low <= a.entry) or (a.side == "venda" and a.zone_high >= a.entry) or a.zone_low > a.zone_high):
        sys.exit("REJEITADO: regiao-alvo do lado errado (compra: zona de oferta ACIMA da entrada; venda: zona de demanda ABAIXO)")
    if per is None:
        if a.mode == "real": sys.exit("REJEITADO (real): a usuaria ainda nao definiu o risco maximo por trade. Definir antes de operar no real.")
    elif a.risk_usd > per:
        if a.mode == "real": sys.exit(f"REJEITADO (real): risco US$ {a.risk_usd} acima do maximo por trade definido pela usuaria (US$ {per}).")
        print(f"AVISO (treino): risco US$ {a.risk_usd} acima do maximo definido (US$ {per}); registrado.")
    today = con.execute("SELECT COALESCE(SUM(result_usd),0) s FROM trades WHERE mode=? AND closed_at LIKE ?", (a.mode, d + "%")).fetchone()["s"]
    total = con.execute("SELECT COALESCE(SUM(result_usd),0) s FROM trades WHERE mode=? AND closed_at IS NOT NULL", (a.mode,)).fetchone()["s"]
    would_stop = []
    if daily is not None and today <= -daily:
        if a.mode == "real": sys.exit(f"REJEITADO: perda do dia US$ {today:.2f} atingiu o limite US$ {daily}. Parar por hoje.")
        would_stop.append(f"perda do dia US$ {today:.2f} passou do limite US$ {daily}")
    if total <= -kill:
        if a.mode == "real": sys.exit(f"REJEITADO: perda total US$ {total:.2f} atingiu o corte US$ {kill}. Parar e revisar tudo.")
        would_stop.append(f"perda total US$ {total:.2f} passou do corte US$ {kill}")
    if would_stop:
        print("AVISO (treino: NAO para, para nao interromper o aprendizado): no REAL o bot pararia aqui -> " + "; ".join(would_stop))
        a.notes = ((a.notes + " | ") if a.notes else "") + "no real teria parado: " + "; ".join(would_stop)
    todo, warn, _ = gate_eval(con)
    if todo and a.mode == "real":
        print("REJEITADO (modo real exige gate LIBERADO). Pendencias:"); [print(" -", m) for m, _h in todo]; sys.exit(1)
    if todo: print(f"treino: entrada PERMITIDA e registrada com gate_ok=0 ({len(todo)} pendencia(s)); sera comparada nas estatisticas.")
    con.execute("""INSERT INTO trades(mode,opened_at,side,entry,stop,target1,target2,size,risk_usd,region_score,bias,plan_id,gate_ok,gate_pending,notes,target_zone_low,target_zone_high)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (a.mode, n.isoformat(timespec="seconds"), a.side, a.entry, a.stop, a.target1, a.target2, a.size, a.risk_usd,
                 a.region_score, a.bias, a.plan_id, 0 if todo else 1, "; ".join(m for m, _h in todo) or None, a.notes, a.zone_low, a.zone_high))
    con.commit(); print("trade aberto, id", con.execute("SELECT last_insert_rowid()").fetchone()[0])

def excursion(r, high, low):
    dist = abs(r["entry"] - r["stop"]); sgn = 1 if r["side"] == "compra" else -1
    fav = ((high if sgn == 1 else low) - r["entry"]) * sgn / dist
    adv = ((low if sgn == 1 else high) - r["entry"]) * sgn / dist
    return fav, adv

def cmd_update_trade(con, a):
    r = con.execute("SELECT * FROM trades WHERE id=? AND closed_at IS NULL", (a.id,)).fetchone()
    if not r: sys.exit("trade nao encontrado ou ja fechado")
    fav, adv = excursion(r, a.high, a.low)
    mfe, mae = max(r["mfe_r"] or 0, fav), min(r["mae_r"] or 0, adv)
    be = 1 if a.be_moved else r["be_moved"]
    con.execute("UPDATE trades SET mfe_r=?, mae_r=?, be_moved=? WHERE id=?", (mfe, mae, be, a.id)); con.commit()
    print(f"MFE={mfe:.2f}R MAE={mae:.2f}R" + (" | stop movido para break-even" if be else ""))

def cmd_close_trade(con, a):
    r = con.execute("SELECT * FROM trades WHERE id=? AND closed_at IS NULL", (a.id,)).fetchone()
    if not r: sys.exit("trade nao encontrado ou ja fechado")
    dist = abs(r["entry"] - r["stop"]); sgn = 1 if r["side"] == "compra" else -1
    res_r = round((a.exit_price - r["entry"]) * sgn / dist, 3) or 0.0
    fav, adv = excursion(r, max(a.exit_price, a.high or a.exit_price), min(a.exit_price, a.low or a.exit_price))
    mfe, mae = max(r["mfe_r"] or 0, fav), min(r["mae_r"] or 0, adv)
    usd = round(res_r * r["risk_usd"], 2) if r["risk_usd"] else None
    con.execute("""UPDATE trades SET closed_at=?, exit_price=?, exit_reason=?, result_r=?, result_usd=?, mfe_r=?, mae_r=?,
                   notes=COALESCE(?,notes) WHERE id=?""",
                (now_brt().isoformat(timespec="seconds"), a.exit_price, a.reason, round(res_r, 3), usd, mfe, mae, a.notes, a.id))
    con.commit(); print(f"fechado: {res_r:+.2f}R (US$ {usd}) | MFE {mfe:.2f}R | devolveu {mfe - res_r:.2f}R | motivo {a.reason}")

def edge_r(r):
    """distancia em R ate a BORDA PROXIMA da regiao-alvo (compra: base da zona de oferta; venda: topo da zona de demanda)"""
    if r["target_zone_low"] is None: return None
    dist = abs(r["entry"] - r["stop"])
    return ((r["target_zone_low"] - r["entry"]) if r["side"] == "compra" else (r["entry"] - r["target_zone_high"])) / dist

def cmd_path(con, a):
    r = con.execute("SELECT * FROM trades WHERE id=? AND closed_at IS NULL", (a.id,)).fetchone()
    if not r: sys.exit("trade nao encontrado ou ja fechado")
    dist = abs(r["entry"] - r["stop"]); sgn = 1 if r["side"] == "compra" else -1
    now_r = (a.price - r["entry"]) * sgn / dist
    if a.o is not None:
        if None in (a.h, a.l, a.c): sys.exit("informe --o --h --l --c juntos (ultimo candle fechado)")
        rng = a.h - a.l; body = abs(a.c - a.o); up = a.h - max(a.o, a.c); lo = min(a.o, a.c) - a.l
        pr, bm = wick_cfg()
        if rng > 0 and a.wick == "nenhum":
            if up >= pr * rng and up >= bm * body: a.wick = "superior"
            elif lo >= pr * rng and lo >= bm * body: a.wick = "inferior"
        if a.wick != "nenhum" and r["target_zone_low"] is not None and not a.wick_where:
            touched = (a.h >= r["target_zone_low"]) if r["side"] == "compra" else (a.l <= r["target_zone_high"])
            a.wick_where = "zona" if touched else "caminho"
        print(f"candle O{a.o} H{a.h} L{a.l} C{a.c}: pavio sup {100*up/rng:.0f}% | inf {100*lo/rng:.0f}% | corpo {100*body/rng:.0f}% -> rejeicao detectada: {a.wick}" if rng > 0 else "candle sem amplitude")
    con.execute("INSERT INTO trade_path(trade_id,at,price,quality,pairs_confirm,note,wick_side,wick_where) VALUES(?,?,?,?,?,?,?,?)",
                (a.id, now_brt().isoformat(timespec="seconds"), a.price, a.quality, a.pairs, a.note, a.wick, a.wick_where)); con.commit()
    er = edge_r(r); msg = f"agora {now_r:+.2f}R"
    if er is not None:
        near = r["target_zone_low"] if r["side"] == "compra" else r["target_zone_high"]
        msg += f" | borda da regiao-alvo a {er:.2f}R da entrada ({abs(near - a.price):.1f} pts do preco)"
    print(msg + f" | caminho {a.quality}, pares confirmam: {a.pairs}")
    against = (r["side"] == "compra" and a.wick == "superior") or (r["side"] == "venda" and a.wick == "inferior")
    if against:
        print(f"ALERTA: REJEICAO DE PAVIO contra o trade ({a.wick}, {a.wick_where or 'local n/i'}). E o seu sinal de saida: considerar realizar/proteger"
              + (" (na propria regiao-alvo)." if a.wick_where == "zona" else "."))
    if a.quality in ("fraca", "revertendo") and a.pairs != "sim" and (r["mfe_r"] or 0) >= 1:
        print("ALERTA (hipotese do docs/gestao-saida.md): caminho deteriorando, pares sem confirmar e o trade ja andou +1R: considerar proteger (parcial, break-even ou trailing).")

def cmd_wick(con, a):
    rng = a.high - a.low
    if rng <= 0: sys.exit("candle sem amplitude")
    body = abs(a.close - a.open); up = a.high - max(a.open, a.close); lo = min(a.open, a.close) - a.low
    print(f"amplitude {rng:.1f} | corpo {body:.1f} ({100*body/rng:.0f}%) | pavio superior {up:.1f} ({100*up/rng:.0f}%) | pavio inferior {lo:.1f} ({100*lo/rng:.0f}%)")
    pr, bm = wick_cfg()
    for nome, w in (("SUPERIOR (rejeicao de topo)", up), ("INFERIOR (rejeicao de fundo)", lo)):
        if w >= pr * rng and w >= bm * body: print(f"  possivel rejeicao de pavio {nome} [criterio atual: pavio >= {pr:.0%} da amplitude e >= {bm}x o corpo]")
    if a.atr: print(f"  maior pavio = {max(up, lo)/a.atr:.2f} x ATR")
    print("  Criterio-hipotese a calibrar com exemplos da usuaria (numeros OHLC).")

def tuning_cfg():
    return load_rules().get("tuning", {})

def cmd_tune(con, a):
    T = tuning_cfg(); reg = T.get("tunable", {})
    if a.param in T.get("protected", []) or a.param not in reg:
        sys.exit(f"REJEITADO: '{a.param}' nao e ajustavel pelo Claude (protegido ou fora do registro). Ajustaveis: {', '.join(reg)}")
    spec = reg[a.param]
    if not (spec["min"] <= a.value <= spec["max"]):
        sys.exit(f"REJEITADO: valor {a.value} fora dos limites [{spec['min']}, {spec['max']}] de {a.param}")
    need_n = T.get("min_evidence", {}).get(a.evidence_kind, 30)
    if a.evidence_n < need_n:
        sys.exit(f"REJEITADO: evidencia insuficiente ({a.evidence_n} {a.evidence_kind}; minimo {need_n}). Nao ajustar com amostra pequena.")
    if a.evidence_kind == "trades":
        have = con.execute("SELECT COUNT(*) c FROM trades WHERE closed_at IS NOT NULL AND mode=?", (a.mode,)).fetchone()["c"]
        if have < a.evidence_n: sys.exit(f"REJEITADO: voce cita {a.evidence_n} trades, mas o banco tem {have} fechados no modo {a.mode}")
    if a.mode == "real" and not a.user_approved:
        sys.exit("REJEITADO: no modo real, ajuste so com aprovacao explicita da usuaria (--user-approved, usado apenas depois dela aprovar).")
    last = con.execute("SELECT at FROM param_changes WHERE reverted=0 ORDER BY at DESC").fetchone()
    cool = T.get("cooldown_trades", 10)
    if last:
        since = con.execute("SELECT COUNT(*) c FROM trades WHERE closed_at > ? AND mode=?", (last["at"], a.mode)).fetchone()["c"]
        if since < cool: sys.exit(f"REJEITADO: um ajuste de cada vez. Desde o ultimo ajuste so ha {since} trades fechados (minimo {cool}) para medir o efeito.")
    R = load_rules(); old = get_path(R, spec["path"]); set_path(R, spec["path"], a.value)
    json.dump(R, open(rules_path(), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    con.execute("INSERT INTO param_changes(at,param,old_value,new_value,reason,evidence_kind,evidence_n,mode) VALUES(?,?,?,?,?,?,?,?)",
                (now_brt().isoformat(timespec="seconds"), a.param, json.dumps(old), json.dumps(a.value), a.reason, a.evidence_kind, a.evidence_n, a.mode))
    con.commit(); print(f"ajustado {a.param}: {old} -> {a.value} (motivo: {a.reason}; evidencia: {a.evidence_n} {a.evidence_kind}). Desfazer: tune-revert")

def cmd_tune_history(con, a):
    rows = con.execute("SELECT * FROM param_changes ORDER BY at DESC").fetchall()
    if not rows: print("nenhum ajuste de parametros registrado"); return
    for r in rows:
        print(f"[{r['id']}] {r['at']} {r['param']}: {r['old_value']} -> {r['new_value']} | {r['reason']} | {r['evidence_n']} {r['evidence_kind']} ({r['mode']})" + (" [DESFEITO]" if r["reverted"] else ""))

def cmd_tune_revert(con, a):
    r = con.execute("SELECT * FROM param_changes WHERE id=? AND reverted=0", (a.id,)).fetchone()
    if not r: sys.exit("ajuste nao encontrado ou ja desfeito")
    spec = tuning_cfg().get("tunable", {}).get(r["param"])
    if not spec: sys.exit("parametro nao esta mais no registro")
    R = load_rules(); set_path(R, spec["path"], json.loads(r["old_value"]))
    json.dump(R, open(rules_path(), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    con.execute("UPDATE param_changes SET reverted=1 WHERE id=?", (a.id,)); con.commit()
    print(f"desfeito: {r['param']} voltou para {r['old_value']}")

def set_bias(con, bias, reason):
    con.execute("INSERT INTO bias_log(at,bias,reason) VALUES(?,?,?)", (now_brt().isoformat(timespec="seconds"), bias, reason))

def cmd_bias(con, a):
    if a.set:
        if not a.reason: sys.exit("REJEITADO: informe --reason (por que esse vies)")
        set_bias(con, a.set, a.reason); con.commit(); print("vies registrado:", a.set); return
    r = con.execute("SELECT * FROM bias_log ORDER BY at DESC, id DESC").fetchone()
    print("nenhum vies registrado" if not r else f"vies atual: {r['bias'].upper()} desde {r['at']} | motivo: {r['reason']}")

def cmd_shock(con, a):
    S = load_rules().get("shock", {}); gap_min = S.get("gap_atr_min", 0.5); rng_min = S.get("range_atr_min", 2.0)
    kinds, gap, gap_atr = [], None, None
    if a.prev_close is not None:
        gap = a.o - a.prev_close; gap_atr = abs(gap) / (a.atr_gap or a.atr)
        if gap_atr >= gap_min: kinds.append("gap")
    rng = a.h - a.l; rng_atr = rng / a.atr
    if rng_atr >= rng_min: kinds.append("vela_enorme")
    fvg = (None, None, None)
    if a.h1 is not None and a.l1 is not None:
        if a.l > a.h1: fvg = (a.h1, a.l, "alta")
        elif a.h < a.l1: fvg = (a.h, a.l1, "baixa")
        if fvg[2]: kinds.append("fvg")
    direction = "alta" if ((gap if gap else a.c - a.o) or 0) >= 0 else "baixa"
    if not kinds:
        print(f"sem choque (gap {gap_atr if gap_atr is not None else 'n/d'} x ATR < {gap_min}; vela {rng_atr:.2f} x ATR < {rng_min}; sem FVG)."); return
    con.execute("""INSERT INTO shocks(detected_at,kinds,gap_pts,gap_atr,range_atr,direction,fvg_low,fvg_high,fvg_dir)
                   VALUES(?,?,?,?,?,?,?,?,?)""", (now_brt().isoformat(timespec="seconds"), ",".join(kinds), gap, gap_atr, rng_atr, direction, fvg[0], fvg[1], fvg[2]))
    sid = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    set_bias(con, "vencido", f"choque #{sid} ({','.join(kinds)}): reavaliar")
    con.commit()
    print(f"*** CHOQUE DE MERCADO #{sid}: {', '.join(kinds)} | direcao {direction} ***")
    if gap is not None: print(f"  gap {gap:+.1f} pts ({gap_atr:.2f} x ATR) | vela {rng:.1f} pts ({rng_atr:.2f} x ATR)")
    if fvg[2]: print(f"  FVG de {fvg[2]}: {fvg[0]} a {fvg[1]}  -> regiao candidata (reteste); pontuar no mapa")
    print("  VIES = VENCIDO. PRIMEIRA TAREFA (rapido, ~5 min): entender o que esta acontecendo:")
    print("   1) O que mudou: numeros acima.")
    print("   2) Por que: `since` + noticias da janela, calendario da ultima hora, snapshot rapido de VIX, Brent, US10Y, ES, DXY.")
    print("   3) Classificar a causa e diagnosticar: shock-diagnose --id", sid, "--category ... --cause ... --confidence ... --bias-after ...")
    print("   4) So depois: regioes (FVG, novos extremos) e o restante do gate.")
    op = con.execute("SELECT * FROM trades WHERE closed_at IS NULL").fetchall()
    for t in op:
        print(f"  TRADE ABERTO #{t['id']} ({t['mode']}, {t['side']} em {t['entry']}, stop {t['stop']}): REVISAR stop/protecao AGORA.")

def cmd_shock_diagnose(con, a):
    r = con.execute("SELECT * FROM shocks WHERE id=? AND status='aberto'", (a.id,)).fetchone()
    if not r: sys.exit("choque nao encontrado ou ja diagnosticado")
    conf = a.confidence
    if a.category == "desconhecida" and conf != "baixa":
        print("aviso: causa desconhecida => confianca forcada para 'baixa'"); conf = "baixa"
    con.execute("UPDATE shocks SET status='diagnosticado', category=?, cause=?, confidence=?, diagnosed_at=?, notes=? WHERE id=?",
                (a.category, a.cause, conf, now_brt().isoformat(timespec="seconds"), a.note, a.id))
    set_bias(con, a.bias_after, f"apos choque #{a.id} ({a.category}, confianca {conf}): {a.cause}")
    con.commit(); print(f"choque #{a.id} diagnosticado ({a.category}, confianca {conf}); vies agora {a.bias_after.upper()}")
    if a.category == "desconhecida": print("  atencao: sem causa confirmada, a leitura do viés tem confianca baixa; continuar procurando a causa.")

def cmd_ready(con, a):
    G = load_rules().get("go_live", {})
    need_n = G.get("min_trades", 50); need_days = G.get("min_days", 10); need_exp = G.get("min_expectancy_r", 0.15)
    need_pf = G.get("min_profit_factor", 1.3); max_dd = G.get("max_drawdown_r", 6.0); sig = G.get("lower_bound_sigma", 1.0)
    rows = con.execute("SELECT * FROM trades WHERE closed_at IS NOT NULL AND mode='treino' ORDER BY closed_at").fetchall()
    n = len(rows); R = [r["result_r"] for r in rows]
    days = len({r["closed_at"][:10] for r in rows})
    print("=== JA DA PARA IR PARA A CONTA REAL? (baseado no treino) ===")
    if n == 0:
        print("NAO. Ainda nao ha trades fechados no treino."); return
    mean = sum(R) / n; var = sum((x - mean) ** 2 for x in R) / (n - 1) if n > 1 else 0.0
    se = (var ** 0.5) / (n ** 0.5) if n > 1 else float("inf"); lower = mean - sig * se
    wins = sum(x for x in R if x > 0); losses = -sum(x for x in R if x < 0)
    pf = wins / losses if losses > 0 else float("inf")
    peak = cum = dd = 0.0
    for x in R:
        cum += x; peak = max(peak, cum); dd = max(dd, peak - cum)
    checks = [
        (n >= need_n, f"trades no treino: {n} (minimo {need_n})"),
        (days >= need_days, f"dias diferentes operados: {days} (minimo {need_days})"),
        (mean >= need_exp, f"ganho medio por trade: {mean:+.2f}R (minimo {need_exp:+.2f}R)"),
        (lower > 0, f"ganho medio descontando a incerteza da amostra: {lower:+.2f}R (precisa ser positivo)"),
        (pf >= need_pf, f"lucro bruto / prejuizo bruto: {pf:.2f} (minimo {need_pf})"),
        (dd <= max_dd, f"maior queda acumulada: {dd:.1f}R (maximo {max_dd}R)"),
        (risk_cfg()[0] is not None, "risco maximo por trade para o REAL definido pela usuaria (hoje: nao definido)"),
    ]
    for ok, msg in checks: print(("  OK   " if ok else "  FALTA") + " " + msg)
    if all(ok for ok, _ in checks):
        print("RESULTADO: os criterios do treino foram cumpridos. Isso NAO garante lucro no real (spread, slippage e emocao pioram). Se for, comece com o menor tamanho possivel e com os limites de capital.")
    else:
        print("RESULTADO: AINDA NAO. Continue no treino; ir agora seria apostar, nao operar com vantagem comprovada.")
    print("(1R = o valor que voce arrisca em cada trade. Criterios sao escolhas minhas e podem ser mudadas por voce.)")

def cmd_entry_check(con, a):
    R = load_rules(); E = R.get("entry_trigger", {}); pr, bm = wick_cfg()
    buf = E.get("stop_buffer_atr", 0.25); min_rr = E.get("min_rr", 1.5)
    side = "compra" if a.zone_type == "demanda" else "venda"
    bl = con.execute("SELECT * FROM bias_log ORDER BY at DESC, id DESC").fetchone()
    bias = a.bias or (bl["bias"] if bl else "neutro")
    with_bias = (side == "compra" and bias == "alta") or (side == "venda" and bias == "baixa")
    min_score = R.get("regions", {}).get("min_score_with_macro" if with_bias else "min_score_against_macro", 3 if with_bias else 4)
    rng = a.h - a.l
    if rng <= 0: sys.exit("candle sem amplitude")
    body = abs(a.c - a.o); up = a.h - max(a.o, a.c); lo = min(a.o, a.c) - a.l
    if side == "compra":
        touched = a.l <= a.zone_high; wick_ok = lo >= pr * rng and lo >= bm * body; held = a.c >= a.zone_low
        stop = a.l - buf * a.atr
    else:
        touched = a.h >= a.zone_low; wick_ok = up >= pr * rng and up >= bm * body; held = a.c <= a.zone_high
        stop = a.h + buf * a.atr
    print(f"=== GATILHO M5 | regiao de {a.zone_type} {a.zone_low}-{a.zone_high} (nota {a.score}) | viés {bias.upper()} | lado {side.upper()} ===")
    print(f"  tocou a regiao: {'SIM' if touched else 'nao'} | rejeicao de pavio a favor: {'SIM' if wick_ok else 'nao'} | fechou sem romper a regiao: {'SIM' if held else 'nao'}")
    if not (touched and wick_ok and held):
        print("  SEM GATILHO. O mercado ainda nao mostrou a reacao (nao antecipar; esperar o candle M5 fechar).")
        if touched and not held: print("  atencao: fechou ALEM da regiao (rompimento): a regiao pode ter falhado.")
        return
    entry = a.c; dist = abs(entry - stop)
    flags = []
    if a.score is not None and a.score < min_score: flags.append(f"nota {a.score} abaixo do minimo {min_score} ({'a favor' if with_bias else 'contra/sem'} do viés): no treino entra e fica registrado; no real nao")
    if not with_bias: flags.append("lado CONTRA o viés (ou viés neutro): exige nota maior, risco menor e saida curta")
    print(f"  GATILHO PRESENTE: {side.upper()} | entrada ~{entry} | stop {stop:.1f} ({dist:.1f} pts)")
    tgt_txt = ""
    if a.target_low is not None and a.target_high is not None:
        near = a.target_low if side == "compra" else a.target_high; rr = abs(near - entry) / dist
        print(f"  alvo: borda proxima da regiao oposta {near} ({abs(near - entry):.1f} pts) | RR {rr:.2f}")
        if rr < min_rr: flags.append(f"RR {rr:.2f} abaixo do minimo {min_rr}")
        tgt_txt = f" --target1 {near} --zone-low {a.target_low} --zone-high {a.target_high}"
    else: flags.append("sem regiao-alvo informada: definir antes de entrar")
    per = risk_cfg()[0]
    if a.usd_per_point:
        if a.risk_usd is None: size = a.min_lot
        else: raw = a.risk_usd / (dist * a.usd_per_point); size = max(a.min_lot, round(raw / a.min_lot) * a.min_lot)
        real_risk = size * dist * a.usd_per_point
        print(f"  tamanho: {size:.2f} lote(s) | risco REAL nesse stop: US$ {real_risk:.2f}" + (f" (alvo de risco US$ {a.risk_usd})" if a.risk_usd is not None else " (lote minimo; o stop e definido pelo mercado, nao pelo dinheiro)"))
        if a.risk_usd is not None and real_risk > a.risk_usd * 1.05: flags.append(f"o lote minimo faz o risco real (US$ {real_risk:.2f}) passar do alvo (US$ {a.risk_usd})")
        if per is not None and real_risk > per: flags.append(f"risco real acima do maximo definido pela usuaria (US$ {per})")
        size_txt = f" --size {size:.2f} --risk-usd {real_risk:.2f}"
    else:
        flags.append("sem --usd-per-point nao da para calcular o risco real; informar o valor do ponto na Pepperstone")
        size_txt = f" --risk-usd {a.risk_usd if a.risk_usd is not None else 'CALCULAR'}"
    for f in flags: print("  aviso:", f)
    print(f"  registrar: open-trade --mode treino --side {side} --entry {entry} --stop {stop:.1f}{tgt_txt}{size_txt} --region-score {a.score} --bias {bias}")

def cmd_stats(con, a):
    rows = con.execute("SELECT * FROM trades WHERE closed_at IS NOT NULL AND mode=?", (a.mode,)).fetchall()
    if not rows: print(f"sem trades fechados no modo {a.mode}"); return
    avg = lambda xs: sum(xs) / len(xs) if xs else 0
    R = [r["result_r"] for r in rows]; give = [(r["mfe_r"] or 0) - r["result_r"] for r in rows]
    rev = [r for r in rows if (r["mfe_r"] or 0) >= 1 and r["result_r"] <= 0]
    print(f"Modo {a.mode}: {len(rows)} trades | acerto {100*sum(1 for x in R if x>0)/len(R):.0f}% | R medio {avg(R):+.2f} | MFE medio {avg([r['mfe_r'] or 0 for r in rows]):.2f}R | devolvido em media {avg(give):.2f}R")
    print(f"Chegaram a +1R e terminaram em 0 ou negativo: {len(rev)} de {len(rows)} (argumento para parcial/break-even)")
    zr = [(r, edge_r(r)) for r in rows if edge_r(r) is not None]
    if zr:
        reached = [(r, e) for r, e in zr if (r["mfe_r"] or 0) >= e]
        print(f"Com regiao-alvo: {len(zr)} trades | chegaram na borda da regiao: {len(reached)} | dos que chegaram, R medio final {avg([r['result_r'] for r, _ in reached]):+.2f} (vs MFE {avg([r['mfe_r'] for r, _ in reached]):.2f}R)")
    print("Por motivo de saida:")
    for k in sorted({r["exit_reason"] for r in rows}):
        g = [r for r in rows if r["exit_reason"] == k]; print(f"  {k}: {len(g)} trades, R medio {avg([x['result_r'] for x in g]):+.2f}")
    print("Por estado do gate na entrada (treino: compara o efeito de cada dever de casa):")
    for v, lab in ((1, "gate OK"), (0, "gate com pendencias")):
        g = [r for r in rows if r["gate_ok"] == v]
        if g: print(f"  {lab}: {len(g)} trades, R medio {avg([x['result_r'] for x in g]):+.2f}")
    print("Amostra pequena nao prova nada: olhar 30-50 trades.")

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
    ot = sub.add_parser("open-trade")
    ot.add_argument("--mode", choices=["treino", "real"], required=True); ot.add_argument("--side", choices=["compra", "venda"], required=True)
    ot.add_argument("--entry", type=float, required=True); ot.add_argument("--stop", type=float, required=True)
    ot.add_argument("--target1", type=float); ot.add_argument("--target2", type=float); ot.add_argument("--size", type=float)
    ot.add_argument("--risk-usd", type=float, required=True); ot.add_argument("--region-score", type=float)
    ot.add_argument("--bias"); ot.add_argument("--plan-id", type=int); ot.add_argument("--notes")
    ot.add_argument("--zone-low", type=float); ot.add_argument("--zone-high", type=float)
    ut = sub.add_parser("update-trade"); ut.add_argument("--id", type=int, required=True)
    ut.add_argument("--high", type=float, required=True); ut.add_argument("--low", type=float, required=True); ut.add_argument("--be-moved", action="store_true")
    ct = sub.add_parser("close-trade"); ct.add_argument("--id", type=int, required=True); ct.add_argument("--exit-price", type=float, required=True)
    ct.add_argument("--reason", required=True, choices=["stop", "alvo1", "alvo2", "breakeven", "trailing", "invalidacao", "tempo", "evento", "manual", "fim_dia"])
    ct.add_argument("--high", type=float); ct.add_argument("--low", type=float); ct.add_argument("--notes")
    pt = sub.add_parser("path"); pt.add_argument("--id", type=int, required=True); pt.add_argument("--price", type=float, required=True)
    pt.add_argument("--quality", choices=["forte", "fraca", "lateral", "revertendo"], required=True)
    pt.add_argument("--pairs", choices=["sim", "parcial", "nao"], required=True); pt.add_argument("--note")
    pt.add_argument("--wick", choices=["nenhum", "superior", "inferior"], default="nenhum")
    pt.add_argument("--wick-where", choices=["zona", "caminho"])
    for k in ("o", "h", "l", "c"): pt.add_argument("--" + k, type=float)
    wk = sub.add_parser("wick"); [wk.add_argument("--" + k, type=float, required=True) for k in ("open", "high", "low", "close")]; wk.add_argument("--atr", type=float)
    tn = sub.add_parser("tune"); tn.add_argument("--param", required=True); tn.add_argument("--value", type=float, required=True)
    tn.add_argument("--reason", required=True); tn.add_argument("--evidence-kind", choices=["trades", "exemplos"], required=True)
    tn.add_argument("--evidence-n", type=int, required=True); tn.add_argument("--mode", choices=["treino", "real"], default="treino")
    tn.add_argument("--user-approved", action="store_true")
    sub.add_parser("tune-history"); tr = sub.add_parser("tune-revert"); tr.add_argument("--id", type=int, required=True)
    bs = sub.add_parser("bias"); bs.add_argument("--set", choices=["alta", "baixa", "neutro"]); bs.add_argument("--reason")
    sk = sub.add_parser("shock"); sk.add_argument("--tf", default="M5"); sk.add_argument("--prev-close", type=float)
    for k in ("o", "h", "l", "c", "atr"): sk.add_argument("--" + k, type=float, required=True)
    sk.add_argument("--atr-gap", type=float, help="ATR (ex.: H1) para medir o gap; padrao = --atr")
    sk.add_argument("--h1", type=float, help="maxima do candle de 2 barras atras (para FVG)"); sk.add_argument("--l1", type=float, help="minima do candle de 2 barras atras (para FVG)")
    sd = sub.add_parser("shock-diagnose"); sd.add_argument("--id", type=int, required=True)
    sd.add_argument("--category", required=True, choices=["petroleo", "geopolitica", "ia_tech", "fed_juros", "dados", "resultado", "liquidez_tecnica", "desconhecida"])
    sd.add_argument("--cause", required=True); sd.add_argument("--confidence", required=True, choices=["alta", "media", "baixa"])
    sd.add_argument("--bias-after", required=True, choices=["alta", "baixa", "neutro"]); sd.add_argument("--note")
    sub.add_parser("ready")
    ec = sub.add_parser("entry-check")
    ec.add_argument("--zone-type", choices=["demanda", "oferta"], required=True)
    for k in ("zone-low", "zone-high", "o", "h", "l", "c", "atr"): ec.add_argument("--" + k, type=float, required=True)
    ec.add_argument("--score", type=float); ec.add_argument("--bias", choices=["alta", "baixa", "neutro"])
    ec.add_argument("--target-low", type=float); ec.add_argument("--target-high", type=float)
    ec.add_argument("--risk-usd", type=float, default=None); ec.add_argument("--usd-per-point", type=float, help="USD por ponto para 1 lote (confirmar na Pepperstone)")
    ec.add_argument("--min-lot", type=float, default=0.01)
    st = sub.add_parser("stats"); st.add_argument("--mode", choices=["treino", "real"], default="treino")
    sub.add_parser("themes"); sub.add_parser("gate"); sub.add_parser("since")
    sm = sub.add_parser("add-sentiment"); sm.add_argument("--source", required=True); sm.add_argument("--metric", required=True)
    sm.add_argument("--value"); sm.add_argument("--data-date"); sm.add_argument("--reading", choices=["risk_on", "risk_off", "neutro", "misto"], required=True); sm.add_argument("--note")
    rr = sub.add_parser("renew-read"); rr.add_argument("--pair", required=True); rr.add_argument("--tf", required=True); rr.add_argument("--note", required=True)
    ar = sub.add_parser("add-read")
    ar.add_argument("--pair", required=True); ar.add_argument("--tf", required=True)
    ar.add_argument("--trend", choices=["alta", "baixa", "lateral"], required=True); ar.add_argument("--structure")
    ar.add_argument("--why", required=True); ar.add_argument("--news-id", type=int)
    ar.add_argument("--implication", choices=["favorece_alta", "favorece_baixa", "neutro", "conflito"], required=True)
    ar.add_argument("--divergence"); ar.add_argument("--confidence", choices=["alta", "media", "baixa"], required=True)
    ar.add_argument("--invalidation", required=True)
    rd = sub.add_parser("reads"); rd.add_argument("--pair")
    mc = sub.add_parser("mark-checked"); mc.add_argument("--name", choices=["calendar", "holidays", "extra_events", "news"], required=True); mc.add_argument("--note")
    bf = sub.add_parser("brief"); bf.add_argument("--date")
    hl = sub.add_parser("upsert-holidays"); hl.add_argument("file")
    ue = sub.add_parser("upsert-extra"); ue.add_argument("file")
    ap = sub.add_parser("add-plan")
    ap.add_argument("--date"); ap.add_argument("--theme", required=True); ap.add_argument("--correlated", required=True)
    ap.add_argument("--up"); ap.add_argument("--down"); ap.add_argument("--position", required=True)
    ap.add_argument("--stance", choices=["compra", "venda"], required=True)
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
     "window": cmd_window, "themes": cmd_themes, "open-trade": cmd_open_trade, "update-trade": cmd_update_trade, "close-trade": cmd_close_trade, "stats": cmd_stats, "ready": cmd_ready, "entry-check": cmd_entry_check, "bias": cmd_bias, "shock": cmd_shock, "shock-diagnose": cmd_shock_diagnose, "tune": cmd_tune, "tune-history": cmd_tune_history, "tune-revert": cmd_tune_revert, "path": cmd_path, "wick": cmd_wick, "gate": cmd_gate, "since": cmd_since, "add-sentiment": cmd_add_sentiment, "renew-read": cmd_renew_read, "add-read": cmd_add_read, "reads": cmd_reads, "mark-checked": cmd_mark_checked, "brief": cmd_brief, "upsert-holidays": cmd_upsert_holidays,
     "upsert-extra": cmd_upsert_extra, "add-plan": cmd_add_plan, "close-plan": cmd_close_plan, "upsert-news": cmd_upsert_news, "news": cmd_news,
     "set-actual": cmd_set_actual, "add-reaction": cmd_add_reaction}[a.cmd](con, a)

if __name__ == "__main__":
    main()
