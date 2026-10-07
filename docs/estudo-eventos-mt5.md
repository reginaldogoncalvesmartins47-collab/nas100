# Estudo de eventos com a base do MT5 (NAS100 M5, 02/10/2025 a 01/05/2026) - feito em 02/10/2026
Script: scripts/estudo_eventos_mt5.py (dados dos eventos: Investing; saida: data/estudo_eventos_mt5.csv). Hora do servidor MT5 = NY + 7h. Reacao = fechamento da vela do evento (+5), +10 (=+15 min) e +55 (=+60 min) menos o fechamento da vela anterior. Amplitude = max-min nos primeiros 20 min. Baseline = mesma hora do dia em dias sem evento.
| Evento | n | Amplitude 20 min | Baseline | Razao | Mov. medio abs +15 min | +60 min |
| NFP (payroll) | 5 | 148 pts | 55 | **2,7x** | 70 | 101 |
| CPI a/a | 6 | 130 | 55 | **2,4x** | 79 | 67 |
| FOMC (decisao) | 5 | 95 | 61 | 1,6x | 40 | 94 |
| Core PCE | 6 | 87 | 81 | 1,1x | 45 | 52 |
| ISM industrial | 6 | 108 | 107 | 1,0x | 52 | 79 |
| Seguro-desemprego (claims) | 24 | 65 | 55 | 1,2x | 28 | 41 |
Direcao (surpresa x reacao; n pequeno): CPI abaixo do previsto (5 de 6 vezes) -> NAS100 subiu em media +73 pts em 15 min (4 de 4 com surpresa negativa). NFP: surpresa positiva forte -> +46 em 15 min (n=3); NFP muito fraco (06/03: -92K vs +58K) -> -134 pts em 15 min (dado fraco = queda quando o medo era recessao; em set/26 com Fed apertando, 29K fraco = alta). ISM acima do previsto -> +82 em 15 min (n=3). Claims: sem vantagem (mov. medio 28 pts; 17 quentes -1,2 / 6 frios +14,9). FOMC: todas 'em linha' (surpresa 0), reacao sem direcao consistente (+/-40 a 60 em 15 min).
Limites: n pequeno por evento (5-6, exceto claims); o NFP de 03/04/26 caiu fora (Sexta-feira Santa, sem barras); periodo out/25-abr/26 em 25-27 mil de pontos (amplitudes atuais ~20% maiores); 'surpresa' = atual - previsao do Investing; PCE tem horarios mistos (10:00 e 08:30 ET). Nao e prova, e orientacao.
