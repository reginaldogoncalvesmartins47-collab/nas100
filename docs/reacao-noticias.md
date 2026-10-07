# Reacao do NAS100 as noticias (amostra para ficarmos bons em operar noticia)

Medido nas velas M5 (CFD Pepperstone), horario de Brasilia. Atualizar a cada evento.

| Data | Hora | Evento | Previsao | Atual | Surpresa | Vela do evento (O->C, amplitude) | Depois |
|---|---|---|---|---|---|---|---|
| 01/10 | 09:30 | Pedidos Iniciais Seguro-Desemprego | 200-201K | 197K | -3K (-1,5%) | 30609 -> 30620 (22 pts) | nada relevante em 20 min |
| 01/10 | 10:45 | PMI Industrial S&P Global | 57,0 (= flash) | 55,9 | -1,1 (-1,9%) | 30513 -> 30462 (93 pts) | foi para baixo primeiro (contra a teoria), depois +76 em 5 min (10:50) |
| 01/10 | 11:00 | ISM industrial: Precos pagos | 72,9 | **77,9** | **+5,0 (+6,9%)** | 30499 -> 30377 (-122; amplitude 143) | varreu 30346 e voltou +111 na vela seguinte (~50% retrace) |

## O que aprendemos (hipoteses a confirmar com mais amostra)
- O tamanho do movimento acompanha o tamanho da SURPRESA (contra a projecao), nao o numero em si nem o anterior.
- A primeira vela costuma exagerar e devolver cerca da metade em 5-10 minutos: trade de noticia e de MINUTOS; sair no primeiro movimento/alvo curto.
- Projecao que e o flash (PMI) ja esta no preco: surpresa pequena, reacao confusa.
- Regime atual (juros 24 anos/maior desde 2002): numero forte/preco alto de insumos = negativo para NAS100.
- Entrada 5 min antes na direcao do vies macro teria ganho ~100 pts no ISM; entrada por vela de rejeicao contra o vies perdeu (trade 6, derrapagem de 28 pts no stop).
- Antes de cada evento: qual e a surpresa mais provavel? (usar regionais, componentes, petroleo) e quao grande? So vale entrar se a surpresa potencial for grande e a regiao tiver espaco.

| 01/10 | 12:30 | Leilao Bill 4 semanas (1 estrela, NAO estava no banco) | 3,850% | 3,890% | +0,04 pp (demanda mais fraca, juro mais alto) | 30388 -> 30326 (-62 pts; amplitude 66) | 12:35 vela +31 (30325->30356), depois lateral 30380-30430 em 30 min |
| 01/10 | 12:30 | Leilao Bill 8 semanas | 3,990% | 3,990% | 0 | (mesma vela) | -- |

Licao 01/10: eu so tinha eventos de 2-3 estrelas no banco e perdi o leilao de 12:30 (a usuaria viu no Investing). Em regime de juros altos, leilao com taxa acima da projecao foi motivo de queda de ~62 pts em 5 min. Incluir leiloes e falas do Fed no calendario do dia (docs/playbook-noticias.md). Correcao: o stop do trade 7 foi as 12:10, NAO ligado ao leilao (que foi 12:30).

| 01/10 | 14:30 | Fala do Jefferson (Fed, vice-chair) | tom (esperado: firme) | preocupado com inflacao (PCE 3,4%, energia, IA) mas SEM endossar alta iminente; "pode levar mais tempo" | tom mais brando que o esperado | NAS100 ~30.541 -> 30.597 na vela das 14:30 (+56) | juros 10a -6 bp, 2a -10 bp; NAS100 voltou a ~30.500 e ficou lateral 30.490-30.595; venda do Claude (30.543,9) fechada em 30.567,8 (-US$ 2,39); MFE ~+57; acertou: NAO |

Licao Jefferson: o "tom duro" que eu presumi nao veio; ler o TEXTO da fala (federalreserve.gov, resumos) assim que sai; "nao endossou alta" = leitura mole para o mercado. Placar de vies: 0 acertos / 1 erro em falas.

