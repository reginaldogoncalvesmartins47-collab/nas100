# Medicao de atraso das fontes de noticia (iniciada 07/10/2026 ~22h BRT)
Objetivo: saber QUAL fonte gratuita traz a manchete primeiro, em minutos, antes de decidir instalar qualquer "terminal" (Fincept etc.) ou montar coleta automatica de noticias para o Claude.
Script: `scripts/medir_noticias.py` (so biblioteca padrao). Fontes (8): Fed press RSS, CNBC mercados, MarketWatch, Investing.com news RSS, Seeking Alpha market-news (HTML), Google News RSS x3 (Fed/Powell/FOMC; petroleo/Brent/Trump tarifa; Nasdaq/Wall Street).
## Como rodar
- Coleta continua: `python -I scripts/medir_noticias.py coletar 2 1200` (a cada 2 min, por 20 h). Log: journal/medicao_noticias.csv (fonte, titulo, publicado_utc, visto_utc).
- Relatorio: `python -I scripts/medir_noticias.py relatorio` (agrupa manchetes parecidas entre fontes; mostra +min de cada fonte vs a mais rapida da historia e o atraso medio).
## Limites (honestidade)
- "publicado" e a hora que a FONTE informa; Google News mostra a hora de indexacao do Google, nao a da materia original. Investing RSS nao informa hora (fica fora do relatorio).
- Agrupamento por palavras e aproximado: conferir os grupos a olho.
- So vale como conclusao com varias historias de mercado (idealmente um dia de evento: quinta 08/10 tem pedidos de seguro-desemprego 09:30 e Waller 05:30 BRT).
- O PC precisa ficar ligado durante a coleta; o processo some se o Claude/terminal fechar (recomecar o comando).
## Decisao pendente
Com o relatorio de 08/10: se alguma fonte gratuita chega em <= 5 min das demais, montar `scripts/noticias.py` (checagem incremental) ligado ao briefing; so entao avaliar o Fincept (testar no outro PC).
- noticias_monitor.py (Monitor): consulta a cada 45 s; filtro de palavras-chave precisa ser mais estrito (Trump politico gera ruido).

## Primeiro achado real (08/10/2026): spike das 13:17 BRT x manchete
- Spike: UMA vela M1 (13:17 BRT, +113 pts no NAS100; US500 +23,6 pts no mesmo minuto, volume 2x).
- Manchete "Trump diz que os EUA nao atacarao o Ira antes das eleicoes": **Bloomberg (feed RSS publico politics/news.rss) 13:24 BRT**; Google News agregou 13:24-13:37; CNBC 13:53; Reuters sancoes 13:59. Ou seja, o MERCADO MEXEU ~7 min ANTES da manchete mais cedo que achei. Nenhuma fonte gratuita chegou antes do preco.
- Bloomberg tem RSS publico GRATIS: feeds.bloomberg.com/{markets,politics,economics,technology}/news.rss (segue 301 para bloomberg.com/feeds/...). Lista curada (~20 itens, nao e o fluxo completo do terminal). Adicionado ao scripts/noticias_monitor.py.
- Conclusao parcial: o noticiario gratuito serve como CONTEXTO/CONFIRMACAO (explica o movimento minutos depois), nao como gatilho antecipado.
