# Checklist de análise COMPLETA (usuária, 07/10/2026) — ninguém fica cego em nenhuma vertente

Regra da usuária: "sempre use Wyckoff, Elliott, notícia, eventos, Brent, juros, o painel; você não pode ficar cego em nenhuma vertente."
Vale para TODA entrada e para toda análise de gráfico, em qualquer horário (das 21:00 às 18:00 sempre vale operar; setup principal = notícia/calendário, mas sem notícia a gente se vira com as zonas).
Uma vertente sem dado (ex.: bolsa fechada, ações "paradas" no painel de madrugada) NÃO é pulada em silêncio: registra-se "sem dado: motivo" na linha da lente.

## Quem cobre o quê (esclarecimento da usuária, 07/10/2026)
O **Painel NAS100 Compacto já traz Brent, juros e todas as informações de mercado necessárias** (ES/NQ, VIX, DXY, níveis, sessões, ATR, sentimento, confluência de nível). As vertentes que o painel NÃO cobre e que ficam por conta do Claude em toda análise são: **notícias, eventos, Elliott e Wyckoff** (mais Fibonacci e os OBs do indicador). O gráfico TVC:UKOIL / TVC:US10Y é só complemento opcional para ver estrutura, não substitui a leitura do painel.

## LIMITE DE 2 SCRIPTS VISÍVEIS (usuária, 07/10/2026)
O plano do TradingView só permite 2 scripts ao mesmo tempo. Decisão: **Painel NAS100 Compacto + Structure Volume Profile Setups** ficam ativos. As demais lentes vêm por cálculo próprio a partir das velas (`ui_evaluate`/`data_get_ohlcv`): momentum (`scripts/momentum_ui_evaluate.js`), volume/Wyckoff, Fibonacci, Elliott, zonas de oferta/demanda (última vela contrária antes do impulso) e níveis de sessão. SMC, ST OB, Sweep, WaveTrend e Killzones só são lidos quando a usuária os ligar, ou ligando UM por leitura e restaurando depois.

## As 10 lentes (ler TODAS antes do ticket)
| # | Lente | Como ler (ferramenta) | O que extrair |
|---|---|---|---|
| 1 | **Painel NAS100 Compacto** | `data_get_pine_tables` (study "Painel") | colunas "15m" e "vs abert": juros, Brent, ES/NQ, VIX, DXY; regime M15/H1; níveis PDH/MEIO/OTE/NY00/PDL; Ásia/Londres/NY AM H-L; ATR M5/M15; sentimento. Uso: **confluência**, nunca gatilho; "zona de compra/venda" dele é só proximidade de nível |
| 2 | **Brent (peso ALTO)** | linha "Brent %" do painel (colunas 15m e vs abert); opcional: gráfico `TVC:UKOIL` (restaurar `PEPPERSTONE:NAS100` M5 depois) | direção do dia e dos últimos 15 min. Quer venda → Brent subindo ajuda; quer compra → Brent caindo ajuda. Contra = só setup A+ ou fica fora |
| 3 | **Juros** | linhas Juros10/Juros2/curva do painel; opcional: `TVC:US10Y` | juros subindo pesa no NAS, caindo ajuda |
| 4 | **Notícias** | Seeking Alpha (WebFetch `seekingalpha.com/market-news`), `calendar_db.py since`, `upsert-news`, `mark-checked --name news` | Fed, juros, petróleo, geopolítica, big techs; tom e hora; 2ª fonte para número |
| 5 | **Eventos** | `calendar_db.py gate/brief`, tabela do dia (`docs/tabela-eventos-AAAA-MM-DD.md`), páginas oficiais (federalreserve.gov, bancos regionais) | próximo evento, horário, estrelas, tema; falas só com confirmação de fonte primária; T-5 e fechamento 17:55 |
| 6 | **Zonas do indicador (OB/FVG)** | `data_get_pine_boxes` (study "Smart Money"; "Killzones" para sessões) + screenshot | OBs de demanda/oferta ativos (um OB mitigado some da lista); entrada, alvo e stop conferidos contra eles ANTES do ticket |
| 6b | **ST OB Rejections** (LuxAlgo, adicionado pela usuária 07/10) | `data_get_pine_boxes` (study "Short-Term") | **só REGIÕES de OB de vida curta (nao da sinal de entrada, correcao da usuaria)**; usar como zona de confluencia com o OB do Smart Money; o gatilho continua sendo a rejeicao M5 fechada lida por mim |
| 7 | **Fibonacci** | perna recente nas velas M5/M15 | 38,2/50/61,8/78,6% da perna; confluência com OB |
| 8 | **Elliott** | swings M5/M15 | contagem provável (impulso x A-B-C), alvo da onda, **invalidação escrita**; só lente, nunca gatilho; confiança baixa/média/alta |
| 9 | **Wyckoff + volume** | `data_get_ohlcv` (volume por vela) | fase (acumulação/distribuição), SC/AR/ST/Spring/UTAD/SOS/LPSY; esforço x resultado; repique em volume decrescente = fraco; teste em volume menor = absorção |
| 10 | **Sessões e liquidez** | painel + velas | Ásia/Londres/NY AM H-L (varrida = descartada, aberta = alvo), PDH/PDL, máx/mín do dia; abertura de NY (10:30 BRT): ler primeiro o que NY fez em 5-10 min |

