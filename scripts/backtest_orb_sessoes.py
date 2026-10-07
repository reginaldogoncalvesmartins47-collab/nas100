"""ORB por sessao (Asia/Londres/NY): faixa dos primeiros 30 min apos a abertura; entra no 1o fechamento M5 fora; stop no lado oposto; alvo 1,5R; sai apos 5h30 ou no fim do dia. Custo 2 pts.
Aberturas em UTC: Asia 00:00 (Toquio 09:00); Londres 08:00 hora local (07:00 UTC no horario de verao UK, 08:00 UTC no inverno); NY 09:30 ET (13:30 UTC verao EUA / 14:30 UTC inverno).
Hora servidor MT5 = UTC+3 (verao EUA) ou UTC+2."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0; K=1.5
def us_dst(day): return day<pd.Timestamp("2025-11-02") or day>=pd.Timestamp("2026-03-08")
def uk_dst(day): return day<pd.Timestamp("2025-10-26") or day>=pd.Timestamp("2026-03-29")
def abertura_servidor(sessao,day):
    off=3 if us_dst(day) else 2
    utc={"ASIA":(0,0),"LONDRES":((7,0) if uk_dst(day) else (8,0)),"NY":((13,30) if us_dst(day) else (14,30))}[sessao]
    return day+pd.Timedelta(hours=utc[0]+off,minutes=utc[1])
def sim(entry,stop,side,w):
    R=abs(entry-stop)
    if R<5: return None
    tgt=entry+K*R if side>0 else entry-K*R
    for t,r in w.iterrows():
        if side>0:
            if r.low<=stop: return (-R-COST)/R
            if r.high>=tgt: return (K*R-COST)/R
        else:
            if r.high>=stop: return (-R-COST)/R
            if r.low<=tgt: return (K*R-COST)/R
    return ((w.close.iloc[-1]-entry)*side-COST)/R
res=[]
for day in sorted(set(pd.to_datetime(d.index.date))):
    for s in ("ASIA","LONDRES","NY"):
        if day.dayofweek>4: continue
        t0=abertura_servidor(s,day); rng=d.loc[t0:t0+pd.Timedelta(minutes=25)]
        if len(rng)<5: continue
        hi,lo=rng.high.max(),rng.low.min(); post=d.loc[t0+pd.Timedelta(minutes=30):t0+pd.Timedelta(hours=5,minutes=30)]
        for t,r in post.iterrows():
            side=1 if r.close>hi else -1 if r.close<lo else 0
            if side:
                w=d.loc[t+pd.Timedelta(minutes=5):t0+pd.Timedelta(hours=5,minutes=30)]
                if len(w)<2: break
                R=sim(r.close,lo if side>0 else hi,side,w)
                if R is not None: res.append((s,day,R,hi-lo))
                break
df=pd.DataFrame(res,columns=["sessao","dia","R","faixa"]); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan,faixa_media=round(g.faixa.mean())))
print(df.groupby("sessao").apply(resumo).to_string()); print(); print(df.groupby(["sessao","fase"]).apply(resumo).to_string())
