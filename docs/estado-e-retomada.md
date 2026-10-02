# Estado e retomada (escrito em 01/10/2026, fim do dia) - LEIA ISTO EM UMA SESSAO NOVA

Uma sessao nova do Claude NAO lembra da conversa. Este arquivo + CLAUDE.md + docs/ sao a memoria. (A memoria automatica do Claude fica fora da pasta, em C:\Users\User\.claude-conta2\projects\...\memory\; os pontos importantes dela estao repetidos aqui.)

## 1. Quem e a usuaria e como trabalhar com ela
- Nayara (usa "ela"), NAO tecnica. Falar em portugues simples, direto, sem enrolar. O psicologico/ansiedade e o inimigo dela; ela esta cansada de "achar" e quer metodo.
- Quer **direcao** (ALTA ou QUEDA) e **previsibilidade**. "Neutro" so com justificativa plausivel (e mesmo assim dizer o lado de menor risco e o gatilho). **Sem pontas soltas**: todo cenario com condicao -> acao -> invalidacao -> alvo.
- **Separacao de papeis (proposta em 01/10, aguardando o ok dela):** ideias dela entram como "hipotese da usuaria"; o Claude avalia e DECIDE e assina. Se ela quiser executar contra a analise: "override", trade etiquetado OVERRIDE no diario e fora do placar do metodo. Ela disse que nao deve se intrometer na analise do Claude.
- Conta REAL tem so US$ 30 (perda aceita 'uns US$ 15'); NADA do que esta flexibilizado na demo vale para o real. Real so apos `ready` + autorizacao dela. Nunca fazer deploy sem pedir (regra do CLAUDE.md da pasta raiz).

## 2. Estrategia atual (decisao dela, 01/10/2026)
**Operar SO NOTICIAS (calendario financeiro), em demo (Paper Trading do TradingView), sem ficar caçando regiao no grafico.** O grafico entra como contexto (painel). Objetivo: medir se o VIES do Claude acerta mais do que erra (placar em docs/reacao-noticias.md; so concluir com ~20 eventos).
- **Cada noticia (todas as estrelas) tem analise PROPRIA, mesmo no mesmo horario** (pagina do evento no Investing com historico, protocolo de tema, vies proprio). Execucao: uma ordem por lado.
- **Entrada a mercado 5 min antes** (T-5, relogio do TradingView) no lado do vies, com stop e alvo no ticket; lote 0,1; sem martingale; nao duplicar posicao no mesmo lado; se o vies virou, fecha a oposta e entra. R:R e espaco = so aviso na demo; stop obrigatorio. Alvo maior (proximo nivel relevante ou >= 1,5x o risco) com protecao (zero a zero a +50% do caminho; travar ~40% a +75%; stop positivo ANTES de esticar alvo).
- **Protocolo de tema antes do vies:** tema -> quando foi abordado pela ultima vez -> como o mercado reagiu -> o que mudou -> vies+confianca+invalidacao. Tema fora de juros/inflacao/emprego = neutro (mantem posicao, nao inverte por palpite).
- **1 estrela:** checar direcao macro 1D e se a noticia potencializa. **2/3 estrelas:** sentimento com confluencia juros, Brent, ES, NQ.
- **Vies vivo** (painel e contexto, nao lei): invalidacao escrita na entrada; mudanca de estrutura = >= 2 de 4 evidencias (quebra de estrutura M15 ou 2 fechamentos alem de nivel-chave; confluencia virada em 2 leituras; conteudo da noticia contradiz; preco aceita alem do nivel); nunca inverter por 1 vela; vies > 30 min sem reavaliar = vencido.
- **Antes de mudar stop/sair:** checklist de cenario (juros, Brent, noticias 30 min, proximo evento, estrutura) e registrar o motivo.
- **Fechar toda posicao as 17:55 (relogio do TV)**; mercado fecha 18:00, reabre 19:00, Asia 21:00 (entradas depois das 19:00 liberadas, ex.: Logan 19:45).
- Diario obrigatorio por trade (journal/diario_trades.csv + resumo-diario.md + open/close-trade no banco).
- Gate `python scripts/calendar_db.py gate` = LIBERADO antes de ordem (renovar leituras H1 a cada ~50 min e H4 a cada ~230 min: VIX, Brent, US10Y, ES, DXY; usar add-read quando algo mudou, nao so renew-read com 'nada mudou').

