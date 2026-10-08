# Backtest da AVALIACAO DAS ZONAS (Structure VP + SMC) via PineTS - 07/10/2026
Metodo: o proprio Pine (pine/structure_vp_smc.pine) rodado no PineTS (npm `pinets`, AGPL, LuxAlgo) sobre as ULTIMAS 24.000 velas M5 do MT5 (~83 dias, ate 01/05/2026). Pasta tools/pinets-lab (node rodar_zonas.mjs) + scripts/backtest_zonas_pinets.py. Copia de laboratorio lab2.pine = script com a tabela trocada por plots por barra e `syminfo.mintick`=0.1.
Evento = 1o toque numa zona (5.031 eventos: 2.499 oferta/venda, 2.532 demanda/compra). Stop = lado oposto da zona + 0,5 ATR; alvo 1R ou 1,5R; horizonte 36 barras; stop primeiro na mesma vela; SEM custo/spread.
## Resultado
| Variante | BOA 5-7 | MEDIA 3-4 | FRACA 0-2 | Todas |
|---|---|---|---|---|
| A (limite na borda, usa a nota da barra do toque = OLHA ADIANTE) alvo 1R | +0,43R (n=1019) | +0,36R (n=3353) | +0,10R (n=659) | +0,34R |
| **B (a mercado na abertura da barra seguinte, sem olhar adiante) alvo 1R** | **+0,00R** | **-0,01R** | **-0,05R** | **-0,01R** |
| B alvo 1,5R | -0,04R | -0,02R | -0,06R | -0,03R |
Erro padrao ~0,03-0,04R por faixa. Por criterio (B, alvo 1R): nenhum separa trade bom de ruim (diferenca sim x nao entre -0,06 e +0,06 com margem +-0,05 a 0,08): estrutura a favor +0,06, 1o toque +0,05, resto ~0.
## Conclusao honesta
1. A variante A parece lucrativa (+0,34R) so por vies de olhar adiante (a vela do toque ja mostra o que vem). Nao vale.
2. Sem olhar adiante (B), **a zona (OB/FVG) sozinha NAO tem vantagem (~0R antes de custo)** e **a nota 0-7 NAO distingue** BOA de FRACA (diferenca +0,05R, dentro do erro). Com spread de 1,5-2 pts fica negativo.
3. Logo: a tabela de avaliacao serve como CHECKLIST/leitura (organiza o que olhar), nao como filtro validado. O gatilho (rejeicao de pavio M5 fechada), o momento, o macro e os eventos continuam sendo o que decide; zona nao e motivo de entrada sozinha.
4. Limites: ~83 dias, um regime, entrada simplificada (sem gatilho M5, sem macro), M5 sem tick. Um estudo com gatilho de rejeicao e filtro de horario/evento pode ser feito; o resultado so vale com amostra grande e sem olhar adiante.
## PineTS - o que aprendi
Roda scripts Pine reais com box/line/label/table/UDT; 24.000 barras = ~140 s. Precisa: candles com tempo UTC REAL (converter hora do servidor MT5: NY+7h) para funcionarem hour(time,"America/New_York") etc.; `syminfo.mintick` nao existe (usar 0.1); `request.security` com timeframe vindo de `switch` falhou (timeframe vazio) - remover/substituir no laboratorio.