| 01/10 | 16:00 | Fala da Bowman (FOMC; tema real: regulacao bancaria eSLR, nao juros) | -- | -- | evento neutro | NAS100 ~30.572 -> max 30.609 / min 30.502 em 1h | compra do Claude (30.572,3) fechada a ~30.536,9 (-US$ 3,54); MFE ~+37; acertou: n/a (evento sem conteudo de juros; saida por Alphabet/Gemini 4) |
Williams/Cook 16:30 (Williams 'sem urgencia' em 29-30/09; Cook seminario sobre bancos centrais globais): sem entrada nova (ja havia posicao no mesmo lado).

| 01/10 | 17:30 | Balanco do Fed (H.4.1, 3*) | sem projecao; anterior 6.748B | total de ativos 6.743B (-5B); reservas (quarta 30/09) 2,948T (+17,9B na semana; fonte: federalreserve.gov) | dentro do ruido (limite +-20B ativos / +-100B reservas) | NAS100 ~30.552 -> ~30.540 em 5 min (sem reacao) | venda do Claude (30.555,6, conf 4/10) segue aberta; viés previa dado plano e foi isso |
Fechamento do trade 10 (17:54 TV): +US$ 2,88; MFE ~+28 pts; previ dado plano / viés venda leve conf 4/10 => acertou (direcao), sem reacao real do mercado ao dado.

### Logan (Dallas Fed) 01/10/2026, evento 19:45 BRT (trade 11, VENDA @30.557) - ANOTACAO PARCIAL
- Conteudo (Seeking Alpha, 19:28 ET = ~20:28 TV; so o titulo/trecho, pagina parcialmente bloqueada): Logan estima que "pelo menos mais duas altas de 25 pb" sao necessarias. TOM: DURO. TEMA: politica monetaria (juros), nao reservas/balanco. Chegou ~43 min DEPOIS do horario do evento (a conversa/fala durou; noticia nao saiu em 20 min como eu esperava; meu "nao houve fala" das 20:00-20:25 estava errado: a fala existiu, so nao havia manchete indexada).
- Reacao ate 20:54 TV: NAS100 ~30.570 (20:28) -> 30.594 (+~20 pts), SEM queda. Hipotese: ja precificado (Fed ja subiu em setembro; Logan pedia alta desde julho) e/ou baixa liquidez noturna. Placar: previ QUEDA (tom duro acertou), reacao de preco nao confirmou (ate agora). Fechar o registro quando o trade 11 encerrar.

### FECHAMENTO do trade 11 (Logan) - 01/10/2026 21:18 TV
Stop 30.631,3, -US$ 7,43 (stop afastado pela usuaria; original 30.610 daria -5,3). MFE ~6 pts: o trade nunca andou a favor. Previ QUEDA (tom duro, politica monetaria): conteudo acertou (2 altas de 25pb), reacao de preco NAO: sem queda; a abertura da Asia (21:00 BRT, Nikkei +1,1%) empurrou o NAS100 +~50 pts. Acertou: conteudo s / lucro n. Licao: fala dura ja precificada (Logan pede alta desde julho; Fed ja subiu em set) nao e gatilho de queda; entrar T-5 de falas de 1* a noite com liquidez fina e Asia abrindo expoe a gap de abertura; a manchete so saiu 43 min depois do evento.

