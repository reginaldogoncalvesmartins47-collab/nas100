# Tudo o que foi alinhado com a usuaria (Nayara)

Legenda: **DECIDIDO** = disse a usuaria | **HIPOTESE** = proposta tecnica do Claude, a calibrar com dados | **PENDENTE** = falta resposta ou descoberta.
Nada aqui foi testado com dados reais ainda.

## 1. Objetivo e forma de trabalhar
- DECIDIDO: operar o **NAS100 (Pepperstone)** com o Claude lendo o TradingView; o repositorio e **so para NAS100**.
- DECIDIDO: **o Claude executa as ordens; a usuaria nao clica.** Primeiro **demo (Paper Trading)**, depois o real (docs/execucao.md).
- DECIDIDO: a usuaria **nao e tecnica**: o Claude decide os parametros tecnicos, explica em portugues simples e pergunta so decisoes de negocio/risco.
- DECIDIDO: o Claude **descobre sozinho** (saldo, valor do ponto, historico, scripts dela, ferramentas) em vez de perguntar (docs/descoberta.md).
- DECIDIDO: **prioridade = crescer o caixa**; lucro nunca justifica afrouxar protecao de capital.
- DECIDIDO: o Claude **aprende** pelos dados e arquivos e **ajusta parametros** com limites (docs/auto-ajuste.md).

## 2. Dinheiro, metas e limites
- DECIDIDO: conta **US$ 30** (era US$ 20); posicao usual **0,1** (o grafico mostra "1"). Valor do ponto: PENDENTE (descoberta).
- DECIDIDO: **meta US$ 25-30 POR DIA, sem teto**; **perda total aceita ~US$ 15** (incerto; antes US$ 10: PENDENTE confirmar).
- DECIDIDO: **sem limite de numero de trades**; **sem janela de horario** (trabalha enquanto ela mantiver ligado).
- DECIDIDO: **na demo o bot tem liberdade** (gate, nota, perda do dia e corte so avisam e registram); stop obrigatorio sempre.
- NAO DECIDIDO por ela (eram sugestoes minhas e foram removidas): risco por trade de US$ 1 e perda do dia de US$ 3. O risco maximo por trade
  precisa ser definido por ela antes do real.
- HIPOTESE: sem martingale; apos bater a meta, **piso de 50%** do melhor ponto do dia (docs/meta-diaria.md); `review` semanal ajusta a expectativa, nunca o risco.
- DECIDIDO: plano **Pro** (limite de uso): testar em fases, cadencia adaptativa (docs/custo-tokens.md). Consumo: PENDENTE medir.

## 3. Metodo
- DECIDIDO: a **macro manda** (viés do dia vem dela / do painel analistamacro.prospectia.space). Pares: **VIX, Brent, juros (US10Y), ES, DXY**,
  em **H1 e H4**, **raciocinando** (nao correlacao simples) e sempre com a noticia (docs/analise-pares.md).
- DECIDIDO: **regioes** = liquidez valida + Fibo no **H1** (todos os niveis operaveis, sem prioridade) + refino Fibo **M15** (regiao 2) + oferta/demanda;
  **pontuar** regioes primeiro; a regiao nao e o gatilho (docs/liquidez-e-regioes.md). SMC (LuxAlgo) = **fator opcional futuro** (docs/smc-luxalgo.md).
- DECIDIDO: **gatilho = o mercado em M5**: o preco chega na regiao e mostra **rejeicao de pavio a favor do viés**; candle fecha sem romper (`entry-check`).
  A usuaria opera e le o pavio em M5; o Claude entende pelos valores OHLC (nao precisa enxergar o grafico).
- DECIDIDO: pode operar **contra a macro do dia** se a regiao for forte (nota maior, saida curta).
- DECIDIDO: **saida**: alvo = proxima regiao de oferta/demanda; acompanhar o caminho; pavio contra = sinal; **nao devolver o que ganhou**.
  Caso 02: saiu em ~US$ 22-24 antes da proxima regiao. Variantes A-E a testar na demo (docs/gestao-saida.md).

## 4. Dever de casa antes de entrar (gate)
- DECIDIDO: **calendario do Investing** (publico; **so pela extensao do navegador, sem scraper**), estrelas e previa; **banco local** para nao reconsultar (docs/analise-calendario.md).
- DECIDIDO: **feriados globais** e **eventos fora do calendario** (ex.: Trump e Xi); **plano antecipado com direcao** (compra/venda) antes de evento;
  **nunca esperar a noticia para entrar** (docs/contexto-feriados-eventos.md).
- DECIDIDO: **noticias**: dom/seg desde **sexta 16h (Brasilia)**; ter-sex **ultimas 24h**; **data e hora obrigatorias**; fontes por nivel; checagem **incremental** (docs/analise-noticias.md).
- DECIDIDO: **sentimento**: Finviz e outras (2+ fontes do dia); **COT so contexto** por causa do atraso (docs/sentimento.md).
- DECIDIDO: **choque de mercado** (gap, vela enorme, FVG): primeiro entender o que esta acontecendo, rapido; vies vira vencido (docs/choque-de-mercado.md).
- DECIDIDO: se o gate esta vermelho, a **prioridade do Claude e concluir as pendencias**; no treino nao trava a entrada.

## 5. O que esta construido (codigo)
`scripts/calendar_db.py` (SQLite local, nao vai para o git): calendario, feriados, eventos extras, noticias com janela, planos, leituras de pares, sentimento,
viés, choque, trades (MFE), `gate`, `entry-check`, `path`, `wick`, `daily`, `goal`, `review`, `ready`, `tune`, `add-fact`/`facts`. Regras em `rules.json`.
Pine: `pine/` (backtest/alertas; nao compilado nem testado).

## 6. O que NAO foi testado / precisa do PC da usuaria
Execucao de ordens no Paper Trading, leitura de velas pelo MCP, Investing pela extensao, fontes de sentimento, valor do ponto, consumo de tokens,
e qualquer resultado de lucro. Plano: `docs/primeira-execucao.md` e `docs/descoberta.md`.

## 7. Erros meus ja corrigidos
- Tinha tratado como regra o risco de US$ 1/trade e a perda de US$ 3/dia (eram sugestoes minhas).
- Tinha deixado "so sinal / o usuario executa" em alguns textos, contra a decisao dela; corrigido.
- Janela fixa de 06:00-23:20 e limite de trades por dia: removidos.
- Dados de calendario da busca na web estavam errados (por isso o Investing e a fonte principal).

## 8. Pendencias que so ela responde
Ver docs/perguntas-abertas.md.
