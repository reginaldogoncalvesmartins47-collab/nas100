# Projeto NAS100 - copiloto de trade com TradingView

Contexto para o Claude Code. Leia `docs/` antes de agir.

## >>> AO INICIAR QUALQUER SESSAO (obrigatorio, sem a usuaria pedir): (1) conferir o MCP tradingview (tv_health_check; se falhar, reabrir o TradingView com a porta 9222: docs/estado-e-retomada.md secao 12); (2) CronList e criar os agendamentos de `docs/agendamentos.md` (GEX automatico, briefing, fechamento, VIGIA DO GRAFICO de 5 min, eventos depois do calendario) E ligar o MONITOR DE NOTICIAS (ferramenta Monitor, comando `python -u scripts/noticias_monitor.py`, timeout 1800000; ele expira a cada 30 min: criar um CronCreate recorrente `*/29 * * * *` para rearmar enquanto a sessao estiver aberta); (3) dizer a usuaria a lista criada. Os crons somem quando o Claude fecha: em outro PC ou sessao nova eles NAO existem ate serem recriados. <<<

## >>> FERRAMENTAS QUE O CLAUDE DEVE USAR POR CONTA PROPRIA (a usuaria nao precisa lembrar; sessao nova nao lembra, so os arquivos): antes de QUALQUER entrada ou analise de entrada -> (1) `docs/ficha-pre-entrada.md` (15 variaveis + 8 perguntas); (2) `scripts/snapshot_ui_evaluate.js` no ui_evaluate (momento, liquidez, estrutura, FVGs, momentum, vela); (3) painel + "Structure VP + SMC" via data_get_pine_tables/boxes; (4) **base estatistica**: `bash scripts/edge.sh query/report ... --symbol USATECH` (Edge Stats local, N e IC; N<30 ou IC com 50% = sem vantagem; docs/edge-stats-local.md); (5) conceito em duvida -> MCP `luxalgo` (library_search/library_get_concept; precisa aprovar o servidor na sessao). Honestidade: zona OB/FVG e nota 0-7 NAO tem vantagem comprovada (docs/estudo-zonas-pinets.md). Se uma ferramenta nao estiver disponivel, dizer "sem dado: motivo", nunca pular em silencio. <<<

## >>> MOTOR DE DECISAO (07/10/2026): `docs/motor-de-decisao.md` define O QUE o Claude opera (eventos/noticias; sem evento bom = painel + setup de regioes; sem ORB; sem limite de trades; Passo 0 = leitura do momento). Vale acima de textos antigos sobre setups. <<<

## >>> RETOMADA: LEIA PRIMEIRO (sessao nova nao lembra da conversa; tudo importante esta NA PASTA) <<<
1. `docs/estado-e-retomada.md` = estado atual, o que a usuaria decidiu em 01/10/2026, rotina diaria, agenda a recriar, armadilhas das ferramentas, pendencias.
2. Estrategia atual = SO NOTICIAS (calendario) em demo, com painel de contexto no grafico e briefing de mesa agendado. Regras: secoes "CALENDARIO: REGRA INQUEBRAVEL", "ROTINA DIARIA DO CALENDARIO", "PROTOCOLO DE TEMA", "PROTECAO DO LUCRO", "FECHAR ANTES DAS 18H" e "VIES VIVO" mais abaixo; detalhes em `docs/calendario-regra-e-coleta.md`, `docs/playbook-noticias.md`, `docs/gestao-saida.md`, `docs/briefing-horario.md`, `docs/enciclopedia-noticias.md`, `docs/analise-dia-2026-10-01.md`.
3. Onde houver conflito entre texto antigo (rules.json, docs de 'regioes/gatilho M5', 'treino nao trava por gate') e estas secoes novas, VALEM AS NOVAS (a usuaria quer auditoria das regras: ver pendencias).

## Objetivo
Tudo o que a usuaria decidiu esta em `docs/decisoes-alinhadas.md` (leia primeiro).
Ajudar o usuario a operar o NAS100 (PEPPERSTONE:NAS100): ler o grafico no TradingView, analisar cenario
(macro + liquidez) e OPERAR: o Claude executa as ordens (com stop e alvo) e a usuaria nao clica. Primeiro em demo (Paper Trading), depois real.

## A usuaria e a prioridade
A usuaria NAO e tecnica e a prioridade dela e o lucro (docs/decisoes-e-objetivo.md). O Claude decide os parametros tecnicos dentro
dos limites (tune), explica em portugues simples e pergunta so decisoes de negocio/risco. Lucro NUNCA justifica afrouxar limites de
capital, stop obrigatorio ou o gate do modo real. Veredito para a conta real: `python scripts/calendar_db.py ready`.

