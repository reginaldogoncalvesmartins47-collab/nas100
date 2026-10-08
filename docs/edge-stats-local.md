# Edge Stats local (LuxAlgo, MIT) - montado em 07/10/2026
Motor de estatisticas condicionais com N, intervalo de confianca de 95% e estabilidade por metades. Instalado em `tools/edge-stats-src` (clone de github.com/LuxAlgo/edge-stats, pnpm install) e usado com a pasta de dados `tools/edge-lab` (config `edge-stats.config.json`, armazenamento `.edge-stats` fora do git).
## Dados
- `NAS100` (adaptador csv): 100.000 velas M1 do MT5 (20/01 a 01/05/2026) = so 72 sessoes RTH (amostras pequenas). Conversao: scripts/mt5_m1_para_edgestats.py.
- **`USATECH` (adaptador dukascopy, GRATIS, sem chave): CFD do Nasdaq 100 em M1 desde 01/10/2024 ate HOJE (689.452 barras, 520 sessoes RTH).** Fonte preferida: mais historico e atualizavel com `sync`. (Preco de CFD da Dukascopy, volume por tick: forma de sessao e robusta, preco exato nao e o da Pepperstone.) Para mais historico mudar `adapterOptions.start`.
## Como rodar (pasta tools/edge-stats-src)
`pnpm edgestats --dir ../edge-lab sync` (atualiza ate hoje) | `report <preset> --symbol USATECH [--group ...]` | `query "<DSL>" --symbol USATECH` | `presets` | `fields` | `serve` (painel em localhost:3343). 42 presets: gaps, faixa de abertura, initial balance, FVG de sessao, dia da semana, dias de CPI/FOMC/NFP/OPEX, horario da maxima, etc. Sessao padrao: rth (09:30-16:00 NY); `--session globex` para a sessao inteira.
## Primeiras leituras (USATECH, sessoes RTH, 2024-10 a 2026-10)
| Pergunta | Resultado |
|---|---|
| Sessao fecha acima da abertura (base) | 53,5% (N=520, IC 49,2-57,7%); 2024 56,9% / 2025 55,3% / **2026 50,0%** |
| Por dia da semana | seg 61,0% (N=105) · ter 52,8% · qua 51,9% · qui 47,1% · sex 54,4% (todos com IC largo; nenhum separa de 53,5%) |
| Dia de CPI | 39,1% fecha acima (N=23, amostra baixa: anedota) |
| Dia de FOMC | 43,8% (N=16, anedota) |
| Dia de NFP | 39,1% (N=23, anedota) |
Leitura: sem vantagem direcional clara; dias de dado forte tendem a fechar abaixo da abertura mas com N<30 (nao e prova). Em 2026 a base caiu para 50%.
## Proximos usos
Estudo "continuar 1 hora" (condicoes de estrutura/VWAP/horario -> prob. 60 min depois) com `query` + campos de `fields`; ORB (so informativo, a usuaria nao quer operar ORB); gap fill; faixa de abertura por tipo de dia (com/sem CPI).
