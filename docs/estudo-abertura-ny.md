# Abertura de NY x dados das 10:00 ET (estudo de 06/10/2026)
Origem: trade 16 de 05/10 (venda 10:35 BRT, stop -US$ 12,59): o spike de abertura de NY pesou mais que PMI/ISM. Script: `python scripts/estudo_abertura_ny.py` (NAS100 M5 do MT5, 02/10/2025-01/05/2026, 149 dias uteis; 71 com dado medio/alto as 10:00 ET).
Hora: abertura NY = 09:30 ET = **10:30 BRT** (outubro, DST dos EUA) = 16:30 servidor MT5. Dado 10:00 ET = 11:00 BRT.

## Resultado
| Medida | Valor |
|---|---|
| Amplitude mediana da vela M5 das 09:30 ET (abertura) | **77 pts** |
| Vela M5 das 09:45 ET (todos os dias; o PMI de servicos so sai em parte deles) | 59 pts |
| Vela M5 das 10:00 ET, dia COM dado medio/alto | 56 pts |
| Vela M5 das 10:00 ET, dia SEM dado | 40 pts |
| Dias em que a abertura teve amplitude maior que a vela do dado | **80%** (73% nos dias com dado) |

Leitura: o dado das 10:00 ET soma ~16 pts (+40%) a uma vela que ja seria 40; a abertura faz 77 sozinha. A abertura vence o dado em 4 de cada 5 dias.

## Entrar CONTRA o spike da abertura (como a venda de 05/10), 10 min depois, olhando 60 min
| Grupo | n | Spike continuou | Foi a favor (medio) | Foi contra (medio) | Resultado em 60 min |
|---|---|---|---|---|---|
| todos os dias | 149 | 54% | 98 | 105 | -1 pt |
| spike grande (>= 52 pts) | 51 | 63% | 83 | 122 | **-27 pts** |
| spike grande para CIMA (venda) | 26 | **69%** | 78 | 120 | **-41 pts** |
| spike grande para BAIXO (compra) | 25 | 56% | 89 | 124 | -12 pts |

Leitura: contra um spike grande de abertura, a media perde. Vender o spike para cima foi o pior caso (69% continuaram subindo). Amostra pequena (26 e 25), nao prova: so desfavorece a regra "entra contra o spike".
Limites: so Out/2025-Mai/2026; nao separa dia de ISM de dia sem dado nem direcao do D1; 'spike' = so a vela 09:30.

## Regra proposta (a usuaria aprova; vai para o CLAUDE.md)
Ver secao "ABERTURA DE NY" no CLAUDE.md.