## Descobrir antes de perguntar (docs/descoberta.md)
O Claude NAO fica travado esperando a usuaria: descobre sozinho o Paper Trading (saldo, tamanho, valor do ponto, historico), as ferramentas
do MCP e os scripts/indicadores dela, e grava com `add-fact`. So pergunta, em lote, o que apenas ela sabe. Se uma ferramenta falhar,
registra e segue.

## Regras que valem sempre
- Conta real pequena (US$ 30). Unico limite dado por ela: pode perder ate 'uns US$ 15' no total (incerto; antes US$ 10; confirmar). Risco por trade e perda do dia NAO foram definidos por ela (docs/regras-risco.md): nao inventar limites.
- **O Claude executa as ordens; a usuaria nao clica** (decisao dela, docs/execucao.md). Treino (Paper Trading): autorizado.
  Conta real: so depois de `ready` cumprido + autorizacao escrita da usuaria dada UMA vez (nao por trade) + stop/alvo como
  ordens na corretora + limites de capital ligados. Toda ordem nasce com stop e alvo.
- Nao prometer resultado. Dizer quando nao ha setup. Resultados de backtest nao valem como prova.
- Nao inventar dados de preco/volume: se o dado nao estiver disponivel, dizer.
- Nao tocar em abas de corretora/banco ao usar o navegador.

## Metodo (resumo, detalhes em `docs/metodo.md`)
- Direcao macro (vies) e do Claude: analista fundamentalista do NAS100. Constroi o vies sozinho (Brent, juros, DXY, ES, VIX, big techs, calendario, noticias, geopolitica, sentimento), justifica em portugues simples e diz "sem vies/sem trade" quando nao houver. A usuaria pode revisar; o painel dela e uma fonte a mais.
- Entrada: regiao pontuada (liquidez + Fibo H1 + oferta/demanda) e o GATILHO e o mercado em M5: o preco chega na regiao, mostra
  rejeicao de pavio a favor do vies e o candle fecha sem romper a regiao (`entry-check`). Esperar o candle FECHAR; nao antecipar.
- Sem janela de horario fixa: o sistema trabalha enquanto a usuaria o mantiver ligado (mercado aberto). Acompanhar o limite de uso do plano.

## Antes de qualquer entrada (ordem)
1. calendario do dia (Investing, pela extensao) -> 2. noticias na janela (dom/seg desde sexta 16h BRT; ter-sex 24h)
-> 3. feriados globais, eventos fora do calendario e plano antecipado -> 4. leitura RACIOCINADA dos pares em H1/H4
-> 5. sentimento do mercado (2+ fontes) -> 6. `python scripts/calendar_db.py gate` = LIBERADO -> so entao regiao com nota + reacao do mercado + RR + risco.
Se o gate estiver BLOQUEADO: a prioridade e concluir a lista de pendencias, na ordem (sem parar, sem pedir permissao
para fazer o dever de casa; so perguntar o que apenas a usuaria sabe). Sem trava de horario. Noticias: so checagem
incremental (`since`). Leitura de par sem mudanca: `renew-read`. Antes de evento importante: plano com direcao (compra/venda).
Nunca perseguir a manchete. Nao usar noticia fora da janela. Nao aplicar correlacao mecanica.

## Modos e saida
- **GATE OBRIGATORIO EM TODA SESSAO, INCLUSIVE NA DEMO (decisao da usuaria, 30/09/2026):** nao abrir ordem sem `gate` = LIBERADO.
  Verificar tudo primeiro (checklist acima); so depois analisar com liberdade, como gestor grande de operacoes especializado em NAS100
  (pode operar os dois lados, recuo dentro da tendencia, alvo no proximo suporte/liquidez). Isso substitui o antigo "treino nao trava por gate".
  Ordem so pelo ticket completo (Shift+T) com stop e alvo antes de confirmar (docs: add-fact `order_procedure_correct`).
- Treino (demo): nota, perda do dia e corte total so avisam e registram 'no real teria parado'. Vale sempre: stop obrigatorio (definido pelo mercado, nao pelo dinheiro). Tamanho 0,1.
- Real: so depois de resultado positivo em amostra grande; gate LIBERADO obrigatorio.
- Todo trade: stop obrigatorio, plano de saida definido antes (docs/gestao-saida.md), registrado em `trades` (MFE, devolvido).
- Stop e alvo ficam como ordens no broker; o Claude ajusta nas checagens, nunca substitui o stop.

