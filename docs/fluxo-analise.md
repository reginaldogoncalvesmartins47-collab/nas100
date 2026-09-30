# Fluxo de analise (quando o preco chega na regiao)

Decisao v1: regioes = liquidez + Fibo (H1, refino M15). SMC (LuxAlgo) = fator opcional futuro.
Modo: somente sinal. O usuario executa. Numeros em `rules.json` sao hipoteses.

## Passo a passo
1. **Mapa do dia:** listar regioes pontuadas (liquidez valida + Fibo H1 + refino M15). Guardar so as com nota minima.
2. **Vigia (ex.: a cada 5 min, PC ligado):** ler o preco do grafico; se estiver a <= 0,5 x ATR(M15) de uma regiao, disparar a analise.
3. **Analise (Claude):**
   - Viés do dia (macro do usuario). A regiao esta a favor ou contra?
   - Nota da regiao vs minimo (3 a favor / 4 contra).
   - Reacao do mercado: varredura valida + fechamento de volta (ou confirmacao do usuario).
   - Alvo = proxima liquidez oposta; RR >= 2?
   - Horario e limites de risco (lote minimo x stop na conta de US$ 30).
4. **Saida:** "sem setup" (com o motivo) ou sinal com entrada, stop, alvo e nota. Nada de ordem automatica.
5. **Registro:** gravar a decisao e os valores em `journal/diario_trades.csv` (inclusive os "sem setup").

## SMC como fator futuro
Para entrar na pontuacao, precisa de uma versao derivada do indicador com `plot()` de: tendencia swing/interna,
order block ativo mais proximo, EQH/EQL, premium/discount. Nao feito ainda.

## Limites
- Vigia de 5 min nao pega movimento de segundos.
- Dados de volume/CME no plano Basic podem vir atrasados; nao inventar dado ausente.
- Nada aqui foi testado ainda.
