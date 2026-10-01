# Meta diaria: o Claude persegue com inteligencia, sem arriscar mais

Meta da usuaria: **US$ 25 a 30 POR DIA**, sem teto ("o ceu e o limite"). Prioridade: crescer o caixa.

## O que "inteligente" significa aqui
**Perseguir a meta escolhendo melhores trades, nunca arriscando mais para alcanca-la.** O que quebra contas e: aumentar o tamanho depois
de perda, entrar sem gatilho para "fechar o dia" e afrouxar stop e criterios. Nada disso e permitido.
- A meta **nao muda** o tamanho, os criterios de entrada nem a frequencia. Sem gatilho, sem trade.
- **Martingale bloqueado:** se o dia esta negativo, o lote nao pode ser maior que o anterior/usual. Treino: avisa e registra;
  real: rejeita.
- **Depois de bater a meta (modo PROTEGER O CAIXA):** pode seguir operando (sem teto), mas existe um **piso**: se o resultado do dia cair
  a 50% do melhor ponto do dia, para por hoje (hipotese do Claude, ajustavel via `tune`). Treino: avisa e registra "no real seria rejeitado";
  real: rejeita. Isto responde ao "nao devolver o que ja ganhei".
- Acompanhar: `python scripts/calendar_db.py daily` mostra o resultado de hoje, o estado (normal/proteger/piso) e o historico de dias.

## Um aviso que a usuaria precisa ouvir
Com conta de US$ 30, **US$ 25-30 por dia e quase dobrar a conta todo dia** (83-100%/dia). Isso exige trades grandes em relacao a conta
(0,1 lote em stops de dezenas de pontos arrisca de US$ 2 a US$ 12 por trade; alguns stops juntos chegam ao limite de perda de ~US$ 15).
A maioria dos operadores nao sustenta retornos assim por dia. Nao e impossivel ganhar num dia, mas **como meta diaria constante e muito
dificil**, e perseguir isso aumenta o risco de ruina. O `daily` mostra, com os dados do treino, quantos dias realmente batem a meta; essa e a
medida honesta. Se a media diaria ficar bem abaixo da meta, a decisao e da usuaria: aceitar uma meta menor ou aceitar mais risco, sabendo o custo.

## Como os dados decidem
- Distribuicao real dos dias no treino (media, melhor, pior, dias que bateram a meta).
- Se o piso de 50% ajuda ou atrapalha: comparar resultado dos dias com e sem o piso (via `stats`/`daily`), e o Claude pode ajustar com `tune`.

## Limites
- O piso e as regras acima sao proposta do Claude; a usuaria pode mudar.
- O tempo "dia" usa a data de Brasilia da hora de fechamento do trade.
