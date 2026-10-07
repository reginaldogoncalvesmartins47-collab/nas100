"""Reproduz o indicador 'ICT - Estrutura (BOS/CHoCH) + FVG + Order Blocks' da usuaria (pivot=5) em M5 (MT5) e testa entradas simples nas zonas dele, a favor do rompimento.
A) retest do ORDER BLOCK (entrada na metade do OB); B) retest do FVG a favor da tendencia (entrada na borda); C) OB que se sobrepoe a um FVG recente (confluencia).
Stop alem da zona (+2 pts), alvo 2R, valido 3 h, so criado/entrado na sessao NY (16:30-22:00 servidor). Custo 2 pts."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
H=d.high.values;L=d.low.values;O=d.open.values;C=d.close.values;T=d.index; n=len(d); SW=5; import sys; COST=2.0; K=float(sys.argv[1]) if len(sys.argv)>1 else 2.0; RISCOS=[]
def hr(i): t=T[i]; return t.hour*60+t.minute
def in_ny(i): return 16*60+30<=hr(i)<=22*60
def sim(i0,entry,stop,side,maxbars=36):
    R=abs(entry-stop)
    if R<4: return None
    RISCOS.append(R)
    tgt=entry+K*R*side
    # vela do toque (i0): se ela tambem passou do stop, assume perda (pior caso); alvo so conta a partir da vela seguinte
    if (side>0 and L[i0]<=stop) or (side<0 and H[i0]>=stop): return (-R-COST)/R
    for j in range(i0+1,min(i0+260,n)):
        if side>0:
            if L[j]<=stop: return (-R-COST)/R
            if H[j]>=tgt: return (K*R-COST)/R
        else:
            if H[j]>=stop: return (-R-COST)/R
            if L[j]<=tgt: return (K*R-COST)/R
        if T[j].hour*60+T[j].minute>22*60+55 and T[j].date()>=T[i0].date(): return ((C[j]-entry)*side-COST)/R
    return None
res=[]; trend=0; lsh=lsl=np.nan; ob_dem=[]; ob_sup=[]; fvg_bull=[]; fvg_bear=[]; lastfvg_b=-99; lastfvg_s=-99
for i in range(SW*2+2,n):
    # pivos confirmados em i (pivot em i-SW)
    p=i-SW
    if H[p]==H[p-SW:i+1].max() and (H[p-SW:i+1]==H[p]).sum()==1: lsh=H[p]
    if L[p]==L[p-SW:i+1].min() and (L[p-SW:i+1]==L[p]).sum()==1: lsl=L[p]
    brokeUp=(not np.isnan(lsh)) and C[i]>lsh and C[i-1]<=lsh
    brokeDn=(not np.isnan(lsl)) and C[i]<lsl and C[i-1]>=lsl
    if brokeUp:
        k=1
        while k<20 and C[i-k]>O[i-k]: k+=1
        if k<20: ob_dem.append(dict(top=H[i-k],bot=L[i-k],born=i,done=False,fvg=(i-lastfvg_b)<=4))
        trend=1; lsh=np.nan
    if brokeDn:
        k=1
        while k<20 and C[i-k]<O[i-k]: k+=1
        if k<20: ob_sup.append(dict(top=H[i-k],bot=L[i-k],born=i,done=False,fvg=(i-lastfvg_s)<=4))
        trend=-1; lsl=np.nan
    if L[i]>H[i-2]: fvg_bull.append(dict(top=L[i],bot=H[i-2],born=i,trend=trend,done=False)); lastfvg_b=i
    if H[i]<L[i-2]: fvg_bear.append(dict(top=L[i-2],bot=H[i],born=i,trend=trend,done=False)); lastfvg_s=i
    if not in_ny(i): continue
    # A/C: retest OB
    for z in ob_dem:
        if z["done"]: continue
        if i-z["born"]>36 or C[i]<z["bot"]: z["done"]=True; continue
        if i>z["born"] and L[i]<=(z["top"]+z["bot"])/2 and in_ny(z["born"]):
            z["done"]=True; e=(z["top"]+z["bot"])/2; x=sim(i,e,z["bot"]-COST,1)
            if x is not None:
                res.append(("A OB retest (compra)",T[i].date(),x))
                if z["fvg"]: res.append(("C OB+FVG confluencia (compra)",T[i].date(),x))
    for z in ob_sup:
        if z["done"]: continue
        if i-z["born"]>36 or C[i]>z["top"]: z["done"]=True; continue
        if i>z["born"] and H[i]>=(z["top"]+z["bot"])/2 and in_ny(z["born"]):
            z["done"]=True; e=(z["top"]+z["bot"])/2; x=sim(i,e,z["top"]+COST,-1)
            if x is not None:
                res.append(("A OB retest (venda)",T[i].date(),x))
                if z["fvg"]: res.append(("C OB+FVG confluencia (venda)",T[i].date(),x))
    # B: retest FVG a favor da tendencia vigente
    for z in fvg_bull:
        if z["done"]: continue
        if i-z["born"]>36 or L[i]<=z["bot"]: z["done"]=True; continue
        if i>z["born"]+1 and L[i]<=z["top"] and trend==1 and z["trend"]==1 and in_ny(z["born"]):
            z["done"]=True; x=sim(i,z["top"],z["bot"]-COST,1)
            if x is not None: res.append(("B FVG retest a favor (compra)",T[i].date(),x))
    for z in fvg_bear:
        if z["done"]: continue
        if i-z["born"]>36 or H[i]>=z["top"]: z["done"]=True; continue
        if i>z["born"]+1 and H[i]>=z["bot"] and trend==-1 and z["trend"]==-1 and in_ny(z["born"]):
            z["done"]=True; x=sim(i,z["bot"],z["top"]+COST,-1)
            if x is not None: res.append(("B FVG retest a favor (venda)",T[i].date(),x))
    if i%2000==0:
        ob_dem=[z for z in ob_dem if not z["done"]]; ob_sup=[z for z in ob_sup if not z["done"]]; fvg_bull=[z for z in fvg_bull if not z["done"]]; fvg_bear=[z for z in fvg_bear if not z["done"]]
df=pd.DataFrame(res,columns=["setup","dia","R"]); df["dia"]=pd.to_datetime(df.dia); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
pd.set_option("display.width",200); print(df.groupby("setup").apply(resumo).to_string()); print("\nTREINO x TESTE:"); print(df.groupby(["setup","fase"]).apply(resumo).to_string())

print("risco medio (pts) por trade: %.1f | mediana %.1f"%(np.mean(RISCOS),np.median(RISCOS)))
