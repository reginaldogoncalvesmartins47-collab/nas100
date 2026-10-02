# Calendario: regra inquebravel e metodo de coleta (usuaria, 01/10/2026)

## A regra
- TODA noticia do calendario (todas as estrelas: dados, falas do Fed, leiloes, balanco do Fed, payroll, CFTC...) recebe uma ENTRADA A MERCADO 5 MIN ANTES, no lado do vies, com stop e alvo no ticket.
- Unica excecao: ja existe posicao ATIVA no MESMO lado (ai so gerir). Se o vies virou: fecha a oposta e entra.
- CADA noticia tem analise propria (pagina do evento no Investing com historico, protocolo de tema, vies e registro no placar), mesmo no mesmo horario. Execucao: uma ordem por lado (se os vies do horario concordam, e uma ordem so; se divergem, vale o de maior peso e registra a divergencia). Vies obrigatorio com 1 linha de motivo; na demo R:R/espaco viram so aviso. Stop obrigatorio, lote 0,1, sem martingale.
- Se uma entrada NAO abrir, avisar a usuaria na hora (motivo), nunca em silencio.
- Resumo: CLAUDE.md (secao "CALENDARIO: REGRA INQUEBRAVEL"), docs/playbook-noticias.md, docs/enciclopedia-noticias.md (parametros por evento).

## Rotina de manha (antes de qualquer analise)
1. Coletar a tabela COMPLETA (abaixo), com estrelas, projecao e anterior.
2. Gravar no banco (`python scripts/calendar_db.py upsert arquivo.json`; tabela `events`, campos date,time_brt,country,event,stars,actual,forecast,previous).
3. `CronCreate` de UMA execucao em T-5 para cada horario distinto (a ANALISE continua sendo de CADA noticia; so a ordem e uma por lado) (one-shot, ex.: payroll 09:30 -> `25 9 D M *`).
4. Conferir `CronList` contra a tabela e mandar a lista de horarios agendados a usuaria.
5. Fim do dia: eventos x entradas feitas x faltantes em journal/resumo-diario.md.

## ROTINA DIARIA OFICIAL (procedimento da usuaria, colado em 01/10/2026) - substitui a "Rotina de manha" acima quando houver conflito
1. TODO DIA acessar https://br.investing.com/economic-calendar
2. Salvar TODOS os eventos relacionados ao NAS100 e o horario em que acontecem.
3. Gerar a TABELA DO DIA (arquivo docs/tabela-eventos-AAAA-MM-DD.md): hora | evento | importancia (estrelas lidas do icone) | atual | projecao | anterior | LINK DA PAGINA DO EVENTO (com o historico).
4. Com a tabela preenchida: pesquisar o HISTORICO de cada evento (abrir o link) e analisar o VIES da noticia, ALTA ou BAIXA, uma a uma (nunca agrupar por horario).
5. Noticia de 1 ESTRELA: SEMPRE analisar a DIRECAO MACRO DO DIA: em 1D o NAS100 esta caindo ou subindo? E a noticia pode POTENCIALIZAR isso? (vies = a favor da direcao macro 1D, salvo historico claro em contrario.)
6. Noticias de 2 e 3 ESTRELAS: priorizar o SENTIMENTO GERAL, sempre com CONFLUENCIA de juros (US10Y/2a), Brent, ES e NQ (NQ1! = futuros do Nasdaq; atraso ~10-13 min no TradingView). Vies so se a confluencia apoiar; sem confluencia, vies neutro de baixa confianca.
7. Registrar tudo na tabela (coluna vies/confianca) e no placar (docs/reacao-noticias.md) apos o evento.

## Metodo de coleta (Investing, via extensao do Chrome)
NAO usar get_page_text nem find: nao trazem a tabela inteira nem as estrelas. Usar `javascript_tool` na pagina https://br.investing.com/economic-calendar/ (horario exibido = BRT; abas Hoje/Amanha mudam o dia; para amanha clicar na aba "Amanha" e esperar ~3 s).

Linhas do dia (so EUA; saida do tool corta em ~1000 caracteres: filtrar por faixa de horas em chamadas separadas):
```js
await new Promise(r=>setTimeout(r,2500));
const stars=r=>[...r.querySelectorAll('svg')].slice(0,3).filter(s=>(s.getAttribute('class')||'').includes('opacity-60')).length;
[...document.querySelectorAll('tr')]
  .filter(r=>/^\d{2}:\d{2} US /.test(r.innerText.replace(/\s+/g,' ').trim()))
  .map(r=>r.innerText.replace(/\s+/g,' ').trim().slice(0,80)+' *'+stars(r)).join('\n')
```
- Estrelas: nos 3 primeiros `svg` da linha, classe com `opacity-60` = estrela preenchida, `opacity-20` = vazia. NUNCA deduzir importancia pelo nome do evento (o balanco do Fed das 17:30 tem 3 estrelas).
- Numeros apos o nome: 3 numeros = atual, projecao, anterior; 2 = projecao, anterior (antes do dado); 1 = so anterior. Nao confundir atual com projecao.
- Para outros paises trocar `US` por `UK|EU|JP|CN` etc. (so 3 estrelas costumam importar para o NAS100).
- Depois do dado: reler a linha para pegar o ATUAL e calcular a surpresa (`calendar_db.py set-actual`).

## Erros que nos custaram (01/10/2026)
Perdi o leilao Bill 4s (12:30, NAS100 -62 pts), o balanco do Fed (17:30, 3 estrelas) e as falas das 10:05/11:00 porque so guardava eventos de 2-3 estrelas e usava ferramentas de texto. Nunca mais: tabela completa, estrelas lidas do icone.
