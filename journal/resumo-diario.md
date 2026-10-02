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
