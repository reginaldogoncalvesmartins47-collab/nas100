"""Variantes do ORB de NY citadas na internet: faixa de 15 min (09:30-09:45 ET) vs 30 min; so compra vs so venda; e 'fade' do rompimento falho. Dados MT5, custo 2 pts, treino x teste."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0
def sim(entry,stop,tgt,side,w):
    R=abs(entry-stop)
    if R<5: return None
    for t,r in w.iterrows():
        if side>0:
            if r.low<=stop: return (-R-COST)/R
            if r.high>=tgt: return ((tgt-entry)-COST)/R
        else:
            if r.high>=stop: return (-R-COST)/R
            if r.low<=tgt: return ((entry-tgt)-COST)/R
    return ((w.close.iloc[-1]-entry)*side-COST)/R
def us_dst(day): return day<pd.Timestamp("2025-11-02") or day>=pd.Timestamp("2026-03-08")
res=[]
for day in sorted(set(pd.to_datetime(d.index.date))):
    if day.dayofweek>4: continue
    t0=day+pd.Timedelta(hours=16,minutes=30)   # 09:30 ET = 16:30 servidor (NY+7)
    for dur in (15,30):
        rng=d.loc[t0:t0+pd.Timedelta(minutes=dur-5)]
        if len(rng)<dur//5: continue
        hi,lo=rng.high.max(),rng.low.min(); post=d.loc[t0+pd.Timedelta(minutes=dur):t0+pd.Timedelta(hours=5,minutes=30)]
        endday=t0+pd.Timedelta(hours=5,minutes=30)
        idx=list(post.index)
        for j,t in enumerate(idx):
            r=post.loc[t]; side=1 if r.close>hi else -1 if r.close<lo else 0
            if not side: continue
            R=hi-lo
            w=d.loc[t+pd.Timedelta(minutes=5):endday]
            if len(w)<2: break
            stop=lo if side>0 else hi; tgt=r.close+1.5*(r.close-stop) if side>0 else r.close-1.5*(stop-r.close)
            x=sim(r.close,stop,tgt,side,w)
            if x is not None: res.append((f"ORB {dur}min",("so compra" if side>0 else "so venda"),day,x))
            # fade do rompimento falho: nas proximas 3 velas volta pra dentro da faixa
            nxt=post.loc[idx[j+1:j+4]] if j+1<len(idx) else None
            if nxt is not None and len(nxt):
                back=nxt[(nxt.close<hi)&(nxt.close>lo)]
                if len(back):
                    tb=back.index[0]; e=back.close.iloc[0]; ext=post.loc[t:tb].high.max() if side>0 else post.loc[t:tb].low.min()
                    s2=ext+COST if side>0 else ext-COST; tg2=lo if side>0 else hi   # fade: oposto; alvo = outro lado da faixa
                    w2=d.loc[tb+pd.Timedelta(minutes=5):endday]
                    if len(w2)>2:
                        x2=sim(e,s2,tg2,-side,w2)
                        if x2 is not None: res.append((f"FADE rompimento falho {dur}min","a contrario",day,x2))
            break
df=pd.DataFrame(res,columns=["setup","lado","dia","R"]); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
print(df.groupby(["setup","lado"]).apply(resumo).to_string()); print("\nTREINO x TESTE:"); print(df.groupby(["setup","lado","fase"]).apply(resumo).to_string())
