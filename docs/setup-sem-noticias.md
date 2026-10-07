# Setup para dias/horas SEM noticia (pesquisado e testado em 02/10/2026) - scripts/backtest_setups.py
Dados: NAS100 M5 do MT5, 02/10/2025-01/05/2026 (hora servidor = NY+7h), custo 2 pts por trade, stop primeiro se stop e alvo na mesma vela, treino out-jan x teste fev-abr.
## Resultado
| Setup | n | Acerto | R medio | PF | Treino R / Teste R |
| S1 ORB (rompimento da faixa da abertura de NY), alvo 1,5R | 145 | 57% | +0,09 | 1,33 | +0,08 / +0,11 |
| S1 ORB, alvo 1,0R | 145 | 58% | +0,08 | 1,28 | +0,06 / +0,10 |
| S1 ORB so em dias SEM pacote grande de noticia (1,5R) | 87 | 60% | +0,15 | 1,60 | - |
| S1 ORB em dias COM pacote grande (1,5R) | 58 | 53% | +0,01 | 1,03 | - |
| S2 varredura da maxima/minima de Londres, reverte | 119 | 46% | -0,15 | 0,73 | NEGATIVO nos dois periodos: NAO usar |
| S3 varredura da PDH/PDL, reverte (alvo 2R) | 78 | 46% | +0,13 | 1,26 | +0,19 / +0,05: fraco e instavel |
## Regra do S1 (mecanica, simples)
1. Faixa = maxima e minima das velas M5 entre 09:30 e 10:00 ET (10:30-11:00 BRT no horario de verao dos EUA; 11:30-12:00 BRT no inverno). Hora servidor MT5: 16:30-17:00.
2. Depois das 10:00 ET, entrada a mercado no PRIMEIRO fechamento M5 fora da faixa (acima = compra, abaixo = venda).
3. Stop no lado oposto da faixa (risco = tamanho da faixa); alvo 1,5R; sair no maximo as 15:00 ET (16:00 BRT) se nao bateu; nunca depois das 17:55 TV.
4. So em dia SEM pacote grande de noticia (payroll, CPI, varejo, Fed) antes das 11:00 ET.
5. Proteger: no +1R levar o stop ao zero a zero.
## Honestidade estatistica
Expectativa pequena (+0,08 a +0,09R por trade, +0,15R em dias sem noticia). Com n=145 e desvio ~1R, o erro padrao e ~0,08R: t ~1, NAO e significativo. Consistente entre treino e teste, mas e um periodo so (7 meses, um regime). Antes de qualquer confianca: rodar em demo ao vivo >= 20 dias e gravar cada trade (journal). Risco por trade = tamanho da faixa (50-150 pts): conferir se cabe no limite de perda.

## ORB nas 3 sessoes (scripts/backtest_orb_sessoes.py; mesma regra, alvo 1,5R, custo 2 pts, aberturas: Asia 00:00 UTC, Londres 08:00 hora local, NY 09:30 ET)
| Sessao | n | Acerto | R medio | PF | Treino R | Teste R | Faixa media |
| Asia | 148 | 51% | +0,08 | 1,19 | +0,16 | -0,03 | 53 pts |
| Londres | 149 | 46% | +0,06 | 1,13 | -0,03 | +0,18 | 52 pts |
| NY | 145 | 57% | +0,09 | 1,33 | +0,08 | +0,11 | 163 pts |
Leitura: SO o NY tem sinal consistente nos dois periodos (e acerto maior). Asia e Londres trocam de sinal entre treino e teste = ruido, NAO usar. NY tem faixa grande (~163 pts): risco por trade maior.
## Rotina basica diaria (o minimo que executo todo dia)
1. Manha: calendario do dia pela API do Investing (occurrences por data); classificar o dia: GRANDE (payroll, CPI, varejo, Fed, Waller/Williams/Trump) / PEQUENO (claims, PMI, ata...) / VAZIO.
2. Regime: Fed Rate Monitor (prob. de alta), juros 2a/10a, DXY, Brent, VIX no painel; gate LIBERADO (renovar leituras).
3. Dia GRANDE: operar so o pacote (entrada T-5 no lado do viés, stop fora do range, protecao). Dia PEQUENO ou VAZIO: ORB NY (10:30-11:00 BRT no horario de verao EUA) com a regra de docs acima.
4. Gestao: 0,1 lote, stop fora do range, +1R ou 50% do alvo => zero a zero; fechar tudo 17:55 TV; registrar cada trade (diario, banco, placar).
5. Fim do dia: resumo e ajuste; semanal: revisar se o ORB e os pacotes mantem vantagem (minimo 20 dias de ORB em demo antes de confiar).

