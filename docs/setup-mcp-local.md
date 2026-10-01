# Setup local (Windows): TradingView Desktop + MCP da comunidade

Repositorio: https://github.com/tradesdontlie/tradingview-mcp (guia SETUP_GUIDE.md). Nao auditado.
O MCP oficial do TradingView exige plano Essential+; este caminho nao usa o MCP oficial.

1. Instalar Node.js, Git e Claude Code.
2. `git clone https://github.com/tradesdontlie/tradingview-mcp.git ~/tradingview-mcp` e `npm install` dentro da pasta.
3. Abrir o TradingView Desktop com `--remote-debugging-port=9222` (script `scripts\launch_tv_debug.bat` do repo).
   Se for MSIX (Microsoft Store) e der "Access is denied", seguir o guia do repo; nao alterar ACLs de WindowsApps.
4. Adicionar em `~/.claude/.mcp.json` (ou `.mcp.json` do projeto):
   `{"mcpServers":{"tradingview":{"command":"node","args":["C:\\Users\\SEU_USUARIO\\tradingview-mcp\\src\\server.js"]}}}`
5. Reiniciar o Claude Code e rodar `tv_health_check`.

Cuidados: a porta 9222 da controle total do app a programas locais; usar so no PC pessoal.
Verificar os termos de uso do TradingView. Nao sei se este MCP coloca ordens (a descoberta vai verificar: docs/descoberta.md); a execucao no Paper Trading sera testada na aceitacao (docs/execucao.md).
