"""Estudo ENTRE SESSOES do NAS100 (CFD Dukascopy M1, 2 anos): como cada sessao se comporta e o que uma faz com a outra.
Sessoes (BRT = UTC-3, sem horario de verao no Brasil; janelas do projeto em docs/sessoes-e-niveis.md):
 NYPM 14:30-17:00 | PAUSA 18:00-19:00 | SYDNEY 19:00-21:00 | ASIA 21:00-03:00 | LONDRES 03:00-10:30 | NYAM 10:30-13:00 | ALMOCO 13:00-14:30
Uso: python -I scripts/estudo_sessoes.py   (le tools/edge-lab/out/usatech_m1.csv, gerado por: bash scripts/edge.sh export --table bars --symbol USATECH --out ...)"""
import csv, datetime as dt, statistics as st, math
def _ny(u):  # UTC -> hora de NY + 1h (= 'BRT de verao'): a abertura de NY fica SEMPRE em 10:30, com ou sem horario de verao dos EUA
    y=u.year
    def nth(m,k):
        d=dt.date(y,m,1);c=0
        while True:
            if d.weekday()==6:
                c+=1
                if c==k:return d
            d+=dt.timedelta(days=1)
    a=dt.datetime.combine(nth(3,2),dt.time(7));b=dt.datetime.combine(nth(11,1),dt.time(6))  # 2h NY = 7h UTC (EST) / 6h UTC (EDT)
    return u+dt.timedelta(hours=(-4 if a<=u<b else -5)+1)
rows = []
with open('tools/edge-lab/out/usatech_m1.csv', encoding='utf8') as f:
    for r in csv.DictReader(f):
        t = _ny(dt.datetime.fromtimestamp(int(r['ts']) / 1000, dt.timezone.utc).replace(tzinfo=None))
        rows.append((t, float(r['open']), float(r['high']), float(r['low']), float(r['close'])))
SES = [('SYDNEY', 19 * 60, 21 * 60), ('ASIA', 21 * 60, 27 * 60), ('LONDRES', 27 * 60, 34 * 60 + 30), ('NYAM', 34 * 60 + 30, 37 * 60),
       ('ALMOCO', 37 * 60, 38 * 60 + 30), ('NYPM', 38 * 60 + 30, 41 * 60)]  # minutos desde 00:00 do dia de ABERTURA (19:00 BRT); 24h+ = dia seguinte
def day_key(t):  # dia de negociacao: comeca 19:00 BRT
    return (t - dt.timedelta(hours=19)).date()
days = {}
for t, o, h, l, c in rows:
    k = day_key(t)
    m = (t - dt.datetime.combine(k, dt.time(19, 0))).total_seconds() / 60  # minutos desde 19:00 BRT
    mm = m + 19 * 60
    for nm, a, b in SES:
        if a <= mm < b: days.setdefault(k, {}).setdefault(nm, []).append((t, o, h, l, c))
agg = {}
for k, ses in days.items():
    d = {}
    for nm, bars in ses.items():
        if len(bars) < 20: continue
        d[nm] = dict(o=bars[0][1], c=bars[-1][4], h=max(b[2] for b in bars), l=min(b[3] for b in bars), bars=bars)
    if len(d) >= 5: agg[k] = d
ks = sorted(agg)
print(f'{len(ks)} dias de negociacao, {ks[0]} a {ks[-1]}')
def ci(p, n):  # Wilson 95%
    z = 1.96; d = 1 + z * z / n; c = p + z * z / (2 * n); a = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - a) / d, (c + a) / d
print('\n1) Cada sessao: sobe mais que cai? tamanho tipico (pontos, % do preco)')
print(f'{"sessao":9s} {"N":>4s} {"%alta":>6s} {"IC95":>13s} {"mov. mediano":>12s} {"amplitude mediana":>17s}')
for nm, _, _ in SES:
    x = [agg[k][nm] for k in ks if nm in agg[k]]
    up = sum(s['c'] > s['o'] for s in x) / len(x); lo, hi = ci(up, len(x))
    print(f'{nm:9s} {len(x):4d} {up*100:5.1f}% [{lo*100:4.1f},{hi*100:4.1f}] {st.median(abs(s["c"]-s["o"]) for s in x):10.0f}pt {st.median(s["h"]-s["l"] for s in x):15.0f}pt')
