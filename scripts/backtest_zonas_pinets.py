"""Backtest da AVALIACAO DAS ZONAS (pine/structure_vp_smc.pine) rodada no PineTS sobre velas M5 do MT5.
Gerar os dados: cd tools/pinets-lab && node rodar_zonas.mjs  (saida_zonas.json = velas + plots por barra)
Evento = 1o toque numa zona (oferta = venda, demanda = compra). Nota = a da propria barra do toque (0-7).
Variante A: limite na borda da zona (usa a nota da barra do toque = pequeno vies de olhar adiante).
Variante B: entrada a mercado na ABERTURA da barra seguinte (sem olhar adiante).
Stop = lado oposto da zona + 0,5 ATR; alvo = k x risco (stop primeiro se os dois na mesma vela); horizonte 36 barras (3h)."""
import json, statistics as st, sys
D = json.load(open('tools/pinets-lab/saida_zonas.json'))
t, O, H, L, C, P = D['t'], D['o'], D['h'], D['l'], D['c'], D['plots']
n = len(t)
for _k, _v in list(P.items()):
    if len(_v) < n: P[_k] = [None] * (n - len(_v)) + _v
g = lambda k, i: P[k][i]
def sim(i0, side, entry, stop, k, hor=36):
    risk = abs(entry - stop)
    if risk <= 0: return None
    tgt = entry + side * k * risk
    for j in range(i0, min(n, i0 + hor)):
        hit_stop = L[j] <= stop if side == 1 else H[j] >= stop
        hit_tgt = H[j] >= tgt if side == 1 else L[j] <= tgt
        if hit_stop: return -1.0
        if hit_tgt: return k
    return (C[min(n - 1, i0 + hor - 1)] - entry) * side / risk
ev = []
for who in ('s', 'd'):
    side = -1 if who == 's' else 1
    prev_key = None; prev_in = False
    for i in range(1, n):
        sc, bo, to = g(who + 'Score', i), g(who + 'Bot', i), g(who + 'Top', i)
        if sc is None or bo is None or to is None or g('atr', i) is None:
            prev_key = None; prev_in = False; continue
        key = (round(bo, 1), round(to, 1)); inside = H[i] >= bo and L[i] <= to
        if inside and not (prev_key == key and prev_in):
            atr = g('atr', i)
            ent = bo if who == 's' else to
            stp = to + 0.5 * atr if who == 's' else bo - 0.5 * atr
            flags = {c: g(who + c, i) for c in ('CE', 'CP', 'CV', 'CC', 'CF', 'CL', 'CR')}
            ev.append(dict(i=i, who=who, side=side, score=int(sc), ent=ent, stp=stp, flags=flags))
        prev_key = key; prev_in = inside
print(f'{n} barras, {len(ev)} eventos de 1o toque ({sum(e["who"]=="s" for e in ev)} oferta / {sum(e["who"]=="d" for e in ev)} demanda)')
def bucket(s): return 'BOA 5-7' if s >= 5 else 'MEDIA 3-4' if s >= 3 else 'FRACA 0-2'
def rep(titulo, rs):
    if not rs: print(f'  {titulo:12s} n=0'); return
    m = sum(rs) / len(rs); w = sum(r > 0 for r in rs) / len(rs) * 100
    sd = st.pstdev(rs) if len(rs) > 1 else 0; se = sd / len(rs) ** .5 if len(rs) > 1 else 0
    print(f'  {titulo:12s} n={len(rs):4d}  acerto {w:5.1f}%  R medio {m:+.2f}  (erro padrao {se:.2f})')
for var in ('A', 'B'):
    for k in (1.0, 1.5):
        print(f'\nVariante {var} (alvo {k}R) - R por nota')
        res = {}
        for e in ev:
            if var == 'A': r = sim(e['i'], e['side'], e['ent'], e['stp'], k)
            else:
                if e['i'] + 1 >= n: continue
                ent = O[e['i'] + 1]; r = sim(e['i'] + 1, e['side'], ent, e['stp'], k)
                if r is None or (e['side'] == -1 and ent >= e['stp']) or (e['side'] == 1 and ent <= e['stp']): continue
            if r is not None: res.setdefault(bucket(e['score']), []).append(r)
        for b in ('BOA 5-7', 'MEDIA 3-4', 'FRACA 0-2'): rep(b, res.get(b, []))
        rep('TODAS', [r for v in res.values() for r in v])
print('\nPor criterio (variante A, alvo 1R): R medio com criterio verdadeiro x falso')
names = dict(CE='estrutura a favor', CP='premio/desconto', CV='lado do VWAP', CC='confluencia OB+FVG', CF='1o toque', CL='sem liquidez colada', CR='R:R>=1,5')
for c, nm in names.items():
    a = [sim(e['i'], e['side'], e['ent'], e['stp'], 1.0) for e in ev if e['flags'][c] == 1]
    b = [sim(e['i'], e['side'], e['ent'], e['stp'], 1.0) for e in ev if e['flags'][c] == 0]
    a = [x for x in a if x is not None]; b = [x for x in b if x is not None]
    ma = sum(a) / len(a) if a else float('nan'); mb = sum(b) / len(b) if b else float('nan')
    print(f'  {nm:22s} sim n={len(a):4d} R {ma:+.2f} | nao n={len(b):4d} R {mb:+.2f} | dif {ma-mb:+.2f}')

print('\nPor criterio (variante B = sem olhar adiante, alvo 1R): R medio sim x nao')
def simB(e, k=1.0):
    if e['i'] + 1 >= n: return None
    ent = O[e['i'] + 1]
    if (e['side'] == -1 and ent >= e['stp']) or (e['side'] == 1 and ent <= e['stp']): return None
    return sim(e['i'] + 1, e['side'], ent, e['stp'], k)
for c, nm in names.items():
    a = [x for x in (simB(e) for e in ev if e['flags'][c] == 1) if x is not None]
    b = [x for x in (simB(e) for e in ev if e['flags'][c] == 0) if x is not None]
    ma = sum(a) / len(a); mb = sum(b) / len(b)
    se = (st.pstdev(a) ** 2 / len(a) + st.pstdev(b) ** 2 / len(b)) ** .5
    print(f'  {nm:22s} sim n={len(a):4d} R {ma:+.2f} | nao n={len(b):4d} R {mb:+.2f} | dif {ma-mb:+.2f} (+-{1.96*se:.2f})')