### Payroll de setembro - 02/10/2026, 09:30 BRT (3*) - trade 12 (COMPRA @30.717,7)
- **Dado:** payroll **29K** (proj 89K, ant 133K revisado de 162K; surpresa -60K); privado 46K (proj 85K); desemprego **4,2%** (proj 4,1%); salario/hora **0,1%** m/m (proj 0,3%), **3,0%** a/a (proj 3,2%); U6 7,6% (ant 7,7%); participacao 61,8% (ant 61,6%).
- **Vies do Claude:** COMPRA 4/10 (cenario Goldilocks/fraco => juros menores e tech sobe). Mudou de VENDA 5/10 apos pesquisa (SpotGamma: 50-125K => acoes sobem; Fed: chance de alta em out ~32-34%; ADP beat; petroleo e juros caindo no pre-mercado).
- **Reacao NAS100:** 09:25 ~30.720 -> vela das 09:30 abriu 30.749 e fechou 30.868 (max 30.875, +125 pts em 5 min), 09:35 ~30.871; juros 10a 5,24% -> 5,16% (-7 pb); DXY -0,17%; VIX -3,5%; confluencia +4. M15/M60: preencher (add-reaction).
- **Resultado do trade:** fechado 30.788,9 (+US$ 7,12, +0,48R) por take movido pela usuaria; o mercado seguiu ate >30.873. **Acertou a direcao: sim.** Capturou ~45% do movimento.
- **Licao de tema:** emprego fraco + salario fraco = alivio de juros (nao pânico de recessao, ao menos na 1a hora). Surpresa (-60K) maior que a de agosto (+109K) em sentido oposto.

### CFTC (posicoes liquidas de especuladores) - 02/10/2026, 16:30 BRT (2*) - trade 15 (COMPRA @30.793,8)
- **Dado:** posicoes liquidas (Nasdaq 100 anterior +56,2K; S&P -133,2K); estudo mostrou razao de reacao ~1,0x (nao move o preco). Evento de baixo impacto no preco.
- **Vies:** COMPRA de contexto, confianca baixa (D1 em alta, preco em desconto no range de NY, mercado calmo, alvo no pino GEX 30.850). Entrada 16:13 TV (T-17, antes do T-5), a mercado, 0,1 lote, stop 30.740, alvo 30.850.
- **Resultado:** **WIN +US$ 3,32 (+0,62R, +33,2 pts)**, fechado 16:37:02 TV a 30.827,0 (fechamento manual ao ajustar o stop). **Acertou a direcao: sim.** Registrado como trade de NOTICIA (decisao da usuaria: 'entramos na noticia das 16:30 e tivemos win'). Obs: a usuaria pediu a montagem da posicao; o estudo mostrava que o CFTC nao move o preco, entao o ganho veio do contexto e nao do dado.
- Placar de vies de noticias em 02/10: payroll (final) certo, 11:00 certo, Baker Hughes certo, CFTC certo. 4 de 4 nos finais; o inicial do payroll (VENDA) errou. Amostra pequena: nao prova nada.

### 05/10/2026 - PMI Servicos S&P 10:45 e ISM Nao-Manufatura 11:00 (analise feita em 06/10; trade 16 venda @30.920,1, stop -US$ 12,59)
- Numeros (Investing; atual/proj/ant): PMI Servicos 58,8/58,7(=flash)/58,7; PMI Composto 58,4/58,4/58,4 (zero de surpresa); ISM geral 54,9/55,1/55,4 (-0,2, miss minimo); ISM Precos 74,0/73,3/72,6 (+0,7, inflacao um pouco acima); ISM Emprego 50,1/48,8/47,8 (+1,3, emprego melhor). Sinais MISTOS e pequenos.
- Preco M5 (BRT): abertura de NY 10:30 = vela de +100 pts (30.824 -> 30.923; amplitude 115) ANTES de qualquer dado; a venda entrou no topo dela (10:35) e o preco subiu mais +57 (10:40 max 30.977,8). PMI 10:45: amplitude 70, fechou 30.932 (sem direcao). ISM 11:00: vela com minima 30.881 (-40 vs entrada, +39 a favor da venda; unico momento no lucro) e depois +120 pts ate 31.013 (11:25). Dai em diante o minimo foi 30.966 (13:20): nunca mais voltou ao lucro; max 31.053 as 14:25 tocou o stop 31.045,2 (14:20-14:24).
- Leitura: o movimento do dia foi o da ABERTURA DE NY e o fluxo de alta do D1, nao o PMI/ISM. Confirma o estudo MT5 (ISM/PMI 10:00 ET = 1,1x do normal, ruido) e o 01/10 ('projecao = flash ja esta no preco'). A venda foi contra D1 ALTA, apos spike, antes do dado.
