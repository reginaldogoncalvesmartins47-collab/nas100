# Relatorio da descoberta (30/09/2026, parcial)

## Funciona
- MCP TradingView conectado (CDP), leitura de velas/quote, screenshot, cliques na UI.
- Paper Trading conectado nesta sessao (nao estava). Saldo US$ 40.159,27; historico de 463 trades lido.
- VIX, Brent (UKOIL), US10Y, DXY carregam em tempo real (VIX fora de pregao).

## Fatos que mudam o plano
- **1 ponto do NAS100 = US$ 1,00 com tamanho "1"** (confirmado por 4 trades). O "0,1" dela seria US$ 0,10/ponto.
- **Conta demo (US$ 40k) nao reflete a real (US$ 30).** Com US$ 1/ponto, um stop de 30 pts = US$ 30 = a conta real inteira.
- **Historico demo: 463 trades, 46% acerto, fator de lucro 0,60, expectativa -US$ 129/trade.** Nao e prova do metodo; e o ponto de partida.
- ES vem **atrasado** (CME_MINI_DL).
- Nenhuma corretora real conectada; Pepperstone real nao lida.

## Nao feito ainda
Scripts dos indicadores dela (D), painel macro (E), Investing/sentimento (F), specs Pepperstone (G),
teste de aceitacao com ordem + stop/alvo (H), consumo de tokens (I).

## Perguntas so dela
1. Posicao de US$ 0,10/ponto (0,1) e viavel na real? Qual o stop maximo em pontos que ela aceita (US$ 15 de perda = 150 pts a 0,1)?
2. Perda total aceita: US$ 15 ou US$ 10?
3. A demo deve usar tamanho 1 (US$ 1/pt) ou 0,1 para simular a conta real?

## Atualizacao (D/E/F parcial)
- 83 scripts Pine dela listados; codigo ainda nao lido. Muita redundancia (varias versoes do mesmo sinal).
- Painel macro (analistamacro.prospectia.space) le por texto, mas avisa cache antigo e tem numeros que nao batem com a Pepperstone.
- Investing abre logado; linhas do calendario so por screenshot.

## Conclusoes do Claude
1. O gargalo nao e falta de indicador (21 no grafico, 83 salvos): e a demo ter expectativa -US$129/trade e R:R 0,68. Mais sinal nao conserta isso.
2. Tamanho 1 = US$1/pt: a demo a US$ 40k nao treina o risco da conta de US$ 30. Treinar com 0,1 (US$ 0,10/pt).
3. Antes de automatizar: reduzir a ~3 fontes (viés macro + regiao + gatilho M5) e medir em 30-50 trades.
4. ES atrasado e painel com cache: viés nao pode depender so de fonte unica.
