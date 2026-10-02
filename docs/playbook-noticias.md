# Playbook de noticias (especializacao pedida pela usuaria em 01/10/2026)

Foco: operar a reacao do NAS100 aos eventos do calendario, nao ficar caçando regiao o dia todo.
Resultados de amostra pequena NAO sao prova (ver docs/reacao-noticias.md). Nada aqui promete meta.

## Antes do evento (T-30 a T-5 min)
1. Evento esta no banco? (inclui leiloes do Tesouro e falas do Fed, mesmo 1 estrela: movem juros.)
2. Surpresa provavel: projecao vs anterior vs componentes/regionais. Direcao e tamanho esperados.
3. Regime atual: juros no topo + petroleo > 100 => numero forte/inflacao = negativo para NAS100.
4. Plano ESCRITO: direcao, invalidacao, stop alem da liquidez + ~30 pts (derrapagem), alvo, R:R >= 1,3, risco <= US$ 7.
5. Sem espaco ou sem R:R => nao entra. Sem evento bom => fica de fora (e normal).

## Entrada e saida
- Entrada a mercado 5 min antes, na direcao do vies (regra da usuaria). Ticket completo, screenshot em cada passo.
- 1a vela exagera e devolve ~50% em 5-10 min: sair em 20-25 min, proteger/parcial se andar a favor.
- Nao operar reacao de noticia velha; nao duplicar posicao.

## Depois (aprender)
- Registrar em docs/reacao-noticias.md: previsto x real, vela do evento, depois de 5/10/20 min, o que o plano acertou.
- A cada ~10 eventos: o que se repete? So entao propor ajuste de hipotese (tune), nunca de limite de capital.

## Calendario a cobrir (fonte: Investing)
Dados 2-3 estrelas + leiloes do Tesouro + falas de dirigentes do Fed. Hoje: Jefferson 14:30, Bowman 16:00, Williams/Cook 16:30, Logan 19:45.

## REGRA DA DEMO (usuaria, 01/10/2026 ~13:20) - substitui "so entra com R:R >= 1,3 e espaco"
Objetivo: medir se o VIES do Claude acerta mais do que erra. Para isso:
- Sempre ter um vies (compra/venda) por evento, com 1 linha de justificativa. "Sem trade" nao existe na demo.
- Sempre entrar a mercado 5 min antes, no lado do vies. R:R e espaco viram AVISO (anotar), nao filtro.
- Mantem sempre: stop obrigatorio (alem da estrutura + ~30 pts), TP/SL no ticket, lote 0,1, sem martingale, sem duplicar.
- Placar: por evento, vies, entrada, resultado em +20 min e acertou s/n em docs/reacao-noticias.md. Ler o placar so com ~20 eventos.
- Conta REAL: nada disso vale; continuam os limites e o `ready`.

## PROTOCOLO DE TEMA (usuaria, 01/10/2026 ~16:30) - OBRIGATORIO antes de definir o vies de QUALQUER evento
Continua valendo: PREVER e ENTRAR ANTECIPADO (T-5). Mas o vies nao pode ser suposto: nasce da pesquisa abaixo.
1. **Descobrir o TEMA** do evento (do que vai falar/medir; ex.: regulacao bancaria x politica monetaria; leilao de curto x longo prazo; payroll x desemprego). Fontes: federalreserve.gov (calendario/discursos), Investing, Reuters/Bloomberg/CNBC.
2. **Quando esse tema foi abordado pela ultima vez** (data e quem/qual dado), com link.
3. **Como o mercado se comportou nessa ocasiao:** direcao e tamanho no NAS100, juros 2a/10a, petroleo (use noticias do dia + docs/reacao-noticias.md; se preciso, o grafico historico).
4. **O que mudou desde entao** (regime, precificacao de juros, fluxo da ultima hora).
5. **Vies + confianca + invalidacao**, com as fontes. Tema que NAO e de juros/inflacao/emprego => vies NEUTRO de baixa confianca (mantem posicao existente; sem inverter por palpite).
6. Pos-evento: 3 linhas (previ x aconteceu x erro) em docs/reacao-noticias.md -> alimenta o placar.
Sem os itens 1-3 preenchidos nao se define o vies. Registrar o resumo do protocolo no open-trade (notes).

