"""Monitor de noticias (usuaria, 08/10/2026: 'o certo era ter um webhook que te avisa de noticias').
Sem webhook gratis de Bloomberg/Reuters, faz POLLING a cada 45 s de: Fed press RSS, Seeking Alpha market-news, Google News RSS (varias buscas),
e imprime 1 linha por manchete NOVA que case com palavras-chave de mercado e tenha sido publicada nos ultimos 40 min. Uso com a ferramenta Monitor:
  python -u scripts/noticias_monitor.py
Linha: 'HH:MM BRT [fonte] titulo (publicado ha N min)'. A 1a rodada so memoriza (nao imprime). So biblioteca padrao."""
import re, sys, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime as dt, io
from email.utils import parsedate_to_datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8', errors='replace', line_buffering=True)
BRT = dt.timezone(dt.timedelta(hours=-3))
KW = re.compile(r"\b(fed|fomc|powell|waller|bowman|williams|logan|treasury|yield|bessent|trump|iran|tariff|oil|opec|nasdaq|nvidia|micron|chip|semiconductor|auction|rate hike|inflation|cpi|payroll|jobs|ceasefire|attack|strike|sanction|china|taiwan|crash|plunge|surge|tumble|selloff|rally)\b", re.I)
Q = lambda q: 'https://news.google.com/rss/search?q=' + urllib.parse.quote(q) + '&hl=en-US&gl=US&ceid=US:en'
FEEDS = {'FedPress': 'https://www.federalreserve.gov/feeds/press_all.xml',
 'GN-Fed/Trump': Q('Fed OR Powell OR Waller OR Trump OR Iran OR Treasury when:1h'),
 'GN-Mercado': Q('stocks OR Nasdaq OR "Wall Street" OR yields OR oil when:1h'),
 'GN-Chips': Q('Nvidia OR Micron OR semiconductor OR chip stocks when:1h'),
 'SeekingAlpha': 'https://seekingalpha.com/market-news'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25).read()
def itens(nome, raw):
    out = []
    if nome == 'SeekingAlpha':
        t = raw.decode('utf8', 'ignore'); pubs = [(m.start(), m.group(1)) for m in re.finditer(r'"publishOn":"([^"]+)"', t)]
        for m in re.finditer(r'"title":"([^"]{20,200})"', t):
            near = min(pubs, key=lambda p: abs(p[0] - m.start()), default=None)
            if near and abs(near[0] - m.start()) < 800:
                try: out.append((m.group(1), dt.datetime.fromisoformat(near[1]).astimezone(dt.timezone.utc)))
                except Exception: pass
        return out
    for it in ET.fromstring(raw).iter('item'):
        try: p = parsedate_to_datetime(it.findtext('pubDate')).astimezone(dt.timezone.utc)
        except Exception: continue
        out.append(((it.findtext('title') or '').strip(), p))
    return out
vistos = set(); primeira = True
while True:
    agora = dt.datetime.now(dt.timezone.utc)
    for nome, url in FEEDS.items():
        try: its = itens(nome, get(url))
        except Exception: continue
        for ti, p in its:
            k = re.sub(r'\W+', '', ti.lower())[:70]
            if k in vistos: continue
            vistos.add(k)
            idade = (agora - p).total_seconds() / 60
            if not primeira and idade <= 40 and KW.search(ti):
                print(f"{p.astimezone(BRT):%H:%M} BRT [{nome}] {ti[:150]} (publicado ha {idade:.0f} min)")
    primeira = False
    time.sleep(45)
