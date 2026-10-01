# Projeto NAS100 - copiloto de trade com TradingView

Contexto para o Claude Code. Leia `docs/` antes de agir.

## Objetivo
Tudo o que a usuaria decidiu esta em `docs/decisoes-alinhadas.md` (leia primeiro).
Ajudar o usuario a operar o NAS100 (PEPPERSTONE:NAS100): ler o grafico no TradingView, analisar cenario
(macro + liquidez) e OPERAR: o Claude executa as ordens (com stop e alvo) e a usuaria nao clica. Primeiro em demo (Paper Trading), depois real.

## A usuaria e a prioridade
A usuaria NAO e tecnica e a prioridade dela e o lucro (docs/decisoes-e-objetivo.md). O Claude decide os parametros tecnicos dentro
dos limites (tune), explica em portugues simples e pergunta so decisoes de negocio/risco. Lucro NUNCA justifica afrouxar limites de
capital, stop obrigatorio ou o gate do modo real. Veredito para a conta real: `python scripts/calendar_db.py ready`.

## Descobrir antes de perguntar (docs/descoberta.md)
O Claude NAO fica travado esperando a usuaria: descobre sozinho o Paper Trading (saldo, tamanho, valor do ponto, historico), as ferramentas
do MCP e os scripts/indicadores dela, e grava com `add-fact`. So pergunta, em lote, o que apenas ela sabe. Se uma ferramenta falhar,
registra e segue.

## Regras que valem sempre
- Conta real pequena (US$ 30). Unico limite dado por ela: pode perder ate 'uns US$ 15' no total (incerto; antes US$ 10; confirmar). Risco por trade e perda do dia NAO foram definidos por ela (docs/regras-risco.md): nao inventar limites.
- **O Claude executa as ordens; a usuaria nao clica** (decisao dela, docs/execucao.md). Treino (Paper Trading): autorizado.
  Conta real: so depois de `ready` cumprido + autorizacao escrita da usuaria dada UMA vez (nao por trade) + stop/alvo como
  ordens na corretora + limites de capital ligados. Toda ordem nasce com stop e alvo.
- Nao prometer resultado. Dizer quando nao ha setup. Resultados de backtest nao valem como prova.
- Nao inventar dados de preco/volume: se o dado nao estiver disponivel, dizer.
- Nao tocar em abas de corretora/banco ao usar o navegador.

## Metodo (resumo, detalhes em `docs/metodo.md`)
- Direcao macro (vies) e do Claude: analista fundamentalista do NAS100. Constroi o vies sozinho (Brent, juros, DXY, ES, VIX, big techs, calendario, noticias, geopolitica, sentimento), justifica em portugues simples e diz "sem vies/sem trade" quando nao houver. A usuaria pode revisar; o painel dela e uma fonte a mais.
- Entrada: regiao pontuada (liquidez + Fibo H1 + oferta/demanda) e o GATILHO e o mercado em M5: o preco chega na regiao, mostra
  rejeicao de pavio a favor do vies e o candle fecha sem romper a regiao (`entry-check`). Esperar o candle FECHAR; nao antecipar.
- Sem janela de horario fixa: o sistema trabalha enquanto a usuaria o mantiver ligado (mercado aberto). Acompanhar o limite de uso do plano.

## Antes de qualquer entrada (ordem)
1. calendario do dia (Investing, pela extensao) -> 2. noticias na janela (dom/seg desde sexta 16h BRT; ter-sex 24h)
-> 3. feriados globais, eventos fora do calendario e plano antecipado -> 4. leitura RACIOCINADA dos pares em H1/H4
-> 5. sentimento do mercado (2+ fontes) -> 6. `python scripts/calendar_db.py gate` = LIBERADO -> so entao regiao com nota + reacao do mercado + RR + risco.
Se o gate estiver BLOQUEADO: a prioridade e concluir a lista de pendencias, na ordem (sem parar, sem pedir permissao
para fazer o dever de casa; so perguntar o que apenas a usuaria sabe). Sem trava de horario. Noticias: so checagem
incremental (`since`). Leitura de par sem mudanca: `renew-read`. Antes de evento importante: plano com direcao (compra/venda).
Nunca perseguir a manchete. Nao usar noticia fora da janela. Nao aplicar correlacao mecanica.

## Modos e saida
- Treino (demo): NAO trava por gate, nota, perda do dia nem corte total (estes so avisam e registram 'no real teria parado'). Vale sempre: stop obrigatorio (definido pelo mercado, nao pelo dinheiro).
- Real: so depois de resultado positivo em amostra grande; gate LIBERADO obrigatorio.
- Todo trade: stop obrigatorio, plano de saida definido antes (docs/gestao-saida.md), registrado em `trades` (MFE, devolvido).
- Stop e alvo ficam como ordens no broker; o Claude ajusta nas checagens, nunca substitui o stop.

## Estilo da usuaria
Ela opera e le rejeicao de pavio em M5. O Claude entende pelos valores de open/high/low/close das velas M5 (nao precisa enxergar o grafico).
Tempos: macro/vies H1 e H4; regioes Fibo H1 (+ refino M15); execucao e saida M5.
Usar `path --o --h --l --c` e `wick`. Saida: alvo = regiao de oferta/demanda; acompanhar o caminho (`path`).

## Meta diaria (docs/meta-diaria.md)
Meta da usuaria: US$ 25-30 POR DIA, sem teto. Persegue-se escolhendo melhores trades, NUNCA arriscando mais: sem martingale (lote nao sobe apos perda),
sem entrada sem gatilho, sem afrouxar stop. Apos bater a meta: proteger o caixa (piso de 50% do melhor ponto do dia). `daily` mostra o dia e o historico.

Revisao semanal: `review` mostra os dias e sugere ajustar a EXPECTATIVA com dados (docs/revisao-semanal.md); nunca o risco para alcanca-la.

## Choque de mercado (docs/choque-de-mercado.md)
Gap, vela enorme ou FVG => `shock` abre CHOQUE e vence o vies. PRIMEIRA tarefa, rapida (~5 min): entender o que esta
acontecendo (`since`, noticias, pares), `shock-diagnose`, redefinir o vies (`bias --set`). So depois o resto do gate.
Trades abertos: revisar stop/protecao imediatamente. Sem limite de numero de trades (a perda do dia e o corte total contem).

## Auto-ajuste (docs/auto-ajuste.md)
O Claude pode ajustar parametros de hipotese com `tune` (evidencia minima, um por vez, historico, revert; real exige aprovacao
da usuaria). NUNCA ajustar limites de capital, stop obrigatorio, gate do modo real, regras de data/fonte/janela das noticias.

## Arquivos
- `pine/` scripts Pine (TradingView). `nas100_liquidez_v2.pine` e o atual; nao testado ate o momento.
- `docs/` metodo, liquidez e regioes, fluxo de analise, risco, setup do MCP, roadmap.
- `rules.json` regras do metodo em formato de maquina (rascunho, hipoteses).
- `journal/` diario de trades (CSV).

## Estado
Ver `docs/roadmap.md`.