## PAINEL NO GRAFICO (pine/painel_noticias_nas100.pine, 01/10/2026)
Indicador "Painel Noticias NAS100" (so contexto, NAO gera sinal). Eu leio com `data_get_pine_tables` (study_filter "Painel"), uma chamada: confluencia 15m/1h de juros 10a (pb), Brent, ES, NQ, VIX, DXY com setas e pontuacao -6..+6 (favorece alta/baixa do NAS100; limiares sao HIPOTESES), regime M15/H1 (topos e fundos de pivos), vs abertura do dia, distancia a PDH/PDL em pts e US$ (lote 0,1), dia H/L, ATR M5/M15, hora do TV (BRT) e minutos para o proximo evento (campo de entrada "Eventos de hoje, BRT" no indicador: preencher de manha, ex.: 09:30,11:00) e para o fechamento 17:55.
Uso: ler o painel no T-5 de cada evento (itens "confluencia" e "regime" do protocolo de tema) e na gestao. Limites: NQ com atraso (~10 min); POC/volume nao incluidos (volume de CFD = ticks). Erro corrigido na 1a versao: str.tostring nao aceita formato "+#;-#;0" (usar prefixo "+" manual).
Se a tabela nao aparecer: ver o "!" vermelho ao lado do nome no grafico (erro de execucao) e a lista de studies (evitar duplicatas ao atualizar: remover a copia antiga).

## NIVEIS DO SCRIPT DA USUARIA: "PAINEL UNIFICADO NAYARA" (lido em 01/10/2026 ~18:25)
Leitura: `data_get_pine_labels` com study_filter "UNIFICADO" (o script usa rotulos; nao tem linhas/tabelas legiveis; o painel dele foi desabilitado pela usuaria).
Niveis de 01/10 (preco | texto do script):
- MAX ONTEM (PDH) 30.655,4 | "alvo do dia - liquidez acima no PDH"
- MEIO 30.458,9 | "tendencia bull forte - 50% distante, siga o fluxo comprador" (= 50% da faixa de ontem)
- MIN ONTEM (PDL) 30.262,4 | "suporte abaixo - nao venda em direcao ao PDL"
- MELHOR ENTRADA 30.344,93 | "observe a forca - vindo forte pode romper o OTE" (= ~79% da faixa a partir do PDH: OTE)
- NY 00:00 30.682,8 | "manipulacao? captura de liquidez, aguarda reversao acima"
- CRT VENDA -> MIN ONTEM 30.262,4 (marca em 30.529,4)
Conferencias: (a) PDH/PDL coincidem com os do meu painel; (b) o "30.263" que a usuaria mandou observar = PDL; (c) a oferta 30.459-30.484 onde o preco rejeitou as 11:40 = MEIO (30.458,9); (d) o "POC" ~30.346 que ela desenhou = MELHOR ENTRADA/OTE (30.344,9); (e) minima do dia 30.285,1 parou 23 pts acima do PDL; maximas da tarde (30.609-30.619) pararam abaixo do PDH.
Uso: tratar estes niveis como o MAPA DE REGIOES do dia (referencia unica) e ler no T-5 junto com o painel de contexto. Validar com contagem de reacoes antes de dar peso.

## PAINEL v3 (01/10/2026 ~18:30) - versao integrada, salva no TradingView como "Painel Noticias NAS100 1"
Acrescenta ao painel de contexto: MAPA DE REGIOES (PDH, MEIO, OTE 79%, NY 00:00, PDL com distancia em pts e US$ e o proximo nivel acima/abaixo), CRT D1 (varreu PDH/PDL e voltou), ontem ALTA/BAIXA + EMA20 D1, sessao (BRT) e direcao da Asia e de Londres (so descritiva). SEM gatilhos de compra/venda e SEM as porcentagens da cadeia (nao validadas).
Referencia diaria 2006-2026 (arquivo NAS100 do MT5/Investing em C:\Users\User\Desktop\TRADING PEIXE GRANDE\utils, 5.037 dias): dia sobe 55,0%; ontem alta/baixa nao muda (54,9% x 55,1%); CRT venda (1.105 dias): dia fecha abaixo da abertura 57,4% (base 45%); CRT compra (1.043 dias): 51,6% (sem vantagem); alvo oposto tocado no proprio dia ~25%. Dado diario NAO valida a cadeia de sessoes (precisa de intradiario). Atencao: parte do efeito do CRT e mecanica (fecha dentro da faixa depois de varrer o extremo).
Leitura: data_get_pine_tables study_filter "Painel". O codigo no arquivo pine/painel_noticias_nas100.pine esta na v2 (a v3 vive no TradingView).
O papel do Claude: o painel e SENSOR; o julgamento (o que importa, conflitos, o que fazer) e do Claude. Regra da usuaria: "o que precisamos e boa regiao e contexto".

