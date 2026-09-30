# Projeto NAS100 - copiloto de trade com TradingView

Contexto para o Claude Code. Leia `docs/` antes de agir.

## Objetivo
Ajudar o usuario a operar o NAS100 (PEPPERSTONE:NAS100): ler o grafico no TradingView, analisar cenario
(macro + liquidez) e sugerir entradas com stop e alvo. Primeiro em demo (Paper Trading), depois real.

## Regras que valem sempre
- Conta real pequena (US$ 20): risco por trade e corte total estao em `docs/regras-risco.md`. Nao relaxar.
- NAO executar ordens em conta real. Execucao em Paper Trading so com autorizacao explicita do usuario.
- Nao prometer resultado. Dizer quando nao ha setup. Resultados de backtest nao valem como prova.
- Nao inventar dados de preco/volume: se o dado nao estiver disponivel, dizer.
- Nao tocar em abas de corretora/banco ao usar o navegador.

## Metodo (resumo, detalhes em `docs/metodo.md`)
- Direcao macro vem do usuario (painel proprio e leitura de Brent, juros, ES, calendario, geopolitica).
- Entrada por varredura de liquidez (dia/semana anterior, Asia, Londres) a favor do vies.
- Horario de operacao: 06:00-23:20 (Brasilia), seg-sex.

## Arquivos
- `pine/` scripts Pine (TradingView). `nas100_liquidez_v2.pine` e o atual; nao testado ate o momento.
- `docs/` metodo, risco, setup do MCP, roadmap.
- `journal/` diario de trades (CSV).

## Estado
Ver `docs/roadmap.md`.