| 11 | **Estrutura de mercado (SMC)** | `data_get_pine_labels` e `data_get_pine_lines` (study "Smart Money") + screenshot | BOS (continuação), CHoCH (1ª quebra contra a tendência = possível virada), EQH/EQL (liquidez), Strong High/Low (extremo protegido que gerou BOS) e Weak High/Low (extremo fraco, alvo provável de varrida). Dizer qual é a estrutura de swing e a interna, e onde está o próximo Weak alvo |

| 12 | **Momentum** (RSI, MACD, estocástico, WaveTrend, divergência) | `scripts/momentum_ui_evaluate.js` colado em `ui_evaluate` (M5 e M15 calculados das velas) | RSI14, MACD hist (esgotando ou acelerando), estocástico 14:3:3 (%K x %D), WaveTrend, divergência RSI/preço; usar para timing e para seguir o fluxo; WaveTrend sozinho não deu vantagem nos dados |

| 13 | **VWAP + faixa de abertura de NY** (adicionado 07/10/2026) | `scripts/vwap_abertura_ui_evaluate.js` colado em `ui_evaluate` (M5). Opcional na tela: indicador `pine/vwaps_ny_dia_extremo.pine` (salvo na conta como "VWAPs NY Dia Extremo") | VWAP de NY (ancora 10:30 BRT), do dia (00:00 ET) e do extremo (minima/maxima do dia) com bandas +-1/+-2 desvios; posicao do preco (acima = compradores no controle; +2 = esticado, nao perseguir; perto do VWAP = zona de valor); ORB15/ORB30 = max/min dos primeiros 15/30 min de NY (rompido ou nao). **Volume do CFD = tick volume: referencia, nao numero exato.** Nao testado como gatilho (so contexto) |

## Como registrar (obrigatório em toda entrada)
No diário (`observacoes` do CSV) e no resumo: uma linha com o veredito de cada lente em ≤ 6 palavras, ex.:
`Painel: confl 0 | Brent: +0,4% a favor da venda | Juros: +1pb contra | Notícia: nada novo | Evento: API 17:30 | OB: oferta 31.265-31.283 | Fibo: 61,8% 31.256 | Elliott: ABC fim, conf. média | Wyckoff: ST vol menor, repique fraco | Sessão: Ásia L varrida`.
Se uma lente discorda do lado da entrada, o texto diz por que a entrada vale mesmo assim, ou a entrada não acontece.

## Regras que continuam valendo
Gatilho = zona do indicador + rejeição M5 FECHADA a favor; stop fora da zona com folga ≥ 1 ATR M5; alvo na PRÓXIMA zona oposta; lote 0,1; stop obrigatório; perda do dia US$ 15; sem martingale; fechar tudo 17:55 TV; conferir o lado do ticket no screenshot; medir degrau de proteção pelo MFE. Varrida pura da Ásia não é gatilho (34% de acerto nos dados).

## Observação sobre limites
- O painel mostra variação, não estrutura; o gráfico do Brent e do US10Y é complemento opcional.
- Elliott e Wyckoff são interpretativos: sempre com confiança e invalidação; divergência entre lentes reduz a confiança, não a esconde.
