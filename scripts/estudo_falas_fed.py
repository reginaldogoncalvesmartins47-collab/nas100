"""Falas de dirigentes (inclui importancia baixa) x NAS100 M5 (MT5). Baseline = mesma hora do servidor em dias sem nenhum evento medio/alto nem fala."""
import json, pandas as pd, numpy as np
fa=json.load(open("data/investing/falas_us.json",encoding="utf-8")); meta,occ=fa["meta"],fa["occ"]
d=pd.read_csv("data/nas100_m5_mt5.csv",sep="\t"); d.columns=[c.strip("<>").lower() for c in d.columns]
d["t"]=pd.to_datetime(d["date"]+" "+d["time"],format="%Y.%m.%d %H:%M:%S"); d=d.set_index("t").sort_index()
tmin,tmax=d.index.min(),d.index.max()
def serv(u):
    u=pd.Timestamp(u); dst = u<pd.Timestamp("2025-11-02 06:00") or u>=pd.Timestamp("2026-03-08 07:00"); return u+pd.Timedelta(hours=3 if dst else 2)
big=pd.read_csv("data/estudo_todos_eventos.csv"); big["t0"]=pd.to_datetime(big.t0)
busy=set((t.date(),t.strftime("%H:%M")) for t in big.t0)
rows=[]
for eid,lst in occ.items():
    nome=meta[eid]["s"]
    for tt in lst:
        t0=serv(tt)
        if t0<tmin+pd.Timedelta(hours=2) or t0>tmax-pd.Timedelta(hours=2): continue
        try:
            ref=d.loc[t0-pd.Timedelta(minutes=5),"close"]; w=d.loc[t0:t0+pd.Timedelta(minutes=20)]
            if len(w)<4: continue
            rows.append(dict(nome=nome,t0=t0,hhmm=t0.strftime("%H:%M"),rng=w.high.max()-w.low.min(),m15=d.loc[t0+pd.Timedelta(minutes=10),"close"]-ref,m60=d.loc[t0+pd.Timedelta(minutes=55),"close"]-ref))
        except KeyError: pass
df=pd.DataFrame(rows)
speech_slots=set((r.t0.date(),r.hhmm) for r in df.itertuples())
cache={}
def base(hhmm):
    if hhmm in cache: return cache[hhmm]
    v=[];m=[]
    for day in sorted(set(d.index.date)):
        ts=pd.Timestamp(day)
        if ts.dayofweek>4 or (day,hhmm) in busy or (day,hhmm) in speech_slots: continue
        t0=ts+pd.Timedelta(hours=int(hhmm[:2]),minutes=int(hhmm[3:]))
        try:
            w=d.loc[t0:t0+pd.Timedelta(minutes=20)]
            if len(w)>=4: v.append(w.high.max()-w.low.min()); m.append(abs(d.loc[t0+pd.Timedelta(minutes=10),"close"]-d.loc[t0-pd.Timedelta(minutes=5),"close"]))
        except KeyError: pass
    cache[hhmm]=(np.mean(v) if v else np.nan, np.mean(m) if m else np.nan); return cache[hhmm]
df["b_rng"]=df.hhmm.map(lambda h:base(h)[0]); df["b_m15"]=df.hhmm.map(lambda h:base(h)[1]); df["ratio"]=df.rng/df.b_rng; df["r15"]=df.m15.abs()/df.b_m15
g=df.groupby("nome").agg(n=("rng","size"),hora_tip=("hhmm",lambda s:s.mode().iat[0]),amp=("rng","mean"),ratio=("ratio","mean"),abs15=("m15",lambda s:s.abs().mean()),r15=("r15","mean"),abs60=("m60",lambda s:s.abs().mean()),m60=("m60","mean")).reset_index()
g["nome"]=g.nome.str.replace("fomc-member-","").str.replace("-speaks","").str.replace("fed-","")
g=g[g.n>=3].sort_values("ratio",ascending=False)
pd.set_option("display.width",250); pd.set_option("display.max_rows",100)
print(f"{len(df)} falas medidas, {df.nome.nunique()} oradores/eventos"); print(g.round(2).to_string(index=False))
df.to_csv("data/estudo_falas_fed.csv",index=False)
