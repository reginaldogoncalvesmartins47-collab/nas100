# Resumo diario (demo / Paper Trading, 0,1 lote = US$ 0,10 por ponto)

Preencher no fim de cada dia e ao abrir/fechar cada trade. Fonte da verdade dos trades: `data/calendario.db` (`stats`, `daily`) + `journal/diario_trades.csv`.

| Data | Saldo inicial | Ganhou | Perdeu | Saldo final | Trades | Observacao |
|---|---|---|---|---|---|---|
| 2026-09-30/10-01 | US$ 40.159,27 | 0,00 | US$ 7,85 | US$ 40.151,42 | 1 fechado (id 1, stop) + 1 limite pendente | Primeiro dia. Teste de execucao. Venda 0,1 @30.583,1, stop 30.660, alvo 30.505; Parado pelo stop em 01/10 00:54 a 30.661,6 (-US$ 7,85, -1,02R). Ordem limite de venda @30.790 (stop 30.845, alvo 30.590, R:R 3,64) pendente. |

Saldo da conta demo: US$ 40.159,27 (a conta real e de US$ 30; ver rules.json > account).

**01/10 02:35** Trade 2 aberto: venda 0,1 @30.790,9 (limite planejada), stop 30.845, alvo 30.590, risco ~US$ 5,41. Saldo antes: US$ 40.151,42.

**01/10 02:59** Trade 2 fechado no stop a 30.845,6: -US$ 5,47 (-1,01R). Saldo: US$ 40.145,95. Resultado do dia ate agora: -US$ 13,32 (2 trades, 0 acertos).

**01/10 03:40** Trade 3 aberto: compra 0,1 @30.819,7 (limite no reteste), stop 30.785, alvo 30.930, risco ~US$ 3,47. Saldo antes: US$ 40.145,95.

**01/10 03:59** Trade 3 fechado no stop a 30.784,2: -US$ 3,55 (-1,02R). Saldo: US$ 40.142,40. Dia: -US$ 16,87 em 3 trades, 0 acertos, MFE ~0 nos tres. Acima da perda aceita (~US$ 15): no real teria parado.

**01/10 09:34** ACIDENTE (trade 4): clique no X da etiqueta 'Buy Limit' no grafico abriu compra a mercado 0,1 @30.612,6 (stop herdado 30.435); fechada em 30.626,5: +US$ 1,39. Saldo: US$ 40.143,79. Dia: -US$ 15,48 em 4 trades (3 stops + 1 acidente). Nenhuma ordem pendente.

**01/10 09:54** Trade 5 aberto: VENDA a mercado 0,1 @30.584,6 (stop 30.640, alvo 30.500, risco ~US$ 5,54). Saldo antes: US$ 40.143,79. Direcao do vies antecipado (baixa).

**01/10 10:31** Trade 5 fechado no ALVO a 30.496,8: **+US$ 8,78** (+1,59R). Saldo: **US$ 40.152,57**. Dia: -US$ 6,70 em 5 trades (1 alvo, 3 stops, 1 acidente +1,39). Meta US$ 25: faltam US$ 31,70.

**01/10 10:56** Trade 6 aberto: COMPRA a mercado 0,1 @30.511,1 (stop 30.445, alvo 30.640, risco ~US$ 6,61), 5 min antes do ISM. Saldo antes: US$ 40.152,57.

**01/10 10:59** Trade 6 parado a 30.416,6 (stop 30.445 + 28 pts de derrapagem): **-US$ 9,45** (-1,43R), ANTES do ISM. Saldo: US$ 40.143,12. Dia: **-US$ 16,15** em 6 trades.

**01/10 11:51** Trade 7 aberto: COMPRA tatica a mercado 0,1 @30.415,7 (stop 30.300, alvo 30.559 Fibo 38,2%, risco ~US$ 11,57, R:R ~1,2), pedido da usuaria: respiro dentro do macro de baixa (nao inverte o vies). Saldo antes: US$ 40.143,12.

**01/10 12:10** Trade 7 parado a 30.299,7 (sem derrapagem): **-US$ 11,60**. Saldo: **US$ 40.131,52**. Dia: **-US$ 27,75** em 7 trades. POC 30.346 quebrou; Brent em novas maximas (101,56). No real teria parado.

