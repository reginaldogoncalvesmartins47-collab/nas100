import { PineTS } from 'pinets';
const t0=Date.UTC(2026,9,7,14,30); // 14:30 UTC = 10:30 NY (EDT)
const cs=[0,1,2].map(i=>({openTime:t0+i*300000,open:1,high:2,low:0.5,close:1.5,volume:10,closeTime:t0+i*300000+299999}));
const p=new PineTS(cs,'X','5');
const {plots}=await p.run(`
//@version=6
indicator("tz")
plot(hour(time,"America/New_York"),"hNY")
plot(hour(time,"UTC"),"hUTC")
plot(dayofmonth(time,"America/New_York"),"dNY")
plot(syminfo.mintick,"mintick")
plot(volume,"vol")
`);
for(const k of ['hNY','hUTC','dNY','mintick','vol']) console.log(k, plots[k]?.data.map(d=>d.value));
