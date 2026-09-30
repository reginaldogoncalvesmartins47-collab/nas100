# Regra de ganho: como nao travar o bot e como nao devolver o ganho

Objetivo da usuaria: o bot deve **fazer entradas** (nao ser travado) e ser **otimizado na demo** ate a conta real.
Problema real: a entrada foi boa, o trade andou a favor, **voltou tudo e nao fechou a tempo**.

## Tempos graficos
Macro/vies: H1 e H4. Regioes: Fibo H1 (+ refino M15). **Execucao e saida (pavio): M5.** M1-M30 nunca como base do macro.

## 1. Como nao travar o bot
Separar duas coisas que estavam misturadas:
- **Dever de casa (gate):** calendario, noticias, pares, sentimento. No **modo treino** isso **nao bloqueia** a entrada:
  ela e permitida e registrada com `gate_ok` (0/1) e a nota da regiao. Depois, `stats` compara o resultado com e sem
  cada dever de casa. Assim os dados dizem o que realmente ajuda.
- **Protecao de capital (sempre ligada, treino e real):** stop obrigatorio e do lado certo, risco maximo por trade,
  perda maxima do dia e corte total (`rules.json` > `risk`). Isso nunca e desligado.
- **Modo real:** so depois de resultado positivo em amostra grande no treino. Aqui o gate LIBERADO passa a ser obrigatorio.

## 2. Por que o ganho volta (causas comuns)
1. Nao havia plano de saida definido **antes** de entrar.
2. A protecao depende de alguem olhando (PC, bot, Claude a cada 5 min): movimento rapido passa entre duas checagens.
3. Sem protecao progressiva: o trade chegou a +1R ou mais e continuou com o stop original.
4. Sem saida quando a tese invalida (noticia, gap, nivel perdido, par virando contra).

## 3. Organizacao da saida (hipoteses a testar; quem decide e o dado)
1. **Na entrada:** stop + alvo 1 (parcial) + alvo final, tudo definido antes. Sem stop, o sistema rejeita.
2. **Ordens de protecao no broker:** stop e alvo ficam como ordens na corretora, nao dependem do PC ligado nem do Claude.
   O Claude ajusta o stop nas checagens, mas o stop protetor esta sempre ativo. Confirmar na plataforma da Pepperstone o
   que e ordem do servidor e o que e "trailing" executado pelo terminal (o trailing de alguns terminais so funciona com
   o terminal aberto; nao confirmado).
3. **Protecao progressiva:** em +1R, realizar parcial (50%) e/ou mover o stop para o ponto de entrada (break-even);
   depois, seguir o preco com stop atras do ultimo fundo (compra) / topo (venda) em M15/H1 ou por ATR.
4. **Saida por invalidacao:** vies vencido (noticia/gap), perda do nivel de invalidacao do plano, par correlacionado
   virando contra com confirmacao. Sai mesmo sem tocar no stop.
5. **Saida por tempo:** sem progresso em N candles (H: 24 de M5, 2 horas), sai ou reduz.
6. **Evento:** se o trade nao foi montado para o evento, reduzir/proteger antes do horario; se foi (posicionamento
   obrigatorio), o stop e o tamanho ja refletem o risco de slippage.
Atencao: break-even cedo demais tira trades bons no ruido; parcial reduz o ganho dos grandes movimentos. Por isso testar.

## 3b. Alvo = regiao de oferta (compra) ou demanda (venda) e leitura do caminho
Decisao da usuaria: no trade comprado, o alvo e a **proxima regiao de oferta**; na venda, a proxima de **demanda**.
Ela acompanha **como esta a movimentacao ate la**.
- **Regiao-alvo:** vem do mapa de regioes (oferta/demanda do SMC, PDH/PWH, topos iguais, Fibo). Gravar a zona no trade:
  `open-trade ... --zone-low L --zone-high H`. O codigo rejeita zona do lado errado.
- **Alvo operacional (hipotese):** a **borda proxima** da zona, nao o meio nem o topo: o preco costuma reagir na borda
  antes de atravessar. Testar borda x meio x borda distante.