**01/10 14:28** Trade 8 aberto: VENDA a mercado 0,1 @30.543,9 (stop 30.655, alvo 30.420, risco ~US$ 11,11, R:R 1,16). Evento: Jefferson (Fed) 14:30. Viés venda (regime Fed apertando; juros 5,213% e IA forte contra). Saldo antes: US$ 40.131,52. Entrada saiu ~2 min antes da fala no relogio do TV, mas depois do T-5 por causa do relogio do PC atrasado.

**01/10 15:41** Trade 8 fechado a mercado em 30.567,8: **-US$ 2,39** (tese virada: Jefferson nao endossou alta iminente de juros; 10a -6 bp, 2a -10 bp). Saldo: **US$ 40.129,13**. Dia: **-US$ 30,14** em 8 trades. MFE ~+57 pts, devolveu tudo; nao houve degrau de protecao (+60). Placar de vies em noticias: Jefferson = VENDA, errou.

**01/10 15:55** Trade 9 aberto: COMPRA a mercado 0,1 @30.572,3 (stop 30.490, alvo 30.650, risco ~US$ 8,23, R:R 0,89 so aviso). Evento: Bowman (FOMC) 16:00. Viés compra, confianca baixa. Saldo antes: US$ 40.129,13.

**01/10 ~16:58** Trade 9 fechado a mercado em ~30.536,9: **-US$ 3,54** (tese enfraquecida: Alphabet cai com Gemini 4, CNBC 16:46; preco a 15 pts do stop). Saldo: **US$ 40.125,59**. Dia: **-US$ 33,68** em 9 trades. Bowman falou de regulacao bancaria (eSLR), nao de juros: viés de compra foi suposto sem pesquisar o tema (pesquisa feita depois da entrada).

**01/10 17:21** Trade 10 aberto: VENDA a mercado 0,1 @30.555,6 (stop 30.640, alvo 30.440, risco ~US$ 8,44, R:R 1,46). Eventos 17:30: balanco do Fed (3*) e reservas (1*). Viés venda leve, confianca 4/10 (confluencia neutra). Saldo antes: US$ 40.125,59.

**01/10 17:54** Trade 10 fechado (regra: antes das 18h) a ~30.526,8: **+US$ 2,88**. Saldo: **US$ 40.128,47**. **Dia: -US$ 30,80 em 10 trades** (2 ganhos + 1 acidente no lucro; 7 perdas). Analise do dia: docs/analise-dia-2026-10-01.md.

**01/10 19:40** Trade 11 aberto: VENDA a mercado 0,1 @30.557,0 (stop 30.610, alvo 30.425, risco ~US$ 5,3, R:R 2,47). Evento: Logan (Fed) 19:45. Viés QUEDA, conf 5/10, protocolo de tema + janela de entrada (rejeicao na maxima da sessao). Saldo antes: US$ 40.128,47.

**01/10 21:18** Trade 11 fechado no STOP em 30.631,3: **-US$ 7,43**. Saldo: **US$ 40.121,04**. **Dia: -US$ 38,23 em 11 trades** (-30,80 ate o trade 10, mais -7,43; saldo inicial do dia ~US$ 40.159,3). O stop foi afastado pela usuaria (30.610 -> 30.631,1) as ~20:00; no stop original a perda seria ~-US$ 5,3. MFE ~6 pts. Viés QUEDA (Logan duro) acertou no conteudo, mas o preco nao reagiu e a abertura da Asia levou o NAS100 para cima.

## 02/10/2026 (sexta) - dia do payroll
Saldo inicial do dia: US$ 40.125,07 (paper). Regra nova gravada: PC ~10 min atras do TV (cron = evento - 15 min).

**02/10 09:26** Trade 12 aberto: COMPRA a mercado 0,1 @30.717,7 (stop 30.570, alvo 30.904, risco ~US$ 14,77, R:R 1,28 so aviso). Evento: Payroll set (09:30, 3*). Viés COMPRA, confianca 4/10 (cenario Goldilocks, consenso 84-98K; antes VENDA 5/10 na 1a leitura, mudou apos SpotGamma/Newsquawk/ADP/FXStreet; fontes lidas: Reuters/CNBC, Bloomberg, Investing, Seeking Alpha, Finviz, NQ Market Wizard). Entrada T-4 (ticket fechou sozinho e tive que reabrir). Limite 30.636,1 (OB da usuaria; SL 30.495, TP 30.841,9) ficou pendente - cancelado depois (nao executou).

