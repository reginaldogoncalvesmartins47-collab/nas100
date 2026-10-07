"""Madrugada: Asia x Londres x NY no NAS100 (M5 MT5, 02/10/2025-01/05/2026). Servidor MT5 = ET+7h; BRT = ET+1h (DST EUA) => BRT ~ servidor-6h.
Asia = 21:00-03:00 BRT = servidor 03:00-09:00; Londres = 03:00-10:30 BRT = servidor 09:00-16:30; NY = 16:30-23:00 servidor.
1) Amplitude por sessao (pts, e em % do preco). 2) Varrida da max/min da Asia na abertura de Londres (09:00-11:00 servidor) e o que vem depois."""
import pandas as pd, numpy as np
df = pd.read_csv("data/nas100_m5_mt5.csv", sep="\t"); df.columns = [c.strip("<>").lower() for c in df.columns]
df["t"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M:%S"); df = df.set_index("t")[["open", "high", "low", "close"]]
rows = []; sw = []
for d, g in df.groupby(df.index.date):
    if pd.Timestamp(d).weekday() > 4: continue
    D = pd.Timestamp(d)
    def win(a, b): return g.loc[D + pd.Timedelta(hours=a):D + pd.Timedelta(hours=b) - pd.Timedelta(minutes=5)]
    A, L, N = win(3, 9), win(9, 16.5), win(16.5, 23)
    if min(len(A), len(L), len(N)) < 30: continue
    px = A.close.iloc[-1]
    rows.append(dict(asia=A.high.max() - A.low.min(), lon=L.high.max() - L.low.min(), ny=N.high.max() - N.low.min(), px=px))
    ah, al = A.high.max(), A.low.min()
    L1 = win(9, 11)          # abertura de Londres (2h)
    L2 = win(11, 14)         # 3h seguintes
    if len(L1) < 20 or len(L2) < 20: continue
    up = L1.high.max() > ah; dn = L1.low.min() < al
    if up == dn: continue    # so varrida de UM lado
    side = "alta(max Asia varrida)" if up else "baixa(min Asia varrida)"
    back = L1.close.iloc[-1] < ah if up else L1.close.iloc[-1] > al   # voltou para dentro do range da Asia
    ent = L1.close.iloc[-1]
    # trade contra a varrida se voltou para dentro: alvo = lado oposto do range, stop = extremo da varrida
    ext = L1.high.max() if up else L1.low.min()
    tgt = al if up else ah
    risk = abs(ext - ent); reward = abs(ent - tgt)
    hit = None
    for _, b in L2.iterrows():
        if up:
            if b.high >= ext: hit = -1; break
            if b.low <= tgt: hit = 1; break
        else:
            if b.low <= ext: hit = -1; break
            if b.high >= tgt: hit = 1; break
    sw.append(dict(d=str(d), side=side, back=back, risk=risk, reward=reward, hit=hit, cont=(L2.close.iloc[-1] - ent) * (-1 if up else 1)))
R = pd.DataFrame(rows); S = pd.DataFrame(sw)
f = lambda s: f"{s.median():.0f} pts (media {s.mean():.0f}; {s.median()/R.px.median()*100:.2f}% do preco)"
print(f"dias: {len(R)}")
print("Amplitude mediana por sessao:")
print("  Asia   :", f(R.asia)); print("  Londres:", f(R.lon)); print("  NY     :", f(R.ny))
print(f"  Londres/Asia = {R.lon.median()/R.asia.median():.1f}x | Londres/NY = {R.lon.median()/R.ny.median():.2f}x")
print(f"\nVarrida de UM lado da Asia na abertura de Londres (09-11h servidor): {len(S)} dias de {len(R)}")
for k, X in S.groupby("side"):
    print(f"  {k}: n={len(X)} | voltou p/ dentro do range: {X.back.mean()*100:.0f}%")
B = S[S.back & S.hit.notna()]
if len(B):
    print(f"\nTrade CONTRA a varrida (so se voltou p/ dentro), alvo = lado oposto da Asia, stop = extremo da varrida, janela 3h (11-14h): n={len(B)}")
    print(f"  alvo antes do stop: {(B.hit==1).mean()*100:.0f}% | R:R mediano {(B.reward/B.risk).median():.2f} | risco mediano {B.risk.median():.0f} pts, alvo mediano {B.reward.median():.0f} pts")
    ev = np.where(B.hit == 1, B.reward, -B.risk)
    print(f"  resultado medio por trade: {ev.mean():+.1f} pts")
sem = S[S.hit.isna()]