## 3. Rotina diaria (checklist)
1. **Calendario** (docs/calendario-regra-e-coleta.md): abrir https://br.investing.com/economic-calendar/ via extensao do Chrome, `javascript_tool` nas linhas <tr> (estrelas = 3 primeiros svg com classe opacity-60); gerar docs/tabela-eventos-AAAA-MM-DD.md (hora, evento, estrelas, atual, projecao, anterior, link do historico); gravar no banco.
2. **Painel:** no TradingView, indicador "Painel NAS100 Compacto"; preencher o campo "Eventos de hoje, BRT"; ler com `data_get_pine_tables` (study_filter "Painel").
3. **Briefing de mesa** (docs/briefing-horario.md): 06:17, 08:25 e de hora em hora na sessao de NY.
4. **Para cada evento:** pagina do evento (historico) + protocolo de tema + vies; agendar a entrada (T-10 no relogio do PC) e a gestao pos-evento (monitor de 4 em 4 min por ~25 min).
5. **17:55 TV:** fechar tudo. Fim do dia: lista eventos x entradas x faltantes; placar em docs/reacao-noticias.md.

## 4. AGENDAMENTOS (CronCreate e SESSION-ONLY: somem ao fechar o Claude; RECRIAR na sessao nova)
Relogio do PC fica ~2-7 min ATRAS do TradingView: agendar T-10 no relogio do PC e conferir a hora no TV antes de entrar. Cron one-shot: `M H D MES *` com recurring:false.
- Briefing recorrente (dias uteis): `13 6 * * 1-5` (06:17), `21 8 * * 1-5` (08:25), `27 10-16 * * 1-5` (de hora em hora, NY). Prompt: "rodar docs/briefing-horario.md" + direcao obrigatoria + sem pontas soltas + vies vivo + registrar em journal/briefings/AAAA-MM-DD.md.
- Entradas de eventos (1 por horario distinto, T-10 PC): prompt padrao = "entrada 5 min antes: gate/renovar leituras, painel, protocolo de tema, vies, ticket com screenshot em cada passo, registrar, avisar se nao abrir ordem".
- Agenda que estava criada para **sexta 02/10** (recriar se a sessao fechou): payroll 09:25 TV (cron 09:20 PC; ler docs/briefing-2026-10-02-payroll.md), 11:00 (cron 10:50), 14:00 (13:50), 15:00 (14:50), 16:30 CFTC (16:20).
- Gestao de posicao aberta: monitor `*/4` com leitura do texto da noticia, degraus de protecao e cenario antes de mudar; fechamento as 17:55 TV.

## 5. Armadilhas das ferramentas (aprendidas na dor)
- **Ticket (TradingView MCP, coordenadas):** clique direito numa area VAZIA do grafico fora da tabela do painel, ex.: (800,250) (em (1000,660) cai na tabela do painel -> menu do indicador; "Adicionar ordem" fica em ~(950,490)) -> screenshot -> "Adicionar ordem" ~(1170,532) -> lado: Venda (620,222) / Compra (815,222) -> toggles TP (893,531) e SL (893,614) -> campos (700,568) e (700,652) (duplo clique, Ctrl+A, digitar) -> screenshot de conferencia -> Confirmar (720,788) -> Alt+R -> conferir em Paper Trading (365,810; abas Posicoes (110,216), Historico de negociacao (769,216); fechar posicao: X da linha ~(1160,309); minimizar painel (1135,19)). SEMPRE screenshot em cada passo (menu/ticket mudam de lugar). Nunca os botoes VENDA/COMPRA do canto do grafico. Nunca o X da etiqueta no grafico (converte limite em mercado). Cancelar ordens so pela aba Ordens.
- **Relogio:** PC atras do TV (2-7 min). Gate vence (H1 60 min, H4 240 min).
- **Extensao do Chrome** cai: reconectar; get_page_text/find nao trazem a tabela do Investing (usar javascript_tool); a saida do JS corta ~1000 caracteres (filtrar por faixa de horas). `tabs_context_mcp` antes de usar abas; fechar abas que abrir.
- **Editor Pine:** abrir com ui_open_panel("pine-editor"); `pine_new` ANTES de `pine_set_source`; o botao circular ao lado do nome ATUALIZA a instancia do grafico (nao clicar quando o editor estiver com codigo de OUTRA pessoa; ler e fechar sem salvar). Pine v5: `str.tostring` nao aceita "+#;-#;0". Conferir `chart_get_state` (ids/nomes) antes e depois. "!" vermelho no indicador = erro de execucao: clicar e ler.
- **Terminal:** o verificador de seguranca do Bash falha as vezes (erro transitorio): tentar de novo ou usar Read/Edit/Write.
- **Fontes:** resumo de busca pode estar errado: confirmar numeros em fonte primaria (federalreserve.gov, BLS). Dados de busca nao sao fato ate checar.

