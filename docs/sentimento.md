# Regra 5: sentimento do mercado (antes de qualquer entrada)

Decisao da usuaria: o Claude precisa entender o sentimento do mercado, usando Finviz e outras fontes.
O gate exige **pelo menos 2 fontes registradas no dia** (`add-sentiment`).

## Fontes candidatas (a usuaria ajusta)
| Fonte | O que mostra | Observacao |
|---|---|---|
| Finviz | Mapa de calor por setor/acao, futuros, noticias | Conferir se o dado gratuito vem atrasado; nao confirmado |
| CNN Fear & Greed | Indice de medo/ganancia | Diario |
| CBOE put/call | Protecao vs aposta de alta em opcoes | Nao confirmado o acesso gratuito |
| AAII | Pesquisa de sentimento de investidores | Semanal |
| CFTC COT | Posicionamento de grandes agentes em futuros | Semanal (divulgado na sexta) |
| VIX | Medo implicito | Ja coberto pela leitura dos pares (H1/H4) |

## Como registrar
`python scripts/calendar_db.py add-sentiment --source Finviz --metric "mapa setorial" --reading risk_on|risk_off|neutro|misto --value V --note N`
Ex.: semicondutores e tecnologia fortes no mapa = risk_on; defensivos liderando = risk_off. Uma leitura e uma
opiniao fundamentada, nao um numero magico.

## Acesso
Como o Investing: **so leitura da pagina no navegador (extensao), sem scraper**. Conferir os termos de cada site.
O que nao puder ser lido, a usuaria cola (print/texto).

## Para que serve
Contexto para o posicionamento antes do evento e para julgar se um movimento e confirmado ou suspeito.
Nao e sinal. Sentimento extremo pode indicar exagero, e isso pede cuidado, nao entrada automatica.

## Limites
- Nenhuma dessas fontes foi testada aqui; nao sei o que o plano gratuito de cada uma entrega.
- Duas fontes concordando nao garantem nada; discordancia entre elas deve ser registrada, nao escondida.
