// Cole no mcp__tradingview__ui_evaluate (expression). Gráfico NAS100 em M5. Calcula SEM indicador na tela:
//  - VWAP NY (ancora 09:30 ET = 10:30 BRT), VWAP Dia (ancora 00:00 ET = 01:00 BRT), VWAP Extremo (ancora na minima do dia de NY)
//    cada um com bandas de +-1 e +-2 desvios (desvio ponderado pelo volume; volume do CFD = tick volume, referencia e nao numero exato)
//  - Faixa de abertura de NY: maxima/minima dos primeiros 15 e 30 min (09:30 ET)
// Mesmo calculo do indicador pine/vwaps_ny_dia_extremo.pine (preco tipico hlc3). Fuso de NY via Intl (respeita horario de verao).
(function(){
const b=window.TradingViewApi._activeChartWidgetWV.value()._chartWidget.model().mainSeries().bars();
const f=b.firstIndex(), l=b.lastIndex();
const fmt=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'});
const ny=t=>{const p={};fmt.formatToParts(new Date(t*1000)).forEach(x=>p[x.type]=x.value);return {d:p.year+p.month+p.day,m:(+p.hour)*60+(+p.minute)};};
const B=[];for(let i=f;i<=l;i++){const v=b.valueAt(i);if(!v)continue;const n=ny(v[0]);B.push({t:v[0],o:v[1],h:v[2],l:v[3],c:v[4],v:v[5]||1,d:n.d,m:n.m});}
const today=B[B.length-1].d, D=B.filter(x=>x.d===today);
const vw=(arr)=>{let sv=0,sp=0,sp2=0;arr.forEach(x=>{const p=(x.h+x.l+x.c)/3;sv+=x.v;sp+=p*x.v;sp2+=p*p*x.v;});if(!sv)return null;const m=sp/sv,sd=Math.sqrt(Math.max(0,sp2/sv-m*m));const r=z=>+z.toFixed(1);return {vwap:r(m),sd:r(sd),p1:r(m+sd),m1:r(m-sd),p2:r(m+2*sd),m2:r(m-2*sd),barras:arr.length};};
const lowBar=D.reduce((a,x)=>x.l<a.l?x:a,D[0]), highBar=D.reduce((a,x)=>x.h>a.h?x:a,D[0]);
const nyArr=D.filter(x=>x.m>=570);
const hhmm=x=>new Date(x.t*1000).toISOString().substr(11,5)+'Z';
const orb=n=>{const a=nyArr.slice(0,n);return a.length<n?null:{max:Math.max(...a.map(x=>x.h)),min:Math.min(...a.map(x=>x.l))};};
const last=B[B.length-1];
return JSON.stringify({dataNY:today,preco:last.c,
 NY:vw(nyArr),Dia:vw(D),
 ExtremoMinima:{ancora:hhmm(lowBar),low:lowBar.l,...vw(D.filter(x=>x.t>=lowBar.t))},
 ExtremoMaxima:{ancora:hhmm(highBar),high:highBar.h,...vw(D.filter(x=>x.t>=highBar.t))},
 ORB15:orb(3),ORB30:orb(6)});})()
