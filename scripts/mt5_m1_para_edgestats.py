"""Converte velas M1 exportadas do MT5 (data/nas100_m1_mt5.csv, hora do servidor = NY+7h) para CSV UTC ISO do Edge Stats (tools/edge-lab/bars/nas100_m1.csv)."""
import csv, datetime as dt
def nth_sun(y, m, k):
    d = dt.date(y, m, 1); c = 0
    while True:
        if d.weekday() == 6:
            c += 1
            if c == k: return d
        d += dt.timedelta(days=1)
cache = {}
with open('data/nas100_m1_mt5.csv', encoding='utf8') as f, open('tools/edge-lab/bars/nas100_m1.csv', 'w', newline='') as o:
    r = csv.DictReader(f, delimiter='\t'); w = csv.writer(o); w.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    for row in r:
        ny = dt.datetime.strptime(row['<DATE>'] + ' ' + row['<TIME>'], '%Y.%m.%d %H:%M:%S') - dt.timedelta(hours=7)
        if ny.year not in cache: cache[ny.year] = (nth_sun(ny.year, 3, 2), nth_sun(ny.year, 11, 1))
        a, b = cache[ny.year]
        utc = ny + dt.timedelta(hours=4 if a <= ny.date() < b else 5)
        w.writerow([utc.strftime('%Y-%m-%dT%H:%M:%SZ'), row['<OPEN>'], row['<HIGH>'], row['<LOW>'], row['<CLOSE>'], row['<TICKVOL>']])
