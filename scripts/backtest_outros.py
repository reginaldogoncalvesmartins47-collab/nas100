"""Outros setups simples sem noticia. Hora servidor MT5 = NY+7h (NY 09:30 ET = 16:30 servidor). Custo 2 pts. Retornos em PONTOS por trade, sem stop (teste de deriva/tempo), mais teste por R onde indicado."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
COST=2.0
days=[pd.Timestamp(x) for x in sorted(set(d.index.date)) if pd.Timestamp(x).dayofweek<5]
def px(day,h,m=0,col="close"):
    t=day+pd.Timedelta(hours=h,minutes=m)
    try: return d.loc[t,col]
    except KeyError: return np.nan
rows=[]
prev_close=None
for k,day in enumerate(days):
    o=px(day,16,30,"open"); c10=px(day,16,55); c1130=px(day,18,25); c15=px(day,21,55); c16=px(day,22,55)  # 10:00,11:30,15:00,16:00 ET
    prevc=px(days[k-1],22,55) if k>0 else np.nan   # fechamento 16:00 ET anterior
    hi_prev=d.loc[days[k-1]:days[k-1]+pd.Timedelta(hours=23,minutes=55)].high.max() if k>0 else np.nan
    lo_prev=d.loc[days[k-1]:days[k-1]+pd.Timedelta(hours=23,minutes=55)].low.min() if k>0 else np.nan
    rows.append(dict(dia=day,dow=day.dayofweek,o=o,c10=c10,c1130=c1130,c15=c15,c16=c16,prevc=prevc,hip=hi_prev,lop=lo_prev))
D=pd.DataFrame(rows).dropna(subset=["o","c10","c1130","c15"]); D["fase"]=np.where(D.dia<"2026-02-01","treino","teste")
def rep(nome,serie,fase=D.fase):
    s=pd.Series(serie,index=D.index).dropna(); out=[]
    for f in ("treino","teste"):
        x=s[fase.loc[s.index]==f]; out.append((f,len(x),round(x.mean(),1),round((x>0).mean()*100),round(x.mean()/(x.std()/np.sqrt(len(x))),2) if len(x)>2 and x.std()>0 else np.nan))
    allx=s; print(f"{nome:46s} n={len(allx):3d} media={allx.mean():7.1f} pts  acerto={(allx>0).mean()*100:3.0f}%  t={allx.mean()/(allx.std()/np.sqrt(len(allx))):5.2f} | treino {out[0][2]:+.1f} (t {out[0][4]}) | teste {out[1][2]:+.1f} (t {out[1][4]})")
dr=np.sign(D.c10-D.o)
rep("A seguir 1a meia hora: 10:00->11:30 ET",(D.c1130-D.c10)*dr-COST)
rep("B contra 1a meia hora: 10:00->11:30 ET",-(D.c1130-D.c10)*dr-COST)
rep("A2 seguir 1a meia hora: 10:00->15:00 ET",(D.c15-D.c10)*dr-COST)
rep("B2 contra 1a meia hora: 10:00->15:00 ET",-(D.c15-D.c10)*dr-COST)
gap=D.o-D.prevc; big=gap.abs()>gap.abs().median()
rep("C gap grande: fade do gap 09:30->11:00 ET (aprox 10:00->11:30)",(-(np.sign(gap)*(D.c1130-D.o)))[big]-COST)
rep("C2 gap grande: seguir o gap 09:30->11:30 ET",((np.sign(gap)*(D.c1130-D.o)))[big]-COST)
rep("D comprar sempre 10:00->15:00 ET (deriva)",(D.c15-D.c10)-COST)
rep("D2 comprar sempre 15:00->16:00 ET (fim do dia)",(D.c16-D.c15)-COST)
rep("D3 comprar 09:30 -> 10:00 ET (1a meia hora)",(D.c10-D.o)-COST)
rep("E sexta: 10:00->16:00 ET comprado",((D.c16-D.c10)-COST)[D.dow==4])
rep("E2 sexta: 15:00->16:00 ET (zeragem de sexta)",((D.c16-D.c15)-COST)[D.dow==4])
# F rompimento da PDH/PDL no NY, ate 15:00 ET: seguir
pdh_b=(D.o>0)
print("\nDeriva media por dia da semana, 10:00->15:00 ET comprado (pts, sem custo):"); print(((D.c15-D.c10).groupby(D.dow).agg(['mean','count'])).round(1).to_string())