## 6. Arquivos e onde as coisas estao
- Regras: CLAUDE.md (secoes novas), docs/playbook-noticias.md, docs/calendario-regra-e-coleta.md, docs/gestao-saida.md (itens 2, 5, 6, 7), docs/briefing-horario.md (prompt da usuaria + adaptacao), docs/enciclopedia-noticias.md (regime, parametros por evento, correcoes), docs/reacao-noticias.md (placar), docs/briefing-2026-10-02-payroll.md, docs/analise-dia-2026-10-01.md (post-mortem).
- Banco: data/calendario.db (fora do git) via scripts/calendar_db.py (gate, add-read, renew-read, open-trade, close-trade, bias --set, upsert...). Armadilha: migration via Management API nao aparece em schema_migrations (regra da raiz).
- Painel: pine/painel_noticias_nas100.pine esta na v2; a v3.1 (compacta: confluencia + mapa de regioes PDH/MEIO/OTE/NY00/PDL + CRT D1 + ontem/EMA20 + sessoes + ATR + relogio) vive no TradingView (script salvo "Painel Noticias NAS100 1", titulo "Painel NAS100 Compacto"). Sincronizar o arquivo (pendencia).
- Script da usuaria: "PAINEL UNIFICADO NAYARA" (ICT: PDH/PDL/MEIO/OTE79/NY 00:00/CRT/cadeia de sessoes; contexto de volume HTF/LTF; gatilhos que ela NAO quer usar) NAO esta salvo na conta (ela tem o codigo em outro TradingView). Base salva: "VIES NAYARA + PDH/PDL". As porcentagens da cadeia de sessoes (69,8/59,2/58/55,7%) tem ORIGEM DESCONHECIDA/nao validada.
- Dados: C:\Users\User\Desktop\TRADING PEIXE GRANDE\utils\NAS100 Historical Data.csv (diario 2006-2026, 5.037 dias; nao valida sessoes, precisa intradiario). Achados: dia sobe 55%; direcao de ontem nao muda nada; CRT venda (1.105 dias): fecha abaixo da abertura 57,4% (base 45%); CRT compra: sem vantagem.
- Seguranca: nao tocar abas de corretora/banco; nao ler .env de outros projetos.

## 7. Resultado de 01/10/2026 (demo, lote 0,1)
10 trades, dia **-US$ 30,80**, saldo demo ~US$ 40.128,47. Acertos: venda ISM (+8,78), balanco do Fed (+2,88), acidente (+1,39). Perdas: 3 stops de madrugada (-16,87), compra "velona" (-9,45), compra tatica (-11,60), venda Jefferson (-2,39), compra Bowman (-3,54). Causas: sem rotina fixa, tons presumidos sem checar o tema, coleta incompleta do calendario (perdi leilao 12:30, balanco do Fed, falas), viés velho que nao acompanhou a mudanca de estrutura (CHoCH de alta ~12:30), entradas por sugestao sem fechar com a propria analise. Reconstrucao: com o painel, os trades 1-3, 6, 7 e 9 provavelmente seriam evitados (~+US$ 10 no dia), com ressalva de retrospectiva.

## 8. PENDENCIAS (em ordem)
1. **Auditoria das regras** + fonte unica: atualizar rules.json para o modo noticias (hoje diz que 'treino nao trava por gate', tem regras de regiao/gatilho M5 e R:R 1,5 que conflitam). Marcar cada regra: seguida / violada / obsoleta / conflitante.
2. **Bloco de ESTRUTURA no painel:** ultimos 2-3 topos/fundos M15 e H1, estado (HH/HL, LH/LL), ultimo BOS/CHoCH (direcao, nivel, ha quantos min), topos/fundos iguais (liquidez), faixa estreita (acumulacao/distribuicao). Antes: a usuaria valida as definicoes e diz como marca distribuicao (quantos topos? em que tempo grafico?).
3. Aguardando o ok dela: separacao de papeis (hipotese/override) e placar "sombra" para noticias de baixo impacto (registrar vies sem operar).
4. Validar a cadeia de sessoes com dados intradiarios (pedir o arquivo M5/M15 ou o relatorio de onde saiu 69,8%).
5. Reconectar/validar a extensao do Chrome e preencher os LINKS DO HISTORICO na tabela do dia.
6. (feito em 01/10) pine/ sincronizado com a v3.1.
7. Renovar agendamentos (briefing e entradas) a cada sessao e a cada 7 dias.
8. Escrever/atualizar docs/tabela-eventos-AAAA-MM-DD.md todo dia; preencher a secao 6 do briefing do payroll apos o evento.

- **Fonte regular de noticias (01/10/2026):** Seeking Alpha, WebFetch https://seekingalpha.com/market-news (manchetes + hora ET). Consultar em todo briefing, em toda checagem de posicao aberta e apos cada evento do calendario. Detalhes em docs/briefing-horario.md.