### Painel v3.1 COMPACTO (01/10/2026 ~18:36) - versao em uso
Indicador no grafico: "Painel NAS100 Compacto" (script salvo como "Painel Noticias NAS100 1"). Canto inferior direito, 23 linhas curtas; opcoes no indicador: posicao e tamanho do texto. Leitura: `data_get_pine_tables` com study_filter "Painel" (uma chamada, mesma informacao da v3; so reformatado). Prioridade da usuaria: ACESSO RAPIDO do Claude a informacao.
Linhas: Juros10 pb, Brent %, ES %, NQ %, VIX %, DXY % (15m | 1h) | Confluencia | Regime M15|H1 | vs abertura dia | PDH, MEIO, OTE, NY00, PDL (preco | dist pts | US$) | Prox acima|abaixo | Ontem|EMA20 D1 | CRT D1 | Sessao|Asia|Londres | Dia H|L | ATR M5|M15 | Hora TV|prox evento | Fechar 17:55.

## VIES VIVO: o painel e contexto, nao lei (usuaria, 01/10/2026 ~18:45)
Em noticia e calendario o painel nao pode ser seguido "a risca": o Claude NAO trava no lado em que estava quando a estrutura muda e o outro lado ganha forca. Mas tambem NAO inverte por uma vela (erro das 10:55).
1. **Invalidacao escrita na entrada:** todo viés/trade nasce com "o que o invalida" (nivel + condicao). Enquanto nao invalidar, mantem; quando invalidar, age (sai e avalia o lado oposto), sem insistir.
2. **Mudanca de estrutura = evidencia COMBINADA (>= 2 de 4), nao uma vela:** (a) quebra de estrutura em M15 (topos/fundos invertem) ou 2 fechamentos M5 alem de um nivel-chave (MEIO, PDH, PDL, OTE); (b) confluencia vira para o outro lado e se mantem em 2 leituras seguidas; (c) o conteudo da noticia/fala contradiz o viés; (d) o preco ACEITA alem do nivel (nao so varre e volta).
3. **Os rotulos do painel ficam atrasados** (ex.: "CRT venda ativo" continuou aceso depois que o preco virou para cima). O painel descreve; quem le a DINAMICA e o Claude. Quando painel e dinamica divergem, vale a dinamica, registrando o motivo.
4. **Checkpoints para reavaliar o viés:** T-5 de cada evento, logo apos o dado/fala, e a cada ~15 min com posicao aberta. Viés velho (>30 min sem reavaliar) conta como VENCIDO.
5. **Registro:** a cada mudanca, 1 linha: o que mudou, quais das 4 evidencias, decisao.

## ESTRUTURA (a construir; usuaria apontou em 01/10 que o Claude nao lia topos/fundos renovados, BOS/CHoCH, distribuicao)
Definicoes de trabalho (a usuaria valida): HH/HL = alta; LH/LL = baixa; renovar topo/fundo = fechar alem do ultimo swing; BOS = rompe o ultimo swing a favor da tendencia; CHoCH = rompe o ultimo swing contra a tendencia (primeiro sinal de virada); sweep = passa do extremo, captura liquidez e volta (nao e quebra); distribuicao = faixa perto de topo com topos que nao renovam (equal highs/topos mais baixos); acumulacao = espelho no fundo.
Leitura do dia 01/10 (aprox.): alta ate 30.904 (varreu PDH 30.655 e NY00) -> CHoCH de baixa ~03-04h -> estrutura de baixa/distribuicao 04-10h (topos 30.704>30.663>30.633>30.612>30.609>30.554; fundos 30.511>30.489>30.457) -> BOS de baixa ~11h (ISM) ate 30.346/30.285 (23 pts acima do PDL) -> CHoCH de alta ~12:30 -> BOS de alta ate 30.609/30.619 (equal highs) -> faixa 30.50-30.62 (possivel distribuicao curta). O CHoCH de alta das 12:30 era o sinal para parar de insistir na venda.

