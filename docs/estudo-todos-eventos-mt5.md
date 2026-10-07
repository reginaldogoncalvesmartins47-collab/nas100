# Estudo de TODOS os eventos US (media/alta) x NAS100 M5 do MT5 - 02/10/2026
Dados: 182 eventos US (importancia media/alta) do Investing (endpoints.investing.com, pagina publica, sem chave) -> 1.068 ocorrencias medidas entre 02/10/2025 e 01/05/2026 (124 eventos com barras M5 no MT5). Hora do servidor MT5 = UTC+3 (DST EUA) ou UTC+2 = NY+7h. Scripts: scripts/estudo_todos_eventos.py; dados: data/investing/*.json, data/estudo_todos_eventos*.csv. Metodo: amplitude (max-min) nos primeiros 20 min / media da mesma hora em dias SEM evento (razao); mov. +15 e +60 min = fechamento - fechamento da vela anterior.
LIMITE CENTRAL: muitos eventos saem JUNTOS (08:30 ET = 53 eventos distintos no mesmo horario), entao a reacao NAO se separa por evento: vale por PACOTE/horario. Correlacao surpresa x direcao por evento nao e confiavel (n=5-7, pacotes misturados).
## Ranking por pacote (razao de amplitude; 1,0 = dia normal)
| Pacote | Horario ET | Razao | Amplitude 20 min | Mov. abs +60 min |
| Payroll (NFP + desemprego + salario/hora...) | 08:30 | 3,0x | 148 | 101 |
| Coletiva do Fed (FOMC press conference) | 14:30 | 2,6x | 145 | 103 |
| CPI + CPI nucleo | 08:30 | 2,5-2,6x | 125-130 | 46-67 |
| Varejo (retail sales + nucleo + control) | 08:30 | 2,4x | 118 | 75 |
| Philly Fed + Philly emprego | 08:30 | 1,8x | 88 | 52 |
| PPI + PPI nucleo | 08:30 | 1,7x | 85 | 60 |
| PIB + deflator + core PCE (sai junto) | 08:30 | 1,5-1,6x | 79-87 | 48-52 |
| Decisao do Fed (taxa + comunicado) | 14:00 | 1,6x | 95 | 94 |
| Falas: Waller (n=16) 1,5x; Williams (n=14) 1,4x e +60 min=101; Trump (n=26) 1,4x; Bowman 1,2x; Kashkari/Bostic 1,1x; Daly 0,9x; Powell (4, fora de horario) 0,8x | - | - | - | - |
| Ata do FOMC / Beige Book | 14:00 | 0,9x | 52-54 | 39-67 |
| Seguro-desemprego (quinta, sozinho) | 08:30 | 1,2x | 65 | 41 |
| ISM / JOLTS / confianca (10:00 ET, 31 eventos) | 10:00 | 1,1x | 115 | 80 |
| Baker Hughes (13:00 ET) | 13:00 | 1,1x | 72 | - |
| CFTC (15:30 ET) | 15:30 | 1,0x | 67 | - |
Por dia da semana no slot 08:30 ET: sexta 2,5x, terca 1,9x, quarta 1,8x, quinta 1,4x, segunda 0,95x.
Dias de maior amplitude no slot 08:30 ET: 06/03/26 (payroll -92K: 228 pts), 01/04 (varejo: 184), 11/02 (payroll: 174), 24/10/25 (CPI: 159), 18/12/25 (CPI: 156), 18/03 (PPI: 142).
## Implicacoes para o metodo
1. Eventos que merecem entrada/gestao ativa: payroll, CPI, varejo, coletiva do Fed, decisao do Fed, falas de Waller/Williams/Trump. O resto (CFTC, Baker Hughes, ata, Beige Book, claims sozinho, ISM no dia comum) e ruido: nao ha amplitude acima do normal.
2. Stop precisa caber na amplitude do pacote: payroll/CPI ~130-150 pts em 20 min (escala 25-27k; hoje ~+20%).
3. Coletiva do Fed (14:30 ET) move mais que a decisao (14:00 ET): esperar a coletiva.
4. Para 'viés' por direcao: so olhar a surpresa do PACOTE inteiro (ex.: payroll + salario + desemprego), nao de cada linha.

## FALAS DE DIRIGENTES, inclusive importancia BAIXA (1 estrela) - 214 falas medidas, 02/10/2025-01/05/2026 (scripts/estudo_falas_fed.py; dados data/estudo_falas_fed.csv)
Correcao: o primeiro levantamento so incluiu eventos de importancia media/alta; Logan e outros (1 estrela) ficaram de fora e foram acrescentados aqui. Baseline = mesma hora do servidor em dias sem evento medio/alto nem fala. 'r15' = |mov. +15 min| / |mov.| normal da mesma hora (1,0 = normal).
| Orador | n | hora tipica (servidor) | Razao amplitude | r15 | Mov. abs +60 min |
| Coletiva do FOMC | 5 | 21:30 | 2,60 | 2,36 | 103 |
| Cook (governadora) | 5 | 01:30 | 2,39 | 3,09 | 189 (n pequeno) |
| Waller | 16 | 16:00 | 1,54 | 1,77 | 60 |
| Trump | 26 | 02:00 | 1,44 | 1,52 | 59 |
| Williams (NY Fed) | 14 | 10:00 | 1,41 | 2,12 | 101 |
| Schmid | 7 | 17:00 | 1,35 | 1,28 | 70 |
| Logan (Dallas) | 14 | 02:00 | 1,28 | **0,80** | 48 |
| Collins | 8 | 16:00 | 1,26 | 1,76 | 58 |
| Jefferson | 7 | 02:00 | 1,23 | 1,50 | 65 |
| Bowman | 23 | 17:00 | 1,16 | 1,25 | 63 |
| Kashkari | 8 | 16:00 | 1,15 | 0,92 | 62 |
| Bostic | 16 | 19:30 | 1,08 | 0,78 | 65 |
| Barkin | 15 | 15:00 | 1,05 | 1,04 | 46 |
| Barr | 19 | 19:45 | 0,98 | 1,17 | 55 |
| Goolsbee | 16 | 02:00 | 0,97 | 1,25 | 60 |
| Daly | 9 | 18:30 | 0,91 | 0,64 | 41 |
| Powell (fora de horario) | 4 | 03:00 | 0,84 | 1,15 | 22 |
Leitura: com impacto acima do normal e n razoavel: Waller (16), Williams (14), Trump (26), Collins (8), Jefferson (7). LOGAN: amplitude 1,28x mas o movimento em 15 min e MENOR que o normal (0,80): na amostra, nao ha impacto util (consistente com 01/10: tom duro e preco sem reagir). Bostic/Daly/Goolsbee/Barkin/Barr: sem impacto. Cook: alto mas n=5 e horario de madrugada (verificar). Limites: n 4-26 por orador; hora da fala vem do calendario (inicio programado, nem sempre a hora real da frase); falas de madrugada (02:00 servidor) tem baseline de baixa liquidez.
