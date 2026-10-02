"""Radar de liquidez a partir de velas OHLC (M5): FVGs abertos e max/min. Uso: python scripts/radar_liquidez.py barras.json [preco]
barras.json = lista de [open,high,low,close] em ordem cronologica. Sem dependencias."""
import json, sys
def fvgs(b):
    out = []
    for i in range(2, len(b)):
        o1,h1,l1,c1 = b[i-2]; o3,h3,l3,c3 = b[i]
        if l3 > h1:   out.append(("alta",  h1, l3, i))   # vacuo de alta: zona entre h1 e l3
        elif h3 < l1: out.append(("baixa", h3, l1, i))   # vacuo de baixa: zona entre h3 e l1
    return out
def abertos(b):
    res = []
    for tipo, lo, hi, i in fvgs(b):
        pos = b[i+1:]
        if tipo == "alta":  fechado = any(x[2] <= lo for x in pos)   # preco voltou a preencher
        else:               fechado = any(x[1] >= hi for x in pos)
        if not fechado: res.append((tipo, round(lo,1), round(hi,1), i))
    return res
if __name__ == "__main__":
    b = json.load(open(sys.argv[1])); p = float(sys.argv[2]) if len(sys.argv) > 2 else b[-1][3]
    print("max %.1f  min %.1f  ultimo %.1f" % (max(x[1] for x in b), min(x[2] for x in b), p))
    for t, lo, hi, i in abertos(b):
        print("FVG %-5s %.1f-%.1f (vela %d) distancia ate o meio: %+.0f" % (t, lo, hi, i, (lo+hi)/2 - p))
