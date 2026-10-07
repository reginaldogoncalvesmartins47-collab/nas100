# Qual filtro aumenta o acerto do gatilho "vela M5 de rejeição num extremo"? (07/10/2026)
Script: `python scripts/estudo_filtros_acerto.py` (NAS100 M5 MT5, 02/10/2025-01/05/2026; 1.474 sinais em 150 dias).
Gatilho-proxy: pavio >= 50% da amplitude, amplitude >= 0,8 ATR14, tocando o extremo das últimas 2h; entrada na vela seguinte; stop = extremo do pavio +/- 0,5 ATR; alvo 1,5R; 2h. Equilíbrio do alvo 1,5R = 40% de acerto.
| Filtro | n | Acerto | Média (R) |
|---|---|---|---|
| BASE (só a vela de rejeição) | 1.474 | 40,6% | -0,002 |
| + tendência M15 a favor (EMA20 inclinada) | 282 | **45,4%** | +0,078 (±0,072) |
| + WaveTrend extremo (±30) | 1.118 | 39,8% | -0,014 |
| + WaveTrend cruzou (3 velas) | 51 | 43,1% | +0,038 (±0,171) |
| + RSI extremo (35/65) | 714 | 38,4% | -0,050 |
| + volume > 1,2x média | 606 | 37,0% | -0,091 |
| volume <= 1,2x média | 868 | 43,2% | +0,060 |
| tendência + volume > 1,2x | 139 | 48,2% | +0,142 (±0,102) |
Sessão (base): Ásia 39,4%, Londres 40,3%, NY 42,1%. Lado: venda 42,6%, compra 38,9%.

## Leitura
- A rejeição pura está no ponto de equilíbrio (40,6% vs 40%): sozinha não tem vantagem.
- **Único filtro com ganho visível: tendência do M15 a favor** (+5 pontos de acerto), ~1 erro-padrão (nao conclusivo). Tendência + volume acima da média chegou a 48,2% (n=139, ~1,4 erro-padrão).
- **WaveTrend NÃO ajudou** como filtro do gatilho (extremo: 39,8%; cruzamento: n pequeno). RSI extremo e volume alto isoladamente pioraram.
- Nenhum filtro é estatisticamente forte; amostra sem zonas de OB (proxy). Usar como regra de "confluência de contexto", nao como garantia.
## Regra derivada
Preferir gatilho a favor do regime M15 do painel; contra o regime M15 = só setup A+. WaveTrend = peso baixo (timing de exaustão, sem vantagem comprovada).
