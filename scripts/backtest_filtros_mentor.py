"""FVG do LuxAlgo (entrada no MEIO, a favor da tendencia interna) + os 3 filtros do mentor: (1) DESCONTO: mid abaixo de 50% da Fibo do impulso (compra) / acima (venda); (2) PULLBACK LENTO: velocidade do pullback em ATR por barra menor que a mediana (proxy de angulo < 60 graus); (3) INDUCAO: o pullback fez >= 2 novas minimas (compra) / maximas (venda) em relacao as 3 barras anteriores. Dados MT5 M5, custo 2, alvo 2R, conservador."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
H=d.high.values;L=d.low.values;O=d.open.values;C=d.close.values;T=d.index;n=len(d);COST=2.0;K=2.0;SZ=5
tr=np.maximum(H-L,np.maximum(abs(H-np.roll(C,1)),abs(L-np.roll(C,1)))); ATR=pd.Series(tr).rolling(14).mean().values
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
rows=[]; leg=0; ihi=ilo=np.nan; ihi_i=ilo_i=0; ihi_c=ilo_c=True; trend=0; cum=0.0; zones=[]
for i in range(SZ+3,n):
    hi_s=H[i-SZ]; lo_s=L[i-SZ]; new=leg
    if hi_s>H[i-SZ+1:i+1].max(): new=0
    elif lo_s<L[i-SZ+1:i+1].min(): new=1
    if new!=leg:
        if new==1: ilo=lo_s; ilo_i=i-SZ; ilo_c=False
        else: ihi=hi_s; ihi_i=i-SZ; ihi_c=False
        leg=new
    if (not np.isnan(ihi)) and (not ihi_c) and C[i]>ihi and C[i-1]<=ihi: ihi_c=True; trend=1
    if (not np.isnan(ilo)) and (not ilo_c) and C[i]<ilo and C[i-1]>=ilo: ilo_c=True; trend=-1
    body=(C[i-1]-O[i-1])/(O[i-1]*100); cum+=abs(body); thr=cum/(i+1)*2
    if L[i]>H[i-2] and C[i-1]>H[i-2] and body>thr: zones.append(dict(b=1,top=L[i],bot=H[i-2],born=i,tr=trend,e=False,p0=ilo_i,pl=ilo))
    if H[i]<L[i-2] and C[i-1]<L[i-2] and -body>thr: zones.append(dict(b=-1,top=L[i-2],bot=H[i],born=i,tr=trend,e=False,p0=ihi_i,pl=ihi))
    keep=[]
    for z in zones:
        if (z["b"]==1 and L[i]<z["bot"]) or (z["b"]==-1 and H[i]>z["top"]) or i-z["born"]>36: continue
        if i>z["born"]+1 and trend==z["b"] and z["tr"]==trend and not z["e"] and not np.isnan(z["pl"]):
            mid=(z["top"]+z["bot"])/2; touched=(L[i]<=mid) if z["b"]==1 else (H[i]>=mid)
            if touched:
                z["e"]=True; side=z["b"]
                p0=z["p0"]; seg_h=H[p0:i+1]; seg_l=L[p0:i+1]
                if side==1:
                    imp_lo=z["pl"]; imp_hi=seg_h.max(); pk=p0+int(seg_h.argmax()); disc=mid<=imp_lo+0.5*(imp_hi-imp_lo)
                    drop=imp_hi-mid; nb=max(1,i-pk); spd=(drop/ATR[i])/nb
                    lows=L[pk:i+1]; ind=sum(1 for k in range(3,len(lows)) if lows[k]<lows[k-3:k].min())
                    x=sim(i,mid,z["bot"]-COST,1)
                else:
                    imp_hi=z["pl"]; imp_lo=seg_l.min(); pk=p0+int(seg_l.argmin()); disc=mid>=imp_lo+0.5*(imp_hi-imp_lo)
                    drop=mid-imp_lo; nb=max(1,i-pk); spd=(drop/ATR[i])/nb
                    highs=H[pk:i+1]; ind=sum(1 for k in range(3,len(highs)) if highs[k]>highs[k-3:k].max())
                    x=sim(i,mid,z["top"]+COST,-1)
                if x is not None: rows.append(dict(dia=T[i].date(),lado=side,R=x,disc=disc,spd=spd,ind=ind))
        keep.append(z)
    zones=keep[-60:]
df=pd.DataFrame(rows); df["dia"]=pd.to_datetime(df.dia); df["fase"]=np.where(df.dia<"2026-02-01","treino","teste")
med=df.spd.median(); df["lento"]=df.spd<med; df["indu"]=df.ind>=2
def resumo(g):
    w=g.R[g.R>0].sum(); l=-g.R[g.R<0].sum(); return pd.Series(dict(n=len(g),acerto=round((g.R>0).mean()*100),R_medio=round(g.R.mean(),2),PF=round(w/l,2) if l>0 else np.nan))
sets={"0 sem filtro (meio do FVG)":df,"1 so DESCONTO":df[df.disc],"2 so PULLBACK LENTO":df[df.lento],"3 so INDUCAO >=2":df[df.indu],
 "1+2 desconto+lento":df[df.disc&df.lento],"1+3 desconto+inducao":df[df.disc&df.indu],"2+3 lento+inducao":df[df.lento&df.indu],"1+2+3 os tres":df[df.disc&df.lento&df.indu],
 "CONTRA: premio (fora do desconto)":df[~df.disc]}
print("TOTAL"); print(pd.DataFrame({k:resumo(v) for k,v in sets.items()}).T.to_string())
print("\nTREINO x TESTE"); 
out={}
for k,v in sets.items():
    for f in ("treino","teste"): out[(k,f)]=resumo(v[v.fase==f])
print(pd.DataFrame(out).T.to_string())