## Outros 11 testes simples (scripts/backtest_outros.py), mesmos dados, custo 2 pts, treino x teste: NENHUM com vantagem
Seguir ou contrariar a 1a meia hora de NY (ate 11:30 e ate 15:00 ET), seguir ou fazer o fade do gap grande de abertura, comprar sempre (10:00-15:00 ET, 15:00-16:00 ET, 1a meia hora), sexta (10:00-16:00 ET e zeragem 15:00-16:00 ET): todas com |t| < 1 (a unica com |t| > 2 foi 15:00-16:00 ET no treino, que se inverte no teste). Deriva media 10:00-15:00 ET por dia da semana: ter -72, seg +15, qua +1 (n=28 por dia, ruido). Conclusao: so o ORB de NY teve sinal consistente; o resto e ruido. Cuidado: testar muitos setups aumenta a chance de achar sorte; o ORB tambem pode ser sorte (t ~ 1).
Proximos candidatos (exigem mais dados): setups com mercados correlacionados (Brent, juros, DXY) em M5 exportados do MT5; testar os indicadores que a usuaria ja tem no TradingView (ex.: confluencia Brent+US10Y+ES).

## Fibo no range do candle H4, a favor da macro (scripts/backtest_fibo_h4.py e backtest_fibo_h4_conf.py) - 02/10/2026
Regra testada: candle H4 completo (do M5); retracao 61,8/70,5/76,4/78,6% da faixa; macro = tendencia diaria (M1: fechamento anterior x EMA20 diaria; M2: direcao do dia anterior; M3: sem filtro); compra se macro alta (nivel = max - f*faixa), venda se baixa; stop na extremidade oposta do candle (+2 pts); alvo = extremidade 0%; valido 12 h; custo 2 pts.
- Ordem a limite no nivel (sem confirmacao): ~450 trades por combinacao; R medio -0,02 a -0,15; PF 0,83-0,97; acerto ~24% (RR ~3,2:1 => empate teorico em 24%): sem vantagem. Com filtro M2 no 76,4%: R -0,02, PF 0,97 (quase zero).
- Com confirmacao (esperar fechar M5 de volta do lado da tendencia apos tocar o nivel; stop no extremo do toque): R medio 0,00 a +0,07; PF 0,94-1,09; mas treino NEGATIVO (-0,24 a -0,03) e teste POSITIVO (+0,14 a +0,44) = instavel, nao confiavel.
Conclusao: mecanizado assim, o Fibo H4 sozinho nao tem vantagem comprovada. A 'macro' usada e um substituto tecnico (tendencia diaria); a macro fundamental da usuaria nao e testavel no passado. Uso recomendado: como FERRAMENTA DE LOCAL DE ENTRADA nos dias de noticia (zona de 61,8-78,6% do H4 / order block) para melhorar preco e stop, nao como setup independente.