## Estilo da usuaria
Ela opera e le rejeicao de pavio em M5. O Claude entende pelos valores de open/high/low/close das velas M5 (nao precisa enxergar o grafico).
Tempos: macro/vies H1 e H4; regioes Fibo H1 (+ refino M15); execucao e saida M5.
Usar `path --o --h --l --c` e `wick`. Saida: alvo = regiao de oferta/demanda; acompanhar o caminho (`path`).

## Meta diaria (docs/meta-diaria.md)
Meta da usuaria: US$ 25-30 POR DIA, sem teto. Persegue-se escolhendo melhores trades, NUNCA arriscando mais: sem martingale (lote nao sobe apos perda),
sem entrada sem gatilho, sem afrouxar stop. Apos bater a meta: proteger o caixa (piso de 50% do melhor ponto do dia). `daily` mostra o dia e o historico.

Revisao semanal: `review` mostra os dias e sugere ajustar a EXPECTATIVA com dados (docs/revisao-semanal.md); nunca o risco para alcanca-la.

## Choque de mercado (docs/choque-de-mercado.md)
Gap, vela enorme ou FVG => `shock` abre CHOQUE e vence o vies. PRIMEIRA tarefa, rapida (~5 min): entender o que esta
acontecendo (`since`, noticias, pares), `shock-diagnose`, redefinir o vies (`bias --set`). So depois o resto do gate.
Trades abertos: revisar stop/protecao imediatamente. Sem limite de numero de trades (a perda do dia e o corte total contem).

## Auto-ajuste (docs/auto-ajuste.md)
O Claude pode ajustar parametros de hipotese com `tune` (evidencia minima, um por vez, historico, revert; real exige aprovacao
da usuaria). NUNCA ajustar limites de capital, stop obrigatorio, gate do modo real, regras de data/fonte/janela das noticias.

## Diario (obrigatorio)
A cada trade aberto/fechado e ao fim do dia: `journal/diario_trades.csv` (saldo antes/depois, ganho, perda, status) + `journal/resumo-diario.md` (saldo inicial, ganhou, perdeu, saldo final) + `open-trade`/`close-trade` no banco. Pedido da usuaria em 30/09/2026.

## Arquivos
- `pine/` scripts Pine (TradingView). `nas100_liquidez_v2.pine` e o atual; nao testado ate o momento.
- `docs/` metodo, liquidez e regioes, fluxo de analise, risco, setup do MCP, roadmap.
- `rules.json` regras do metodo em formato de maquina (rascunho, hipoteses).
- `journal/` diario de trades (CSV).

## Estado
Ver `docs/roadmap.md`.

## CALENDARIO: REGRA INQUEBRAVEL (usuaria, 01/10/2026)
- TODA noticia do calendario (todas as estrelas, discursos do Fed, leiloes, balanco do Fed, payroll, tudo) recebe uma ENTRADA A MERCADO 5 MIN ANTES, no lado do vies, com stop e alvo no ticket. Excecao UNICA: ja existe posicao ativa no MESMO lado (ai so gerir). Se o vies virou, fecha a oposta e entra.
- CADA NOTICIA TEM ANALISE PROPRIA, mesmo no mesmo horario (usuaria, 01/10/2026: "agrupar por horario NAO pode acontecer"). Para CADA linha do calendario: abrir a PAGINA DO EVENTO no Investing (historico atual/projecao/anterior), protocolo de tema, vies proprio e registro proprio no placar. Execucao: uma posicao por lado; se os vies do mesmo horario concordam, e uma ordem so (ja ha ordem ativa); se divergem, decidir pelo evento de maior peso/estrelas e registrar a divergencia. Falha em coletar o calendario = falha minha, nao desculpa.
- NA RESPOSTA TAMBEM: nunca apresentar dois eventos do mesmo horario como um bloco so. Sempre um bloco por evento (nome, estrelas, projecao/anterior, tema, ultima vez, vies proprio, impacto), mesmo quando a ordem e uma so. Evento de fala (ex.: Logan) e SEPARADO do dado do mesmo horario. Erro de 02/10/2026: misturei Logan com as encomendas a industria.
- Rotina de MANHA (antes de qualquer analise): (1) ler a tabela COMPLETA do Investing via javascript_tool (todas as linhas, estrelas pelos icones, projecao/anterior; ver memoria reference-investing-calendario-js); (2) gravar no banco; (3) CronCreate de UMA entrada em T-5 para cada horario distinto; (4) conferir CronList contra a tabela e dizer a usuaria a lista dos horarios agendados.
- No horario: a entrada ocorre; se NAO foi aberta ordem (erro de interface, sem sessao), AVISAR na hora que falhou e por que, nunca em silencio.
- Verificacao a cada entrada: screenshot do Paper Trading mostrando a posicao com TP/SL.
- Ao fim do dia: lista de eventos x entradas feitas x faltantes, no resumo-diario.md.
- Detalhes e codigo da coleta: docs/calendario-regra-e-coleta.md (leia antes de coletar o calendario).

