# Historico dos eventos de 2 estrelas de 02/10/2026 (fonte: paginas dos eventos no Investing, lidas pela extensao em 02/10 ~13:15 TV)

Pedido da usuaria: ver o historico e como o mercado se comportou nas datas. LIMITE: so consegui os VALORES dos eventos e o fechamento diario do mercado (manchetes); a reacao intradiaria (janela de ~1h apos cada divulgacao) NAO foi medida (historico local de precos so vai ate 19/03/2026; a ferramenta do TradingView so devolve as velas recentes). A partir de hoje gravar a reacao de cada divulgacao com `add-reaction`.

## Baker Hughes - sondas de PETROLEO (14:00 BRT, semanal, sexta). Resultado | previsao
07/08 454|452; 14/08 455|-; 21/08 452|456 (-4); 28/08 447|454 (-7); 04/09 449|447; 11/09 450|449; 18/09 452|451; 25/09 455|453. Hoje: anterior 455. Tendencia: 447 -> 455 em 4 semanas.

## Baker Hughes - TOTAL de sondas EUA (14:00 BRT). Resultado | anterior
07/08 588|588; 14/08 593|588; 21/08 588|593; 28/08 588|588; 04/09 588|588; 11/09 591|588; 18/09 595|591; 25/09 599|595. Hoje: anterior 599 (+4 por semana, 3 semanas).

## CFTC (16:30 BRT, semanal; dado de terca-feira). Posicao liquida de especuladores
- Nasdaq 100: 31/07 +4,9K; 07/08 -14,6K; 14/08 -39,3K; 21/08 -10,4K; 28/08 +10,0K; 04/09 +25,9K; 11/09 +20,9K; 18/09 +33,7K; 25/09 +56,1K (comprado e lotado).
- S&P 500: 07/08 -27,3K; 14/08 +11,3K; 21/08 -10,6K; 28/08 -68,0K; 04/09 -75,9K; 11/09 -76,0K; 18/09 -100,5K; 25/09 -133,2K (vendido, crescendo).
- Petroleo: 31/07 +120,1K... 07/08 +112,4K; 14/08 +99,2K; 21/08 +122,1K; 28/08 +123,4K; 04/09 +129,9K; 11/09 +136,6K; 18/09 +135,9K; 25/09 +141,1K (comprado, crescendo; 31/07 era +81,7K ant.).
- Ouro: anterior +225,9K (historico nao lido).

## Fechamento diario do Nasdaq Composite nas sextas (manchetes; NAO isola o efeito do evento)
21/08 +0,4% (rig 452 vs 456 previsto; semana -2,1%); 28/08 -0,52% (Jackson Hole/Warsh, apostas de alta de juros; rig 447 vs 454); 25/09 +0,5% (otimismo de tech, petroleo cedendo; rig 455 vs 453). 04/09 = payroll (-0,29%). 11/09 e 18/09: manchetes ambiguas (misturadas com quinta-feira), nao usar.
Leitura honesta: nas sextas, o movimento do dia foi explicado por Fed, juros, petroleo e tech, nao pelo rig count. Sem evidencia de que a sonda mova o NAS100 sozinha.

## Reacao do NAS100 (M5) nas divulgacoes das 14:00 BRT - observada no grafico
- **25/09 14:00** (rig 455 vs 453): sem reacao relevante no horario; a alta forte do dia foi ~13:00 (antes do dado); na hora seguinte lateral (~30.600-30.660), alta leve depois. Leitura minha (screenshot): lateral/alta leve. Usuaria: **leve alta**.
- **18/09 14:00** (rig 452 vs 451): a usuaria confirma **leve alta** na tela dela. Minha captura mostrou drift de alta lento (volatilidade baixa) e salto ~15:15; descartei por preco incompativel com a semana, mas a descricao e coerente. Usar a observacao dela.
- 28/08, 21/08, 11/09, 04/09 e anteriores: NAO verificadas (historico M5 do TradingView limitado a ~17/09; pedir print a usuaria).
- Amostra = 2 (ambas leve alta, baixa volatilidade). Hipotese a testar hoje: sondas de petroleo = evento de baixa volatilidade com leve vies de alta no NAS100.
- **11/09 14:00** (rig 450 vs 449): usuaria confirma **leve alta**. 
- **Padrao relatado pela usuaria (11/09, 18/09, 25/09 e "todas que vi"): leve alta, range PEQUENO, movimentacao de ~10-20 minutos.** Implicacao operacional: alvo curto (~30-50 pts), saida por tempo (~20 min apos o dado), nao esticar o take; stop fora do range MICRO (nao do range do dia).

## ESTUDO COM DADOS DO MT5 (arquivo da usuaria: NAS100 M5, 02/10/2025 a 01/05/2026, 40.904 barras; salvo em data/nas100_m5_mt5.csv) - 02/10/2026 14:2x TV
Fuso: hora do servidor MT5 = hora de NY (ET) + 7h (o maior range medio por barra e 16:30 servidor = abertura de NY 09:30 ET). Entao 13:00 ET (Baker Hughes) = 20:00 servidor; 15:30 ET (CFTC) = 22:30 servidor; 08:30 ET (payroll) = 15:30 servidor. Obs.: o horario BRT desses eventos muda quando os EUA saem do horario de verao (3 nov 2026: 13:00 ET = 15:00 BRT).
Metodo: preco = fechamento da vela M5 anterior ao evento; reacao a +5/+15/+30/+60 min; amplitude = max-min nos primeiros 20 min. Baseline = mesmo horario de segunda a quinta.
| | n | amplitude 20min (media/mediana) | %altas +5 | +15 | +30 | +60 |
| Baker Hughes sexta 13:00 ET | 29 | 77,5 / 74,5 pts | 55% | 41% | 38% | 55% |
| baseline seg-qui 13:00 ET | 115 | 66,2 / 57,8 | 52% | 50% | 51% | 57% |
| CFTC sexta 15:30 ET | 29 | 67,0 / 62,9 | 41% | 38% | 48% | 41% |
| baseline seg-qui 15:30 ET | 114 | 67,5 / 55,7 | 47% | 55% | 50% | 61% |
Leitura honesta: (1) a "leve alta" que a usuaria viu em 3 sextas de setembro NAO se confirma em 29 sextas (out/25-abr/26): em +15/+30 min so 41%/38% sobem. (2) Baker Hughes: amplitude um pouco maior que o baseline (mediana 74 vs 58 pts), sem direcao. (3) CFTC: deriva levemente negativa na 1h (-9 pts vs +9 do baseline) mas com ruido grande (n=29, nao significativo). (4) Nivel de preco em out/25-mai/26 era ~25-27k; hoje ~30,8k (escala ~+20%): amplitudes de hoje tendem a ser maiores. (5) O range tipico de 20 min nesse horario (~65-75 pts, ~80-90 em 30k) e MAIOR que um stop de 36 pts: stops curtos nesse horario tendem a ser varridos (como o trade 14).
