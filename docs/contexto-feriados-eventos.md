# Regra 3: feriados globais, eventos fora do calendario e posicionamento antecipado

Decisao da usuaria: o Claude nao espera a noticia sair para entrar. Ele se antecipa: levanta o contexto do dia,
analisa o impacto no NAS100 e define ONDE pode se posicionar, olhando o movimento do mercado e os pares
correlacionados com cada noticia.

## O que levantar todo dia (antes de qualquer entrada)
1. **Feriados globais de hoje e dos proximos 2 dias:** EUA, China, Japao, Coreia, Taiwan, Reino Unido, Alemanha/UE, Brasil.
   Por que importa: mercado fechado = liquidez menor e reacao incompleta (ex.: Taiwan/Coreia fechados deixam
   semicondutores sem reacao completa). Fontes: calendarios oficiais das bolsas (CME, NYSE/Nasdaq) e o calendario
   de feriados do Investing (so pela extensao do navegador). Gravar pais, nome, fechado/cedo e a fonte.
2. **Eventos FORA do calendario oficial:** cupulas, reunioes entre lideres (ex.: Trump e Xi), discursos, anuncios de
   empresas, decisoes politicas. Exigem `published_at` com fuso, 2 fontes nivel 1-2 para confirmar e um status
   (anunciado / confirmado / ocorrido / cancelado).
3. **Impacto das noticias do dia no NAS100** e **tema** de cada uma (petroleo/geopolitica, China/comercio, IA/tecnologia,
   Fed/juros, dados macro, resultados). O tema define os **ativos correlacionados** a observar (`rules.json` >
   `theme_correlations`, hipoteses a calibrar; comando `themes`).
4. **Plano de posicionamento antecipado** para cada evento relevante (calendario 3 estrelas e eventos extras):
   cenarios (acima/abaixo do esperado), ativos correlacionados a vigiar, regiao candidata e a nota.

## Regras de antecipacao
- **Posicionamento obrigatorio antes do evento:** todo evento de 3 estrelas e todo evento fora do calendario exige um
  plano com **direcao (compra ou venda)**, regiao/entrada e stop (`add-plan --stance compra|venda`). Continua sujeito
  aos limites de risco (`docs/regras-risco.md`). O sistema so sinaliza; quem executa e a usuaria.
  Atencao (registrada para a usuaria decidir): posicionar sempre, mesmo sem vantagem clara, aumenta o numero de trades
  e o risco de slippage em evento; a conta de US$ 20 e o lote minimo limitam o tamanho do stop.
- O plano e criado **antes** do evento. Plano criado depois e gravado como **TARDIO** e **nao gera entrada pela manchete**.
- Plano tardio nao conta como plano: o item continua **SEM PLANO** no briefing.
- Depois do evento: ler a reacao do preco e dos correlacionados para **gerir/ajustar** o plano, nao para perseguir a manchete.
- A entrada continua exigindo o restante do portao (regiao com nota, reacao do mercado, RR, risco).

## Memoria do dia (para nada se perder)
Tudo vai para `data/calendario.db` (tabelas `holidays`, `extra_events`, `news`, `plans`). O comando
`python scripts/calendar_db.py brief` mostra de uma vez: feriados, calendario, eventos extras, noticias dentro da
janela e planos ativos, com as pendencias **SEM PLANO** e **TARDIO**. Rodar no inicio do dia e a cada nova noticia.

## Comandos
`upsert-holidays`, `upsert-extra`, `add-plan --stance compra|venda --theme T --correlated A,B --position TXT [--event-id|--extra-id|--event-time]`,
`close-plan --id N --status concluido|invalidado`, `themes`, `brief`.

## Limites
- Quem levanta e grava os dados (feriados, eventos extras, noticias) e o Claude, com busca/extensao; o codigo so
  guarda, exige data/hora/fonte e aponta pendencias. Erro de fonte continua possivel.
- Os ativos correlacionados e os temas sao hipoteses. Nada disso foi testado com dados reais.
- Antecipar nao e adivinhar: o plano descreve cenarios, nao garante resultado.
