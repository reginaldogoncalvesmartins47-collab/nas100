# Regras de risco

Conta real: US$ 30 (antes US$ 20; decisao da usuaria). Perda maxima aceita pelo usuario no total: US$ 10 (parar tudo e revisar).
Os limites em dolares (US$ 1 por trade, US$ 3 por dia, corte US$ 10) **nao mudaram** com o novo capital; a usuaria pode ajustar.

| Regra | Valor sugerido |
|---|---|
| Risco por trade | US$ 0,50 a US$ 1 |
| Perda maxima por dia | US$ 2 a US$ 3 |
| Corte total | US$ 10 |
| Trades por dia | **Sem limite** (decisao da usuaria). O que contem o excesso de trades e a perda maxima do dia e o corte total |

Pendente (usuario deve confirmar): lote minimo, valor do ponto e margem do NAS100 na Pepperstone.
Se o lote minimo exigir risco maior que o permitido para o stop do setup, NAO operar esse setup.

## Demo (Paper Trading, saldo US$ 30)
- Mesmas regras do real. Meta: 30 a 50 trades antes de concluir qualquer coisa.
- Paper Trading nao simula spread/slippage reais; em eventos fortes o real tende a ser pior.
- Marcar no diario os "trades de evento" para separar a estatistica.

## Backtest no TradingView
Para validar logica (nao a conta de US$ 30): modo teste ligado, capital 1000, limites diario/total altos.
Comparar em R (multiplos do risco), nao em dolares. Sem o ajuste, o corte de seguranca desliga o teste cedo.
