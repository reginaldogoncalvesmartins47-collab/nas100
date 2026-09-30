# Choque de mercado: gap, vela enorme, FVG

Decisao da usuaria: quando o mercado abre com gap, muda o vies, faz uma vela enorme e deixa um fair value gap, a primeira
coisa e **entender o que esta acontecendo com o mercado, sempre rapido e agil**. Sem limite de numero de trades.

## Deteccao (`python scripts/calendar_db.py shock ...`)
- **Gap:** abertura contra o fechamento anterior, em multiplos de ATR (sugestao: ATR de H1). Limiar inicial: 0,5 x ATR.
- **Vela enorme:** amplitude >= 2 x ATR do mesmo tempo grafico (M5). Limiar inicial: 2,0.
- **FVG:** lacuna entre a maxima/minima do candle de 2 barras atras e o candle atual (passe `--h1` e `--l1`).
- Limiares sao **hipoteses** (ajustaveis pelo Claude via `tune`, com evidencia: `shock_gap_atr_min`, `shock_range_atr_min`).
- Ao detectar: abre o **CHOQUE**, marca o **viés como VENCIDO** e lista os **trades abertos** para revisar stop/protecao AGORA.

## Protocolo rapido (orcamento ~5 minutos), nesta ordem
1. **O que mudou:** gap, tamanho da vela e FVG (numeros).
2. **Por que:** `since` -> noticias desde a ultima checagem (com data/hora), calendario da ultima hora, snapshot de
   VIX, Brent, US10Y, ES e DXY (quem se moveu junto e quem nao).
3. **Classificar e diagnosticar:** `shock-diagnose --id N --category petroleo|geopolitica|ia_tech|fed_juros|dados|resultado|liquidez_tecnica|desconhecida --cause TXT --confidence alta|media|baixa --bias-after alta|baixa|neutro`.
   Se a causa for **desconhecida**, a confianca fica **baixa** (nao se inventa explicacao) e se continua procurando.
4. **So depois:** regioes (o FVG deixado vira regiao candidata para reteste, os novos extremos) e o restante do gate.
O choque aberto e o vies vencido aparecem **no topo** da lista de pendencias do `gate`.

## Regra do vies (implementada)
- O vies do dia e registrado com motivo (`bias --set alta|baixa|neutro --reason TXT`). Sem vies do dia = pendencia.
- Choque ou noticia de alto impacto depois de definido => **VENCIDO** => pendencia ate redefinir.
- Dominio: domingo/segunda ja comecam sem vies (o de sexta nao vale).

## Limites
- Quem mede ATR, passa os candles e le as noticias e o Claude; o codigo so calcula, registra e cobra o diagnostico.
- Causa conhecida nao garante leitura certa: confianca media/baixa deve reduzir agressividade (decisao da usuaria).
- Numeros de teste usados aqui eram inventados e nao foram gravados no banco real.
