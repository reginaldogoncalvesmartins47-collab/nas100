# Compra esticada x perto da base (estudo de 06/10/2026)
Origem: a usuaria achou que a compra 19 (06/10 12:22, stop -US$ 3,50) foi feita com o preco esticado. Script: `python scripts/estudo_esticado.py` (NAS100 M5 MT5, 02/10/2025-01/05/2026; 545 entradas em 122 dias).
Metodo: compra a mercado a cada 30 min na sessao NY AM (09:35-12:35 ET), so com preco acima da EMA20 M15; stop 0,8 ATR15, alvo 1,07 ATR15 (como a compra 19); 60 min. Esticamento = (entrada - minima das ultimas 2h) / ATR15 (proxy do OB de demanda: o OB do indicador nao tem historico).
| Esticamento | n | Acerto | Media por trade |
|---|---|---|---|
| perto (< 2,1 ATR) | 180 | 49% | -0,008 ATR |
| medio (2,1-3,1) | 180 | 46% | -0,058 ATR |
| esticado (> 3,1) | 185 | 43% | -0,026 ATR |
| muito esticado (top 15%, > 4,3) | 82 | 38% | -0,101 ATR |
Ponto de equilibrio: acerto de ~43% (0,8 / 1,87). Leitura: o acerto cai de forma consistente com o esticamento (49 -> 46 -> 43 -> 38%), mas NENHUM grupo tem vantagem (media ~0) e a diferenca nao e estatisticamente forte (a media de -0,10 ATR com n=82 e ~1 erro-padrao; entradas se sobrepoem). Compra 19: ~3,4 ATR (esticado); compra 18: ~1,5 ATR (perto).
Conclusao: a opiniao da usuaria aponta a direcao certa, sem prova. Uso como filtro SUAVE, nao regra dura: esticado (> ~3 ATR M15 acima da base de 2h) exige recuo ao OB ou R:R >= 1,5; muito esticado (> ~4 ATR) nao entra.