order = [n for n, _, _ in SES]
print('\n2) A sessao anterior PREVE a seguinte? (quando a anterior foi de alta, a proxima foi de alta?)')
print(f'{"anterior -> proxima":22s} {"N":>4s} {"prox alta|ant alta":>19s} {"prox alta|ant baixa":>20s}')
for a, b in zip(order, order[1:]):
    pa = [agg[k] for k in ks if a in agg[k] and b in agg[k]]
    ua = [s[b]['c'] > s[b]['o'] for s in pa if s[a]['c'] > s[a]['o']]; da = [s[b]['c'] > s[b]['o'] for s in pa if s[a]['c'] <= s[a]['o']]
    print(f'{a+" -> "+b:22s} {len(pa):4d} {sum(ua)/len(ua)*100:12.1f}% (n={len(ua)}) {sum(da)/len(da)*100:12.1f}% (n={len(da)})')
print('\n3) Varredura entre sessoes: a sessao seguinte rompe a maxima/minima da anterior?')
print(f'{"anterior -> proxima":22s} {"varre max":>9s} {"varre min":>9s} {"varre as 2":>10s} {"nenhuma":>8s}')
for a, b in zip(order, order[1:]):
    pa = [agg[k] for k in ks if a in agg[k] and b in agg[k]]; n = len(pa)
    vh = [s[b]['h'] > s[a]['h'] for s in pa]; vl = [s[b]['l'] < s[a]['l'] for s in pa]
    print(f'{a+" -> "+b:22s} {sum(vh)/n*100:8.0f}% {sum(vl)/n*100:8.0f}% {sum(1 for x,y in zip(vh,vl) if x and y)/n*100:9.0f}% {sum(1 for x,y in zip(vh,vl) if not x and not y)/n*100:7.0f}%')
print('\n4) Depois de varrer, a sessao FECHA na direcao da varredura ou reverte? (varreu a maxima da anterior -> fechou acima da maxima?)')
for a, b in (('SYDNEY', 'ASIA'), ('ASIA', 'LONDRES'), ('LONDRES', 'NYAM'), ('NYAM', 'ALMOCO'), ('ALMOCO', 'NYPM')):
    pa = [agg[k] for k in ks if a in agg[k] and b in agg[k]]
    sh = [s for s in pa if s[b]['h'] > s[a]['h'] and not s[b]['l'] < s[a]['l']]; sl = [s for s in pa if s[b]['l'] < s[a]['l'] and not s[b]['h'] > s[a]['h']]
    r1 = sum(s[b]['c'] > s[a]['h'] for s in sh) / len(sh) if sh else float('nan'); r2 = sum(s[b]['c'] < s[a]['l'] for s in sl) / len(sl) if sl else float('nan')
    print(f'  {b:8s} varreu so a MAX de {a:8s} (n={len(sh):3d}): fechou acima da max {r1*100:4.0f}% | so a MIN (n={len(sl):3d}): fechou abaixo da min {r2*100:4.0f}%')
print('\n5) Dia inteiro: a direcao da sessao X tem a ver com o fechamento do dia (NYPM)?')
for nm in order[:-1]:
    pa = [agg[k] for k in ks if nm in agg[k] and 'NYPM' in agg[k]]
    same = sum((s[nm]['c'] > s[nm]['o']) == (s['NYPM']['c'] > s['NYPM']['o']) for s in pa) / len(pa)
    print(f'  {nm:8s} e NYPM andam na mesma direcao em {same*100:4.1f}% dos dias (N={len(pa)}; acaso = ~50%)')
k = ks[-1]; print(f'\n6) HOJE e ontem (dia de negociacao iniciado em {ks[-2]} e {k}): movimento de cada sessao')
for kk in ks[-2:]:
    print(' ', kk, ' '.join(f'{nm}:{agg[kk][nm]["c"]-agg[kk][nm]["o"]:+.0f}' for nm in order if nm in agg[kk]))
