"""Mede o ATRASO das fontes de noticia: a cada rodada anota a hora (relogio do PC, UTC) em que cada manchete apareceu pela 1a vez
em cada fonte e a hora de publicacao informada pela fonte. Depois `python -I scripts/medir_noticias.py relatorio` cruza manchetes parecidas
entre fontes e mostra quem trouxe primeiro e a diferenca em minutos.
  rodar:      python -I scripts/medir_noticias.py coletar [minutos_entre_rodadas=2] [duracao_min=0 (infinito)]
  1 rodada:   python -I scripts/medir_noticias.py uma
  relatorio:  python -I scripts/medir_noticias.py relatorio
Log: journal/medicao_noticias.csv. So biblioteca padrao, nao instala nada."""
import sys, csv, re, time, urllib.request, urllib.parse, datetime as dt, os, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
LOG = 'journal/medicao_noticias.csv'
Q = lambda q: 'https://news.google.com/rss/search?q=' + urllib.parse.quote(q) + '&hl=en-US&gl=US&ceid=US:en'
RSS = {  # nome -> url
 'fed_press': 'https://www.federalreserve.gov/feeds/press_all.xml',
 'cnbc_mercados': 'https://www.cnbc.com/id/20910258/device/rss/rss.html',
 'marketwatch': 'https://feeds.content.dowjones.io/public/rss/mw_topstories',
 'gnews_fed': Q('Federal Reserve OR Powell OR FOMC when:1d'),
 'gnews_oil_trump': Q('oil OR Brent OR Trump tariff when:1d'),
 'gnews_nasdaq': Q('Nasdaq OR "Wall Street" stocks when:1d'),
 'investing_news': 'https://www.investing.com/rss/news_25.rss',
 'seekingalpha': 'https://seekingalpha.com/market-news',
}
def get(u):
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (medicao de atraso de noticias)'})
    return urllib.request.urlopen(r, timeout=25).read()
def parse(nome, raw):
    out = []
    if nome == 'seekingalpha':  # HTML: tenta pegar titulos e horas no JSON embutido
        t = raw.decode('utf8', 'ignore')
        pubs = [(m.start(), m.group(1)) for m in re.finditer(r'"publishOn":"([^"]+)"', t)]
        for m in re.finditer(r'"title":"([^"]{20,200})"', t):  # liga cada titulo a publishOn mais proximo (<800 car.)
            near = min(pubs, key=lambda p: abs(p[0] - m.start()), default=None)
            if near and abs(near[0] - m.start()) < 800:
                try: iso = dt.datetime.fromisoformat(near[1]).astimezone(dt.timezone.utc).isoformat()
                except Exception: continue
                out.append((m.group(1), iso))
        return out
    root = ET.fromstring(raw)
    for it in root.iter('item'):
        ti = (it.findtext('title') or '').strip(); pd = it.findtext('pubDate') or ''
        try: pub = parsedate_to_datetime(pd).astimezone(dt.timezone.utc).isoformat()
        except Exception: pub = ''
        out.append((ti, pub))
    return out
def vistos():
    if not os.path.exists(LOG): return set()
    with open(LOG, encoding='utf8') as f: return {(r['fonte'], r['titulo']) for r in csv.DictReader(f)}
def rodada():
    os.makedirs('journal', exist_ok=True); novo = not os.path.exists(LOG); v = vistos(); n = 0; resumo = []
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    with open(LOG, 'a', newline='', encoding='utf8') as f:
        w = csv.writer(f)
        if novo: w.writerow(['fonte', 'titulo', 'publicado_utc', 'visto_utc'])
        for nome, url in RSS.items():
            try: itens = parse(nome, get(url))
            except Exception as e: resumo.append(f'{nome}: ERRO {type(e).__name__}'); continue
            k = 0
            for ti, pub in itens:
                if (nome, ti) in v: continue
                w.writerow([nome, ti, pub, now]); v.add((nome, ti)); k += 1; n += 1
            resumo.append(f'{nome}: {len(itens)} itens, {k} novos')
    print(now, '|', ' | '.join(resumo)); return n
def norm(s): return set(w for w in re.findall(r'[a-z0-9]{4,}', s.lower()) if w not in {'with', 'from', 'that', 'this', 'stock', 'stocks', 'market', 'says', 'will', 'after', 'about'})
def relatorio():
    with open(LOG, encoding='utf8') as f: rows = [r for r in csv.DictReader(f) if r['publicado_utc']]  # sem hora de publicacao nao da para medir atraso
    def t(r): return dt.datetime.fromisoformat(r['publicado_utc']) if r['publicado_utc'] else dt.datetime.fromisoformat(r['visto_utc'])
    grupos = []
    for r in sorted(rows, key=t):
        a = norm(r['titulo'])
        for g in grupos:
            if len(a & g['pal']) >= 4 and len(a & g['pal']) / max(1, len(a | g['pal'])) > .35 and all(x['fonte'] != r['fonte'] for x in g['r']):
                g['r'].append(r); g['pal'] |= a; break
        else: grupos.append({'pal': a, 'r': [r]})
    multi = [g for g in grupos if len(g['r']) >= 2]
    print(f'{len(rows)} manchetes, {len(multi)} historias em 2+ fontes')
    atraso = {}
    for g in multi:
        base = min(t(x) for x in g['r'])
        print('\n*', g['r'][0]['titulo'][:90])
        for x in sorted(g['r'], key=t):
            d = (t(x) - base).total_seconds() / 60; atraso.setdefault(x['fonte'], []).append(d)
            print(f'    {x["fonte"]:16s} +{d:5.1f} min (publicado {x["publicado_utc"][11:16] or "?"} UTC, visto {x["visto_utc"][11:16]})')
    print('\nATRASO MEDIO vs a fonte mais rapida de cada historia (min):')
    for k, v in sorted(atraso.items(), key=lambda kv: sum(kv[1]) / len(kv[1])): print(f'  {k:16s} {sum(v)/len(v):5.1f}  (n={len(v)})')
if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else 'uma'
    if c == 'uma': rodada()
    elif c == 'relatorio': relatorio()
    elif c == 'coletar':
        gap = float(sys.argv[2]) if len(sys.argv) > 2 else 2; dur = float(sys.argv[3]) if len(sys.argv) > 3 else 0; fim = time.time() + dur * 60
        while not dur or time.time() < fim: rodada(); time.sleep(gap * 60)
