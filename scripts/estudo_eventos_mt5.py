"""Estudo de eventos: reacao do NAS100 (M5 do MT5, hora servidor = NY + 7h) a eventos do calendario. Dados dos eventos: Investing (lidos em 02/10/2026)."""
import pandas as pd, numpy as np
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
# (tipo, aaaammdd, hora BRT, atual, previsao, sinal_quente) sinal_quente=+1 se atual>previsao e "quente" (juros altos); -1 se invertido (claims)
E=[]
def add(tipo,lst,sg=1):
    for dt,h,a,f in lst: E.append((tipo,dt,h,a,f,sg))
add("NFP",[("20251120","10:30",119,53),("20251216","10:30",64,51),("20260109","10:30",50,66),("20260211","10:30",130,66),("20260306","10:30",-92,58),("20260403","09:30",178,65)])
add("CPI a/a",[("20251024","09:30",3.0,3.1),("20251218","10:30",2.7,3.1),("20260113","10:30",2.7,2.7),("20260213","10:30",2.4,2.5),("20260311","09:30",2.4,2.4),("20260410","09:30",3.3,3.4)])
add("FOMC",[("20251029","15:00",4.0,4.0),("20251210","16:00",3.75,3.75),("20260128","16:00",3.75,3.75),("20260318","15:00",3.75,3.75),("20260429","15:00",3.75,3.75)])
add("Core PCE",[("20260430","09:30",3.2,3.2),("20260409","09:30",3.0,3.0),("20260313","09:30",3.1,3.1),("20260220","10:30",3.0,2.9),("20260122","12:00",2.8,2.8),("20251205","12:00",2.8,2.9)])
add("ISM ind.",[("20251103","12:00",48.7,49.4),("20251201","12:00",48.2,49.0),("20260105","12:00",47.9,48.3),("20260202","12:00",52.6,48.5),("20260302","12:00",52.4,51.7),("20260401","11:00",52.7,52.3)])
cl="20260430,09:30,189,213;20260423,09:30,214,211;20260416,09:30,207,213;20260409,09:30,219,210;20260402,09:30,202,212;20260326,09:30,210,211;20260319,09:30,205,215;20260312,09:30,213,214;20260305,10:30,213,215;20260226,10:30,212,217;20260219,10:30,206,223;20260212,10:30,227,222;20260205,10:30,231,212;20260129,10:30,209,206;20260122,10:30,200,209;20260115,10:30,198,215;20260108,10:30,208,213;20251231,10:30,199,219;20251224,10:30,214,224;20251218,10:30,224,224;20251211,10:30,236,220;20251204,10:30,191,219;20251126,10:30,216,226;20251120,10:30,220,228"
add("Claims",[(x.split(",")[0],x.split(",")[1],float(x.split(",")[2]),float(x.split(",")[3])) for x in cl.split(";")],sg=-1)
def servidor(dt,hbrt):
    day=pd.Timestamp(dt); winter = pd.Timestamp("2025-11-02")<=day<pd.Timestamp("2026-03-08")
    h,m=map(int,hbrt.split(":")); return day+pd.Timedelta(hours=h+(5 if winter else 6),minutes=m)
rows=[]
for tipo,dt,h,a,f,sg in E:
    t0=servidor(dt,h)
    try:
        ref=d.loc[t0-pd.Timedelta(minutes=5),"close"]; w=d.loc[t0:t0+pd.Timedelta(minutes=20)]
        r=dict(tipo=tipo,dia=dt,t0=t0.strftime("%H:%M"),surp=(a-f)*sg,rng20=w.high.max()-w.low.min(),
               m5=d.loc[t0,"close"]-ref,m15=d.loc[t0+pd.Timedelta(minutes=10),"close"]-ref,m60=d.loc[t0+pd.Timedelta(minutes=55),"close"]-ref)
        r["max_ext"]=max(w.high.max()-ref, ref-w.low.min())
        # baseline: mesma hora do dia em dias sem evento (amplitude 20 min)
        rows.append(r)
    except KeyError: pass
df=pd.DataFrame(rows)
# baseline por hora do servidor
ev_days={(r.dia,r.t0) for r in df.itertuples()}
def base(hhmm):
    v=[]
    for day in sorted(set(d.index.date)):
        ts=pd.Timestamp(day)
        if ts.dayofweek>4 or (ts.strftime("%Y%m%d"),hhmm) in ev_days: continue
        t0=ts+pd.Timedelta(hours=int(hhmm[:2]),minutes=int(hhmm[3:]))
        try: w=d.loc[t0:t0+pd.Timedelta(minutes=20)]; v.append(w.high.max()-w.low.min()) if len(w)>=4 else None
        except KeyError: pass
    return np.mean(v)
out=[]
for tipo,g in df.groupby("tipo",sort=False):
    b=np.mean([base(h) for h in g.t0.unique()])
    quente=g[g.surp>0]; frio=g[g.surp<0]
    out.append(dict(evento=tipo,n=len(g),hora_serv=",".join(sorted(g.t0.unique())),amp20=round(g.rng20.mean()),base=round(b),ratio=round(g.rng20.mean()/b,2),
        mov15_abs=round(g.m15.abs().mean(),1),mov60_abs=round(g.m60.abs().mean(),1),
        n_q=len(quente),m15_q=round(quente.m15.mean(),1) if len(quente) else None,n_f=len(frio),m15_f=round(frio.m15.mean(),1) if len(frio) else None,
        m60_q=round(quente.m60.mean(),1) if len(quente) else None,m60_f=round(frio.m60.mean(),1) if len(frio) else None))
pd.set_option("display.width",250); pd.set_option("display.max_columns",30)
print(pd.DataFrame(out).to_string(index=False))
print("\nDETALHE NFP/CPI/FOMC/ISM:")
print(df[df.tipo.isin(["NFP","CPI a/a","FOMC","ISM ind."])][["tipo","dia","t0","surp","rng20","m5","m15","m60"]].round(1).to_string(index=False))
df.to_csv("data/estudo_eventos_mt5.csv",index=False)