## FVG / Order Block do indicador da usuaria ('ICT - Estrutura (BOS/CHoCH) + FVG + Order Blocks', Pine v6, pivot=5) - scripts/backtest_indicador_ict.py (02/10/2026)
Regras do indicador (lidas no codigo): pivos de 5 velas; BOS/CHoCH quando o FECHAMENTO rompe o ultimo topo/fundo (CHoCH se a tendencia anterior era contraria); FVG = low > high[2] (alta) / high < low[2] (baixa), apagado ao tocar a base/topo; OB = ultima vela contraria (ate 20 velas atras) antes do BOS/CHoCH, apagado quando o fechamento passa do outro lado. O indicador NAO tem regra de entrada/saida; as entradas abaixo sao minhas (a confirmar com a usuaria).
Teste (M5 MT5, sessao NY 16:30-22:00 servidor, custo 2 pts, valido 3h, stop alem da zona +2 pts, alvo 2R). CORRECAO IMPORTANTE: a 1a versao contava a maxima da vela do toque e dava R +0,5 (otimista, enviesado); a versao conservadora (vela do toque so conta o stop) deu:
| Entrada | n | R medio | PF | Treino / Teste |
| B FVG retest a favor do BOS/CHoCH (compra) | 208 | +0,21 | 1,34 | +0,23 / +0,17 |
| B FVG retest a favor (venda) | 187 | +0,20 | 1,32 | +0,19 / +0,22 |
| A OB retest (compra / venda) | 108 / 113 | +0,05 / +0,01 | 1,08 / 1,01 | instavel (compra: +0,33 / -0,33) |
| C OB + FVG confluencia | 40 / 50 | +0,14 / +0,12 | 1,21 / 1,18 | instavel |
B com alvo 1,5R: R +0,21/+0,20 (PF 1,39/1,37); alvo 3R: +0,17/+0,21 (PF 1,23/1,30): estavel na variacao do alvo. Risco medio 22,7 pts (mediana 17,5) => ~US$ 2,3 por trade com 0,1 lote; expectativa ~+0,2R = ~US$ 0,45/trade; ~2,8 trades/dia => ~US$ 1,3/dia em 0,1 lote. NAO chega a meta de US$ 25-30/dia.
Conclusao: o retest do FVG a favor da estrutura e o setup tecnico mais consistente testado ate agora (395 trades, dois lados, treino e teste); OB sozinho nao. Cuidados: um unico periodo/regime; custo e preenchimento simulados; precisa de demo ao vivo registrado antes de confiar.

## FVG do LuxAlgo Smart Money Concepts (replica fiel: scripts/backtest_luxalgo_fvg.py; fonte: Desktop/TRADING PEIXE GRANDE/INDICADORES TXT/SMART MONEY CONCEPTS.txt, CC BY-NC-SA 4.0, uso pessoal) - 02/10/2026
Regras do LuxAlgo: estrutura interna por 'leg' com pivot 5 (BOS/CHoCH no fechamento); FVG = low[i] > high[i-2] E close[i-1] > high[i-2] E corpo%[i-1] > 2 x media acumulada de |corpo%| (FILTRO DE DESLOCAMENTO, que o meu 1o teste nao tinha); mitigado quando low < base (alta) / high > topo (baixa); desenha duas caixas (metade de cima e de baixo do FVG). OB = vela de menor min/maior max (com filtro de volatilidade ATR200) entre o pivo e o rompimento.
Teste (a favor da tendencia interna, alvo 2R, stop alem da borda oposta +2, custo 2 pts, vela do toque so conta stop):
| Entrada | n | R medio | PF | Treino / Teste |
| E1 toque na BORDA (compra / venda) | 416 / 442 | +0,08 / +0,10 | 1,14 / 1,16 | +0,12 / +0,04 ; +0,03 / +0,19 (fraco) |
| E2 toque no MEIO do FVG (compra / venda) | 268 / 285 | +0,26 / +0,25 | 1,43 / 1,42 | +0,25 / +0,28 ; +0,28 / +0,22 (CONSISTENTE) |
| E2 so sessao NY (compra / venda) | 95 / 113 | +0,53 / +0,33 | 2,05 / 1,56 | n menor |
Leitura: com o filtro de deslocamento, a entrada no MEIO do FVG e a melhor vista ate agora (positiva nos dois periodos e nos dois lados). A borda sozinha e fraca. Ressalvas: um periodo/regime; entradas E1 e E2 da mesma zona nao sao independentes; preenchimento simulado; so demo ao vivo confirma.
## Metodo do mentor (pasta TRADING PEIXE GRANDE/PEIXE GRANDE -SKILL, transcricoes das aulas): 3 FILTROS DE ENTRADA
1) ANGULO: pullback com angulo < 60 graus = a favor (>60 = contra). 2) CONTEXTO: regiao de compra deve estar ABAIXO de 50% da Fibo do impulso (desconto); de venda, ACIMA de 50% (premio). 3) INDUCAO: o pullback deve ter varios submovimentos que geram liquidez (rompe minimas menores); queda/alta reta ate a regiao = filtro contra. Alinhamento: tempo maior (1h) para contexto e alvo, M5 para gatilho e stop. Contextos: captura de liquidez, Wyckoff, inversao de fluxo. Gatilhos: CHoCH, POI, troca de polaridade, rompimento de regioes, FVG e IFVG. Gestao: apos romper o topo anterior, stop no zero a zero. Estatistica: minimo 25 operacoes para avaliar a tecnica. PROXIMO TESTE: aplicar os 3 filtros como filtros no FVG do LuxAlgo.

