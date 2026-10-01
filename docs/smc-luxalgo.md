# SMC (LuxAlgo): o que o indicador calcula e como entra no projeto

Fonte: codigo colado pela usuaria (Smart Money Concepts [LuxAlgo], CC BY-NC-SA 4.0, (c) LuxAlgo). **Uso pessoal; manter atribuicao;** uma versao
derivada distribuida precisa da mesma licenca. O codigo de terceiros **nao esta neste repositorio**; aqui fica so a analise.

## O que ele calcula (leitura do codigo, nao rodado)
- **Estrutura:** pivos de swing (padrao 50 barras) e internos (5 barras); BOS/CHoCH quando o **fechamento** passa do pivo.
- **Order blocks:** na quebra, o candle com maior maxima (baixa) ou menor minima (alta) entre o pivo e a quebra, com filtro de volatilidade; mitigado quando o preco o cruza.
- **EQH/EQL:** pivos proximos (limiar 0,1 x ATR(200)), confirmados por 3 barras.
- **FVG** com filtro automatico; **premium/discount/equilibrio**; **Strong/Weak High/Low**; niveis D/W/M.
- **Alertas:** 16 (BOS/CHoCH, order block rompido, EQH/EQL, FVG formado). **Nao** avisa "preco entrou no order block".
- E um `indicator`: **nao faz backtest** e **nao expoe numeros** (so desenha).

## Pontos de atencao
- Pivos de swing so sao confirmados varias barras depois; o order block so aparece na quebra (nao olha o futuro, mas e tardio).
- Em "Weak High" + "Strong Low" o swing e de alta; na caso 02 a macro da usuaria era de baixa: macro manda, SMC e um fator.

## Plano
v1 usa liquidez + Fibo (calculaveis e testaveis). Para o SMC virar fator de pontuacao: uma **versao derivada com `plot()`** de tendencia swing/interna,
order block ativo mais proximo, EQH/EQL e premium/discount, para a estrategia ler via `input.source`. **Nao feito.** Pendente: repo publico ou privado
(afeta onde guardar codigo derivado) e quais configuracoes do SMC a usuaria usa.
