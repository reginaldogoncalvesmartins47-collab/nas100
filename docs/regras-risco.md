# Regras de risco

## O que a usuaria decidiu
- Conta: **US$ 30** (antes US$ 20).
- Pode perder ate **uns US$ 15 no total** (incerto: antes disse US$ 10) - corte: parar tudo e revisar.
- **Meta de ganho:** pelo menos US$ 25 a 30, **sem teto** ("o ceu e o limite"). Periodo nao informado.
- **Sem limite** de numero de trades.
- Quer **liberdade para operar**: o bot nao deve ser travado na demo.

## O que NAO foi decidido por ela (e eu tinha colocado como regra por engano)
- Risco maximo por trade: **nao definido**. (US$ 0,50-1 era sugestao minha e nao funciona bem: obrigaria stops curtos demais.)
- Perda maxima do dia: **nao definida**.
Ate ela definir, esses dois nao existem como regra. Antes do **real**, o risco maximo por trade precisa ser definido por ela
(o `ready` cobra isso).

## Como o stop e o tamanho funcionam sem esses limites
- **O stop e definido pelo mercado** (alem do extremo do pavio + folga de ATR), nao pelo dinheiro. Um stop apertado so para caber
  num valor em dolares seria parado por ruido.
- O **lote** e o minimo (ou calculado). O **risco real** de cada entrada e **mostrado e registrado** (`entry-check --usd-per-point`),
  para aprender qual risco o stop do mercado impoe na conta de US$ 30.
- O valor do ponto e o lote minimo na Pepperstone ainda precisam ser confirmados.

## O que para o bot e o que so avisa
| Regra | Treino (demo) | Real |
|---|---|---|
| Stop obrigatorio e do lado certo | **Para** (sem stop nao ha R) | **Para** |
| Risco maximo por trade | Nao definido; se a usuaria definir, so avisa | **Exige estar definido**; acima disso, para |
| Perda do dia | Nao definida | Se definida, para |
| Corte total (US$ 15, a confirmar) | So avisa e registra "no real teria parado" | **Para** |
| Gate / nota da regiao | So registra | Gate obrigatorio; nota minima vale |
| Numero de trades | Sem limite | Sem limite |
Motivo: na demo o dinheiro e ficticio e parar cedo interromperia a coleta de dados que permite aprender rapido.

## Backtest no TradingView
Para validar a logica (nao a conta): modo teste ligado, capital 1000. Comparar em R, nao em dolares.

## Pendencia importante: tamanho real das posicoes (inferido do caso 02)
No print do caso 02 a posicao aparece como **-1** (venda de 1) com **+US$ 24,30**. Se 1 = uma unidade do NAS100 a US$ 1 por ponto,
**um stop de 20 pontos custaria ~US$ 20**, quase a conta inteira de US$ 30, e a margem de 1 unidade seria muito maior que a conta.
Isso indica que o **Paper Trading da usuaria pode estar com saldo bem maior que US$ 30** (o padrao costuma ser alto; nao confirmado).
Se for isso, os resultados de demo **nao representam** a conta de US$ 30. **Confirmar:** tamanho usado, saldo do Paper Trading e valor do ponto.
