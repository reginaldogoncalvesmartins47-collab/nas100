# Checklist antes de QUALQUER ordem (regra da usuaria, 01/10/2026)

Perguntar e responder, por escrito, ANTES de enviar a ordem:

0. **Qual e a ESTRUTURA?** (usuaria, 01/10) Sequencia de topos/fundos em M5 e H1: renovou topo (HH) ou fundo (LL)? Topos/fundos MAIS ALTOS ou MAIS BAIXOS? Fundo/topo duplo ou triplo? Mudanca de estrutura (primeiro topo mais alto numa queda = CHoCH)? Fundo/topo multiplo = liquidez de stops logo alem dele. Isso da o norte: a ordem deve estar a favor da estrutura ou em uma falha clara dela.

1. **Onde esta a liquidez mais proxima?** (max/min do dia, da sessao Asia/Londres/NY, de ontem, da semana, do mes; topos/fundos duplos)
2. **Tem FVG (vacuo) perto?** Calcular pelas velas (`python scripts/radar_liquidez.py barras.json preco`): FVG aberto atrai o preco; o stop nunca fica logo acima/abaixo de um FVG que o preco pode preencher.
3. **Qual nivel de Fibo?** Da perna mais recente (38,2 / 50 / 61,8 / 78,6) e se coincide com liquidez/FVG/POC.
4. **Tem espaco ate o alvo, ou o alvo e o limite?** Calcular em pontos: ate o proximo FVG oposto, POC, liquidez e demanda/oferta. O alvo fica ANTES do proximo obstaculo. Verificar R:R com stop real.
5. **O stop esta a uma distancia razoavel?** Alem da estrutura que invalida (acima do FVG e da Fibo seguinte, + overshoot da liquidez ~80 pts se for topo semanal) e maior que o ruido do M5 (ATR ~35). Stop curto = violinado.
6. **A ordem tem chance de pegar?** Entrar no PRIMEIRO CONTATO com a zona (borda do FVG / Fibo), nao no nivel "perfeito" mais longe: ordem longe perde o movimento (caso 01/10: preco foi a 30.704 e a ordem estava em 30.720).
6b. **Estrategico (usuaria, 01/10): nao colocar ordem onde o preco ACABOU DE PASSAR.** Nivel ja testado/usado perde valor; a ordem fica em liquidez AINDA NAO TOCADA (alem do ultimo topo/fundo testado: FVG nao preenchido, demanda/oferta virgem, onde ficam os stops). Equilibrio: perto o bastante para pegar (~100 pts) e longe do que ja foi usado.
7. **So ordem LIMITE** pelo ticket Shift+T, stop e alvo anexados. Nunca a mercado.

Mapa de exemplo 01/10: FVGs de baixa abertos 30.642-30.655, 30.661-30.678, 30.692-30.708, 30.722-30.774, 30.811-30.855; FVGs de alta 30.577-30.585 e 30.606-30.612; Fibo da queda 30.904->30.511: 38,2%=30.661, 50%=30.708, 61,8%=30.754, 78,6%=30.820.

## Duas ordens (compra e venda) pendentes: regra de cancelamento (usuaria, 01/10/2026)
- Sem vies fixo: manter um plano de compra E um de venda.
- Quando uma executar e o trade andar a favor (>= +25 pts), CANCELAR a ordem oposta: nao faz sentido manter a venda com a compra funcionando (e vice-versa).
- Se o trade executado for parado, refazer os dois planos pelo checklist (a nova leitura pode ser outra).
- Cancelar pela aba Paper Trading > Ordens (X na linha da ordem e de seus TP/SL).

## Execucao: ordem a mercado e foco no calendario (usuaria, 01/10/2026)
Substitui "so ordem limite": entrar SO a mercado, pelo ticket completo (aba Mercado) com stop e alvo anexados antes de confirmar (stop obrigatorio). Foco: noticias do calendario com surpresa a favor, em regioes interessantes (liquidez/FVG/Fibo/POC/estrutura). Cancelar ordens so pela aba Paper Trading > Ordens (o X da etiqueta no grafico converte em ordem a mercado).
