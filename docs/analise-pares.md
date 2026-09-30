# Regra 4: analise raciocinada dos pares (antes de qualquer entrada)

Repositorio exclusivo do NAS100. Decisao da usuaria: o Claude **pensa**; nao aplica correlacao simples.
Se ela quisesse um robo de formula, usaria o script Pine. Base do macro: **H1 e H4**, sempre junto com a noticia.

## O que NAO fazer
- Regra mecanica do tipo "petroleo caiu => compra / petroleo subiu => vende".
- Usar M1-M30 como base do macro (o codigo rejeita).
- Explicar um movimento com noticia fora da janela (ver `docs/analise-noticias.md`).

## Pares obrigatorios (dentro do horario de operacao)
VIX, Brent, US10Y, ES, DXY. Opcionais por tema: US02Y, NVDA, SOX, USDCNH.

## Para cada par, em H1 e em H4, responder (e gravar com `add-read`)
1. **Tendencia:** alta, baixa ou lateral? Onde esta a estrutura e o nivel importante mais proximo?
2. **Por que?** Qual a causa do movimento (noticia, dado, geopolitica, estoques, Fed, fluxo)? A causa muda a implicacao.
3. **Implicacao para o NAS100:** favorece alta / favorece baixa / neutro / conflito.
4. **Confianca:** alta, media ou baixa.
5. **O que invalida** essa leitura (nivel ou evento concreto).
6. Se for **conflito** ou se o par diverge do NAS: explicar a divergencia (o codigo exige).

## Como a causa muda a leitura (hipoteses, nao regras; a usuaria corrige)
- **Brent caindo:** por alivio de oferta ou desescalada tende a aliviar inflacao/juros (favorece o NAS);
  por medo de demanda ou recessao pode vir junto com aversao a risco (nao favorece).
- **Brent subindo:** por choque de oferta ou geopolitica pressiona inflacao e juros (contra o NAS);
  por demanda forte e ambiguo.
- **Juros (US10Y/US02Y) subindo:** por inflacao ou Fed mais duro = pressao; por crescimento forte = ambiguo.
  **Caindo:** por desinflacao = favorece; por fuga para seguranca = nao favorece.
- **VIX:** nivel e direcao em H1/H4. VIX subindo com NAS caindo = queda confirmada; VIX estavel ou caindo com NAS
  caindo = queda suspeita (possivel varredura de liquidez ou ruido).
- **ES:** confirma ou diverge do NAS (divergencia pede explicacao, ex.: noticia especifica de tecnologia/IA).
- **DXY:** dolar forte costuma pesar; conferir se e causa ou consequencia da noticia do dia.

## Movimento contra o macro durante o dia (o caso "queda que custaria um stop")
Antes de tratar uma queda intradia como ameaca ao viés, responder:
1. A **estrutura do NAS em H1/H4** mudou (quebra de estrutura) ou foi um recuo dentro da tendencia?
2. Os **pares confirmaram** a queda (VIX, juros, Brent, ES) ou nao?
3. Existe **noticia dentro da janela** que explique?
4. A queda foi ate uma **regiao de liquidez/Fibo** (varredura provavel) e ate onde ela pode ir?
Conclusao registrada: **correcao dentro do macro** (viés mantido) ou **mudanca de regime** (viés vencido, sem sinal
ate a usuaria confirmar).

## Trava no codigo (`python scripts/calendar_db.py gate`)
Retorna **LIBERADO** ou **BLOQUEADO** com os motivos. Bloqueia se:
- fora do horario de operacao (06:00-23:20 BRT, seg-sex);
- calendario do dia nao capturado; feriados e eventos fora do calendario nao verificados hoje;
- noticias nao verificadas nos ultimos 60 min (`mark-checked --name news`, inclusive "nada relevante");
- evento de 3 estrelas ou extra ainda por vir sem plano antecipado;
- falta leitura de qualquer par obrigatorio em H1 ou H4, ou a leitura esta velha (H1 > 60 min, H4 > 240 min).
**LIBERADO nao e sinal.** Regiao com nota, reacao do mercado, RR e limites de risco ainda precisam passar.
Ainda nao inclui a regra do gap/viés vencido.

## Comandos
`add-read`, `reads`, `mark-checked`, `gate`, `brief` (ver `docs/contexto-feriados-eventos.md`).

## Limites
- Quem raciocina e grava e o Claude; o codigo so exige estrutura, validade e a explicacao. Uma leitura mal feita
  passa na trava se estiver bem preenchida. O diario e a revisao semanal existem para pegar isso.
- Dados de VIX, Brent, juros e ES no plano Basic podem vir atrasados; nao inventar dado ausente.
- As hipoteses acima nao foram testadas com dados.
