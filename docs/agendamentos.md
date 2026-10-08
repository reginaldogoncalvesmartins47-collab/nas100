# Agendamentos obrigatorios (recriar em TODA sessao nova) - criado 07/10/2026
CronCreate e session-only: some quando o Claude fecha e expira em 7 dias. Por isso, NO INICIO DE TODA SESSAO o Claude cria estes jobs (CronList antes, para nao duplicar) e diz a usuaria a lista criada. Relogio: o cron usa o relogio do PC; o PC fica alguns minutos ATRAS do TradingView (docs/estado-e-retomada.md secao 4).
Pre-requisito: TradingView aberto com a porta de depuracao (docs/estado-e-retomada.md secao 12) e MCP tradingview conectado.

## 1. GEX automatico (painel 'Painel NAS100 Compacto', inputs in_11 flip, in_12 muro call, in_13 muro put)
| cron (PC) | quando | aviso a usuaria |
|---|---|---|
| `17 9 * * 1-5` | pre-abertura (open interest novo da OCC) | SEMPRE: 1 linha com regime e muros do dia |
| `50 10,15 * * 1-5` | pregao NY | so se regime mudou ou preco < 20 pts de um muro |
| `20 12,14 * * 1-5` | pregao NY | idem |
| `7 21 * * 0-4` | abertura da Asia | so se preco < 20 pts de um muro |
Prompt padrao: "GEX automatico: (1) quote_get PEPPERSTONE:NAS100; (2) `python scripts/gex_para_painel.py <preco>`; (3) indicator_set_inputs no painel (entity via chart_get_state) in_11=flip, in_12=muro call, in_13=muro put; (4) registrar em journal/gex_log.csv (data, hora BRT, preco, regime, flip, call, put); (5) aviso conforme a tabela. Nao mexer em mais nada."
Leitura simples para a usuaria: regime positivo = mercado mais calmo (preco volta ao meio, muros seguram); negativo = movimentos esticam (rompimentos seguem, stop curto sofre). Muro de call = teto; muro de put = piso. Importancia ainda NAO testada (medir pelo gex_log em 2-4 semanas).

## 2. Briefing de mesa (docs/briefing-horario.md)
`13 6 * * 1-5` (06:17 TV), `21 8 * * 1-5` (08:25 TV), `27 10-16 * * 1-5` (NY, de hora em hora). Prompt: "rodar docs/briefing-horario.md; direcao obrigatoria ALTA/QUEDA; sem pontas soltas; vies vivo; registrar em journal/briefings/AAAA-MM-DD.md".

## 3. Eventos do dia (criar DEPOIS de coletar o calendario da manha)
Um cron one-shot por horario distinto: cron = hora do evento - 15 min no relogio do PC (= T-5 do TV com folga). Prompt: "entrada 5 min antes: ficha pre-entrada (docs/ficha-pre-entrada.md), protocolo de tema, vies, ticket com stop e alvo, screenshot, registrar; avisar se nao abrir ordem". Preencher tambem o campo 'Eventos de hoje, BRT' do painel (input in_8, 'HH:MM, HH:MM').

## 4. Fechamento
`45 17 * * 1-5` (~17:55 TV): fechar toda posicao do Claude a mercado e registrar (diario, resumo-diario.md, banco).

## 5. Verificacao de fontes do painel (enquanto houver pendencia de atraso)
Uma vez por dia no pregao (~10:40 BRT): medir a ultima vela de TVC:VIX, BATS (gigantes, SMH, MU), TVC:UKOIL, TVC:DXY contra OANDA:EURUSD; trocar no painel so o que estiver atrasado.

## 6. VIGIA DO GRAFICO (usuaria, 08/10/2026: "fica de olho no grafico, agende para vc sempre estar atenta")
| cron (relogio do PC) | quando | o que faz |
|---|---|---|
| `*/5 0-17 * * 1-5` | seg-sex 00:00 a 17:55 | a cada 5 min: quote + painel; gerir posicao; evento em <= 15 min -> ficha + T-5; senao Passo 0 + Setup 2 (so com ficha e gate LIBERADO) |
| `*/5 19-23 * * 0-4` | dom-qui 19:00 a 23:55 | idem; 19h-21h e a janela mais morta (exigir gatilho fechado) |
| `45 17 * * 1-5` | ~17:55 TV | FECHAMENTO: fechar posicoes, diario, resumo-diario, aviso a usuaria |
Regra do vigia: falar SO se algo mudou (entrada, saida, veto relevante, risco, falha de ferramenta); senao 1 linha. Toda entrada vetada -> journal/vetos.csv. Sessao-only: recriar a cada sessao nova (expira em 7 dias). Custo: cada disparo gasta uso do plano; se o limite apertar, passar para */10.
- GEX: teste forward em scripts/gex_teste.py (rodar no fim de cada dia ou semana; so conclui com >= 20 dias; sem historico gratis do GEX). 08/10: N=1 (muro de put 31012 de 07/10 rompeu em 60 min).

## 7. MONITOR DE NOTICIAS (usuaria, 08/10/2026: "so foi ligada hoje as 13, pq nao ligou antes?")
Deve ligar NO INICIO DE TODA SESSAO (CLAUDE.md, bloco "AO INICIAR"). Ferramenta Monitor: `cd <projeto> && python -u scripts/noticias_monitor.py`, timeout 1800000 (30 min, limite da ferramenta). Rearmar a cada 29 min com `CronCreate */29 * * * *` (prompt: "se o Monitor de noticias nao estiver ativo, rearmar"). Consulta a cada 30 s: Fed press, Bloomberg (politica/mercados/economia RSS publicos), Seeking Alpha, Google News (3 buscas). Limites: polling, atraso das fontes gratis; nao vale como gatilho antecipado (docs/medicao-noticias.md). Falha de 08/10: so foi ligado as 13:57 BRT; o Waller (05:30) e o seguro-desemprego (09:30) passaram sem monitor.
