# NAS100 Macro + Liquidez (Pine Script v5)

Rascunho de estrategia baseado no operacional descrito:

1. **Direcao macro (score 0-3):** Brent caindo, juros 10Y caindo e ES subindo favorecem compra no NAS; o inverso favorece venda.
2. **Liquidez:** entrada na varredura de um fundo/topo anterior (pavio passa o nivel e o candle fecha de volta).
3. **Volume:** exige volume acima da media (no CFD e tick volume, nao volume real).
4. **Risco:** risco fixo em US$ por trade, stop alem do pavio + folga de ATR, alvo em multiplo de R, maximo de trades por dia, perda diaria maxima e corte total.
5. **Horario:** 06:00-23:20 (Brasilia), seg-sex.

## Como testar
1. TradingView > Pine Editor > cole `nas100_macro_liquidez.pine` > Add to chart.
2. Grafico `PEPPERSTONE:NAS100`, M5 ou M15.
3. Aba **Strategy Tester** para ver resultado (win rate, R, drawdown).
4. Se algum simbolo de macro nao carregar no plano Basic, troque em Inputs (Brent, 10Y, ES).

## Limites conhecidos
- E um **ponto de partida**: as regras exatas (janela do Brent, pivots, volume) foram assumidas e precisam ser ajustadas ao operacional real.
- O backtest no TradingView nao simula spread/slippage reais da Pepperstone.
- Se o lote minimo exigir risco maior que o configurado, o trade e ignorado (protecao da conta de US$ 20).
- Noticias/geopolitica nao entram na regra; servem de filtro manual.
- Nao executa ordens: gera sinais e alertas. Execucao automatica exige robo na plataforma da corretora.
