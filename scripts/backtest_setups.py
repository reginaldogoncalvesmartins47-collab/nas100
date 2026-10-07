"""Backtest de setups simples SEM noticia (NAS100 M5 do MT5, hora servidor = NY+7h). Custo 2 pts por trade. Stop primeiro se stop e alvo na mesma vela.
S1 ORB: range 16:30-17:00 servidor (09:30-10:00 ET); entra no 1o fechamento fora do range; stop no lado oposto; alvo K*R; sai 22:00 servidor.
S2 SWEEP Londres: na NY AM (16:30-20:00) varre max/min de Londres (10:00-16:30) com pavio e fecha de volta dentro em ate 2 velas; reverte; stop alem do pavio; alvo K*R.
S3 SWEEP PDH/PDL: igual, com max/min do dia anterior (00:00-23:55)."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0
evdays=set(pd.read_csv("data/estudo_todos_eventos.csv").assign(t0=lambda x:pd.to_datetime(x.t0)).query("imp==3 and hhmm in ['15:30','21:00','21:30']").t0.dt.date)  # dias com pacote grande
def sim(day,i0,side,entry,stop,K,end):
    R=abs(entry-stop); 
    if R<5: return None
    tgt=entry+K*R if side>0 else entry-K*R
    w=d.loc[i0:end]
    for t,r in w.iterrows():
        if side>0:
            if r.low<=stop: return (-R-COST)/R
            if r.high>=tgt: return (K*R-COST)/R
        else:
            if r.high>=stop: return (-R-COST)/R
            if r.low<=tgt: return (K*R-COST)/R
    last=w.close.iloc[-1]; return ((last-entry)*side-COST)/R
res=[]
days=sorted(set(d.index.date))
for k,day in enumerate(days):
    ts=pd.Timestamp(day)
    if ts.dayofweek>4: continue
    T=lambda h,m=0: ts+pd.Timedelta(hours=h,minutes=m)
    end=T(22,0)
    # S1 ORB
    orb=d.loc[T(16,30):T(16,55)]
    if len(orb)>=6:
        hi,lo=orb.high.max(),orb.low.min(); post=d.loc[T(17,0):T(21,0)]
        for t,r in post.iterrows():
            if r.close>hi: 
                for K in (1.0,1.5,2.0): res.append(("S1 ORB K=%.1f"%K,day,sim(day,t+pd.Timedelta(minutes=5),1,r.close,lo,K,end)))
                break
            if r.close<lo:
                for K in (1.0,1.5,2.0): res.append(("S1 ORB K=%.1f"%K,day,sim(day,t+pd.Timedelta(minutes=5),-1,r.close,hi,K,end)))
                break
    # S2/S3 sweeps
    lon=d.loc[T(10,0):T(16,25)]; prev=d.loc[pd.Timestamp(days[k-1]):pd.Timestamp(days[k-1])+pd.Timedelta(hours=23,minutes=55)] if k>0 else None
    for nome,lvh,lvl in (("S2 SWEEP Londres",lon.high.max() if len(lon)>20 else None,lon.low.min() if len(lon)>20 else None),("S3 SWEEP PDH/PDL",prev.high.max() if prev is not None and len(prev)>100 else None,prev.low.min() if prev is not None and len(prev)>100 else None)):
        if lvh is None: continue
        bars=d.loc[T(16,30):T(20,0)]; done=False
        idx=list(bars.index)
        for j,t in enumerate(idx[:-3]):
            r=bars.loc[t]
            if r.high>lvh and r.close<lvh or (j+1<len(idx) and r.high>lvh and bars.loc[idx[j+1]].close<lvh):
                ext=bars.loc[idx[:j+2]].high.max(); e=bars.loc[idx[min(j+1,len(idx)-1)]].close
                if r.close<lvh or bars.loc[idx[j+1]].close<lvh:
                    for K in (1.0,2.0): res.append((nome+" K=%.1f"%K,day,sim(day,idx[min(j+2,len(idx)-1)],-1,e,ext+1,K,end)))
                    done=True;break
            if r.low<lvl and r.close>lvl or (j+1<len(idx) and r.low<lvl and bars.loc[idx[j+1]].close>lvl):
                ext=bars.loc[idx[:j+2]].low.min(); e=bars.loc[idx[min(j+1,len(idx)-1)]].close
                if r.close>lvl or bars.loc[idx[j+1]].close>lvl:
                    for K in (1.0,2.0): res.append((nome+" K=%.1f"%K,day,sim(day,idx[min(j+2,len(idx)-1)],1,e,ext-1,K,end)))
                    done=True;break
df=pd.DataFrame(res,columns=["setup","dia","R"]).dropna(); df["dia"]=pd.to_datetime(df.dia)
df["fase"]=np.where(df.dia<"2026-02-01","treino(out-jan)","teste(fev-abr)"); df["noticia"]=df.dia.dt.date.isin(evdays)
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum()
    return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
pd.set_option("display.width",200)
print(df.groupby("setup").apply(resumo).round(2).to_string())
print("\nTREINO x TESTE:"); print(df.groupby(["setup","fase"]).apply(resumo).round(2).to_string())
print("\nDIAS COM PACOTE GRANDE x SEM:"); print(df.groupby(["setup","noticia"]).apply(resumo).round(2).to_string())