## Os 3 filtros do mentor sobre o FVG do LuxAlgo (scripts/backtest_filtros_mentor.py, rodado 02/10/2026 ~16:40 TV)
Mesma base: entrada no MEIO do FVG a favor da tendencia interna, alvo 2R, custo 2 pts, vela do toque so conta stop. Filtros: (1) DESCONTO = meio do FVG abaixo de 50% da Fibo do impulso (compra) / acima (venda); (2) PULLBACK LENTO = velocidade em ATR/barra abaixo da mediana (proxy de angulo < 60 graus); (3) INDUCAO = pullback fez >= 2 novas minimas (compra) / maximas (venda).
| Filtro | n | Acerto | R medio | PF | Treino R / Teste R |
|---|---|---|---|---|---|
| Nenhum | 553 | 48% | +0,26 | 1,43 | +0,26 / +0,25 |
| So desconto | 158 | 49% | +0,30 | 1,51 | +0,22 / +0,41 |
| So pullback lento | 276 | 49% | +0,26 | 1,43 | +0,25 / +0,27 |
| So inducao | 181 | 49% | +0,26 | 1,44 | +0,13 / +0,45 |
| Desconto + lento | 75 | 53% | +0,42 | 1,76 | +0,22 / +0,79 |
| Desconto + inducao | 77 | 51% | +0,34 | 1,60 | +0,14 / +0,73 |
| Lento + inducao | 162 | 51% | +0,30 | 1,51 | +0,23 / +0,40 |
| Os 3 | 65 | 54% | +0,44 | 1,82 | +0,25 / +0,90 (n=19) |
| CONTRA (premio, fora do desconto) | 395 | 48% | +0,24 | 1,40 | +0,28 / +0,20 |
Leitura: o filtro ajuda pouco. Sem desconto ainda da +0,24R, entao o desconto quase nao separa trade bom de ruim. Com os 3 filtros o TREINO fica igual ao sem filtro (+0,25); a melhora vem so do TESTE (n=19): pode ser sorte. O que esta firme e o FVG no meio sem filtro (+0,26R, 553 trades, treino e teste iguais). Retorno pequeno (~US$ 1-2/dia com 0,1 lote), longe da meta de US$ 25-30. NAO confirmado ao vivo: mentor pede >= 25 operacoes em demo antes de avaliar.
Pendente: diario proprio da demo desse setup (separado do placar de noticias), com a regra de entrada/stop/alvo que a usuaria confirmar.