**02/10 ~09:31** Trade 12 fechado em 30.788,9: **+US$ 7,12 (+0,48R)**. A usuaria subiu o take para garantir ~US$ 7 e a ordem foi executada. Saldo: **US$ 40.132,19**. Payroll saiu **29K** (proj 89K; anterior revisado 162K->133K), desemprego 4,2% (proj 4,1%), salario/hora 0,1% m/m (proj 0,3%) e 3,0% a/a (proj 3,2%), privado 46K (proj 85K): fraco. NAS100 saltou 30.748 -> 30.873 em uma vela M5 (+125 pts), juros 10a -7 pb. Viés de COMPRA acertou; MFE do mercado ~+155 pts vs +71 capturados.
Licoes: (1) stop nunca colado/dentro do range, fora da minima do dia e do OB, com folga de ATR (usuaria); (2) olhar o grafico/OB do indicador dela, nao so niveis do painel; (3) ler a aba Ordens antes de editar (a usuaria mexeu na ordem e eu sobrescrevi o stop sem saber); (4) o ticket fecha sozinho: pre-abrir no maximo T-4 e reabrir se preciso; (5) varias fontes (Reuters, Bloomberg, Investing, SA) antes de entrar; (6) payroll fraco com desemprego 4,2% = alivio de juros e alta inicial.

**02/10 10:54** Trade 13 aberto: COMPRA a mercado 0,1 @30.943,0 (stop 30.790, alvo 31.050, risco ~US$ 15,3, R:R 0,72 so aviso). Eventos 11:00: encomendas a industria (2*), encomendas ex-transporte, duraveis ex-transporte e ex-defesa (1* cada) + Logan (1*, evento separado). Viés ALTA (macro). Saldo antes: US$ 40.132,19.
**02/10 11:00** Resultados: encomendas 0,1% (proj 0,1%, ant 0,8%): em linha; ex-transporte 0,3%; duraveis ex-transporte 0,2% (ant 0,3%); ex-defesa 0,0% (ant 0,1%): impacto nulo no preco. Quem moveu foi NY: NAS100 31.012 (max).
**02/10 11:20** Stop movido de 30.790 para 30.946 (zero a zero, +3 pts): trade em +72 pts (66% do caminho ao alvo). Checklist de cenario: juros -4,6 pb vs abertura, NQ +1,6%, sentimento 10/10, preco colado na max. de NY 31.012 (zona de venda), proximo evento 14:00 (Baker Hughes): risco de devolucao na resistencia => protegido. Regra da usuaria: nao devolver.
**02/10 ~11:25** Trade 13 fechado a ~31.010 (manual, a usuaria tocou no painel sem querer): **+US$ 6,73 (+0,44R)**. Saldo: **US$ 40.138,92**. Dia: **+US$ 13,85 em 2 trades** (payroll +7,12; 11:00 +6,73). Stop ja estava no zero a zero, entao o lucro estava protegido. Cron de gestao apagado. Proxima entrada: 14:00 (Baker Hughes) em T-5 = 13:55 TV.

**02/10 13:41** Trade 14 aberto: COMPRA 0,1 @30.821,1 (LIMITE autorizado so nesta operacao, 30.822; stop 30.785, alvo 30.882; depois a usuaria alargou para 30.739,6/30.909,8). Evento: Baker Hughes 14:00 (2*). Viés ALTA 3/10 (parametro de sexta: leve alta, range pequeno, 10-20 min; GEX QQQ pino ~30.855). Falha minha: gate vencido ao colocar a ordem (renovado depois).
**02/10 14:06** Trade 14 fechado a 30.831,1: **+US$ 1,00 (+0,28R)** no stop do zero a zero. Saldo: **US$ 40.139,92**. **Dia: +US$ 15,05 em 3 trades** (payroll +7,12; 11:00 +6,73; Baker Hughes +1,00). Reacao ao dado: +17 pts em 5 min e devolveu em ~6 min: o padrao 'leve alta' apareceu, de curta duracao.