## JANELA DE ENTRADA: analisar ~10 min o MELHOR PONTO a mercado (usuaria, 01/10/2026 ~19:33)
Com viés definido e ordem a MERCADO, a hora e o preco da entrada importam. Regra:
1. A partir de ~T-10 o Claude observa (1 em 1 min) o preco e as velas M5 (e M1 se disponivel).
2. Com a vela atual CONTRA o viés (ex.: viés QUEDA e vela de compra), NAO entrar dentro da forca contraria: esperar o preco chegar numa regiao de venda (maxima da sessao, MEIO, oferta) e a REJEICAO (pavio >= ~40%, fechamento abaixo da abertura ou da maxima anterior). Vale o espelho para viés ALTA (comprar no desconto com rejeicao de baixa).
3. Stop mais curto quando entra na rejeicao (acima/abaixo do extremo da sessao + folga); se nao houver ponto melhor, ENTRA NO PRAZO (T-2/T-3 do TV) com o stop estrutural original. A regra "sempre entrar T-5" continua: a janela so escolhe o melhor preco dentro dela, nao permite pular a entrada.
4. Nao perseguir: se o preco andar a favor sem rejeicao, aguardar reteste ate o prazo.
5. Registrar no open-trade qual ponto foi escolhido e por que.

### CORRECAO DA JANELA DE ENTRADA (01/10/2026 ~19:45, apos a usuaria perguntar se eu ia falhar)
- O PRAZO e em horario do TRADINGVIEW (nao do PC): janela de T-10 a T-5 do TV; no T-5 entra-se com ou sem rejeicao. (Na 1a aplicacao o prazo foi 'PC 19:40' = TV ~19:42 = T-3: atrasado.)
- Ticket PRE-ABERTO a partir de T-7 (lado e lote marcados), para sobrar so preco/stop/alvo.
- Toda resposta da janela diz a HORA EXATA da entrada forcada (ex.: 'entro as 19:40:00 TV se nao houver rejeicao antes').
- Zona boa ja no T-10 => entra logo.
- Clique direito para abrir o ticket: area vazia fora da tabela do painel, ex.: (800,250); 'Adicionar ordem' ~(950,490).

### Painel v3.2: CESTA DE GIGANTES (01/10/2026 ~19:55)
Acrescenta ao painel: GIGANTES pond. % (15m | 1h) com pesos aproximados do NDX (NVDA 10, MSFT 8, AAPL 8, AMZN 5, GOOGL 5, AVGO 5, META 4, TSLA 3: AJUSTAR nas configuracoes), quantas das 8 sobem, setas por ativo e Semis (SMH). So contexto (nao entra na soma da confluencia). Primeira leitura (19:56 BRT, apos o fechamento das acoes; liquidez fina): gigantes -0,27% (15m) e -0,42% (1h), 1 de 8 subindo, SMH -0,15%/-0,35%, enquanto o CFD subia: divergencia CFD x acoes (efeito pos-mercado/futuros), a conferir amanha em horario normal. Pine: o painel usa ~32 chamadas request.security (limite 40).

### Painel v3.3: + Micron (MU) (01/10/2026 20:10 TV) e CORRECAO da leitura das gigantes
- Linha "Micron (MU) %" (15m|1h) adicionada (pesos/limiares: 0,15%/0,40%). 33 chamadas request.security (limite 40).
- **CORRECAO:** as linhas de gigantes/SMH/MU usam velas M5 de ACOES, que NAO tem dado fora do pregao regular (ate 17:00 BRT). Depois disso o painel mostra o ULTIMO movimento do pregao, congelado (a leitura "gigantes -0,27%" das 19:56 era do fim da tarde, nao de agora). So vale com o mercado de acoes aberto (10:30-17:00 BRT). Fora disso, para MU/semis usar noticias/pos-mercado (WebSearch), nao o painel.
- Micron FQ4/26 (divulgada apos o fechamento de 01/10): LPA US$ 33,42 vs ~31,2-31,6 esperado; receita US$ 54,23 bi vs ~50,5-51,1; guidance FQ1/27 receita US$ 61,5 bi, margem 86,25%, LPA 38,15. Pos-mercado: MU -0,78% (US$ 1.056,75 vs 1.066,10) por capex alto (Benzinga/Investing). Leitura: bom para IA/semis, mas reacao morna = "vender o fato"; NAO e gatilho de alta para o NAS100 a esta hora.

