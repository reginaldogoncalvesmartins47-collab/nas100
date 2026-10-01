# Objetivo (lucro) e quem decide o que

A usuaria nao e tecnica e a prioridade dela e **o lucro**. Este documento fixa como isso funciona.

## Quem decide o que
| Quem | Decide |
|---|---|
| **Claude** | Parametros tecnicos (pavio, break-even, validades, limiares de choque, notas de regiao...) dentro de `tuning.tunable`, com evidencia minima e historico (`docs/auto-ajuste.md`). Explica em portugues simples. |
| **Usuaria** | Quanto arriscar, quando ir para o real, em quais fontes confia, a meta de lucro. O Claude so pergunta decisoes de negocio/risco, nao tecnicas. |

## Meta e limite informados pela usuaria
- Ganho: **sem teto**; gostaria de **pelo menos US$ 25 a 30** (periodo nao informado).
- Perda total aceita: **uns US$ 15** (incerto).
- Conta de US$ 30: a meta e cerca de 83-100% da conta e a perda aceita e 50%. Ambicioso; sem garantia.
- Comando `goal`: mostra quantos trades e quantos stops, no ritmo medido do treino, separam da meta e do limite.

## O que "lucro como prioridade" significa aqui
- Medida: **lucro liquido depois dos custos** (spread/slippage), em **R por trade** (R = o que se arrisca em cada trade).
- **Nunca** se busca lucro afrouxando o que protege o capital: limites de risco, stop obrigatorio e o gate do modo real.
  Com conta de US$ 30, sobreviver e pre-condicao para lucrar.
- Nao ha garantia de lucro. A maioria dos operadores de varejo perde dinheiro; a demo existe para descobrir, sem custo,
  se este metodo tem vantagem.

## Como o Claude "aprende"
O Claude nao guarda memoria sozinho entre conversas. O aprendizado fica **nos dados e nos arquivos**: trades (MFE,
quanto devolveu), estatisticas, exemplos da usuaria e parametros ajustados (`tune`, com historico). O `CLAUDE.md` faz
o Claude ler tudo isso em cada sessao.

## Ja da para ir para a conta real? (`python scripts/calendar_db.py ready`)
Veredito em portugues simples, com os criterios do treino (escolhas minhas, ajustaveis em `rules.json` > `go_live`):
- pelo menos 50 trades em pelo menos 10 dias diferentes;
- ganho medio por trade de pelo menos +0,15R;
- ganho medio **descontando a incerteza da amostra** positivo (evita confundir sorte com vantagem);
- lucro bruto / prejuizo bruto de pelo menos 1,3;
- maior queda acumulada de no maximo 6R.
Mesmo cumprindo tudo: nao garante lucro no real (spread, slippage e emocao pioram). Comecar com o menor tamanho possivel.
