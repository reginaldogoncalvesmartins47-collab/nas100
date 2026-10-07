"""Qual indicador aumenta o acerto do gatilho 'vela M5 de rejeicao (pavio longo) num extremo recente'? NAS100 M5 MT5, 02/10/2025-01/05/2026.
Entrada (replica o gatilho do metodo): vela M5 fechada com pavio >= 50% da amplitude, amplitude >= 0,8 ATR14, tocando o extremo das ultimas 24 velas (2h).
Compra: pavio inferior no fundo; venda: pavio superior no topo. Entrada na abertura da vela seguinte; stop = extremo do pavio -/+ 0,5 ATR; alvo = 1,5R; 2h; stop primeiro se ambos.
Filtros testados: tendencia M15 (EMA20 inclinada), WaveTrend (LazyBear n1=10 n2=21) extremo e cruzamento, RSI14 extremo, volume (tick) acima da media, sessao."""
import pandas as pd, numpy as np
df = pd.read_csv("data/nas100_m5_mt5.csv", sep="\t"); df.columns = [c.strip("<>").lower() for c in df.columns]
df["t"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M:%S"); df = df.set_index("t")
df = df[["open", "high", "low", "close", "tickvol"]].rename(columns={"tickvol": "vol"})
tr = pd.concat([df.high - df.low, (df.high - df.close.shift()).abs(), (df.low - df.close.shift()).abs()], axis=1).max(axis=1)
df["atr"] = tr.rolling(14).mean()
ap = (df.high + df.low + df.close) / 3
esa = ap.ewm(span=10, adjust=False).mean(); d = (ap - esa).abs().ewm(span=10, adjust=False).mean()
ci = (ap - esa) / (0.015 * d); df["wt1"] = ci.ewm(span=21, adjust=False).mean(); df["wt2"] = df.wt1.rolling(4).mean()
chg = df.close.diff(); up = chg.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean(); dn = (-chg.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
df["rsi"] = 100 - 100 / (1 + up / dn)
m15 = df.close.resample("15min").last().dropna(); e20 = m15.ewm(span=20, adjust=False).mean()
slope = (e20 - e20.shift(3)).reindex(df.index, method="ffill").shift(1)
df["slope"] = slope
df["volr"] = df.vol / df.vol.rolling(20).mean()
df["lo24"] = df.low.rolling(24).min().shift(1); df["hi24"] = df.high.rolling(24).max().shift(1)
rng = df.high - df.low
lw = (np.minimum(df.open, df.close) - df.low); uw = (df.high - np.maximum(df.open, df.close))
buy = (lw >= 0.5 * rng) & (rng >= 0.8 * df.atr) & (df.low <= df.lo24)
sell = (uw >= 0.5 * rng) & (rng >= 0.8 * df.atr) & (df.high >= df.hi24)
idx = np.arange(len(df)); H = df.high.values; L = df.low.values; O = df.open.values
rows = []
for i in np.where((buy | sell).values)[0]:
    if i + 26 >= len(df) or np.isnan(df.atr.iloc[i]): continue
    if (df.index[i + 1] - df.index[i]) != pd.Timedelta(minutes=5): continue
    side = 1 if buy.iloc[i] else -1
    ent = O[i + 1]; a = df.atr.iloc[i]
    stop = (df.low.iloc[i] - 0.5 * a) if side == 1 else (df.high.iloc[i] + 0.5 * a)
    r = abs(ent - stop)
    if r <= 0: continue
    tgt = ent + side * 1.5 * r; res = 0.0
    for j in range(i + 1, i + 26):
        if side == 1:
            if L[j] <= stop: res = -1; break
            if H[j] >= tgt: res = 1.5; break
        else:
            if H[j] >= stop: res = -1; break
            if L[j] <= tgt: res = 1.5; break
    else:
        res = (df.close.iloc[i + 25] - ent) * side / r
    t = df.index[i]; h = t.hour  # servidor: Asia 03-09, Londres 09-16:30, NY 16:30-23
    sess = "Asia" if 3 <= h < 9 else ("Londres" if 9 <= h < 16 or (h == 16 and t.minute < 30) else "NY")
    w1, w2 = df.wt1.iloc[i], df.wt2.iloc[i]
    wprev = df.wt1.iloc[i - 3:i + 1].values - df.wt2.iloc[i - 3:i + 1].values
    cross = (side == 1 and (wprev[:-1] < 0).any() and wprev[-1] > 0) or (side == -1 and (wprev[:-1] > 0).any() and wprev[-1] < 0)
    rows.append(dict(side=side, res=res, win=res > 0, sess=sess,
                     trend=(df.slope.iloc[i] * side > 0), wt_ext=(w1 < -30 if side == 1 else w1 > 30), wt_cross=cross,
                     rsi_ext=(df.rsi.iloc[i] < 35 if side == 1 else df.rsi.iloc[i] > 65), vol=df.volr.iloc[i] > 1.2))
R = pd.DataFrame(rows)
def line(nome, S):
    if len(S) < 30: return f"  {nome:34s} n={len(S):4d} (amostra pequena)"
    se = S.res.std() / np.sqrt(len(S))
    return f"  {nome:34s} n={len(S):4d} | acerto {S.win.mean()*100:4.1f}% | media {S.res.mean():+.3f}R (+-{se:.3f})"
print(f"sinais: {len(R)} | dias: {df.index.normalize().nunique()} | ponto de equilibrio do alvo 1,5R: acerto 40%")
print(line("BASE (so a vela de rejeicao)", R))
for c, nome in [("trend", "+ tendencia M15 a favor"), ("wt_ext", "+ WaveTrend extremo (+-30)"), ("wt_cross", "+ WaveTrend cruzou (3 velas)"), ("rsi_ext", "+ RSI extremo (35/65)"), ("vol", "+ volume > 1,2x media")]:
    print(line(nome, R[R[c]])); print(line(nome.replace("+", "-", 1) + " (contra)", R[~R[c]]))
print("\nCombinacoes:")
print(line("tendencia + WT extremo", R[R.trend & R.wt_ext]))
print(line("tendencia + volume", R[R.trend & R.vol]))
print(line("tendencia + WT extremo + volume", R[R.trend & R.wt_ext & R.vol]))
print(line("WT cruzou + volume", R[R.wt_cross & R.vol]))
print("\nPor sessao (base):")
for s, S in R.groupby("sess"): print(line(s, S))
print("\nPor lado (base):")
for s, S in R.groupby("side"): print(line("compra" if s == 1 else "venda", S))
