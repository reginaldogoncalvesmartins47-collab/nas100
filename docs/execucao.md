# Execucao: o Claude coloca as ordens

Decisao da usuaria: **o Claude executa; ela nao clica.** Este documento define como, com seguranca, e o que ainda NAO foi testado.

## Gatilho (resumo)
Regiao pontuada -> o preco chega -> em M5 o mercado mostra rejeicao de pavio a favor do viés e o candle FECHA sem romper
a regiao -> `entry-check` confirma, calcula stop (alem do pavio + folga de ATR), alvo (borda da regiao oposta), RR e lote
-> o Claude coloca a ordem e registra com `open-trade`.

## Regras da execucao
1. **Toda ordem nasce com stop e alvo** (ordens na corretora). Sem stop, nao ha ordem.
2. **Antes de ordenar:** conferir posicoes abertas (evitar ordem duplicada) e os limites (`open-trade` recusa se passar do
   risco por trade, da perda do dia ou do corte total).
3. **Depois de ordenar:** ler a posicao de volta e confirmar preco, lote, stop e alvo; so entao registrar. Se algo diferir, corrigir na hora.
4. **Falha de ordem:** avisar a usuaria e nao insistir em loop.
5. **Acompanhamento:** a cada candle M5 fechado, `update-trade` e `path` (pavio contra, pares). O stop protetor fica no broker.
6. **Limites atingidos** (perda do dia ou corte total): parar de ordenar.

## Treino (Paper Trading): autorizado
Saldo de US$ 30 (mesmo capital do real). Os resultados sao a **prova**: as entradas do proprio Claude.

## Real: objetivo final, com chave unica
Somente com: (1) `ready` cumprido; (2) autorizacao escrita da usuaria, dada uma vez para virar a chave (nao a cada trade);
(3) stop e alvo como ordens na corretora; (4) limites de capital ligados. Comecar com o menor lote.

## O que NAO foi testado (precisa ser o primeiro marco no PC da usuaria)
- Se o Claude consegue **colocar ordem com stop e alvo** no Paper Trading do TradingView (extensao do navegador ou MCP).
  Nao sei se o MCP da comunidade inclui ordens; a extensao poderia clicar no painel, mas nao foi verificado.
- Latencia: entre fechar o candle M5 e a ordem sair.
- Continuidade: precisa de PC ligado, Claude Code ativo e a rotina de 5 em 5 minutos rodando; se cair, o stop no broker protege
  a posicao, mas nao abre novas entradas.
- Conta real na Pepperstone: se as ordens podem ser colocadas da mesma forma (ou se exige robo em MT5/cTrader).
- Valor do ponto e lote minimo do NAS100 (o `entry-check` mostra o risco real a cada entrada, com `--usd-per-point`).

## Teste de aceitacao sugerido (demo)
1. Ordem de compra de lote minimo com stop e alvo no Paper Trading; ler a posicao de volta; fechar.
2. Repetir com venda. 3. Forcar uma falha (ex.: stop invalido) e ver se ele avisa. 4. So depois, rodar o fluxo completo.
