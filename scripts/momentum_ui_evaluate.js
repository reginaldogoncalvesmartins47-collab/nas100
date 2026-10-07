// Cole no mcp__tradingview__ui_evaluate (expression). Calcula RSI14, MACD 12/26/9, WaveTrend (10/21) e estocastico 14:3:3 de M5 e M15 das velas do grafico (400 velas). Retorna JSON.
(function(){
const b=window.TradingViewApi._activeChartWidgetWV.value()._chartWidget.model().mainSeries().bars();
const N=400, l=b.lastIndex(), s=Math.max(b.firstIndex(),l-N+1);
const T=[],O=[],H=[],L=[],C=[];
for(let i=s;i<=l;i++){const v=b.valueAt(i); if(!v)continue; T.push(v[0]);O.push(v[1]);H.push(v[2]);L.push(v[3]);C.push(v[4]);}
const ema=(a,n)=>{const k=2/(n+1);const r=[a[0]];for(let i=1;i<a.length;i++)r.push(a[i]*k+r[i-1]*(1-k));return r;};
const sma=(a,n)=>a.map((_,i)=>i<n-1?NaN:a.slice(i-n+1,i+1).reduce((x,y)=>x+y,0)/n);
const rsi=(c,n)=>{let g=0,d=0;const r=[NaN];for(let i=1;i<c.length;i++){const ch=c[i]-c[i-1];const u=Math.max(ch,0),dn=Math.max(-ch,0);if(i<=n){g+=u/n;d+=dn/n;r.push(i==n?100-100/(1+g/d):NaN);}else{g=(g*(n-1)+u)/n;d=(d*(n-1)+dn)/n;r.push(100-100/(1+g/d));}}return r;};
const macd=(c)=>{const e12=ema(c,12),e26=ema(c,26);const m=e12.map((x,i)=>x-e26[i]);const sg=ema(m,9);return {m,sg,h:m.map((x,i)=>x-sg[i])};};
const wt=(h,l,c)=>{const ap=c.map((x,i)=>(h[i]+l[i]+x)/3);const esa=ema(ap,10);const d=ema(ap.map((x,i)=>Math.abs(x-esa[i])),10);const ci=ap.map((x,i)=>(x-esa[i])/(0.015*(d[i]||1e-9)));const w1=ema(ci,21);return {w1,w2:sma(w1,4)};};
const stoch=(h,l,c)=>{const k=c.map((x,i)=>{if(i<13)return NaN;const hh=Math.max(...h.slice(i-13,i+1)),ll=Math.min(...l.slice(i-13,i+1));return 100*(x-ll)/(hh-ll);});const k3=sma(k.map(x=>isNaN(x)?0:x),3);return {k:k3,d:sma(k3,3)};};
const calc=(h,l,c)=>{const R=rsi(c,14),M=macd(c),W=wt(h,l,c),S=stoch(h,l,c);const n=c.length-1;const f=x=>(x==null||isNaN(x))?null:Number(x.toFixed(2));
 const win=40;const idx=[...Array(win).keys()].map(i=>n-win+1+i);
 const lo=idx.filter(i=>i>2&&i<n-2&&l[i]<=l[i-1]&&l[i]<=l[i+1]&&l[i]<=l[i-2]&&l[i]<=l[i+2]);
 const hi=idx.filter(i=>i>2&&i<n-2&&h[i]>=h[i-1]&&h[i]>=h[i+1]&&h[i]>=h[i-2]&&h[i]>=h[i+2]);
 let div='nenhuma';
 if(lo.length>=2){const a=lo[lo.length-2],z=lo[lo.length-1];if(l[z]<l[a]&&R[z]>R[a])div='ALTA';}
 if(hi.length>=2){const a=hi[hi.length-2],z=hi[hi.length-1];if(h[z]>h[a]&&R[z]<R[a])div='BAIXA';}
 return {rsi:f(R[n]),rsi3:f(R[n-3]),macd:f(M.m[n]),sig:f(M.sg[n]),hist:f(M.h[n]),hist3:f(M.h[n-3]),wt1:f(W.w1[n]),wt2:f(W.w2[n]),stK:f(S.k[n]),stD:f(S.d[n]),div};};
const m5=calc(H,L,C);
const g={};T.forEach((t,i)=>{const k=Math.floor(t/900);(g[k]=g[k]||{h:-1e9,l:1e9,c:0}).h=Math.max(g[k].h,H[i]);g[k].l=Math.min(g[k].l,L[i]);g[k].c=C[i];});
const ks=Object.keys(g).sort((a,b)=>a-b);const h15=ks.map(k=>g[k].h),l15=ks.map(k=>g[k].l),c15=ks.map(k=>g[k].c);
const m15=calc(h15.slice(0,-1),l15.slice(0,-1),c15.slice(0,-1));
return JSON.stringify({preco:C[C.length-1],M5:m5,M15:m15});})()
