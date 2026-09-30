# Auto-ajuste: o Claude ajusta parametros, com limites

Decisao da usuaria: o proprio Claude vai ajustando algumas informacoes conforme necessario.
Regra: pode ajustar o que e **hipotese**; nunca o que protege capital ou a integridade dos dados.

## O que o Claude PODE ajustar (registro em `rules.json` > `tuning.tunable`, com limite minimo e maximo)
- criterio de pavio em M5 (`wick_min_range_pct` 0,3-0,8; `wick_min_body_multiple` 1-4);
- saida: break-even (R), parcial (R e %), saida por tempo (candles de M5);
- validade das leituras de pares (H1, H4) e aviso de checagem de noticias;
- gap que vence o vies (x ATR de H1);
- nota minima da regiao (a favor e contra a macro).

## O que NUNCA ajusta sozinho (protegido)
- limites de capital (risco por trade, perda do dia, corte total);
- stop obrigatorio; gate obrigatorio no modo real; execucao em conta real;
- nao perseguir manchete; data/hora e fonte das noticias; janela de informacao.

## Como ajusta (`python scripts/calendar_db.py tune ...`)
1. **Evidencia minima:** 30 trades fechados **ou** 10 exemplos da usuaria. Menos que isso: rejeitado.
2. **Um ajuste de cada vez:** so depois de 10 trades fechados desde o ultimo ajuste, para medir o efeito.
3. **Dentro dos limites** de cada parametro.
4. **Com motivo e historico:** cada ajuste grava parametro, valor antigo e novo, motivo, evidencia e modo.
5. **Reversivel:** `tune-revert --id N` volta ao valor anterior. `tune-history` lista tudo.
6. **Modo treino:** pode aplicar sozinho. **Modo real:** so com aprovacao explicita da usuaria.

## Como o Claude decide o que ajustar
Olhando os numeros: `stats` (R medio, MFE, quanto devolveu, resultado por motivo de saida e por estado do gate) e os
exemplos de pavio da usuaria. Regra de bolso: mudar so quando a diferenca aparece de forma consistente na amostra.
Amostra pequena nao autoriza mudanca (o codigo recusa).

## Riscos que a regra tenta conter
- **Ajustar ao ruido:** mexer em parametros depois de poucos trades so ajusta o sistema ao passado recente. Por isso o
  minimo de evidencia e o um-de-cada-vez.
- **Deriva silenciosa:** por isso o historico e o revert.
- **Afrouxar protecao por conta propria:** por isso a lista de protegidos.
- **Ainda e palpite:** os limites e os minimos (30 trades, 10 exemplos, 10 de espera) sao escolhas minhas, que a usuaria pode mudar.
