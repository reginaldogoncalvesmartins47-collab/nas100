"""Abertura de NY (09:30 ET = 16:30 servidor MT5) x dados das 10:00 ET (17:00 servidor). NAS100 M5, 02/10/2025-01/05/2026.
Pergunta: a abertura de NY move mais que o dado? Depois do spike de abertura, vender/comprar contra ele funciona?"""
import json, pandas as pd, numpy as np
df = pd.read_csv("data/nas100_m5_mt5.csv", sep="\t")
df.columns = [c.strip("<>").lower() for c in df.columns]
df["t"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M:%S")
df = df.set_index("t")[["open", "high", "low", "close"]]
ev = json.load(open("data/investing/eventos_us.json", encoding="utf-8")); oc = json.load(open("data/investing/ocorrencias_us.json", encoding="utf-8"))
dias10 = set()  # dias com evento medio/alto as 10:00 ET (14:00Z ou 15:00Z)
for k, lst in oc.items():
    if ev.get(k, {}).get("i", 0) < 2: continue
    for r in lst:
        d, h = r[0][:10], r[0][11:16]
        if h in ("14:00", "15:00"): dias10.add(d)
rows = []
for d, g in df.groupby(df.index.date):
    ds = str(d)
    if pd.Timestamp(d).weekday() > 4: continue
    def bar(hhmm):
        ts = pd.Timestamp(f"{ds} {hhmm}")
        return g.loc[ts] if ts in g.index else None
    b0, b45, b10 = bar("16:30"), bar("16:45"), bar("17:00")   # abertura / 09:45 ET (PMI flash-like) / 10:00 ET
    pre = bar("16:25"); c35 = bar("16:35"); e = bar("16:40")
    if any(x is None for x in (b0, b45, b10, pre, c35, e)): continue
    f = lambda b: b.high - b.low
    sp = b0.close - b0.open                                   # spike da abertura (vela das 09:30)
    ent = e.close                                             # entrada contra o spike apos 2 velas (~09:40 ET, como a venda de 05/10)
    jan = g.loc[pd.Timestamp(f"{ds} 16:45"):pd.Timestamp(f"{ds} 18:00")]   # 60 min seguintes
    if len(jan) < 10: continue
    lado = -np.sign(sp)                                       # contra o spike
    fav = (jan.low.min() - ent) * -1 if lado < 0 else (jan.high.max() - ent)
    adv = (jan.high.max() - ent) if lado < 0 else (ent - jan.low.min())
    fim = (jan.close.iloc[-1] - ent) * lado
    rows.append(dict(d=ds, r_open=f(b0), r_45=f(b45), r_10=f(b10), spike=sp, dado10=ds in dias10, fav=fav, adv=adv, fim=fim, cont=np.sign(jan.close.iloc[-1] - ent) == np.sign(sp)))
R = pd.DataFrame(rows)
print(f"dias: {len(R)} | com dado medio/alto as 10:00 ET: {R.dado10.sum()}")
print("\nAmplitude mediana (pts) por vela M5:")
print(f"  09:30 ET (abertura NY) : {R.r_open.median():.0f}")
print(f"  09:45 ET (PMI servicos): {R.r_45.median():.0f}")
print(f"  10:00 ET dia COM dado  : {R[R.dado10].r_10.median():.0f}   dia SEM dado: {R[~R.dado10].r_10.median():.0f}")
print(f"  abertura > vela 10:00 ET em {(R.r_open > R.r_10).mean()*100:.0f}% dos dias (com dado: {(R[R.dado10].r_open > R[R.dado10].r_10).mean()*100:.0f}%)")
big = R[R.spike.abs() >= R.spike.abs().quantile(0.66)]
print(f"\nSpikes grandes (|vela 09:30| >= {R.spike.abs().quantile(0.66):.0f} pts, n={len(big)}) e a entrada CONTRA o spike 10 min depois:")
for nome, S in (("todos", R), ("spike grande", big), ("spike grande p/ CIMA (venda)", big[big.spike > 0]), ("spike grande p/ BAIXO (compra)", big[big.spike < 0])):
    print(f"  {nome:32s} n={len(S):3d} | continuou no spike 60min: {S.cont.mean()*100:3.0f}% | fav medio {S.fav.mean():6.1f} adv medio {S.adv.mean():6.1f} | resultado final contra-spike {S.fim.mean():+6.1f} pts")
