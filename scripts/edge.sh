#!/bin/bash
# Atalho do Edge Stats local (docs/edge-stats-local.md). Uso:
#   bash scripts/edge.sh sync                                  # atualiza os dados ate hoje (Dukascopy, gratis)
#   bash scripts/edge.sh report green-rate --symbol USATECH
#   bash scripts/edge.sh query "closeGreen WHERE dayOfWeek = Thu" --symbol USATECH
#   bash scripts/edge.sh fields                                # todos os campos/condicoes/resultados possiveis
cd "$(dirname "$0")/../tools/edge-stats-src" && pnpm edgestats --dir ../edge-lab "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -v '^\$'
