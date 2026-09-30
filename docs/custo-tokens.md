# Custo em tokens: o que pesa e como controlar

Status: **sem medicao ainda**. Nao conheco o plano da usuaria nem os precos atuais; nao ha valor em dolar aqui de proposito.
A primeira tarefa e MEDIR (secao 4).

## 0. Plano da usuaria: Pro (informado por ela)
- No Pro nao se paga por token: existe um **limite de uso** que se renova por periodos (a usuaria ja viu um reset as 22h).
  Os limites exatos mudam e eu nao os conheco; conferir no site e na conta.
- O uso do Claude Code provavelmente divide o limite com o uso do chat (a confirmar).
- Consequencia: um Claude checando tudo de 5 em 5 minutos o dia inteiro **tende a estourar o limite do Pro** (nao medido).
  O desenho orientado a evento deixa de ser otimizacao e passa a ser **requisito**.
- Se mesmo assim nao couber: opcoes sao um plano com mais uso ou a API paga por token (custo previsivel depois de medir).
- Teste em fases: **Fase A** = janela curta por dia na demo (ex.: 1-2 h) medindo consumo; **Fase B** = ampliar so se couber.
- Medir: comandos `/cost` e `/usage` do Claude Code (conferir o que cada um mostra na versao dela).

## 1. O que faz o consumo subir
- **Checar de 5 em 5 minutos com o Claude** durante 06:00-23:20 sao ~200 checagens por dia. Se cada uma exigir ler regras,
  ler velas de varios pares e raciocinar, o total diario vira milhoes de tokens (ordem de grandeza, nao medido).
- **Sessao unica que nunca termina:** a conversa cresce e o contexto inteiro e reenviado a cada passo (com desconto de cache,
  mas cresce). Sessao longa = custo crescente.
- **Arquivos de contexto grandes:** o `CLAUDE.md` e lido em toda sessao; quanto maior, mais caro cada checagem.
- **Ler muitos pares e tempos graficos a toda hora** (5 pares x H1 e H4) quando nada mudou.
- **Modelo mais forte em tarefa simples.**

## 2. Como reduzir (desenho ja pensado para isso)
1. **Memoria no banco, nao na conversa.** Tudo fica em `data/calendario.db` e em `rules.json`. Assim cada checagem pode ser uma
   **execucao curta e nova** (sem carregar historico de chat), lendo so o estado de que precisa.
2. **Claude so acorda quando ha motivo** (evento, nao relogio):
   - preco a menos de 0,5 x ATR de uma regiao pontuada, ou trade aberto precisando de acompanhamento;
   - choque detectado (gap, vela enorme, FVG);
   - horario de evento do calendario (antes) e logo depois;
   - rotinas fixas: calendario/feriados de manha, noticias incrementais a cada ~1 h, leituras de pares H1 a cada ~1 h e H4 a cada ~4 h
     (`renew-read` quando nada mudou).
   Um vigia simples (script, sem IA) poderia detectar esses gatilhos e so entao chamar o Claude. **Ainda nao existe**: depende de
   como os precos chegam ao script (MCP/CDP), a testar no PC.
3. **Modelo certo para cada tarefa:** modelo menor/mais barato para checagens de rotina; o mais forte so para diagnostico de
   choque e decisao de entrada.
4. **Ler menos:** noticias incrementais (`since`), `renew-read`, `brief` em vez de varias consultas, `CLAUDE.md` enxuto.
5. **Nao checar quando nao importa:** sem regiao proxima e sem trade aberto, dormir ate o proximo gatilho.

## 3. Ordem de grandeza (estimativa, NAO medida)
- Ingenuo (IA checando tudo a cada 5 min): ~200 rodadas/dia, cada uma pesada. Custo alto ou limite do plano estourado.
- Orientado a evento: talvez de 30 a 60 rodadas uteis/dia, a maioria leve. Bem menor, mas o numero real so sai de medicao.

## 4. Como medir (primeiro dia de demo)
- Rodar um dia completo no Paper Trading e anotar o consumo da sessao (o Claude Code tem o comando `/cost`; conferir na
  versao da usuaria o que ele mostra no plano dela).
- Registrar: tokens por checagem leve, por analise completa, por diagnostico de choque, e total do dia.
- Com esses numeros decidir: frequencia, modelo por tarefa, e se o plano da usuaria comporta.

## 5. Limites
- Precos e limites de plano mudam; conferir no site da Anthropic e na conta da usuaria.
- Reduzir custo nunca pode custar seguranca: stop no broker e limites de capital continuam sempre ligados.
