"""Calcula os niveis de GEX (QQQ, via ANALISTA-MACRO/scraper/gex.py) e converte para NAS100 CFD.
Uso: python scripts/gex_para_painel.py <preco_NAS100_agora>
Saida: valores para preencher no painel (inputs in_11 flip, in_12 muro call, in_13 muro put) com indicator_set_inputs."""
import sys; sys.path.insert(0, r"C:\Users\User\Desktop\ANALISTA-MACRO\scraper")
import gex
nas = float(sys.argv[1]); r = gex.calcular_gex()
if not r: sys.exit("GEX indisponivel (CBOE)")
k = nas / r["spot"]
print(f"QQQ {r['spot']:.2f} | regime: {r['regime']} | fator NAS100/QQQ = {k:.3f}")
print(f"in_11 (flip) = {round(r['nivel_flip']*k) if r['nivel_flip'] else 0} | in_12 (muro call) = {round(r['muro_call']['strike']*k)} | in_13 (muro put) = {round(r['muro_put']['strike']*k)}")