## PROTECAO DO LUCRO (usuaria, 01/10/2026)
Trade no lucro nao pode virar prejuizo por descuido: degraus (zero a zero a >=50% do alvo; travar ~40% a >=75%), pre-noticia com lucro >= ~30 pts => proteger/inverter. ANTES de qualquer mudanca (stop, parcial, saida) analisar o cenario geral (juros, Brent, noticias 30 min, proximo evento, estrutura) e registrar o motivo. Detalhes: docs/gestao-saida.md. Nunca afastar stop nem aumentar lote.

## PROTOCOLO DE TEMA ANTES DO VIES (usuaria, 01/10/2026)
Prever e entrar antecipado (T-5) SIM, mas o vies so depois de: (1) descobrir o TEMA do evento; (2) quando esse tema foi abordado pela ultima vez; (3) como o mercado se comportou; (4) o que mudou desde entao; (5) vies+confianca+invalidacao com fontes. Tema fora de juros/inflacao/emprego => vies neutro. Detalhes: docs/playbook-noticias.md. Nunca presumir "hawkish de manual".

## ROTINA DIARIA DO CALENDARIO (usuaria, 01/10/2026) - ver docs/calendario-regra-e-coleta.md
Todo dia: Investing -> salvar todos os eventos do NAS100 com horario -> TABELA DO DIA (hora, evento, estrelas, atual, projecao, anterior, link do historico) -> pesquisar o historico e analisar o vies (alta/baixa) de CADA noticia. 1 estrela: checar a direcao macro 1D do NAS100 e se a noticia a potencializa. 2/3 estrelas: sentimento geral com confluencia de juros, Brent, ES e NQ.

## FECHAR ANTES DAS 18H (usuaria, 01/10/2026)
O mercado fecha as 18:00 (BRT). SEMPRE fechar toda posicao aberta as 17:55 (relogio do TradingView; o relogio do PC fica ~10 min atras: arredondado, ver docs/estado-e-retomada.md secao 4), a mercado, pelo painel Paper Trading, e registrar close-trade/journal/resumo. Nao deixar posicao aberta na pausa/fechamento. Pausa das 18:00 ate a REABERTURA as 19:00 (BRT); abertura da Asia as 21:00. Entradas de eventos depois das 19:00 (ex.: Logan 19:45) estao liberadas: o mercado ja esta operando.

## VIES VIVO (usuaria, 01/10/2026)
O painel e contexto, nao lei: nao insistir no lado antigo quando a estrutura muda, mas so inverter com evidencia combinada (>= 2 de 4: quebra de estrutura M15 ou 2 fechamentos alem de nivel-chave; confluencia virada em 2 leituras seguidas; conteudo da noticia contradiz; preco aceita alem do nivel), nunca por 1 vela. Todo trade nasce com invalidacao escrita; viés > 30 min sem reavaliar e vencido. Rotulos do painel sao atrasados: vale a dinamica, registrando o motivo. Detalhes: docs/playbook-noticias.md.

## BRIEFING DE MESA E PAINEL (usuaria, 01/10/2026)
- Roteiro oficial (prompt dela, adaptado): docs/briefing-horario.md. Rodar 06:17, 08:25 e de hora em hora na sessao de NY (10:27 a 16:27 no relogio do PC). DIRECAO OBRIGATORIA ALTA/QUEDA ("neutro" so com justificativa plausivel, mesmo assim indicando o lado de menor risco), SEM pontas soltas (condicao -> acao -> invalidacao -> alvo; decisao para os proximos 30-60 min). Registrar em journal/briefings/AAAA-MM-DD.md.
- **FONTE REGULAR DE NOTICIAS: Seeking Alpha** (usuaria, 01/10/2026): a cada briefing, a cada checagem de posicao aberta e apos eventos do calendario, WebFetch `https://seekingalpha.com/market-news` (manchetes recentes + hora ET; ET = BRT - 1h). Ela cobre o que o painel nao ve a noite (petroleo, geopolitica, falas do Fed). Manchete pode sair 20-45 min apos o evento; tom/numero conferir em 2a fonte. Ver docs/briefing-horario.md.
- Painel no grafico: indicador "Painel NAS100 Compacto" (ler com data_get_pine_tables, study_filter "Painel"). Sensor, nao gatilho. Estado/pendencias/armadilhas das ferramentas e agendamentos a recriar: docs/estado-e-retomada.md.

