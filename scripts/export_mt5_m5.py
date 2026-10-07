"""Exporta historico M5 do NAS100 do MetaTrader 5 (SOMENTE LEITURA de precos; nao envia ordem, nao le saldo/conta).
Uso: abrir o MT5 (Pepperstone) e deixar logado; depois: python scripts/export_mt5_m5.py [dias]
Saida: data/nas100_m5_mt5.csv (time_utc, time_server, open, high, low, close, tick_volume, spread)
ponytail: usa o pacote oficial MetaTrader5; hora do servidor != UTC (corretora GMT+2/+3), por isso grava as duas colunas.
"""
import sys
from datetime import datetime, timedelta, timezone
import MetaTrader5 as mt5
import csv

dias = int(sys.argv[1]) if len(sys.argv) > 1 else 90
if not mt5.initialize():
    sys.exit(f"MT5 nao conectou: {mt5.last_error()} (abra o terminal e deixe logado)")
syms = [s.name for s in (mt5.symbols_get() or []) if any(k in s.name.upper() for k in ("NAS100", "USTEC", "US100", "NDX"))]
print("simbolos candidatos:", syms)
if not syms:
    mt5.shutdown(); sys.exit("nenhum simbolo NAS100/US100/USTEC encontrado")
sym = syms[0]
mt5.symbol_select(sym, True)
fim = datetime.now(timezone.utc)
import time
# o MT5 baixa o historico do servidor sob demanda: pedir varias vezes ate parar de crescer
rates, n_ant = None, -1
for _ in range(8):
    rates = mt5.copy_rates_range(sym, mt5.TIMEFRAME_M5, fim - timedelta(days=dias), fim)
    n = 0 if rates is None else len(rates)
    print("tentativa: barras =", n)
    if n and n == n_ant:
        break
    n_ant = n
    time.sleep(4)
mt5.shutdown()
if rates is None or len(rates) == 0:
    sys.exit("sem barras (o MT5 so devolve o que ja baixou; abra o grafico M5 do simbolo e role para tras)")
with open("data/nas100_m5_mt5.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["symbol", "time_server_as_utc", "open", "high", "low", "close", "tick_volume", "spread"])
    for r in rates:
        w.writerow([sym, datetime.fromtimestamp(int(r["time"]), timezone.utc).strftime("%Y-%m-%d %H:%M"),
                    r["open"], r["high"], r["low"], r["close"], int(r["tick_volume"]), int(r["spread"])])
print(f"{sym}: {len(rates)} barras M5, de {datetime.fromtimestamp(int(rates[0]['time']), timezone.utc)} a {datetime.fromtimestamp(int(rates[-1]['time']), timezone.utc)} (hora do SERVIDOR) -> data/nas100_m5_mt5.csv")
