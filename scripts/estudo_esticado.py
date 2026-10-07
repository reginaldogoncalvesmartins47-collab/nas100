"""Compra 'esticada' x perto da base (proxy de OB de demanda). NAS100 M5 MT5, 02/10/2025-01/05/2026.
Hipotese da usuaria (06/10/2026): comprar quando o preco esta esticado perde. Proxy: esticamento = (entrada - minima das ultimas 2h) / ATR M15.
Entrada a mercado a cada 30 min na sessao NY AM (09:35-12:35 ET = 16:35-19:35 servidor), so com preco acima da EMA20 M15 (vies de alta).
Stop 0,8 ATR15, alvo 1,07 ATR15 (como a compra 19: 34/46 pts com ATR15 ~43); resultado em 60 min; stop conta primeiro se ambos na mesma vela."""
import pandas as pd, numpy as np
df = pd.read_csv("data/nas100_m5_mt5.csv", sep="\t"); df.columns = [c.strip("<>").lower() for c in df.columns]
df["t"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y.%m.%d %H:%M:%S"); df = df.set_index("t")[["open", "high", "low", "close"]]
m15 = df.resample("15min").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
tr = pd.concat([m15.high - m15.low, (m15.high - m15.close.shift()).abs(), (m15.low - m15.close.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean(); ema = m15.close.ewm(span=20, adjust=False).mean()
rows = []
for d, g in df.groupby(df.index.date):
    if pd.Timestamp(d).weekday() > 4: continue
    for hm in range(16 * 60 + 35, 19 * 60 + 36, 30):
        ts = pd.Timestamp(d) + pd.Timedelta(minutes=hm)
        if ts not in df.index: continue
        k = m15.index[m15.index <= ts]
        if len(k) < 30: continue
        k = k[-2]  # ultima vela M15 fechada
        a, e = atr.loc[k], ema.loc[k]
        px = df.loc[ts, "close"]
        if np.isnan(a) or px <= e: continue
        w = df.loc[ts - pd.Timedelta(minutes=115):ts]
        fut = df.loc[ts + pd.Timedelta(minutes=5):ts + pd.Timedelta(minutes=60)]
        if len(w) < 20 or len(fut) < 10: continue
        s = (px - w.low.min()) / a
        st, tp = px - 0.8 * a, px + 1.07 * a
        res = None
        for _, b in fut.iterrows():
            if b.low <= st: res = -0.8 * a; break
            if b.high >= tp: res = 1.07 * a; break
        if res is None: res = fut.close.iloc[-1] - px
        rows.append(dict(d=str(d), s=s, res=res / a, win=res > 0))
R = pd.DataFrame(rows)
print(f"entradas: {len(R)} em {R.d.nunique()} dias | esticamento mediano {R.s.median():.2f} ATR")
q = R.s.quantile([.33, .66]).values
R["b"] = pd.cut(R.s, [-1, q[0], q[1], 99], labels=[f"perto (<{q[0]:.1f} ATR)", f"medio ({q[0]:.1f}-{q[1]:.1f})", f"esticado (>{q[1]:.1f} ATR)"])
print("\nPor esticamento (resultado em ATR15 por trade; stop -0,8 / alvo +1,07):")
for b, S in R.groupby("b", observed=True):
    print(f"  {str(b):26s} n={len(S):3d} | acerto {S.win.mean()*100:3.0f}% | media {S.res.mean():+.3f} ATR | soma {S.res.sum():+.1f}")
print(f"  todos                      n={len(R):3d} | acerto {R.win.mean()*100:3.0f}% | media {R.res.mean():+.3f} ATR")
ex = R[R.s >= R.s.quantile(.85)]
print(f"\nMuito esticado (top 15%, >{R.s.quantile(.85):.1f} ATR): n={len(ex)} | acerto {ex.win.mean()*100:.0f}% | media {ex.res.mean():+.3f} ATR")
