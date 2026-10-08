# Volume/amplitude por hora (medido em 08/10/2026) e avaliacao do Fincept

## 1. Volume e amplitude do NAS100 por hora (PEPPERSTONE:NAS100 M5, mesma fonte do painel)
Amostra: SO 2 dias carregados no grafico (420 velas M5, 06/10 14:45 UTC a 08/10 03:40 UTC). Volume = tick volume da Pepperstone. Hora = Brasilia (= hora de NY + 1h no horario de verao dos EUA). Mediana por vela M5.
| Hora BRT | Volume | Amplitude (pts) |
|---|---|---|
| 19-20h (abertura) | 733-818 | 10 |
| 21-22h | ~1.780 | 15 |
| 23h | 1.606 | 15,6 |
| 00h | 1.286 | 12 |
| 01h (mais fraca da madrugada) | 1.051 | 8,3 |
| 02-03h | 1.370-1.390 | 11-14 |
| 04-09h | 1.790-2.120 | 16-26 |
| 10-11h (abertura NY) | 2.550-2.580 | 33-43 |
| 12-16h | 2.000-2.380 | 14-21 |
| 17h | 734 | 8,5 |
Conclusoes (usuaria, 08/10: "nao suponha nada... a abertura das 19h nao tem volume"):
- A janela 19h-21h tem ~40% do volume da Asia seguinte e < 1/3 do de NY: e a mais morta do dia (confirmado nos 2 dias). Nao dar peso a movimento dessa janela.
- Asia (21h em diante) e "normal para Asia", nao "sem volume": 08/10 00:37, ultimas 36 velas = vol 1.695 e amplitude 15,1 vs 1.780/15 das mesmas horas.
- Erro corrigido: o Claude disse "mercado sem volume" sem medir. REGRA: nunca afirmar volume/liquidez sem numero; medir antes (ui_evaluate nas velas do grafico; ver scripts/snapshot_ui_evaluate.js para ler `bars()`).
- Limite: 2 dias. Para base maior, carregar mais historico no grafico (rolar para tras) ou usar amplitude do estudo de 2 anos (docs/estudo-sessoes.md; CFD Dukascopy: mediana M5 Asia 21-24h 23,1 pts / 00-03h 17,2 / Londres 21,0 / NY AM 44,2 nos ultimos 120 dias).
## 2. Painel: como ler juros (para nao confundir)
USB10YUSD/USB02YUSD da lista do TV sao PRECO do titulo: preco caindo = juro SUBINDO (o painel inverte certo). O painel marca juros so acima de 3 pb no dia (1,5 pb em 15 min); abaixo disso = neutro. VIX fica "sem dado" fora do horario das acoes (10:30-17:00 BRT). DXY so conta acima de 0,15% no dia.
## 3. Fincept Terminal (testado 07-08/10/2026, ja DESINSTALADO)
- Oficial v4.5.0 (Fincept-Corporation, AGPL, instalador nao assinado). Fork unal-ai: 0 estrelas, v3.1.1, nao usar. kadeconsole: repositorio inexistente (404), nao usar. bbterm-tui: sem sinal de malicia no codigo, mas so acoes/SEC/Google News por ticker.
- Fincept: leitor de 54 feeds RSS publicos (CNBC, Guardian, Nikkei, DW, NYT, MarketWatch, BBC) com marcacao de ativo/sentimento; MARKETS atualiza a cada 10 min (AUTO 10M); sem calendario economico visto; AI Chat gasta creditos do servico (349 CR) e envia texto a eles; nao tem API para o Claude. NAO resolve velocidade de noticia; nao reinstalar sem motivo novo.
- Nao exploradas: DASHBOARD, EQUITY, QUANT LAB, NODES, ALGO, QUANTLIB.
- Medicao de atraso das fontes gratis: docs/medicao-noticias.md (coleta interrompida pelo sistema por memoria em 07/10 22:45 BRT; reiniciar com `python -I scripts/medir_noticias.py coletar 2 1200`).