**02/10 16:13** Trade 15 aberto: COMPRA a mercado 0,1 @30.793,8 (stop 30.740, alvo 30.850, risco ~US$ 5,38, R:R 1,0 so aviso). Evento: CFTC 16:30 (2*, sem efeito no estudo). Entrada por ORDEM da usuaria; contexto D1 alta, desconto no range de NY. Saldo antes: US$ 40.139,92.
**02/10 16:37** Trade 15 fechado a 30.827,0 (manual, sem querer: a usuaria foi ajustar o stop e fechou a posicao; 3a vez no dia): **+US$ 3,32 (+0,62R)**. Saldo: **US$ 40.143,24**. **Dia: +US$ 18,37 em 4 trades**. Degrau do zero a zero (+25 pts) estava atingido e pendente. Dica: para mexer em stop, usar a aba Ordens com o painel Paper Trading aberto, nao o grafico.

## 05/10/2026 (segunda) - registrado em 06/10 (nao tinha sido atualizado na hora)
Saldo inicial do dia: US$ 40.143,24 (paper). Saldo final: **US$ 40.132,28**. **Dia: -US$ 10,96 em 2 trades** (1 ganho, 1 stop). Fonte: Historico de ordens/negociacao do Paper Trading (conferido em 06/10).

**05/10 09:56** Trade 17: COMPRA a mercado 0,1 @30.761,9 (stop 30.620,6, TP 30.893,9). Motivo/viés NAO foram registrados na hora; sem como reconstruir. **10:24** fechada a mercado @30.778,2 (manual): **+US$ 1,63**.

**05/10 10:35** Trade 16: VENDA a mercado 0,1 @30.920,1 (entrada pedida pela usuaria, 'entra vendido agora', oferta pos-spike de abertura de NY; PMI Servicos 10:45 + ISM Nao-Manufatura 11:00, 3*, mesmo lado). Viés baixa, confianca baixa/media. Ordens finais: stop 31.045,2, TP 30.622,6 (o stop inicial registrado era 31.018; afastado, nao ha registro de quem). **14:24** STOP @31.046,0: **-US$ 12,59 (-1,0R)**. O mercado foi contra a venda e subiu ate o stop.
Licoes: (1) venda contra D1 ALTA acima da EMA20, entrada logo apos o spike de abertura de NY e sem esperar a reacao do dado; (2) o stop foi alterado sem registro: sempre gravar mudanca de stop na hora (update + journal); (3) dois trades do dia sem fechamento no banco: regra de fim de dia exige conferir o Historico do Paper Trading contra o banco.

## 06/10/2026 (terca) - sem noticias de 3*; dia de ruido
**06/10 10:56 TV** Entrada T-5 do evento 11:00 (IBD/TIPP, 1*) NAO executada, por decisao: preco subiu de 31.280 (10:45) para 31.304 e o painel marcou ZONA DE VENDA (Londres H, +4); R:R 0,36 (stop 31.220 / alvo 31.334) comprando na base da oferta 31.300-31.336, sem o recuo para a demanda 31.225-31.247 que o plano esperava. Viés segue ALTA; nova chance: compra a mercado se voltar a demanda com rejeicao M5 fechada. Registrado como decisao, nao falha de interface.

**06/10 11:37 TV** Trade 18 aberto: COMPRA a mercado 0,1 @31.291,1 (stop 31.222, alvo 31.350, risco ~US$ 6,91, R:R 0,85 so aviso). Evento: Bowman 11:45 (regulacao bancaria, neutro). Viés ALTA 3-4/10. Gatilho: vela M5 11:30 fechou com rejeicao perto da demanda 31.225-31.247 (min 31.250,8), apos rompimento falho de 31.336. Invalida: M5 fecha < 31.222. Saldo antes: US$ 40.132,28. Meta do dia (usuaria): +US$ 20.

**06/10 11:51 TV** Trade 18: stop movido de 31.222 para **31.318** (trava ~+27 pts / ~US$ 2,7, ~46% do alvo; degrau de >=75% do caminho: preco 31.342, +51 pts). Alvo mantido em 31.350 (colado na max do dia 31.351,4 / zona de venda NY AM H). Cenario: juros10 -4,4 pb, Brent -2%, confluencia +2, sentimento 8/10, SA sem noticia nova de Fed/juros, proximo evento GDPNow 12:30. Stop logo abaixo do fundo M5 de 11:45 (31.322,7). Risco: stop dentro da amplitude normal (ATR M5 ~31); se for varrido, sai com ganho.

