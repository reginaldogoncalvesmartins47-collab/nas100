# Motor de decisao do Claude (definido com a usuaria em 07/10/2026) - FONTE UNICA DO "O QUE OPERAR"
Onde houver conflito com texto antigo sobre O QUE operar, vale este arquivo. Regras de seguranca do CLAUDE.md continuam valendo (stop obrigatorio no ticket, lote 0,1, sem martingale, fechar 17:55 TV, real so apos `ready` + autorizacao escrita, demo primeiro).

## Decisoes da usuaria (07/10/2026)
- **Sem limite de numero de trades.** (Na demo a perda do dia so avisa e registra "no real teria parado".)
- **Dois setups, nesta prioridade:** (1) EVENTOS e NOTICIAS; (2) quando nenhum evento for bom: GRAFICO PURO = painel + SETUP DE REGIOES.
- **ORB NAO** (a usuaria nao quer, apesar do backtest em docs/setup-sem-noticias.md).
- O Claude opera sozinho na demo, decide e assina; a usuaria acompanha. Entradas dela = "entrada da usuaria", fora do placar do Claude.

## ANTES DE QUALQUER ORDEM: preencher docs/ficha-pre-entrada.md (15 variaveis, vetos). Sem ficha, sem ordem.

## Passo 0 - LEITURA DO MOMENTO (antes de QUALQUER entrada; licao de 07/10)
Tendencia do dia NAO e motivo de entrada. Responder por escrito, em 4 linhas:
1. **Esticado?** preco x VWAP NY e bandas (scripts/vwap_abertura_ui_evaluate.js). Perto de +-2 desvios = nao perseguir; esperar retorno.
2. **Liquidez:** maximas/minimas de Asia, Londres, NY AM, PDH/PDL: varrida (descartada) ou aberta (alvo). Varrida + volta = possivel reversao: nao entrar a favor do movimento que acabou de varrer.
3. **Abertura de NY (10:30 BRT):** nos primeiros 15 min so ler (spike, varrida, direcao); entrada so depois, com gatilho (docs/estudo-abertura-ny.md).
4. **Momentum M15/M5:** esgotado (estocastico extremo, divergencia) ou acelerando (scripts/momentum_ui_evaluate.js).
Se o momento contradiz a entrada: nao entra, ou entra so com gatilho fechado na regiao e diz por que.

## Setup 1 - EVENTOS e NOTICIAS
- Regra inquebravel do calendario (CLAUDE.md): toda noticia tem analise propria, entrada a mercado em T-5 TV no lado do vies, stop/alvo no ticket.
- Peso pelo estudo (docs/estudo-todos-eventos-mt5.md): ALTO = payroll, CPI, varejo, decisao e coletiva do Fed, falas de Waller/Williams/Trump; BAIXO (ruido, amplitude <= 1x) = ata do FOMC, CFTC, Baker Hughes, claims sozinho, falas de Logan/Bostic/Daly. Evento de peso baixo: entrada minima e protecao rapida; o vies vem do MOMENTO + painel, nao da manchete.
- Noticia fora do calendario (Seeking Alpha + 2a fonte): so opera se mudar juros/Brent/DXY no painel; nunca perseguir manchete.

## Setup 2 - GRAFICO PURO (sem evento bom): painel + SETUP DE REGIOES
Regra confirmada pela usuaria em 02/10 (docs/setup-sem-noticias.md, secao SETUP DE REGIOES), com o Passo 0 antes:
1. Regiao = OB ou FVG (oferta = venda, demanda = compra). Fonte: indicador "Structure VP + SMC" na tela (Structure VP + OB/FVG com regras do LuxAlgo; ler com data_get_pine_boxes/labels) e/ou scripts/snapshot_ui_evaluate.js (FVGs abertos calculados das velas). Plano do TradingView = 2 indicadores visiveis: "Painel NAS100 Compacto" (Semaforo v4) + "Structure VP + SMC". Melhor resultado testado: entrada no MEIO do FVG a favor da estrutura interna (+0,26R, 553 trades, treino e teste iguais; nao confirmado ao vivo).
2. Painel "Painel NAS100 Compacto" (Semaforo v4) a favor ou neutro; contra = so A+ e dizer por que.
3. Gatilho: preco na regiao + rejeicao de pavio M5 + vela FECHA de volta sem romper a regiao. Esperar fechar.
4. Stop fora da regiao + folga de ATR; alvo = proxima regiao/liquidez aberta; zero a zero com +50% do caminho.
5. Diario proprio: journal/diario_setup_regioes.csv (avaliar com >= 25 trades).

## Rotina autonoma (recriar a cada sessao: CronCreate e session-only)
- Manha: calendario completo (docs/calendario-regra-e-coleta.md), tabela do dia, um cron por evento (T-15 no relogio do PC).
- Durante o mercado (21:00-17:55): ciclo de 5 em 5 min: Passo 0 -> evento proximo? (Setup 1) -> senao regiao proxima? (Setup 2) -> entra, gere ou passa -> registra -> uma linha para a usuaria.
- 17:55 TV: fechar tudo. Fim do dia: placar por setup (Claude x usuaria).
