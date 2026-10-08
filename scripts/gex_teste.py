"""TESTE DO GEX (usuaria, 08/10/2026: "entao testa"). O GEX gratis (CBOE) so existe AGORA, sem historico: o unico teste honesto e o forward:
cada leitura vai para journal/gex_log.csv (data,hora_brt,preco,regime,flip,muro_call,muro_put) e este script mede, por dia, o que o preco fez depois.
Perguntas: (1) regime NEGATIVO tem amplitude de sessao NY maior que POSITIVO? (2) quando o preco chega a +-20 pts de um muro (call/put), 60 min depois ele esta do lado de dentro (muro segurou) ou do lado de fora (rompeu)?
Dados: CFD Dukascopy M1 (bash scripts/edge.sh sync; export). Uso: python -I scripts/gex_teste.py   (N<20 leituras = sem conclusao)."""
import csv, subprocess, os, datetime as dt, statistics as st, collections
OUT = 'tools/edge-lab/out/usatech_m1.csv'
subprocess.run(['bash', 'scripts/edge.sh', 'sync'], capture_output=True)
subprocess.run(['bash', 'scripts/edge.sh', 'export', '--table', 'bars', '--symbol', 'USATECH', '--since', '2026-10-01', '--out', os.path.abspath(OUT)], capture_output=True)
def nth(y, m, k):
    d = dt.date(y, m, 1); c = 0
    while True:
        if d.weekday() == 6:
            c += 1
            if c == k: return d
        d += dt.timedelta(days=1)
bars = []
for r in csv.DictReader(open(OUT, encoding='utf8')):
    u = dt.datetime.fromtimestamp(int(r['ts']) / 1000, dt.timezone.utc).replace(tzinfo=None)
    a = dt.datetime.combine(nth(u.year, 3, 2), dt.time(7)); b = dt.datetime.combine(nth(u.year, 11, 1), dt.time(6))
    t = u + dt.timedelta(hours=(-4 if a <= u < b else -5) + 1)  # relogio BRT de verao (NY+1h)
    bars.append((t, float(r['high']), float(r['low']), float(r['close'])))
log = list(csv.DictReader(open('journal/gex_log.csv', encoding='utf8')))
por_dia = collections.defaultdict(list)
for r in log: por_dia[r['data']].append(r)
print(f'{len(log)} leituras em {len(por_dia)} dias')
print('\n1) amplitude da sessao NY (10:30-17:00 BRT) por regime da 1a leitura do dia')
reg = collections.defaultdict(list)
for d, rs in sorted(por_dia.items()):
    day = dt.date.fromisoformat(d); s = [b for b in bars if b[0].date() == day and dt.time(10, 30) <= b[0].time() < dt.time(17, 0)]
    if len(s) < 100: print(f'  {d}: sessao NY incompleta/sem dado ({len(s)} velas)'); continue
    rng = max(b[1] for b in s) - min(b[2] for b in s); k = rs[0]['regime']; reg[k].append(rng); print(f'  {d} regime {k}: amplitude NY {rng:.0f} pts')
for k, v in reg.items(): print(f'  {k}: N={len(v)} mediana {st.median(v):.0f} pts')
print('\n2) muros: preco chegou a +-20 pts; onde estava 60 min depois (dentro/fora do muro)')
res = []
for d, rs in sorted(por_dia.items()):
    day = dt.date.fromisoformat(d); last = rs[-1]
    for nome, w in (('call', float(last['muro_call'])), ('put', float(last['muro_put']))):
        if w <= 0: continue
        ts = [b for b in bars if b[0].date() == day and dt.time(10, 30) <= b[0].time() < dt.time(17, 0)]
        hit = next((i for i, b in enumerate(ts) if b[2] - 20 <= w <= b[1] + 20), None)
        if hit is None: print(f'  {d} muro {nome} {w:.0f}: nao tocou'); continue
        fut = ts[min(hit + 60, len(ts) - 1)][3]; dentro = (fut < w) if nome == 'call' else (fut > w)
        res.append(dentro); print(f'  {d} muro {nome} {w:.0f}: tocou {ts[hit][0]:%H:%M}; 60 min depois {fut:.0f} -> {"SEGUROU" if dentro else "ROMPEU"}')
if res: print(f'  segurou {sum(res)}/{len(res)}  (N<20: sem conclusao; acaso ~50%)')
print('\nConclusao: so valida o GEX com >= 20 dias. Ate la e contexto, nao gatilho.')
