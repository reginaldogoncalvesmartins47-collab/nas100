# Roadmap

- [x] Estrategia Pine v1 (macro + liquidez) - backtest mostrou 5 trades; teste parou cedo pelo corte de seguranca
- [x] Estrategia Pine v2 (liquidez + vies manual) - escrita, NAO testada/compilada
- [x] Documento de liquidez valida, Fibo H1 e pontuacao de regioes (hipoteses a calibrar)
- [x] Caso de estudo 01 registrado; niveis de Fibo configuraveis e sem prioridade (docs/casos/)
- [x] Regiao 2 (Fibo M15 como refinamento) registrada em docs/liquidez-e-regioes.md
- [ ] Confirmar com o usuario como ancorar a Fibo M15
- [ ] Definir com o usuario o fim da lateralizacao e a volta da macro (caso 01)
- [ ] Calibrar pontos/tolerancias com a base M15 do NAS100 (usuario precisa fornecer o CSV)
- [ ] Compilar e rodar v2 no Pine Editor (M15, modo teste, capital 1000, limites altos)
- [ ] Ler backtest e lista de negociacoes; ajustar niveis/gatilho
- [ ] Definir gatilho exato e criterio de volume (ver docs/metodo.md, secao A DEFINIR)
- [ ] Conferir lote minimo/valor do ponto/margem do NAS100 na Pepperstone
- [ ] Ativar Paper Trading (PEPPERSTONE:NAS100, saldo US$ 20) e registrar trades em journal/
- [ ] Instalar Node/Git/Claude Code e o MCP local (docs/setup-mcp-local.md)
- [ ] Checagem periodica (ex.: /loop 5m) com o grafico real, somente sinalizando
- [ ] 30-50 trades na demo; revisar diario semanalmente
- [ ] Decidir sobre robo (MT5/cTrader) somente depois de resultado positivo na demo