## SETUP DE REGIOES (OB + FVG do LuxAlgo) - regra confirmada pela usuaria em 02/10/2026 ~16:45 TV
Uso: dias/horas SEM noticia. DEMO. Diario proprio: journal/diario_setup_regioes.csv (fora do placar de noticias; contar >= 25 trades antes de avaliar).
1. Regiao = ORDER BLOCK ou FVG do LuxAlgo Smart Money Concepts (oferta = venda, demanda = compra). O FVG do LuxAlgo esta desligado no grafico: ligar antes, ou calcular (low[i] > high[i-2] alta / high[i] < low[i-2] baixa).
2. Antes de entrar (nesta ordem): gate; painel (confluencia, regime, juros, Brent, DXY, GEX, nivel perto); noticias na janela; o evento e a REGIAO: ALTA ou BAIXA, oferta ou demanda; trazer a analise de confluencia a usuaria (painel de correlacoes + LuxAlgo no grafico) ANTES da ordem.
3. Gatilho: preco na regiao + rejeicao de pavio em M5 + a vela FECHA de volta (nao romper a regiao). Esperar fechar. Compra na demanda, venda na oferta; preferir o lado do D1/H1 e dizer quando for contra.
4. Stop fora da regiao + folga de ATR (nunca colado nem dentro do range); alvo = proxima regiao oposta; R:R e so aviso na demo, mas registrar; lote 0,1; sem martingale; zero a zero com +50% do caminho; fechar 17:55 TV.
5. Registrar cada trade: diario (journal/diario_setup_regioes.csv), banco (open-trade/close-trade com notes 'SETUP REGIOES') e resumo-diario.md.
6. Alterar stop so pela aba Ordens com o painel Paper Trading aberto (o grafico fecha a posicao sem querer; aconteceu 3x em 02/10).
Hipotese: nao validada em backtest; OB sozinho foi fraco/instavel no teste (scripts/backtest_indicador_ict.py: OB retest R +0,05/+0,01). A demo ao vivo e a prova.

## Mapeado em 02/10/2026 (16:10-16:50 TV): leitura ao vivo do setup de regioes (SEM ordem; usuaria pediu so analisar cenarios)
- Regiao analisada: OFERTA 30.823,9-30.864 = order block do LuxAlgo (vela de topo das 12:20), 1o toque desde entao; muro de call do GEX 30.855 dentro da zona; acima PDH 30.904 e OB 31.015-31.038. Demanda alvo: OB 30.782-30.798 (onde o Trade 15 entrou) e minima de NY 30.744. Rejeicao M5 16:35: maxima 30.845,4, fechou 30.831,2 (pavio 14 pts); duplo topo M5 30.845/30.844 sob o muro.
- FVG: nenhum FVG de baixa aberto; um FVG de alta minusculo (30.824,2-30.829,6) sem filtro de deslocamento. O FVG do LuxAlgo estava DESLIGADO (so OB aparece em data_get_pine_boxes); usuaria corrigiu: o evento e a REGIAO (OB ou FVG), nao so FVG.
- Painel (fonte principal; 'Painel NAS100 Compacto'): confluencia 0 -> -1, regime M15 lateral / H1 alta, D1 acima da EMA20, sentimento ALTA 5/10, juros 10a +4,7 pb sobre a abertura (virou de -4,6 as 11:20: divergencia com NQ +0,98%), big techs 6 de 8, nenhum nivel perto. Veredito: alta com cautela, painel NAO aponta baixa.
- Cenarios (condicao -> alvo -> invalidacao): (1) reacao de baixa: volta a 30.855-30.864 + M5 fecha de volta com pavio -> alvo 30.798/30.744 -> inv. fechamento > 30.864; (2) rompe: 2 fechamentos > 30.864 -> PDH 30.904 e 31.015 -> inv. volta < 30.855; (3) lateral 30.798-30.855 ate o fechamento (o mais provavel, sexta tarde, ATR M5 ~23); (4) perde demanda: fecha < 30.782 e < 30.744 -> NY00 30.638 -> inv. volta > 30.798.
- Venda em 30.843 (stop ~30.890, alvo 30.798): R:R ~1,0, contra o D1 = NAO compensa; venda no reteste 30.855-30.864 com stop ~30.890: R:R ~2, confianca 4/10 (contra o D1).
- Resultado do dia sem notícia: nenhuma entrada do setup. Trade 15 (compra 16:13, +US$ 3,32) foi de NOTICIA (CFTC), por ordem da usuaria; NAO entra no diario do setup.
- Ferramentas: 'Inversion FVG TFlab' (TradingFinder) adicionado pela usuaria NAO roda: plano do TradingView no limite de 4 indicadores (erro do '!'); oculto nao conta menos. Para rodar, remover um (candidato: ICT Killzones Toolkit, oculto). Nao confundir com o painel dela: o painel obrigatorio e o 'Painel NAS100 Compacto'.
