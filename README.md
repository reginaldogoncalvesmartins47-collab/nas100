# NAS100 - copiloto de trade com TradingView e Claude

Projeto da usuaria (Nayara) para o **Claude operar o NAS100 (Pepperstone)**: ler o mercado, fazer o dever de casa (calendario, noticias, pares, sentimento),
achar regioes de liquidez/Fibo/oferta-demanda, entrar quando o mercado mostra rejeicao de pavio em M5, e gerir a saida. **Demo primeiro, real depois.**

> **Status honesto:** tudo aqui e planejamento + codigo de apoio. **Nada foi testado com dados reais** e nao ha garantia de lucro.

## Comece por aqui
1. `docs/decisoes-alinhadas.md` - tudo o que a usuaria decidiu (e o que e hipotese ou pendencia).
2. `CLAUDE.md` - instrucoes que o Claude Code le a cada sessao.
3. `docs/primeira-execucao.md` - texto para colar no Claude Code do PC na primeira vez (fase de descoberta).

## Mapa
| Pasta/arquivo | O que e |
|---|---|
| `CLAUDE.md`, `rules.json` | Instrucoes e regras em formato de maquina |
| `docs/` | Metodo, regioes, calendario, noticias, pares, sentimento, choque, saida, meta diaria, risco, execucao, custo, descoberta, roadmap |
| `docs/casos/` | Casos reais (graficos e calendario) |
| `scripts/calendar_db.py` | Banco local SQLite e todos os comandos (`python scripts/calendar_db.py -h`) |
| `pine/` | Scripts Pine para backtest e alertas (nao compilados) |
| `journal/` | Diario de trades |
| `data/` | Banco local (nao vai para o git) e exemplos |

## Comandos principais
`gate` (semaforo e pendencias) | `entry-check` (gatilho em M5) | `open-trade`/`update-trade`/`close-trade` | `path`/`wick` | `daily`/`review`/`goal`/`ready` | `shock` | `tune`.