### TESTE: pares de Asia/Europa x NDX (01/10/2026, historico diario ~40 anos, rodado no TradingView)
Metodo: Pine temporario no grafico NASDAQ:NDX diario; sinal do retorno do dia do par vs (a) NDX intradia (open->close) do MESMO dia, (b) gap, (c) NDX de ontem (eco). Base: NDX sobe intradia em 53,0% dos dias (N=10.498).
| Par | acerta intradia | eco do dia anterior | intradia nas divergencias com ontem |
| ASX 200 | 49,7% | 62,5% | 46,8% |
| Nikkei | 50,4% | 60,5% | 48,2% |
| Hang Seng | 51,3% | 59,0% | 49,0% |
| Kospi | 50,6% | 57,1% | 48,3% |
| DAX | 56,2% | 56,2% | 55,0% |
| FTSE | 56,3% | 55,6% | 55,1% |
Leitura: Asia/Australia NAO preveem a direcao do NAS100 na sessao americana (~50%, abaixo da base 53%); elas repetem o fechamento americano de ontem (57-62%) = causalidade invertida. Europa ~56% (+3 pts sobre a base) mas o pregao europeu se sobrepoe ao de NY (contemporaneo, nao e sinal antecipado). Coluna "GAP" invalida (NDX antigo tem open=close anterior, gap=0). Nao testado: FX (AUDUSD/USDJPY: barra diaria cobre NY), amostra recente (so ultimos 3-5 anos), movimentos grandes (|ret|>0,5%), pre-mercado.
Decisao: NAO colocar Asia/Europa no painel como "confirmacao" ate passar em teste mais fino (recente + movimentos grandes). Usar so como contexto de noticia (BoJ, China, etc.).
Incidente: o pine_new nao criou script novo e o save sobrescreveu o script salvo "Painel Noticias NAS100 1" com o teste; restaurado a partir de pine/painel_noticias_nas100.pine (v9 no TV). Sempre conferir pine_list_scripts apos pine_new; ou testar em script separado criado pela interface.

### Painel v3.5: SENTIMENTO CALCULADO (01/10/2026 20:48 TV) - substitui a linha escrita a mao
Pedido da usuaria: "vc nao tem que escrever, o painel calcula". Removidos os inputs manuais (viés/confianca/motivo).
Score (-8..+8, pesos iguais, NAO validado): confluencia 1h (limitada a +-2, so feeds vivos) + regime H1 + regime M15 + ontem alta/baixa + acima/abaixo EMA20 D1 + preco acima/abaixo do MEIO do dia + gigantes 1h (so com acoes abertas). Rotulo: >=+3 ALTA, <=-3 QUEDA, senao "MISTO (inclina ALTA/QUEDA)" (indica o lado de menor risco). Confianca = |score|/8 x 10.
Feeds PARADOS: cada simbolo ve a hora da ultima barra; >20 min = "parado" e fica FORA do score. Linha "Dados vivos x de 7". Leitura 20:48 TV: so ES, NQ e DXY vivos (3 de 7); juros, Brent, VIX e gigantes parados; score +1 => MISTO (inclina ALTA) 1/10.
Limite: nao inclui noticia/calendario (payroll) nem Asia/Europa (teste mostrou ~50%). Sentimento do payroll continua sendo o briefing (docs/briefing-2026-10-02-payroll.md), nao o painel. 27 chamadas request.security (limite 40).