**06/10 ~11:53 TV** Trade 18 fechado no ALVO @31.350: **+US$ 5,89 (+0,85R)**. Saldo: **US$ 40.138,17**. Dia: **+US$ 5,89 em 1 trade**. Faltam US$ 14,11 para a meta de US$ 20 da usuaria. O stop em 31.318 nao chegou a ser testado. Licao: compra na rejeicao M5 fechada perto da demanda + viés ALTA a favor funcionou; a decisao de nao comprar colado na oferta as 10:55 evitou entrar 50 pts acima.

**06/10 12:22 TV** Trade 19 aberto: COMPRA a mercado 0,1 @31.373,8 (stop 31.340, alvo 31.420, risco ~US$ 3,38, R:R 1,16). Evento: GDPNow 12:30 (2*, crescimento). Viés ALTA, tudo alinhado (juros -5,1pb, Brent -1,9%, DXY -0,33%, ES +0,8%, sentimento 9/10). Setup: continuacao em flag estreito abaixo da max do dia; EXCECAO consciente ao filtro 'nao comprar em zona de venda do painel' (NY AM H +5): preco aceito acima da oferta antiga, sem rejeicao, stop curto. Saldo antes: US$ 40.138,17. Invalida: M5 fecha < 31.340.

**06/10 12:55 TV** Trade 19 fechado no STOP @31.338,8: **-US$ 3,50 (-1,04R)**. Saldo: **US$ 40.134,67**. Dia: **+US$ 2,39 em 2 trades** (+5,89 e -3,50). O GDPNow (12:30) nao deu direcao; o flag sob a max do dia (31.386) foi devolvido, o sentimento caiu de 9 para 5/10, as big techs viraram e o Brent recuperou. Licao: a excecao ao filtro 'zona de venda do painel' (compra no topo do dia) nao funcionou desta vez: 1 trade, nao prova nada, mas registrar como 'seguiu_plano=n' para comparar com os que respeitaram o filtro (trade 18: +5,89 com filtro; trade 19: -3,50 sem filtro).

**06/10 13:52 TV** Trade 20 aberto: VENDA a mercado 0,1 @31.309,9 (stop 31.323, alvo 31.262, risco ~US$ 1,31, R:R 3,66). Evento: Leilao Note 3 anos 14:00 (2*, juros/demanda). Viés curto prazo BAIXA (set 13:24; 2 de 4 evidencias): perda do Londres H, confluencia virada, Elliott flat completo (alvo base de B 31.250,8). Setup: reteste do Londres H por baixo com rejeicao M5 (13:45). Stop curto (13 pts vs ATR M5 ~21): pode ser varrido. Saldo antes: US$ 40.134,67.

**06/10 14:11 TV** Trade 20: stop movido de 31.323 para **31.300** (trava ~+10 pts / ~US$ 1,0). Preco 31.280 (+29,9 pts, 62% do alvo; MFE ja +31,3 em 14:00). O degrau de >=50% do alvo (+24 pts) foi atingido na vela das 14:00 e eu so protegi as 14:11: ERRO MEU, avaliei pelo preco do momento (48%) e nao pelo maximo favoravel. Cenario: confluencia mista (0), sentimento 6/10, preco dentro do topo do OB de demanda (segurou 3x), Schmid 14:15. Stop acima do ultimo topo M5 (14:05, 31.291,3). Alvo mantido 31.262 (base de B 31.250,8 abaixo). Regra a seguir: medir o degrau pelo MFE, nao pelo preco atual.

**06/10 ~14:13 TV** Trade 20 fechado no ALVO @31.261,5: **+US$ 4,84 (+3,7R)**. Saldo: **US$ 40.139,51**. Dia: **+US$ 7,23 em 3 trades** (+5,89, -3,50, +4,84). Faltam US$ 12,77 para a meta de US$ 20. A venda no reteste do Londres H por baixo (viés curto BAIXA, Elliott flat completo, rejeicao M5 13:45) funcionou; stop movido tarde (14:11). Com o take executado o preco (31.261,9 min) parou exatamente na zona prevista (base de B 31.250,8 / OB 31.228,5-31.288,6): decidir se estica ou nao so faz sentido ANTES do take bater; a vigia de 3 min nao chegou a tempo.

**06/10 14:32 TV** Trade 21 aberto: COMPRA a mercado 0,1 @31.283,5 (stop 31.245, alvo 31.334, risco ~US$ 3,85, R:R 1,31). Sem evento (caça). Gatilho: vela M5 14:20 tocou 31.251,2 (base de B 31.250,8, alvo de Elliott do flat) e fechou 31.269,5 com pavio inferior de ~18 pts dentro do OB de demanda; o viés curto BAIXA chegou ao alvo e volta ao D1 ALTA. Entrei 14 pts acima do gatilho (a tarefa de 14:28 vi tarde). Brent virou para cima (+0,2%): risco. Saldo antes: US$ 40.139,51.

