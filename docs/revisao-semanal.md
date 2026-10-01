# Revisao semanal: ir ajustando as expectativas com dados

Decisao da usuaria: a meta diaria (US$ 25-30) e possivel de perseguir, e as expectativas vao sendo ajustadas ao longo do caminho.
Regra: **ajustar a expectativa com dados, nunca o risco para alcanca-la.**

## Como funciona
- Uma vez por semana (ou quando a usuaria pedir): `python scripts/calendar_db.py review [--days 7]`.
- Mostra: resultado de cada dia, media, melhor e pior, dias que bateram a meta, acerto, R medio, quanto devolveu, entradas que o real barraria
  (martingale, piso, perda) e ajustes de parametros feitos no periodo.
- Termina com uma **sugestao em portugues simples**. So sugestao: quem muda a meta e a usuaria.

## Escada de expectativa (proposta)
1. Medir a distribuicao real dos dias (`daily`, `review`).
2. Se a meta nao e batida em nenhum dia: usar como degrau intermediario a mediana dos dias positivos; subir de volta conforme melhora.
3. Se e batida em poucos dias: tratar como dia bom, planejar pela media.
4. Se e batida na maioria dos dias: manter, mas verificar se nao vem com risco crescente.
5. Menos de 5 dias de dados: nao ajustar.

## O que NAO muda com a expectativa
Limites de capital, stop obrigatorio, gate do modo real, regra anti-martingale e piso do dia continuam iguais. Baixar a meta e aceitavel;
aumentar o risco para bater a meta, nao.