- **Leitura do caminho a cada checagem:** `path --id N --price P --quality forte|fraca|lateral|revertendo --pairs sim|parcial|nao`.
  Olhar: forca do movimento, estrutura de M15/H1 (quebra interna contra?), se os pares continuam confirmando (VIX, juros,
  Brent, ES), obstaculos no meio do caminho (outra zona/liquidez = candidato a parcial) e sinais perto da zona
  (pavios, desaceleracao). O comando mostra quantos R faltam ate a borda.
- **Alerta (hipotese):** caminho fraco/revertendo + pares sem confirmar + trade ja em +1R => considerar proteger
  (parcial, break-even ou trailing). E um aviso, nao uma ordem.
- `stats` passa a mostrar quantos trades chegaram a borda da regiao-alvo e quanto devolveram depois.

### Sinal principal: rejeicao de pavio (calculada das velas)
A usuaria le **rejeicao de pavio**. Para o Claude, **nao precisa enxergar o grafico**: o pavio sai dos valores de
open, high, low e close.
- A cada checagem (logo apos o fechamento de cada candle de **M5**, tempo gráfico da usuaria), ler o **ultimo candle M5 fechado** e rodar:
  `path --id N --price P --quality ... --pairs ... --o O --h H --l L --c C`. O codigo calcula os pavios, detecta a rejeicao
  (criterio-hipotese: pavio >= 50% da amplitude e >= 2x o corpo) e diz se foi **na regiao-alvo** ou no caminho.
- Pavio **contra** o trade, principalmente **na regiao-alvo**, gera alerta para considerar realizar/proteger.
- `wick --open --high --low --close [--atr]` mede um candle isolado.
- **Calibracao:** a usuaria passa exemplos em numeros (OHLC) de rejeicoes que ela considera boas e de outras que nao
  considera, com uma frase de por que. Com eles ajustamos o criterio (50%/2x) ate bater com o dela. Sem isso o criterio
  e palpite.
- **M5 e mais ruidoso** que M15/H1: o criterio pode precisar ser relativo ao ATR de M5. Calibrar com exemplos de M5.
- Limite: os numeros nao mostram contexto que o olho pega de relance (por exemplo, a estrutura em volta). Por isso o
  alerta e um aviso e o criterio e calibrado com os exemplos dela.

## 4. Como otimizar com dados (antes da conta real)
Cada trade entra na tabela `trades` (comandos `open-trade`, `update-trade`, `close-trade`, `stats`):
- **MFE** = quanto o trade andou a favor (em R) no melhor momento. **Devolvido** = MFE - resultado final.
- `update-trade --high H --low L` a cada checagem usa a maxima/minima do periodo (mais exato do que olhar so o preco).
- `stats` mostra: acerto, R medio, MFE medio, quanto devolveu, quantos chegaram a +1R e terminaram em 0 ou negativo,
  resultado por motivo de saida e por estado do gate.
Decisoes guiadas pelos numeros (exemplos de leitura):
- Muitos trades chegam a +1R e terminam em 0 ou negativo => justifica parcial/break-even em +1R.
- Break-even tira muitos trades que depois iriam ao alvo => mover o break-even para +1,5R ou usar trailing por estrutura.
Experimento: rodar variantes em sequencia, uma por vez, com o mesmo numero de trades:
A) stop e alvo fixos; B) break-even em +1R; C) parcial de 50% em +1R + trailing; D) saida na borda da regiao-alvo x meio x borda distante. Comparar R medio e devolvido.

## 5. Limites
- Amostra pequena nao prova nada (30 a 50 trades por variante, no minimo).
- Demo nao simula spread/slippage reais; os numeros do real serao piores.
- MFE depende de o Claude atualizar o trade com a maxima/minima; se faltar checagem, o MFE fica subestimado.
- O sistema so sinaliza e registra; quem executa e a usuaria (ou um robo na corretora, decidido depois).