**06/10 14:51 TV** Trade 21: stop movido de 31.245 para **31.292** (trava ~+8,5 pts / ~US$ 0,85; lucro nao realizado +US$ 2,9). Medido pelo MFE: maximo 31.316,2 (+32,7 pts = 65% do alvo 31.334) > degrau de 50%; aplicado na hora, sem atraso. Cenario: juros10 -4,0 pb, ES +0,66%, big techs positivas, Brent estavel (+0,12%), sentimento 5/10, preco recuperou o Londres H (31.309) e o painel marca ZONA DE VENDA (-5): risco de reteste. Stop abaixo da minima M5 de 14:40 (31.293). Alvo mantido 31.334 (ainda nao esticar: a oferta de NY AM fica em 31.386).

**06/10 14:56 TV** Trade 21 fechado no stop protetor @31.289,3: **+US$ 0,58 (+0,15R)**. Saldo: **US$ 40.140,09**. Dia: **+US$ 7,81 em 4 trades** (+5,89, -3,50, +4,84, +0,58). Faltam US$ 12,19 para a meta de US$ 20. Licao: o stop de protecao (31.292) ficou so 11 pts abaixo do preco (ATR M5 ~19, ruido normal) e foi varrido por uma vela (min 31.285,1) que voltou +17 pts na seguinte; sem o stop o trade ainda estaria aberto em +19 pts. Equilibrio: proteger cedo evita virar prejuizo (trade 18 e 20) mas sai de trade bom no ruido; prox vez, stop atras do fundo estrutural ABAIXO do ruido (>= 1 ATR M5) ou so no degrau de 75%.

**06/10 16:42 TV** Trade 22 aberto: VENDA a mercado 0,1 @31.276,5 (stop 31.299, alvo 31.252, risco ~US$ 2,25, R:R 1,09). Gatilho: M5 16:35 fechou abaixo da minima de 15:35 e do topo do OB de demanda (31.288,6) apos 5 testes; reteste por baixo. Macro: Brent +0,72% vs abertura, semis/Micron fracos, big techs fracas, sentimento 5/10; juros10 -3,2 pb vai contra. Viés BAIXA curto prazo (fraco), D1 ALTA: scalp. Stop 22,5 pts (1,4 ATR M5, acima do ruido, licao do trade 21). Fill 1,3 pt pior que a cotacao. Fechar tudo as 17:55. Saldo antes: US$ 40.140,09.

**06/10 16:43 TV** Trade 22 fechado manual @31.272,0: **+US$ 0,45 (+0,20R)**. Saldo: **US$ 40.140,54**. Dia: **+US$ 8,26 em 5 trades** (+5,89, -3,50, +4,84, +0,58, +0,45). Faltam US$ 11,74 para a meta de US$ 20. Motivo da saida: o Smart Money Concepts voltou a ficar visivel/legivel (OBs: oferta 31.296,1-31.307,6; demanda 31.251,2-31.274,2 e 31.250,8-31.290,3) e mostrou que a venda abriu 2 pts acima do topo da demanda, com alvo na base dela e stop dentro da oferta. ERRO DE PROCESSO: entrei sem ler o OB do indicador, mesmo tendo dito horas antes que passaria a ler. Regra: ANTES de abrir ticket, rodar data_get_pine_boxes (study Smart Money) e conferir entrada/alvo/stop contra os OBs.

**06/10 17:12 TV** Trade 23 aberto: VENDA a mercado 0,1 @31.265,3 (stop 31.292, alvo 31.160, risco ~US$ 2,67, R:R 3,9). OB lido ANTES do ticket (regra nova): o Smart Money removeu os OBs de demanda 31.250,8-31.290,3/31.251,2-31.274,2 apos o M5 de 16:50 fechar 31.243,2; oferta 31.296,1-31.307,6 ativa; proxima demanda 31.131-31.154,7. Reteste por baixo da zona rompida. Macro: Brent +0,88%, semis -0,47%/Micron -1,13% (1h), big techs fracas, sentimento 5/10; juros -3,0 pb vai contra. Scalp contra o D1. API 17:30 no mesmo lado: so gerir. Fechar tudo 17:55. Saldo antes: US$ 40.140,54.

