import { PineTS } from 'pinets';
import fs from 'fs';
const rows = fs.readFileSync('../../data/nas100_m5_mt5.csv','utf8').trim().split(/\r?\n/).slice(1);
const candles = rows.map(l=>{const c=l.split('\t');const [y,m,d]=c[0].split('.').map(Number);const [H,M,S]=c[1].split(':').map(Number);
 const ts=Date.UTC(y,m-1,d,H,M,S)-7*3600000; const dst=(()=>{const yr=new Date(ts).getUTCFullYear();const nth=(mo,wd,k)=>{let c=0;for(let dd=1;dd<=31;dd++){const x=new Date(Date.UTC(yr,mo,dd));if(x.getUTCMonth()!==mo)break;if(x.getUTCDay()===wd&&++c===k)return Date.UTC(yr,mo,dd,7);}};return ts>=nth(2,0,2)&&ts<nth(10,0,1);})(); const t=ts+(dst?4:5)*3600000;return {openTime:t,open:+c[2],high:+c[3],low:+c[4],close:+c[5],volume:+c[6],closeTime:t+300000-1};});
const src = fs.readFileSync('lab2.pine','utf8');
const p = new PineTS(candles.slice(-24000), 'NAS100', '5');
try {
  const t0=Date.now();
  const r = await p.run(src);
  console.log('OK em ms', Date.now()-t0); const cs=candles.slice(-24000); const out={t:cs.map(c=>c.openTime),o:cs.map(c=>c.open),h:cs.map(c=>c.high),l:cs.map(c=>c.low),c:cs.map(c=>c.close),plots:{}}; for(const k of Object.keys(r.plots)){ if(k.startsWith('__'))continue; out.plots[k]=r.plots[k].data.map(d=>d.value);} fs.writeFileSync('saida_zonas.json',JSON.stringify(out)); console.log('plots',Object.keys(out.plots).length,'barras',out.t.length);
} catch(e) { console.log('ERRO:', String(e.message||e).slice(0,600)); }
