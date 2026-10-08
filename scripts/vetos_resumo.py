"""Resume journal/vetos.csv: por item da ficha, quantos vetos e quantos acertaram (preco foi contra o lado). N<20 = sem conclusao."""
import csv, collections
c = collections.defaultdict(lambda: [0, 0, 0])  # total, acertou, errou
for r in csv.DictReader(open('journal/vetos.csv', encoding='utf8')):
    k = r['item_que_vetou'] or '?'; v = r['veto_acertou(sim/nao/incerto)'].strip().lower(); c[k][0] += 1
    if v == 'sim': c[k][1] += 1
    elif v == 'nao': c[k][2] += 1
print('item   vetos  acertou  errou  taxa_acerto')
for k, (t, a, e) in sorted(c.items()): print(f'{k:6s} {t:5d} {a:8d} {e:6d}  {a/(a+e)*100:5.0f}%' + ('  (N<20: sem conclusao)' if t < 20 else '') if a + e else f'{k:6s} {t:5d}  sem desfecho preenchido')
