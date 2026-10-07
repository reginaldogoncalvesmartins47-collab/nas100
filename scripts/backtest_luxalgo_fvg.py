"""Replica o FVG e a estrutura INTERNA (pivot 5, 'leg') do LuxAlgo Smart Money Concepts (Pine v5, CC BY-NC-SA 4.0, uso pessoal) e testa a entrada no retest do FVG a favor da tendencia interna.
FVG alta: low[i] > high[i-2] E close[i-1] > high[i-2] E corpo%[i-1] > 2 x media acumulada de |corpo%| (filtro de deslocamento). Mitigado quando low < base (alta) / high > topo (baixa).
Entradas: E1 = primeiro toque na BORDA (topo p/ alta); E2 = toque no MEIO (math.avg). Stop alem da borda oposta (+2 pts), alvo 2R, valido 3h, custo 2 pts. Conservador: vela do toque so conta stop.
Variantes: NY (16:30-22:00 servidor) x dia todo."""
import pandas as pd, numpy as np, sys
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
H=d.high.values;L=d.low.values;O=d.open.values;C=d.close.values;T=d.index;n=len(d);COST=2.0;K=2.0;SZ=5
def hm(i): return T[i].hour*60+T[i].minute
def sim(i0,entry,stop,side):
    R=abs(entry-stop)
    if R<3: return None
    if (side>0 and L[i0]<=stop) or (side<0 and H[i0]>=stop): return (-R-COST)/R
    tgt=entry+K*R*side
    for j in range(i0+1,min(i0+300,n)):
        if side>0:
            if L[j]<=stop: return (-R-COST)/R
            if H[j]>=tgt: return (K*R-COST)/R
        else:
            if H[j]>=stop: return (-R-COST)/R
            if L[j]<=tgt: return (K*R-COST)/R
        if T[j].date()>T[i0].date() or hm(j)>22*60+55: return ((C[j]-entry)*side-COST)/R
    return None
res=[]; leg=0; ihi=ilo=np.nan; ihi_crossed=ilo_crossed=True; trend=0; cum=0.0; zones=[]
for i in range(SZ+3,n):
    # leg (LuxAlgo): newLegHigh = high[SZ] > highest(SZ) ; newLegLow = low[SZ] < lowest(SZ)  (janela das SZ barras mais recentes, i-SZ+1..i)
    hi_s=H[i-SZ]; lo_s=L[i-SZ]; wmax=H[i-SZ+1:i+1].max(); wmin=L[i-SZ+1:i+1].min()
    new=leg
    if hi_s>wmax: new=0
    elif lo_s<wmin: new=1
    if new!=leg:
        if new==1: ilo=lo_s; ilo_crossed=False        # inicio de perna de alta = pivo de fundo
        else: ihi=hi_s; ihi_crossed=False
        leg=new
    if (not np.isnan(ihi)) and (not ihi_crossed) and C[i]>ihi and C[i-1]<=ihi: ihi_crossed=True; trend=1
    if (not np.isnan(ilo)) and (not ilo_crossed) and C[i]<ilo and C[i-1]>=ilo: ilo_crossed=True; trend=-1
    # FVG LuxAlgo
    body=(C[i-1]-O[i-1])/(O[i-1]*100); cum+=abs((C[i-1]-O[i-1])/(O[i-1]*100)); thr=cum/(i+1)*2
    if L[i]>H[i-2] and C[i-1]>H[i-2] and body>thr: zones.append(dict(bias=1,top=L[i],bot=H[i-2],born=i,tr=trend,e1=False,e2=False))
    if H[i]<L[i-2] and C[i-1]<L[i-2] and -body>thr: zones.append(dict(bias=-1,top=L[i-2],bot=H[i],born=i,tr=trend,e1=False,e2=False))
    keep=[]
    for z in zones:
        if (z["bias"]==1 and L[i]<z["bot"]) or (z["bias"]==-1 and H[i]>z["top"]) or i-z["born"]>36: continue
        if i>z["born"]+1 and trend==z["bias"] and z["tr"]==trend:
            mid=(z["top"]+z["bot"])/2; ny=16*60+30<=hm(i)<=22*60
            if z["bias"]==1:
                if not z["e1"] and L[i]<=z["top"]:
                    z["e1"]=True; x=sim(i,z["top"],z["bot"]-COST,1)
                    if x is not None: res.append(("E1 borda (compra)",ny,T[i].date(),x))
                if not z["e2"] and L[i]<=mid:
                    z["e2"]=True; x=sim(i,mid,z["bot"]-COST,1)
                    if x is not None: res.append(("E2 meio (compra)",ny,T[i].date(),x))
            else:
                if not z["e1"] and H[i]>=z["bot"]:
                    z["e1"]=True; x=sim(i,z["bot"],z["top"]+COST,-1)
                    if x is not None: res.append(("E1 borda (venda)",ny,T[i].date(),x))
                if not z["e2"] and H[i]>=mid:
                    z["e2"]=True; x=sim(i,mid,z["top"]+COST,-1)
                    if x is not None: res.append(("E2 meio (venda)",ny,T[i].date(),x))
        keep.append(z)
    zones=keep[-60:]
df=pd.DataFrame(res,columns=["setup","ny","dia","R"]); df["dia"]=pd.to_datetime(df.dia); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
pd.set_option("display.width",200)
print("DIA TODO:"); print(df.groupby("setup").apply(resumo).to_string())
print("\nSO NY:"); print(df[df.ny].groupby("setup").apply(resumo).to_string())
print("\nTREINO x TESTE (dia todo):"); print(df.groupby(["setup","fase"]).apply(resumo).to_string())
