// FOTOGRAFIA PRE-ENTRADA: cole no mcp__tradingview__ui_evaluate (expression). Grafico PEPPERSTONE:NAS100 em M5.
// Calcula das velas do grafico, SEM indicador na tela, o que o Passo 0 e o Setup de Regioes precisam (docs/ficha-pre-entrada.md):
//  momento (esticado x VWAP NY), liquidez varrida/aberta (Asia, Londres, NY AM, PDH/PDL), abertura de NY (15 min),
//  estrutura interna (pivo 5, BOS/CHoCH), FVGs abertos estilo LuxAlgo (filtro de deslocamento), momentum M5/M15, ultima vela fechada (pavio), ATR.
// Sessoes em UTC iguais ao Painel: Asia 00-06, Londres 06-13:30, NY AM 13:30-16. Dia de NY = 00:00 ET. Volume do CFD = tick volume.
(function(){
const b=window.TradingViewApi._activeChartWidgetWV.value()._chartWidget.model().mainSeries().bars();
const f=b.firstIndex(), l=b.lastIndex();
const fmt=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
const nyp=t=>{const p={};fmt.formatToParts(new Date(t*1000)).forEach(x=>p[x.type]=x.value);return {d:p.year+p.month+p.day,m:(+p.hour)*60+(+p.minute)};};
const B=[];for(let i=f;i<=l;i++){const v=b.valueAt(i);if(!v)continue;const n=nyp(v[0]);B.push({t:v[0],o:v[1],h:v[2],l:v[3],c:v[4],v:v[5]||1,d:n.d,m:n.m});}
const N=B.length, last=B[N-1], px=last.c, r1=x=>x==null||isNaN(x)?null:+(+x).toFixed(1);
const hhmm=t=>{const d=new Date(t*1000);return String((d.getUTCHours()+21)%24).padStart(2,'0')+':'+String(d.getUTCMinutes()).padStart(2,'0')+' BRT';};
// ---- ATR(14) Wilder ----
let atr=null;{let s=0;for(let i=1;i<N;i++){const tr=Math.max(B[i].h-B[i].l,Math.abs(B[i].h-B[i-1].c),Math.abs(B[i].l-B[i-1].c));if(i<=14){s+=tr;if(i===14)atr=s/14;}else atr=(atr*13+tr)/14;}}
// ---- VWAP NY (09:30 ET) e do dia ----
const today=last.d, D=B.filter(x=>x.d===today), NYs=D.filter(x=>x.m>=570);
const vw=a=>{let sv=0,sp=0,sp2=0;a.forEach(x=>{const p=(x.h+x.l+x.c)/3;sv+=x.v;sp+=p*x.v;sp2+=p*p*x.v;});if(!sv)return null;const m=sp/sv,sd=Math.sqrt(Math.max(0,sp2/sv-m*m));return {vwap:r1(m),sd:r1(sd),z:sd?+((px-m)/sd).toFixed(2):null};};
const vNY=vw(NYs), vDia=vw(D);
const esticado=vNY&&vNY.z!=null?(Math.abs(vNY.z)>=2?'MUITO ESTICADO (>=2 desvios): nao perseguir':Math.abs(vNY.z)>=1?'esticado (1-2 desvios)':'perto do valor (<1 desvio)'):'sem VWAP NY (antes de 10:30 BRT)';
// ---- Liquidez: sessoes do dia UTC corrente + dia anterior de NY ----
const dUTC=new Date(last.t*1000);const day0=Date.UTC(dUTC.getUTCFullYear(),dUTC.getUTCMonth(),dUTC.getUTCDate())/1000;
const sess=(nm,a,z)=>{const s=B.filter(x=>x.t>=day0+a&&x.t<day0+z);if(!s.length)return null;const H=Math.max(...s.map(x=>x.h)),L=Math.min(...s.map(x=>x.l));const after=B.filter(x=>x.t>=day0+z);const fim=last.t>=day0+z;
 return {sessao:nm,max:H,min:L,maxVarrida:fim?after.some(x=>x.h>H):null,minVarrida:fim?after.some(x=>x.l<L):null,emCurso:!fim};};
const S=[sess('Asia',0,6*3600),sess('Londres',6*3600,13.5*3600),sess('NY AM',13.5*3600,16*3600)].filter(Boolean);
const days=[...new Set(B.map(x=>x.d))];const prevD=days[days.indexOf(today)-1];const P=B.filter(x=>x.d===prevD);
const pdh=P.length?Math.max(...P.map(x=>x.h)):null, pdl=P.length?Math.min(...P.map(x=>x.l)):null;
const liq=S.map(s=>({sessao:s.sessao,max:s.max,maxStatus:s.emCurso?'em curso':s.maxVarrida?'varrida':'ABERTA (alvo)',min:s.min,minStatus:s.emCurso?'em curso':s.minVarrida?'varrida':'ABERTA (alvo)'}));
liq.push({sessao:'Ontem (dia NY)',max:pdh,maxStatus:D.some(x=>x.h>pdh)?'varrida':'ABERTA (alvo)',min:pdl,minStatus:D.some(x=>x.l<pdl)?'varrida':'ABERTA (alvo)'});
// ---- Abertura de NY: primeiros 15 min ----
const ab=NYs.slice(0,3);const abertura=ab.length<3?(NYs.length?'formando (ainda nos 15 min)':'NY nao abriu'):{max:Math.max(...ab.map(x=>x.h)),min:Math.min(...ab.map(x=>x.l)),movimento:r1(ab[2].c-ab[0].o),precoAgora:px>Math.max(...ab.map(x=>x.h))?'acima':px<Math.min(...ab.map(x=>x.l))?'abaixo':'dentro'};
// ---- Estrutura interna (pivo 5; BOS/CHoCH no fechamento) ----
let lh=null,ll=null,ht=true,lt=true,tr=0,ev=[];const sw=5;
for(let i=2*sw;i<N;i++){const j=i-sw;let okh=true,okl=true;for(let k=j-sw;k<=i;k++){if(k===j)continue;if(k<j){if(B[k].h>=B[j].h)okh=false;if(B[k].l<=B[j].l)okl=false;}else{if(B[k].h>B[j].h)okh=false;if(B[k].l<B[j].l)okl=false;}}
 if(okh){lh=B[j].h;ht=false;} if(okl){ll=B[j].l;lt=false;}
 if(!ht&&lh!==null&&B[i].c>lh){ht=true;ev.push({tipo:tr===1?'BOS':'CHoCH',lado:'ALTA',nivel:lh,t:B[i].t});tr=1;}
 if(!lt&&ll!==null&&B[i].c<ll){lt=true;ev.push({tipo:tr===-1?'BOS':'CHoCH',lado:'BAIXA',nivel:ll,t:B[i].t});tr=-1;}}
const ultimos=ev.slice(-4).map(e=>({tipo:e.tipo,lado:e.lado,nivel:e.nivel,ha_min:Math.round((last.t-e.t)/60)}));
// ---- FVGs abertos (LuxAlgo: filtro de deslocamento; mitigado ao cruzar a borda oposta) ----
let cum=0;const Z=[];
for(let i=2;i<N;i++){const bd=(B[i-1].c-B[i-1].o)/(B[i-1].o*100);cum+=Math.abs(bd);const thr=cum/(i+1)*2;
 if(B[i].l>B[i-2].h&&B[i-1].c>B[i-2].h&&bd>thr)Z.push({dir:'ALTA (demanda)',top:B[i].l,bot:B[i-2].h,i});
 if(B[i].h<B[i-2].l&&B[i-1].c<B[i-2].l&&-bd>thr)Z.push({dir:'BAIXA (oferta)',top:B[i-2].l,bot:B[i].h,i});}
const abertos=Z.filter(z=>!B.slice(z.i+1).some(x=>z.dir[0]==='A'?x.l<z.bot:x.h>z.top)).slice(-8).map(z=>({dir:z.dir,top:r1(z.top),meio:r1((z.top+z.bot)/2),bot:r1(z.bot),dist_meio:r1((z.top+z.bot)/2-px),idade_min:Math.round((last.t-B[z.i].t)/60),aFavorDaEstrutura:(z.dir[0]==='A'&&tr===1)||(z.dir[0]==='B'&&tr===-1)}));
// ---- Momentum (RSI14, MACD 12/26/9 hist, estocastico 14:3:3) M5 e M15 ----
const ema=(a,n)=>{const k=2/(n+1);const r=[a[0]];for(let i=1;i<a.length;i++)r.push(a[i]*k+r[i-1]*(1-k));return r;};
const sma=(a,n)=>a.map((_,i)=>i<n-1?NaN:a.slice(i-n+1,i+1).reduce((x,y)=>x+y,0)/n);
const rsi=(c,n)=>{let g=0,d=0,r=NaN;for(let i=1;i<c.length;i++){const ch=c[i]-c[i-1],u=Math.max(ch,0),dn=Math.max(-ch,0);if(i<=n){g+=u/n;d+=dn/n;}else{g=(g*(n-1)+u)/n;d=(d*(n-1)+dn)/n;}if(i>=n)r=100-100/(1+g/(d||1e-9));}return r;};
const mom=(H,L,C)=>{const n=C.length-1;const m=ema(C,12).map((x,i)=>x-ema(C,26)[i]);const sg=ema(m,9);const k=C.map((x,i)=>{if(i<13)return NaN;const hh=Math.max(...H.slice(i-13,i+1)),lo=Math.min(...L.slice(i-13,i+1));return 100*(x-lo)/((hh-lo)||1e-9);});const k3=sma(k.map(x=>isNaN(x)?50:x),3),d3=sma(k3,3);
 const st=k3[n];return {rsi:r1(rsi(C,14)),macdHist:r1(m[n]-sg[n]),macdHistAntes:r1(m[n-3]-sg[n-3]),stochK:r1(st),stochD:r1(d3[n]),leitura:st>=80?'sobrecomprado':st<=20?'sobrevendido':'meio'};};
const W=B.slice(-400);const m5=mom(W.map(x=>x.h),W.map(x=>x.l),W.map(x=>x.c));
const g={};W.forEach(x=>{const k=Math.floor(x.t/900);(g[k]=g[k]||{h:-1e9,l:1e9,c:0}).h=Math.max(g[k].h,x.h);g[k].l=Math.min(g[k].l,x.l);g[k].c=x.c;});
const ks=Object.keys(g).sort((a,c)=>a-c).slice(0,-1);const m15=mom(ks.map(k=>g[k].h),ks.map(k=>g[k].l),ks.map(k=>g[k].c));
// ---- Ultima vela M5 FECHADA (gatilho de pavio) ----
const q=B[N-2], corpo=Math.abs(q.c-q.o), sup=q.h-Math.max(q.o,q.c), inf=Math.min(q.o,q.c)-q.l;
const vela={hora:hhmm(q.t),o:q.o,h:q.h,l:q.l,c:q.c,corpo:r1(corpo),pavioSup:r1(sup),pavioInf:r1(inf),leitura:inf>=2*corpo&&inf>=0.5*(atr||0)?'REJEICAO COMPRADORA (pavio inferior)':sup>=2*corpo&&sup>=0.5*(atr||0)?'REJEICAO VENDEDORA (pavio superior)':'sem rejeicao clara'};
return JSON.stringify({hora:hhmm(last.t),preco:px,atrM5:r1(atr),
 momento:{vwapNY:vNY,vwapDia:vDia,esticado,aberturaNY15:abertura},
 liquidez:liq,
 estrutura:{tendenciaInterna:tr===1?'ALTA':tr===-1?'BAIXA':'indefinida',ultimos},
 fvgAbertos:abertos,momentum:{M5:m5,M15:m15},ultimaVelaFechada:vela});})()
