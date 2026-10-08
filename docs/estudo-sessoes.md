# Estudo entre sessoes (07/10/2026) - NAS100 CFD Dukascopy M1, 520 dias (30/09/2024 a 06/10/2026)
Script: scripts/estudo_sessoes.py (relogio ancorado em NY: abertura de NY sempre 10:30; sessoes: Sydney 19-21, Asia 21-03, Londres 03-10:30, NY AM 10:30-13, almoco 13-14:30, NY PM 14:30-17).
## Resultado
- **Direcao: nenhuma sessao tem vies claro.** % de alta: Sydney 52, Asia 52, Londres 56 (unica perto de separar), NY AM 55, almoco 54, NY PM 51 (todos IC inclui 50%).
- **Uma sessao NAO preve a seguinte** (alta->alta ~ baixa->alta, diferencas <5 pts) e NAO preve o fechamento do dia (concordancia 49-51%).
- **Tamanho (isso e estavel e util):** amplitude mediana Sydney 71 pt | Asia 106 | Londres 164 | NY AM 228 (mov. liquido 103) | almoco 106 | NY PM 128. NY AM e a sessao que mais move.
- **Varredura (descritivo):** a sessao seguinte rompe a maxima da anterior em 59-67% (Sydney/Asia/Londres->proxima); almoco rompe pouco a de NY AM (34% max / 23% min; 43% nao rompe nenhuma). Rompe as DUAS em 21-27%.
- **Depois de varrer so um lado, fecha alem do nivel:** ~64-68% (Asia, Londres, NY AM varrendo maxima), 53-56% no almoco/NY PM. ATENCAO: isso condiciona em algo que so se sabe DURANTE a sessao; serve para entender o comportamento, nao como gatilho (e quase tautologico: quem rompe e mais provavel fechar la).
## Lacunas
Nao testado ainda: reversao apos varredura com pavio (fechar de volta DENTRO) ao vivo; efeito de dia de evento por sessao; amostra de 2026 separada.