### TESTE: o que se mexe junto com o NAS100 (01/10/2026 21:35 TV; pedido da usuaria: "petroleo cai => NAS cai?")
Metodo: Pine temporario; retorno do par vs retorno do NAS na MESMA barra e na PROXIMA barra; bars sem variacao ignoradas. Janela "recente" = ultimas 756 barras (D) ou 3000 (intraday). NDX no diario; PEPPERSTONE:NAS100 no 1h e 5m. Futuros ES/ZN/NQ tem ~10 min de atraso no TV: no intraday so servem como curiosidade (o diario nao sofre).
| Par | corr D (todo/recente) | corr 1h (todo/recente) | corr 5m (todo/recente) |
| S&P CFD | 0,88/0,92 | 0,95/0,92 | 0,90/0,91 |
| VIX | -0,60/-0,75 | -0,29/-0,25 | -0,58/-0,58 |
| Juros 10a | -0,04/0,02 | -0,05/-0,33 | -0,48/-0,51 |
| Juros 2a | -0,01/-0,01 | 0,08/-0,28 | -0,42/-0,44 |
| Brent | -0,03/0,01 | -0,10/-0,37 | -0,40/-0,36 |
| DXY | 0,01/0,01 | -0,10/-0,36 | -0,35/-0,39 |
| Ouro | -0,02/0,17 | 0,22/0,50 | 0,47/0,46 |
| USDJPY | 0,13/0,11 | 0,12/-0,20 | -0,24/-0,28 |
| ZN fut (atraso) | -0,09/0,00 | 0,01/0,38 | 0,45/0,50 |
Brent no 5m: quando o Brent SOBE, o NAS sobe so 40% das barras; quando o Brent CAI, o NAS CAI so 38% (=> NAS sobe 62%). Brent grande (>=0,2% em 5m) sobe => NAS sobe 25%; cai => NAS cai 22%. Ou seja: relacao INVERSA (petroleo sobe => NAS cai), nao a tese "petroleo cai => NAS cai". No diario ~0 (sem relacao); no intraday e mais forte no regime recente (guerra/juros altos).
"Proxima barra" (lead): ~50-53% para todos os pares: NENHUM par antecipa o NAS na barra seguinte; a reacao e simultanea. Servem como confirmacao/explicacao do movimento, nao como sinal antecipado.
Ressalva: correlacao contemporanea nao e causalidade; petroleo que cai por medo de recessao pode derrubar o NAS junto (o teste nao separa a causa). Janela recente = regime atual, pode mudar.
Incidentes: 2 vezes o save sobrescreveu o script "Painel Noticias NAS100 1" com codigo de teste; painel restaurado do arquivo (v3.5). Para testar sem risco, copiar o painel antes ou criar script pela interface (pine_new nao basta).

### Painel v3.6 (01/10/2026 21:50 TV): linha ES (atrasada ~10 min) trocada por S&P CFD da Pepperstone (PEPPERSTONE:US500, tempo real, corr 0,90 com o NAS100). NQ segue como contexto (atraso ~10 min ao vivo). CORRECAO: o atraso dos futuros so omite os ultimos ~10 min; o historico do teste de correlacao esta alinhado e vale.

### Painel v3.8 (01/10/2026 21:49 TV, pedido da usuaria): nos 6 mercados (juros, Brent, S&P CFD, NQ, VIX, DXY) a coluna "1h" foi trocada por "vs abert" (mudanca desde a abertura do dia DO PROPRIO ativo; juros em pb, o resto em %); 15m mantida. A variacao de 1h continua sendo calculada para o score de sentimento, so nao aparece. Gigantes/SMH/MU continuam com 15m|1h (rotulos ajustados). Atencao: a "abertura do dia" muda por ativo (futuros NQ abrem 19:00 BRT; CFD/indices/juros em outro horario), entao comparar vs abert entre linhas e aproximado.

### Painel v3.11 (01/10/2026 22:07 TV, pedido da usuaria: "venda na maxima de Londres" como confluencia): linhas Asia H|L, Londres H|L, NY AM H|L (sessoes COMPLETAS em UTC: Asia 00-06 = 21:00-03:00 BRT; Londres 06-13:30 = 03:00-10:30 BRT; NY AM 13:30-16 = 10:30-13:00 BRT; valor da sessao em curso ou da ultima concluida; entre parenteses a distancia em pts) + linha "Confluencia de nivel": se o preco esta a <= 0,4 x ATR15 (min 10 pts) de uma maxima (PDH/Asia H/Londres H/NY AM H) = ZONA DE VENDA; de uma minima = ZONA DE COMPRA. E ZONA DE ATENCAO (liquidez), NAO sinal: exige rejeicao de pavio M5 e viés compativel. Nao validado com dados. Substitui o uso do LuxAlgo Killzones para o Claude (aquele tem 278 caixas e e dificil de ler). Obs: apos 21:00 BRT o "Dia H|L" mostrou os valores de PDH/PDL; conferir a virada do dia amanha.
