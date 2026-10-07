"""Setup: faixa do candle H4 (completo) + Fibo (retracao) + a favor da macro (tendencia diaria). Compra se macro alta: nivel = max - f*faixa; venda se macro baixa: nivel = min + f*faixa. Ordem a limite no nivel; stop na extremidade oposta do candle (+2 pts); alvo = extremidade do lado da tendencia (0%) ou K*R. Cancela se o alvo for tocado antes do nivel. Valido por 12h. Custo 2 pts. Stop primeiro se mesma vela.
Macro: M1 = fechamento diario anterior acima/abaixo da EMA20 diaria; M2 = direcao do dia anterior; M3 = sem filtro (os dois lados)."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0
h4=d.resample("4h").agg(dict(open="first",high="max",low="min",close="last")).dropna()
dd=d.resample("1D").agg(dict(open="first",close="last")).dropna(); dd["ema20"]=dd.close.ewm(span=20,adjust=False).mean()
dd["m1"]=np.sign(dd.close-dd.ema20); dd["m2"]=np.sign(dd.close-dd.open)  # valores do DIA; usar o do dia anterior
M1=dd.m1.shift(1); M2=dd.m2.shift(1)
def trade(side,L,S,T,start,end):
    w=d.loc[start:end]; filled=False
    for t,r in w.iterrows():
        if not filled:
            if side>0:
                if r.high>=T: return None            # alvo antes do nivel: cancela
                if r.low<=L: filled=True; entry=min(L,r.open)
                else: continue
            else:
                if r.low<=T: return None
                if r.high>=L: filled=True; entry=max(L,r.open)
                else: continue
            R=abs(entry-S)
            if R<8: return None
        if filled:
            if side>0:
                if r.low<=S: return (-R-COST)/R
                if r.high>=T: return ((T-entry)-COST)/R
            else:
                if r.high>=S: return (-R-COST)/R
                if r.low<=T: return ((entry-T)-COST)/R
    if filled: return ((w.close.iloc[-1]-entry)*side-COST)/R
    return None
res=[]
idx=list(h4.index)
for i in range(1,len(idx)-3):
    c=h4.iloc[i]; t_end=idx[i]+pd.Timedelta(hours=4); rng=c.high-c.low
    if rng<30 or t_end>d.index[-1]: continue
    day=pd.Timestamp(idx[i].date()); 
    for fib in (0.618,0.705,0.764,0.786):
        for nome,M in (("M1 EMA20 diaria",M1),("M2 dia anterior",M2)):
            m=M.get(day,np.nan)
            if np.isnan(m) or m==0: continue
            side=int(m)
            if side>0: L=c.high-fib*rng; S=c.low-COST; T=c.high
            else: L=c.low+fib*rng; S=c.high+COST; T=c.low
            r=trade(side,L,S,T,t_end,t_end+pd.Timedelta(hours=12))
            if r is not None: res.append((nome,fib,idx[i],r))
        # sem filtro: compra e venda
        for side in (1,-1):
            if side>0: L=c.high-fib*rng; S=c.low-COST; T=c.high
            else: L=c.low+fib*rng; S=c.high+COST; T=c.low
            r=trade(side,L,S,T,t_end,t_end+pd.Timedelta(hours=12))
            if r is not None: res.append(("M3 sem filtro",fib,idx[i],r))
df=pd.DataFrame(res,columns=["macro","fib","t","R"]); df["fase"]=np.where(df.t<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
pd.set_option("display.width",200)
print(df.groupby(["macro","fib"]).apply(resumo).to_string())
print("\nTREINO x TESTE (fib 0.764 e 0.786):"); print(df[df.fib.isin([0.764,0.786])].groupby(["macro","fib","fase"]).apply(resumo).to_string())
