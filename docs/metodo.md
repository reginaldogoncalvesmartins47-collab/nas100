# Metodo de operacao (NAS100)

Fonte: descricao do usuario na conversa. Itens marcados A DEFINIR ainda nao foram decididos.

## 1. Direcao macro (vies do dia) - decidida pelo usuario
Motores do NAS no dia a dia:
- Brent: em baixa tende a favorecer alta do NAS; em alta pressiona.
- Juros (US10Y): juros subindo pressionam o NAS; caindo favorecem.
- ES: correlacao positiva com o NAS (confirma ou diverge).
- Calendario do dia: antecipar o que o mercado espera (consenso) e se posicionar antes do evento. O usuario NAO evita eventos (FOMC/CPI/NFP): estuda e se posiciona.
- Noticias e geopolitica.
- Volume de Brent/ES/juros como leitura de cenario. Limite: juros (indice) nao tem volume; Brent CFD nao tem volume real; dado da CME pode vir atrasado no plano Basic.
- Painel proprio do usuario: https://analistamacro.prospectia.space/ (A DEFINIR: que dados expoe).

## 2. Entrada - liquidez
Dor principal: acertar a direcao e tomar stop (entrar antes da busca de liquidez).
Abordagem em teste:
- Niveis: maxima/minima do dia anterior, da semana anterior, faixa da Asia e de Londres.
- Gatilho: varredura do nivel + candle fechando de volta a favor do vies.
- Stop atras do pavio da varredura; alvo na proxima liquidez oposta; RR minimo configuravel.
- Medias (semanal, 24h) foram tentadas como suporte/resistencia e nao resolveram.

## 2b. Regioes e liquidez valida
Ver `docs/liquidez-e-regioes.md` (criterios de liquidez valida, Fibo no H1, pontuacao de regioes).

## 3. A DEFINIR
- Gatilho exato alem da varredura (FVG depois da varredura? CHoCH? horario?).
- Como julgar volume do Brent/ES (criterio objetivo).
- Quais horarios de Asia/Londres o usuario considera (defaults no script sao palpite).
- Regras de saida alem do alvo na proxima liquidez (parcial, break-even).