## SESSOES E NIVEIS (usuaria, 01/10/2026) - ver docs/sessoes-e-niveis.md
O Claude SABE os horarios (BRT/TV): Asia 21:00-03:00, Londres 03:00-10:30, NY 10:30-17:00 (AM 10:30-13:00, almoco 13:00-14:30, PM 14:30-17:00), pausa 18:00-19:00. Calcula SOZINHO (data_get_ohlcv M5) a maxima/minima de cada sessao e se foi VARRIDA (pavio passou do nivel apos a sessao) ou ABERTA; varrida = descartada, aberta = alvo/ponto de operacao; observar a sequencia das varreduras. O painel NAO precisa calcular isso (v3.11 no TradingView; a v3.12 do arquivo pine/ nao foi publicada).

## JANELA DE ENTRADA (usuaria, 01/10/2026)
Viés definido + ordem a mercado: observar ~10 min (T-10 ate T-2/T-3 do TV) o MELHOR PONTO; com vela atual contra o viés, esperar a regiao e a rejeicao em vez de entrar na forca contraria; no prazo, entrar de qualquer forma com o stop estrutural. Detalhes: docs/playbook-noticias.md.

Correcao da JANELA DE ENTRADA: prazo em horario do TRADINGVIEW (T-5 = entrada forcada), ticket pre-aberto a partir de T-7, toda resposta diz a hora exata da entrada forcada. Ver docs/playbook-noticias.md.

## ABERTURA DE NY (usuaria + estudo, 06/10/2026) - docs/estudo-abertura-ny.md
A abertura de NY (10:30 BRT) move mais que o dado das 10:45/11:00 em 80% dos dias (vela M5 mediana 77 pts x 56). Regras: (1) antes de qualquer entrada da manha, ler o que NY fez nos primeiros 5-10 min (varrida de Londres/Asia/PDH, direcao, pavio); (2) NAO entrar contra um spike grande de abertura (>= ~50 pts) logo depois dele: na amostra o contra-spike perdeu ~27 pts em 60 min (venda de spike para cima: -41); esperar regiao + rejeicao M5 fechada; (3) evento de 1-2 estrelas no mesmo horario da abertura nao justifica entrada sozinho: o viés vem da leitura de NY + D1; (4) ISM/PMI so contam quando a SURPRESA e grande (acima de ~1 desvio vs projecao) e nao e o flash ja conhecido. A regra inquebravel do calendario continua valendo, mas a entrada de T-5 nesse horario segue a leitura de NY, nao a manchete.

## ANÁLISE COMPLETA OBRIGATÓRIA — NENHUMA VERTENTE CEGA (usuária, 07/10/2026) - docs/checklist-analise-completa.md
Antes de QUALQUER entrada ou análise de gráfico, ler as 10 lentes: painel (que já traz Brent, juros e as informações de mercado), Brent (peso alto, linha do painel), juros (linhas do painel), notícias, eventos, OB/FVG do indicador (data_get_pine_boxes), Fibonacci, Elliott, Wyckoff com volume (data_get_ohlcv), sessões/liquidez e ESTRUTURA SMC (BOS/CHoCH, Strong/Weak High/Low via data_get_pine_labels/lines) e MOMENTUM (RSI, MACD, estocástico, WaveTrend: scripts/momentum_ui_evaluate.js). Seguir o fluxo: quando estrutura, regime M15, Brent/juros e momentum concordam, entrar a favor sem esperar o toque ideal, com stop estrutural e alvo no extremo fraco. Todo motivo de entrada é salvo (banco, CSV, resumo). Vertente sem dado = registrar "sem dado: motivo", nunca pular em silêncio. Cada entrada leva no diário uma linha com o veredito das 10 lentes; se uma lente discorda, o texto diz por que a entrada vale mesmo assim ou a entrada não acontece. Painel/Elliott/Wyckoff/Fibo = confluência; gatilho continua sendo OB + rejeição M5 fechada. Brent: venda com Brent subindo, compra com Brent caindo; contra = só A+. Das 21:00 às 18:00 sempre vale operar (setup principal = notícia/calendário; sem notícia, operar as zonas). Fechar tudo às 17:55 TV.

Limite de 2 scripts visíveis (usuária, 07/10/2026): ficam Painel NAS100 + Structure Volume Profile Setups; as demais lentes por cálculo próprio (docs/checklist-analise-completa.md).
