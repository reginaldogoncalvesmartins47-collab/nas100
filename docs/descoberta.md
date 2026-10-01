# Fase de descoberta: o Claude aprende o ambiente sozinho, sem travar

Decisao da usuaria: o Claude conhece tudo do Paper Trading antes, usa as ferramentas e analisa os scripts. **Nao precisa ficar
travado esperando resposta dela.**

## Regras
1. **Descobrir antes de perguntar.** So perguntar o que nao der para descobrir, e em lote (uma mensagem so).
2. **Nao parar:** se uma ferramenta falhar, registrar a falha e seguir para o proximo item.
3. **Somente leitura**, exceto o teste de aceitacao da execucao (ordem de lote minimo no **Paper Trading**, autorizada).
4. **Registrar tudo:** `python scripts/calendar_db.py add-fact --key K --value V --source S --confidence alta|media|baixa`.
   Chaves de conta (`usd_per_point_per_lot`, `min_lot`, `usual_lot`, `paper_balance_usd`, `leverage`, `margin_per_lot_usd`) atualizam
   o `rules.json` (so com confianca alta ou media). Ver o que ja foi descoberto: `facts`.
5. **Nao inventar:** dado nao encontrado = "nao encontrado", nunca um palpite gravado como fato.

## Roteiro (nesta ordem)
**A. Ambiente:** Node/Git; MCP do TradingView (`tv_health_check`); listar as ferramentas disponiveis e o que cada uma faz
(inclusive se existe alguma que coloque ordens).
**B. TradingView:** simbolo e tempo grafico atuais; ler as ultimas velas M5; informacoes do simbolo (tamanho do tick, valor do
ponto, quantidade minima); abrir VIX, Brent, US10Y, ES e DXY e anotar se carregam e se vem **atrasados** (plano Basic).
**C. Paper Trading:** saldo, moeda, alavancagem, margem por lote, **o que "1" significa na posicao** (a usuaria usa 0,1), recursos do
painel de ordens (stop e alvo na ordem), comissoes/spread. **Ler o historico de trades dela** (se houver): distancia dos stops,
tamanho, ganho/perda, horarios; calcular o valor do ponto por (lucro / pontos / lote).
**D. Scripts da usuaria:** ler o codigo dos indicadores no grafico dela (ex.: "Score ZN + Brent", "Score ES + ZN", "Sinal NAS100 a cada
5 velas", "FVG/IFVG", "Session Liquidity", "POI Liquidez + Expansao V1.9") e documentar em `docs/indicadores-da-usuaria.md` o que cada um
calcula e quais saidas numericas ele expoe. Codigo de terceiros (ex.: LuxAlgo, CC BY-NC-SA): so uso pessoal, manter atribuicao.
**E. Painel macro dela:** https://analistamacro.prospectia.space/ (publico): anotar que dados mostra e como o viés poderia sair dele.
**F. Fontes:** testar a leitura do calendario do Investing (pela extensao) e das fontes de sentimento (Finviz etc.), anotando o que
funciona, o que vem atrasado e o que e bloqueado.
**G. Corretora:** se a Pepperstone estiver conectada ao TradingView, ler (sem operar) as especificacoes do NAS100: lote minimo,
passo do lote, valor do ponto, margem.
**H. Teste de aceitacao da execucao (Paper Trading):** ordem de compra de lote minimo com stop e alvo; ler a posicao de volta; fechar;
repetir com venda; forcar uma falha (stop invalido) e ver se avisa. Medir o tempo da ordem.
**I. Consumo:** anotar o uso de tokens da sessao (`/cost`, `/usage`).

## Saida da descoberta
- Fatos em `facts` (e `rules.json` > `account` atualizado).
- `docs/indicadores-da-usuaria.md` e `docs/descoberta-relatorio.md` (o que funciona, o que nao, o que falta e o que so a usuaria sabe).
- Lista curta de perguntas **que so ela pode responder** (por exemplo: "aqui eu ja paro" = fechar a operacao ou parar o dia?).
