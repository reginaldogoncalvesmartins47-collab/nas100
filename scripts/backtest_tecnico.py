"""Testes de analise tecnica: (T1) VWAP da sessao (09:30 ET): pullback a favor / (T2) VWAP so venda; (T3) order block com deslocamento + FVG. Dados MT5 M5 (hora servidor=NY+7h), custo 2 pts, treino x teste."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0
tr=pd.concat([d.high-d.low,(d.high-d.close.shift()).abs(),(d.low-d.close.shift()).abs()],axis=1).max(axis=1); d["atr"]=tr.rolling(14).mean()
def sim(entry,stop,K,side,w):
    R=abs(entry-stop)
    if R<4 or len(w)<2: return None
    tgt=entry+K*R*side
    for t,r in w.iterrows():
        if side>0:
            if r.low<=stop: return (-R-COST)/R
            if r.high>=tgt: return (K*R-COST)/R
        else:
            if r.high>=stop: return (-R-COST)/R
            if r.low<=tgt: return (K*R-COST)/R
    return ((w.close.iloc[-1]-entry)*side-COST)/R
res=[]
days=[pd.Timestamp(x) for x in sorted(set(d.index.date)) if pd.Timestamp(x).dayofweek<5]
for day in days:
    s=d.loc[day+pd.Timedelta(hours=16,minutes=30):day+pd.Timedelta(hours=22,minutes=55)].copy()
    if len(s)<40: continue
    tp=(s.high+s.low+s.close)/3; s["vwap"]=(tp*s.tick_volume).cumsum()/s.tick_volume.cumsum() if "tick_volume" in s else (tp).expanding().mean()
    endt=day+pd.Timedelta(hours=22,minutes=55); done_l=done_s=False
    idx=list(s.index)
    for j in range(24,len(idx)-3):
        t=idx[j]; r=s.loc[t]
        if t<day+pd.Timedelta(hours=17,minutes=30): continue
        above=(s.close.iloc[j-12:j]>s.vwap.iloc[j-12:j]).all(); below=(s.close.iloc[j-12:j]<s.vwap.iloc[j-12:j]).all()
        w=d.loc[t+pd.Timedelta(minutes=5):endt]
        if above and r.low<=r.vwap and r.close>r.vwap and not done_l:
            done_l=True; stop=r.vwap-0.5*r.atr
            x=sim(r.close,stop,2.0,1,w); 
            if x is not None: res.append(("T1 VWAP pullback (compra, tendencia)",day,x))
        if below and r.high>=r.vwap and r.close<r.vwap and not done_s:
            done_s=True; stop=r.vwap+0.5*r.atr
            x=sim(r.close,stop,2.0,-1,w)
            if x is not None: res.append(("T2 VWAP pullback (venda, tendencia)",day,x))
    # T3 order block + deslocamento + FVG, dia inteiro 16:30-22:00
    ob=None
    for j in range(2,len(idx)-1):
        c0,c1,c2=s.iloc[j-2],s.iloc[j-1],s.iloc[j]
        body=abs(c1.close-c1.open)
        if body>=1.5*c1.atr:
            if c1.close>c1.open and c2.low>c0.high:   # deslocamento de alta + FVG
                # OB = ultimo candle de baixa antes
                k=j-2
                while k>=0 and s.iloc[k].close>=s.iloc[k].open: k-=1
                if k>=0:
                    o=s.iloc[k]; L=(o.open+o.low)/2  # entrada na metade do OB
                    w=d.loc[idx[j]+pd.Timedelta(minutes=5):idx[j]+pd.Timedelta(hours=3)]
                    for t,r in w.iterrows():
                        if r.low<=L:
                            x=sim(L,o.low-COST,2.0,1,d.loc[t:endt].iloc[1:])
                            if x is not None: res.append(("T3 Order block + FVG (compra)",day,x))
                            break
            if c1.close<c1.open and c2.high<c0.low:
                k=j-2
                while k>=0 and s.iloc[k].close<=s.iloc[k].open: k-=1
                if k>=0:
                    o=s.iloc[k]; L=(o.open+o.high)/2
                    w=d.loc[idx[j]+pd.Timedelta(minutes=5):idx[j]+pd.Timedelta(hours=3)]
                    for t,r in w.iterrows():
                        if r.high>=L:
                            x=sim(L,o.high+COST,2.0,-1,d.loc[t:endt].iloc[1:])
                            if x is not None: res.append(("T3 Order block + FVG (venda)",day,x))
                            break
df=pd.DataFrame(res,columns=["setup","dia","R"]); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
pd.set_option("display.width",200)
print(df.groupby("setup").apply(resumo).to_string()); print("\nTREINO x TESTE:"); print(df.groupby(["setup","fase"]).apply(resumo).to_string())
