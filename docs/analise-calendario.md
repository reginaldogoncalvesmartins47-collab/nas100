# Regra 1: analisar o calendario economico antes de qualquer entrada

O usuario NAO evita eventos: estuda e se posiciona antes. Por isso o calendario nao e um "bloqueio": e uma
analise obrigatoria. **Sem analise do calendario feita no dia, nao ha sinal (falha fechada).**

## O que analisar (horario de Brasilia)
1. **Lista do dia:** hora, pais, impacto, anterior, consenso (e realizado, quando sair).
2. **EUA que movem o NAS:** CPI, PCE, NFP, FOMC (decisao, ata, falas do Fed), PIB, ISM, varejo, pedidos de
   seguro-desemprego, leiloes do Tesouro (juros).
3. **Empresas e tecnologia:** resultados de gigantes de tecnologia/semicondutores e eventos de IA que mexem com o indice.
4. **Feriados e horario reduzido** nos EUA.
5. **Expectativa do mercado:** consenso, probabilidades de juros, tom das noticias; como o preco ja esta posicionado.
6. **Cenarios:** realizado acima / em linha / abaixo do consenso -> o que tendem a fazer NAS, juros, Brent e ES, e em quais regioes.
7. **Geopolitica e petroleo** do dia.

## Janelas
- **Antes:** posicionamento do usuario permitido; o Claude comenta o plano dentro do cenario.
- **No instante:** marcar como trade de evento (spread/slippage piores; Paper Trading nao simula isso).
- **Depois:** ler a reacao contra o consenso antes de novo sinal.

## Fonte principal: Investing.com (escolha da usuaria)
- Calendario: https://br.investing.com/economic-calendar (fuso Brasilia, pais EUA, importancia 2 e 3 estrelas).
- Capturar: hora, pais, evento, estrelas, atual, projecao, anterior e a previa do evento quando houver.
- Acesso: ler a pagina aberta e logada no navegador do PC da usuaria (extensao do navegador). **Nao guardar senha em arquivo.**
  Conferir os termos de uso do Investing antes de automatizar; sites assim costumam ter protecao contra robos (nao testado).
- Fallback que funciona hoje: colar print ou texto do calendario na conversa.
- Motivo: em 30/09/2026 uma busca na web trouxe dados errados (PIB projetado 5,0% vs 1,5% no Investing).

## Leitura da surpresa (hipotese, o preco manda)
- Inflacao/juros abaixo do consenso = leitura dovish (tende a favorecer o NAS); acima = hawkish (pressiona).
- Crescimento/emprego acima do consenso = ambiguo (bom para lucros, ruim se empurrar juros): depende do regime.
- A reacao real do preco, nos niveis do mapa, vale mais que a leitura teorica.

## Fontes e confiabilidade
- Cruzar **pelo menos 2 fontes**. Se divergirem (valores, horarios, dia da semana), dizer e nao assumir.
- Nao inventar dado ausente. Horarios: converter ET para Brasilia (em setembro, ET = UTC-4; Brasilia = UTC-3: +1h).

## Modelo de briefing
```
Data: ____   Fontes: ____ / ____
Eventos (BRT): hora | evento | impacto | anterior | consenso | realizado
Empresas/IA/feriados: ____
O que o mercado espera: ____
Cenarios: acima ____ | em linha ____ | abaixo ____
Brent/geopolitica: ____
Conclusao do calendario: (liberado / liberado com cuidado / dados insuficientes) + motivo
```
