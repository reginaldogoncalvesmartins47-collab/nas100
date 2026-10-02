# Sessoes, maximas/minimas e varreduras (regra da usuaria, 01/10/2026)

A usuaria decidiu: **o Claude sabe as sessoes e calcula os niveis sozinho; o painel NAO precisa fazer isso.** O painel so mostra a hora do TV.

## Horarios das sessoes (BRT = horario do TradingView; UTC entre parenteses)
| Sessao | Abre | Fecha | UTC |
|---|---|---|---|
| ASIA | 21:00 | 03:00 | 00:00-06:00 |
| LONDRES | 03:00 | 10:30 | 06:00-13:30 |
| NOVA YORK (NY) | 10:30 | 17:00 | 13:30-20:00 |
| - NY AM | 10:30 | 13:00 | 13:30-16:00 |
| - NY almoco | 13:00 | 14:30 | 16:00-17:30 |
| - NY PM | 14:30 | 17:00 | 17:30-20:00 |
Mercado do CFD: fecha 18:00, reabre 19:00 (BRT); a Asia abre 21:00. Fechar posicoes ate 17:55 TV (regra existente).
**Horario de verao:** valido enquanto NY esta em EDT (ate 01/11/2026). Depois que NY/Londres mudarem de horario, Londres e NY ficam 1 h mais cedo/tarde em BRT: reconferir.

## O que o Claude faz com isso
1. **Marcar** a maxima (H) e a minima (L) de cada sessao: Asia, Londres e Nova York (NY AM se precisar de detalhe), da ultima concluida e da anterior.
2. **Status de cada nivel:** VARRIDA = depois que a sessao acabou, algum pavio passou do nivel (high > H ou low < L). ABERTA = ainda nao foi tocada.
3. **Nivel varrido = descartado.** Nivel ABERTO = alvo ou ponto de operacao (liquidez ainda por pegar).
4. **Leitura de sequencia:** observar a ordem das varreduras (ex.: NY AM varrida e a Asia comecando a cair = movimento iniciando). Registrar a hora da ultima varredura.
5. **Confluencia:** viés + preco perto de um nivel ABERTO (maxima = zona de venda, minima = zona de compra; tolerancia ~0,4 x ATR M15, minimo 10 pts) + rejeicao de pavio M5. Zona de atencao, NAO sinal: sem validacao estatistica ainda.

## Como calcular (ferramentas)
- `data_get_ohlcv` do PEPPERSTONE:NAS100 em M5 (count ~400 cobre 2 dias com mercado 24h menos a pausa) e agrupar as velas pela hora (UTC) de cada sessao; H = maior high, L = menor low da sessao; depois da sessao, varrida se qualquer high/low posterior passou do nivel.
- Quando: no briefing (06:13, 08:21, hora cheia), no T-10 de cada evento, a cada checagem de posicao aberta, e quando a usuaria pedir.
- PDH/PDL/MEIO/OTE/NY00 continuam lidos pelo painel (`data_get_pine_tables`, study_filter "Painel"). O painel v3.11 mostra tambem Asia/Londres/NY AM H|L sem o status (a v3.12 com varrida/aberta no arquivo `pine/` NAO foi publicada: no TradingView roda a 3.11).
