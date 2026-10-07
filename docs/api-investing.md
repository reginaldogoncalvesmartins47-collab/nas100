# Investigacao da API do Investing (02/10/2026) - publica, sem chave, sem login, sem Pro
Metodo: (1) rotas lidas no JavaScript publico que o proprio site baixa; (2) chamadas GET de teste, poucas e so leitura, feitas pela sessao normal do Chrome. NAO foram tocadas rotas de chat/IA, pro-research, pro-reports, creditos, fair-value (exigem conta/assinatura). Termos do site restringem coleta em volume: uso pessoal, poucas chamadas, uma vez. Se o Chrome pedir verificacao 'sou humano', PARAR.
Base: https://endpoints.investing.com/pd-instruments/v1/ (a API devolve erro 400 autoexplicativo com os valores permitidos).
## Confirmado funcionando
| Rota | O que entrega | Parametros |
| calendars/economic/events/{id} | metadados do evento (pais, categoria, importancia high/medium/low, fonte oficial, descricao, page_link) | domain_id |
| calendars/economic/events/{id}/occurrences | historico do evento: occurrence_time (UTC), actual, forecast, previous, preliminary, revised_to_previous, actual_to_forecast | domain_id, limit, cursor (next_page_cursor) |
| calendars/economic/events/occurrences | TODAS as ocorrencias num periodo (+ metadados dos eventos) | start_date e end_date em formato data-hora ISO com Z, country_ids (5 = EUA), importance, categories, cursor. Testado: semana 03-08/11/2025 -> 74 ocorrencias EUA |
| instruments/{id}/charts/events/{intervalo} | noticias (date_time UTC, titulo, url), balancos, dividendos, splits de um instrumento num periodo | from, to (ISO Z), domain_id; intervalo em minusculas: pt1m, pt5m, pt15m, pt30m, pt1h... Testado id 20 (Nasdaq 100): 20 noticias em 2 dias |
| (api.investing.com) financialdata/{id}/historical/chart/ | velas (ms UTC, O,H,L,C,volume) | interval=PT5M, pointscount (maximo 160; maior -> erro 500); datas ignoradas |
| Pagina /central-banks/fed-rate-monitor | probabilidade de cada reuniao do Fed (atual, dia anterior, semana anterior), calculada com futuros 30-day Fed Funds | leitura da pagina (texto) |
| Pagina /earnings-calendar/ | balancos do dia (EPS/receita atual x previsto, valor de mercado, variacao) | leitura da pagina |
## Rotas vistas no codigo, NAO testadas
calendars/holidays; calendars/economic/events/{id}/occurrences/closest; historical/{id}; api/v2/articles/delivery/... (listas de noticias: homepage, breaking-news, most-popular, instruments/{id}/top); api/v1/wdim/.../instruments/{id}/summary ('por que moveu'); api/v1/earnings-calls. Algumas ficam em outro host (api.investing.com devolveu 404 para wdim e articles com o prefixo que tentei).
## Observacoes
- domain_id=7 devolve textos em russo (nomes, descricoes, titulos); descobrir o domain_id de pt-BR/en para titulos legiveis (o slug em page_link e em ingles).
- O filtro de seguranca da ferramenta do navegador esconde resultados que parecem URLs com parametros ([BLOCKED: Cookie/query string data]); nao e bloqueio do Investing.
- Usos uteis: (a) calendario completo por periodo sem varrer IDs; (b) noticias com hora exata por instrumento para cruzar com o preco; (c) Fed Rate Monitor diario para medir 'medo de juros'.
