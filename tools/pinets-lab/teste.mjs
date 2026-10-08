import { PineTS } from 'pinets';
import fs from 'fs';
const rows = fs.readFileSync('../../data/nas100_m5_mt5.csv','utf8').trim().split(/\r?\n/).slice(1);
const candles = rows.map(l=>{const c=l.split('\t');const [y,m,d]=c[0].split('.').map(Number);const [H,M,S]=c[1].split(':').map(Number);
 const t=Date.UTC(y,m-1,d,H,M,S);return {openTime:t,open:+c[2],high:+c[3],low:+c[4],close:+c[5],volume:+c[6],closeTime:t+300000-1};});
console.log('velas',candles.length);
const p = new PineTS(candles);
const t0=Date.now();
const { plots } = await p.run(`
//@version=6
indicator("teste")
plot(ta.rsi(close,14),"rsi")
plot(ta.ema(close,26),"ema26")
plot(ta.atr(14),"atr")
`);
console.log('ms',Date.now()-t0);
for (const k of Object.keys(plots)) { const d=plots[k].data; console.log(k, d.length, d[d.length-1]?.value ?? d[d.length-1]); }
const last=candles[candles.length-1]; console.log('ultima vela',new Date(last.openTime).toISOString(), last.close);
