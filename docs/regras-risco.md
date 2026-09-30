# Regras de risco

Conta real: US$ 20. Perda maxima aceita pelo usuario no total: US$ 10 (parar tudo e revisar).

| Regra | Valor sugerido |
|---|---|
| Risco por trade | US$ 0,50 a US$ 1 |
| Perda maxima por dia | US$ 2 a US$ 3 |
| Corte total | US$ 10 |
| Trades por dia | 3 a 5 |

Pendente (usuario deve confirmar): lote minimo, valor do ponto e margem do NAS100 na Pepperstone.
Se o lote minimo exigir risco maior que o permitido para o stop do setup, NAO operar esse setup.

## Demo (Paper Trading, saldo US$ 20)
- Mesmas regras do real. Meta: 30 a 50 trades antes de concluir qualquer coisa.
- Paper Trading nao simula spread/slippage reais; em eventos fortes o real tende a ser pior.
- Marcar no diario os "trades de evento" para separar a estatistica.

## Backtest no TradingView
Para validar logica (nao a conta de US$ 20): modo teste ligado, capital 1000, limites diario/total altos.
Comparar em R (multiplos do risco), nao em dolares. Sem o ajuste, o corte de seguranca desliga o teste cedo.
