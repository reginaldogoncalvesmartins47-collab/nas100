# Licoes e descobertas de 08/10/2026 (memoria do projeto)
Resumo do dia: journal/resumo-diario.md (+US$ 12,94, 5 trades). Este arquivo guarda o que NAO se ve no codigo.
## Operacao
1. Paper Trading precisa estar CONECTADO; conferir no inicio. Como abrir/modificar ordens: item 15 de docs/estado-e-retomada.md e docs/gestao-saida.md.
2. Stop: minimo ~1 ATR de folga; spikes por sessao (pavio sup p90/p95): Asia 12/17, Londres 13/17, NY AM 29/37, NY PM 16/22 pts. Stop de 6 pts (trade 25) foi parado em 1 min; stop da usuaria 10 pts da entrada cortou +36.
3. Protecao em degraus (+25 pts -> 0x0; 50% -> travar 25%; 75% -> travar 50%) e acompanhamento de 1 em 1 min com posicao (cron `* * * * *` ao entrar, CronDelete ao sair).
4. Entradas de evento (T-5) a favor do vies funcionaram: GDPNow +2,33; leilao Bond 30a +7,53. Entradas "perseguindo" depois de queda de 100+ pts precisam de stop 1,5-2 ATR.
5. Falhas do dia: vigia nao disparou 01:15-09:30 (Waller 05:30 e claims 09:30 perdidos); Paper Trading desconectado as 11:00; gate bloqueado por pendencias (viés, calendario, feriados, sentimento, leituras de pares H1/H4, plano do evento) - fazer a rotina da manha logo no inicio.
## Dados e mercado
6. Volume/amplitude por hora (mesma fonte, so 2 dias): docs/volume-por-hora-e-fincept.md. 19h-21h BRT = janela morta.
7. Sessoes (2 anos): sem vies direcional; o util e o tamanho; docs/estudo-sessoes.md.
8. Spike de 13:17 BRT = noticia Trump/Ira (Bloomberg RSS 13:24, 7 min depois do preco); queda de ~400 pts antes do leilao das 14:00 (petroleo/Hormuz, Waller hawkish, chips -3%). Fontes gratis servem de contexto, nao de gatilho (docs/medicao-noticias.md).
9. Juros no painel: titulo OANDA = preco; queda de preco = juro SUBINDO. VIX so vivo 10:30-17:00 BRT.
10. GEX (CBOE/QQQ): regime negativo hoje; muros longe do preco; importancia nao testada (>=20 dias; scripts/gex_teste.py). Dukascopy so entrega o dia anterior (sem M1 de hoje).
## Ferramentas
11. Monitor de noticias (scripts/noticias_monitor.py): liga no inicio da sessao; Monitor expira em 30 min; cron `*/29` rearma.
12. Edge Stats (tools/edge-stats-src + tools/edge-lab; scripts/edge.sh); LuxAlgo MCP hospedado so tem cripto no Edge; Biblioteca e Rastreadores (CC0) servem de referencia.
13. Fincept Terminal/bbterm/kadeconsole: nao resolvem velocidade de noticia; Fincept desinstalado.
