"""Estudo de TODOS os eventos US (importancia media/alta, Investing) x NAS100 M5 (MT5). Hora servidor = NY+7h = UTC+3 (horario de verao EUA) ou UTC+2."""
import json, pandas as pd, numpy as np
ev=json.load(open("data/investing/eventos_us.json",encoding="utf-8")); sl=json.load(open("data/investing/slugs_us.json",encoding="utf-8")); oc=json.load(open("data/investing/ocorrencias_us.json",encoding="utf-8"))
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
tmin,tmax=d.index.min(),d.index.max()
def serv(utc):
    u=pd.Timestamp(utc); dst = u<pd.Timestamp("2025-11-02 06:00") or u>=pd.Timestamp("2026-03-08 07:00")
    return u+pd.Timedelta(hours=3 if dst else 2)
rows=[]
for eid,lst in oc.items():
    meta=ev.get(eid,{})
    for tt,a,f,p in lst:
        t0=serv(tt)
        if t0<tmin+pd.Timedelta(hours=2) or t0>tmax-pd.Timedelta(hours=2): continue
        try:
            ref=d.loc[t0-pd.Timedelta(minutes=5),"close"]; w=d.loc[t0:t0+pd.Timedelta(minutes=20)]
            if len(w)<4: continue
            m15=d.loc[t0+pd.Timedelta(minutes=10),"close"]-ref; m60=d.loc[t0+pd.Timedelta(minutes=55),"close"]-ref
        except KeyError: continue
        rows.append(dict(id=eid,nome=sl.get(eid,meta.get("n","?"))[:34],suf="",imp=meta.get("i",2),t0=t0,hhmm=t0.strftime("%H:%M"),dow=t0.dayofweek,
                         a=a,f=f,p=p,sur=(None if a is None or f is None else a-f),rng=w.high.max()-w.low.min(),m15=m15,m60=m60))
df=pd.DataFrame(rows); print("ocorrencias medidas:",len(df),"| eventos:",df.id.nunique())
# baseline: amplitude 20 min por hora do servidor em dias sem NENHUM evento naquela hora
ev_slots=set((r.t0.date(),r.hhmm) for r in df.itertuples())
base={}
def baseline(hhmm):
    if hhmm in base: return base[hhmm]
    v=[]
    for day in sorted(set(d.index.date)):
        ts=pd.Timestamp(day)
        if ts.dayofweek>4 or (day,hhmm) in ev_slots: continue
        t0=ts+pd.Timedelta(hours=int(hhmm[:2]),minutes=int(hhmm[3:]))
        w=d.loc[t0:t0+pd.Timedelta(minutes=20)]
        if len(w)>=4: v.append(w.high.max()-w.low.min())
    base[hhmm]=np.mean(v) if v else np.nan; return base[hhmm]
df["base"]=df.hhmm.map(baseline); df["ratio"]=df.rng/df.base
# por evento
g=df.groupby(["id","nome","suf"]).agg(n=("rng","size"),imp=("imp","first"),hora=("hhmm",lambda s:s.mode().iat[0]),amp=("rng","mean"),ratio=("ratio","mean"),
    abs15=("m15",lambda s:s.abs().mean()),abs60=("m60",lambda s:s.abs().mean())).reset_index()
def corr(x):
    y=x.dropna(subset=["sur"]); y=y[y.sur!=0]
    if len(y)<4: return np.nan
    return np.corrcoef(np.sign(y.sur),y.m15)[0,1]
c=df.groupby("id").apply(corr).rename("corr_sinal_sur_m15"); g=g.merge(c,left_on="id",right_index=True)
g=g[g.n>=4].sort_values("ratio",ascending=False)
pd.set_option("display.width",250); pd.set_option("display.max_rows",200)
print("\nTOP 30 por razao de amplitude (n>=4):"); print(g.head(30)[["nome","suf","hora","n","imp","amp","ratio","abs15","abs60","corr_sinal_sur_m15"]].round(2).to_string(index=False))
print("\nPOR SLOT (hora servidor): ocorrencias, amplitude media, razao"); 
s=df.groupby("hhmm").agg(n=("rng","size"),eventos=("id","nunique"),amp=("rng","mean"),ratio=("ratio","mean"),abs15=("m15",lambda s:s.abs().mean())).sort_values("ratio",ascending=False)
print(s[s.n>=8].head(15).round(2).to_string())
df.to_csv("data/estudo_todos_eventos.csv",index=False); g.to_csv("data/estudo_todos_eventos_resumo.csv",index=False)