**06/10 17:53 TV** Trade 23 fechado a mercado @31.271,5 (regra das 17:55): **-US$ 0,62 (-0,23R)**. Saldo final: **US$ 40.139,92**.

### FECHAMENTO DO DIA 06/10/2026 (terca)
Saldo inicial US$ 40.132,28 -> final **US$ 40.139,92**: **+US$ 7,64 em 6 trades** (conferido no Historico de negociacao do Paper Trading: +5,89, -3,50, +4,84, +0,58, +0,45, -0,62). Meta da usuaria (+US$ 20): NAO batida (faltaram US$ 12,36). Acertos 4 de 6; maior ganho +5,89 (compra no OB de demanda, trade 18); maior perda -3,50 (compra no topo do dia, contra o filtro, trade 19).
| Evento | Hora | Entrada | Resultado |
|---|---|---|---|
| IBD/TIPP (1*) | 11:00 | NAO entrou (decisao: R:R 0,36, zona de venda) | - |
| Bowman (2*) | 11:45 | trade 18 compra | +5,89 |
| GDPNow (2*) | 12:30 | trade 19 compra (excecao ao filtro) | -3,50 |
| EIA STEO (2*) | 13:00 | so gerir (compra 19 ativa) | - |
| Leilao Note 3a (2*) | 14:00 | trade 20 venda (reteste do Londres H) | +4,84 |
| Schmid (1*) | 14:15 | so gerir (venda 20 ativa) | - |
| (caca, sem evento) | 14:32 | trade 21 compra (base de B/OB) | +0,58 |
| (caca, sem evento) | 16:42 | trade 22 venda (fechada a 16:43 apos ler o OB) | +0,45 |
| (caca) / API (2*) 17:30 | 17:12 | trade 23 venda (so gerir no API) | -0,62 |
| Logan (1*) 20:00, Williams (2*) 22:05 | apos a pausa | agendadas (cron), Logan duvidoso (nao ha fala no Dallas Fed) | pendente |
Faltantes: nenhum evento de ate 17:30 ficou sem decisao registrada. Licoes do dia: (1) ler o OB do indicador (Smart Money/Killzones) ANTES do ticket; (2) medir degrau de protecao pelo MFE, nao pelo preco; (3) stop de protecao com folga >= 1 ATR M5 (trade 21 varrido); (4) nao comprar esticado nem em zona de venda do painel; (5) o ticket lembra o ultimo lado: conferir o lado no screenshot; (6) olhar Brent/juros pela estrutura do grafico: proposta pendente de aprovacao.

**06/10 ~19:50 TV** Logan 20:00 (1*): NAO entrei, por decisao. Verificado em 19:48 PC: a pagina de discursos do Dallas Fed nao lista nenhum evento do Logan em 06 ou 07/10 (so 01/10 e 02/10) e o Seeking Alpha nao mostra manchete dele; a usuaria ja tinha desconfiado (o Investing lista horarios previstos que nao se cumprem, como o de 01/10 19:45). Mercado reaberto 19:00 em baixa energia: M5 entre 31.258 e 31.291 (ATR ~10), sem zona nem gatilho. Registrar no placar: 'evento do calendario sem fala confirmada' (Logan 06/10).

**06/10 ~21:55 TV** Williams 22:05 (2*): NAO entrei, por decisao. Verificado em 21:53 PC: a pagina de discursos da NY Fed lista falas dele em 25/09 e 29/09 mas NADA em 06 ou 07/10; o Seeking Alpha nao mostra manchete dele nem de Fed/juros/petroleo (feed sem atualizacao recente). Sem fala confirmada e sem tema para o protocolo de tema, nao ha viés de evento. Mercado: M5 entre 31.252 e 31.289 (ATR baixo), sem zona nem gatilho.

### Fechamento final do dia 06/10 (apos a pausa)
Eventos ate 17:30: todos com decisao registrada (ver tabela acima). Apos a reabertura: Logan 20:00 e Williams 22:05 = falas NAO confirmadas pelos bancos centrais (Dallas Fed e NY Fed nao listam), nao houve entrada. Resultado do dia: +US$ 7,64 em 6 trades; saldo final US$ 40.139,92; sem posicao aberta; sem agendamentos pendentes de hoje.
Proposta para a usuaria decidir: tirar da 'regra inquebravel' os eventos de fala listados so no Investing e nao confirmados pelo banco central (Logan 01/10 19:45 existiu com atraso; Logan 02/10 11:00, 06/10 20:00 e Williams 06/10 22:05 sem confirmacao).

