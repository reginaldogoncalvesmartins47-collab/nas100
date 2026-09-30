# Regra 1: analisar o calendario economico antes de qualquer entrada

O usuario NAO evita eventos: estuda e se posiciona antes. Por isso o calendario nao e um "bloqueio": e uma
analise obrigatoria. **Sem analise do calendario feita no dia, nao ha sinal (falha fechada).**

## O que analisar (horario de Brasilia)
1. **Lista do dia:** hora, pais, impacto, anterior, consenso (e realizado, quando sair).
2. **EUA que movem o NAS:** CPI, PCE, NFP, FOMC (decisao, ata, falas do Fed), PIB, ISM, varejo, pedidos de
   seguro-desemprego, leiloes do Tesouro (juros).
3. **Empresas e tecnologia:** resultados de gigantes de tecnologia/semicondutores e eventos de IA que mexem com o indice.
4. **Feriados e horario reduzido** nos EUA.
5. **Expectativa do mercado:** consenso, probabilidades de juros, tom das noticias; como o preco ja esta posicionado.
6. **Cenarios:** realizado acima / em linha / abaixo do consenso -> o que tendem a fazer NAS, juros, Brent e ES, e em quais regioes.
7. **Geopolitica e petroleo** do dia.

## Janelas
- **Antes:** posicionamento do usuario permitido; o Claude comenta o plano dentro do cenario.
- **No instante:** marcar como trade de evento (spread/slippage piores; Paper Trading nao simula isso).
- **Depois:** ler a reacao contra o consenso antes de novo sinal.

## Fonte principal: Investing.com (escolha da usuaria)
- Calendario: https://br.investing.com/economic-calendar (fuso Brasilia, pais EUA, importancia 2 e 3 estrelas).
- Capturar: hora, pais, evento, estrelas, atual, projecao, anterior e a previa do evento quando houver.
- Acesso: **somente pela extensao do navegador** (Claude in Chrome), lendo a aba do calendario do Investing aberta no PC da usuaria (calendario publico: login nao necessario).
  **Proibido scraper, script ou requisicao automatica** (o Investing nao aceita). - Rotina: captura diaria antes do horario de operacao (ex.: 05:30 BRT) e nova leitura quando sair cada evento relevante.
  Exige PC ligado, Chrome aberto e a aba do calendario do Investing aberta.
- Nao testado: nao sei se a extensao le bem essa pagina nem se os termos do site permitem esse uso; conferir.
- Fallback que funciona hoje: colar print ou texto do calendario na conversa.
- Motivo: em 30/09/2026 uma busca na web trouxe dados errados (PIB projetado 5,0% vs 1,5% no Investing).

## Armazenamento (para nao consultar o site toda hora)
- Banco local SQLite em `data/calendario.db` (nao vai para o git). Script: `scripts/calendar_db.py`.
- Tabela `events`: data, hora BRT, pais, evento, estrelas, categoria, atual, projecao, anterior, previa,
  surpresa (atual - projecao), relevante_nas, notas, fonte, capturado_em/atualizado_em.
- Tabela `reactions`: preco do NAS antes e 5/15/60 min depois do evento. Com o tempo vira a base para calibrar
  a leitura da surpresa com dados reais.
- Comandos: `init`, `upsert arquivo.json`, `today [--date] [--min-stars]`, `set-actual`, `add-reaction`.
- Regra: consultar o banco primeiro; voltar ao Investing (pela extensao) so para capturar o dia, atualizar
  realizados e eventos novos. Dia sem eventos no banco = nao capturado = sem sinal.
- Exemplo de dados: `data/examples/calendario-2026-09-30.json` (transcrito de print; conferir).

## Leitura da surpresa (hipotese, o preco manda)
- Inflacao/juros abaixo do consenso = leitura dovish (tende a favorecer o NAS); acima = hawkish (pressiona).
- Crescimento/emprego acima do consenso = ambiguo (bom para lucros, ruim se empurrar juros): depende do regime.
- A reacao real do preco, nos niveis do mapa, vale mais que a leitura teorica.

## Fontes e confiabilidade
- Cruzar **pelo menos 2 fontes**. Se divergirem (valores, horarios, dia da semana), dizer e nao assumir.
- Nao inventar dado ausente. Horarios: converter ET para Brasilia (em setembro, ET = UTC-4; Brasilia = UTC-3: +1h).

## Modelo de briefing
```
Data: ____   Fontes: ____ / ____
Eventos (BRT): hora | evento | impacto | anterior | consenso | realizado
Empresas/IA/feriados: ____
O que o mercado espera: ____
Cenarios: acima ____ | em linha ____ | abaixo ____
Brent/geopolitica: ____
Conclusao do calendario: (liberado / liberado com cuidado / dados insuficientes) + motivo
```
