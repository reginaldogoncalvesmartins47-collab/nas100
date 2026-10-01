# Perguntas em aberto: quem responde

## O Claude descobre sozinho (fase de descoberta, docs/descoberta.md) e grava em `facts` / docs
- Saldo do Paper Trading e moeda.
- O que "1" significa na posicao (a usuaria disse que o tamanho real e 0,1).
- Valor do ponto (USD por ponto por lote), lote minimo, passo do lote, margem e alavancagem do NAS100.
- Distancia tipica dos stops e tamanho dos trades **lendo o historico de trades da usuaria** no Paper Trading.
- Quais ferramentas o MCP tem (inclusive se coloca ordens) e quais pares/dados carregam e com atraso.
- A logica dos indicadores e scripts da usuaria (`docs/indicadores-da-usuaria.md`).
- O que o painel macro dela mostra (analistamacro.prospectia.space).
- Quais fontes (Investing, Finviz...) funcionam pela extensao.
- Consumo de tokens/uso do plano.
Resultado: `docs/descoberta-relatorio.md`. Nada disso deve ser perguntado a ela antes de tentar descobrir.

## So a usuaria pode responder (perguntar em lote, depois da descoberta)
1. "Aqui eu ja paro" (caso 02): **fechar a operacao** ou **parar de operar no dia**?
2. A meta de US$ 25-30: **por dia, semana ou mes**?
3. A perda total aceita: **US$ 15** (antes US$ 10)? E o **risco maximo por trade** que ela aceita (exigido antes do real).
4. A saida em ~US$ 22-24 foi por **valor**, por **pavio** ou pela distancia da proxima regiao?
5. Exemplos de rejeicao de pavio (candles em numeros) que ela considera boas e outras que nao, para calibrar.
6. Autorizacao para virar a chave para o **real** (uma vez, por escrito), so quando o `ready` cumprir.