## 07/10/2026 (quarta)
Saldo inicial do dia: US$ 40.139,92 (paper). Madrugada (regra: das 21:00 as 18:00 sempre vale operar).
**07/10 00:49 TV** Trade 24 aberto: VENDA a mercado 0,1 @31.248,1 (stop 31.262, alvo 31.200, risco ~US$ 1,39, R:R 2,9). MOTIVO: seguir o fluxo (pedido da usuaria) em vez de esperar o toque na oferta. Estrutura SMC: CHoCH de baixa, Strong High 31.293,1 (invalidacao), Weak Low 31.203,1 (alvo). Painel: regime M15 BAIXA, Brent +0,48% e juros +1,1 pb a favor. Momentum: M5 estocastico virando de 74 e MACD esgotando; M15 com divergencia de baixa. Wyckoff: repique em volume decrescente. Elliott: ABC de queda terminado, repique de correcao (61,8% 31.256 / 78,6% 31.271 / oferta 31.265-31.283). Estudo: tendencia M15 a favor sobe o acerto de 40,6% para 45,4%. Stop 1,3 ATR M5 acima da ultima maxima. Calendario completo do Investing NAO capturado (extensao do Chrome desconectada): recaptura as 08:03.

## 08/10/2026 (quinta) - Claude no Paper Trading (conta nayaramarinhomartins, lote 0,1)
Saldo inicial do dia (antes do 1o trade do Claude): US$ 106.814,79. Saldo final (ultimo trade): US$ 106.827,73. **Resultado dos trades do Claude: +US$ 12,94 (5 trades, 4 ganhos, 1 perda).** (Correcao: o placar dito no chat, +9,93, omitia o trade das 11:56.)
| # | hora | lado | entrada | saida | resultado | observacao |
|---|---|---|---|---|---|---|
| 25 | 11:20 | venda | 31.065,6 | 31.072,1 | -0,65 | stop de 6 pts (curto demais), sem gatilho fechado, entrada por ordem da usuaria |
| 26 | 11:56 | venda | 31.044,3 | 31.015,7 | +2,86 | stop apertado PELA USUARIA para 31.014,7 (Claude nao protegeu) |
| 27 | 12:24 | venda (T-5 GDPNow) | 31.003,7 | 30.980,4 | +2,33 | degraus: 31.045 -> 31.002 -> 30.992 -> 30.980 (apertado com atraso) |
| 28 | 13:49 | venda | 30.851,6 | 30.842,9 | +0,87 | stop apertado pela usuaria para 30.841,3 (10 pts, ruido) |
| 29 | 13:54 | venda (T-5 leilao Bond 30a) | 30.774,5 | 30.699,2 | +7,53 | ALVO; stop 30.850 -> 30.748 aos +56 pts; vigia de 1 min |
Eventos x entradas: Waller 05:30 (PERDIDO: vigia nao disparou 01:15-09:30), seguro-desemprego 09:30 (PERDIDO), atacado 11:00 (perdido: Paper Trading desconectado), GDPNow 12:30 (entrada 12:24), leilao Bond 30a 14:00 (entrada 13:54), balanco do Fed 17:30 (nao ocorreu ate o fim desta sessao).
Vetos: 2 (00:52 compra vetada: acertou aos 15 min; 13:25 venda apos rejeicao de 78 pts: vetada por macro/R:R).
Licoes: (1) stop de ATR/folga de spike por sessao (docs/gestao-saida.md); (2) protecao em degraus aplicada de verdade; (3) acompanhar de 1 em 1 min com posicao; (4) vigia e monitor de noticias precisam ligar no INICIO da sessao; (5) spike de 13:17 foi noticia de Trump/Ira (Bloomberg RSS 13:24, 7 min DEPOIS do preco).
Pendencias: balanco do Fed 17:30; registrar o resultado dos vetos (60 min); medicao de atraso das fontes de noticia (docs/medicao-noticias.md); estudo do Structure em PineTS (docs/estudo-zonas-pinets.md); GEX so conclui com >= 20 dias (scripts/gex_teste.py).
