# Ficha pre-entrada (obrigatoria antes de QUALQUER ordem do Claude) - criada 07/10/2026
Objetivo: o Claude so entra depois de olhar TODAS as variaveis. Se alguma vertente nao tiver dado, escrever "sem dado: motivo". Se alguma VETA, nao entra.
Complementa docs/motor-de-decisao.md (o que operar) e docs/checklist-analise-completa.md (as lentes em detalhe).

## 1. Coleta (3 leituras, nesta ordem)
1. `data_get_pine_tables` study "Painel" -> semaforo (macro, mercado, preco, tempo).
2. `ui_evaluate` com scripts/snapshot_ui_evaluate.js -> momento (VWAP/esticado), liquidez varrida/aberta, abertura de NY, estrutura interna, FVGs abertos, momentum M5/M15, ultima vela fechada.
3. `data_get_pine_boxes` / `data_get_pine_labels` study "Structure VP + SMC" -> OB oferta/demanda, FVG, BOS/CHoCH e setups do Structure.
Mais: `calendar_db.py gate` (LIBERADO?), proximo evento (tabela do dia), Seeking Alpha (noticias 30 min), posicoes/ordens abertas (Paper Trading).

## 2. Ficha (copiar no diario de cada entrada, uma linha por item)
| # | Variavel | Pergunta | Veta quando |
|---|---|---|---|
| 1 | Gate | gate = LIBERADO? | BLOQUEADO |
| 2 | Evento | proximo evento e peso (alto/baixo); falta quanto? | entrada de regiao com evento ALTO em < 15 min (exceto a propria entrada T-5 do evento) |
| 3 | Noticias | algo nos ultimos 30 min muda juros/Brent/DXY? | manchete contra a entrada sem reacao do preco ainda |
| 4 | Macro (painel) | juros, Brent, DXY, VIX: a favor / contra / neutro | 3+ contra |
| 5 | Mercado (painel) | NQ, S&P, gigantes, chips, Micron | maioria contra no 15 min |
| 6 | Momento - esticado | z do VWAP NY | comprar com z >= +2 ou vender com z <= -2 (perseguir) |
| 7 | Momento - liquidez | a liquidez do lado da entrada ja foi varrida? alvo aberto? | entrar a favor de um movimento que ACABOU de varrer liquidez e voltou |
| 8 | Momento - abertura NY | ja passaram 15 min? preco dentro/acima/abaixo da faixa | entrada nos primeiros 15 min de NY (salvo T-5 de evento) |
| 9 | Estrutura | tendencia interna (BOS/CHoCH), H1 | contra a estrutura sem CHoCH a favor |
| 10 | Regiao | OB/FVG (Structure VP + SMC ou snapshot) com preco dentro | sem regiao (setup de regioes) |
| 11 | Gatilho | ultima vela M5 FECHADA rejeitou a regiao (pavio) e fechou de volta? | vela ainda aberta ou fechou rompendo a regiao |
| 12 | Momentum | M5/M15 esgotado a favor da reversao ou acelerando a favor da entrada? | acelerando forte contra a entrada |
| 13 | Risco | stop fora da regiao + folga ATR; alvo = proxima liquidez aberta; R:R | sem stop estrutural possivel |
| 14 | Posicao | ja existe posicao no mesmo lado? oposta? | duplicar o mesmo lado |
| 15 | Hora | falta quanto para 17:55 TV? | menos de 15 min (salvo evento) |

## 2b. PERGUNTAS que o Claude se faz ANTES de entrar (sem a usuaria pedir; responder por escrito)
1. O que o MERCADO esta fazendo agora (fase: tendencia, correcao, varredura de liquidez, lateral)? Entrar a favor dessa fase ou contra?
2. Em que fase do dia/sessao estou (primeiros 15 min de NY, almoco, Asia fina)? Essa hora tem movimento confiavel?
3. O que precisa ser verdade para essa entrada dar certo? E o que a INVALIDA (preco e hora)?
4. Quanto espaco livre existe ate o proximo obstaculo em relacao ao ATR? Cabe o stop ESTRUTURAL?
5. Estou entrando por analise ou por vontade de recuperar/operar? (nao entrar por impulso)
6. Ja existe base estatistica? Rodar `bash scripts/edge.sh query "..." --symbol USATECH` com a condicao parecida e olhar N e IC: **N < 30 = anedota, sem vantagem; IC que inclui 50% = sem vantagem**. Dizer o numero na decisao.
7. Estou em duvida sobre um conceito (OB, FVG, BOS, sweep)? Consultar a Biblioteca do LuxAlgo MCP (library_search / library_get_concept) em vez de usar de memoria.
8. O que a zona/nota do Structure VP + SMC diz E o que o backtest diz dela: **sem vantagem comprovada (docs/estudo-zonas-pinets.md)**; a zona e checklist, nunca motivo de entrada sozinha.

## 3. Decisao (escrever em 3 linhas)
- **Lado e por que** (as 3 razoes mais fortes).
- **O que esta contra** e por que a entrada vale mesmo assim (ou "nao entra").
- **Plano:** entrada, stop, alvo, invalidacao, protecao (zero a zero com +50% do caminho).

## Exemplo real (07/10/2026, 10:30-10:45 BRT, venda da usuaria em 30.992) - a ficha teria vetado
- Item 8: entrada dentro dos 15 primeiros min de NY (faixa 30.922-31.048 ainda formando).
- Item 7: a minima de Londres (30.979) estava para ser varrida e foi varrida em seguida com reversao.
- Item 6: preco ja muito abaixo do VWAP do dia (esticado para baixo) = vender ali era perseguir.
Depois: estrutura virou ALTA (CHoCH 31.057,9 + 3 BOS), maximas de Londres/Asia/ontem ficaram abertas como alvo.
