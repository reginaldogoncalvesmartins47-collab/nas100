# Fase 2: analise das noticias e do gap (antes de qualquer entrada)

Caso que motivou: viés de alta na sexta; abertura de domingo em queda forte por petroleo e noticia de IA (OpenAI).
Quem opera com o vies de sexta leva loss. Regra: **noticia nova invalida o vies ate nova analise.**

## Niveis de fonte (definicao inicial, a usuaria ajusta)
| Nivel | O que e | Uso |
|---|---|---|
| **1** | Oficial/primario: comunicados das empresas (ex.: OpenAI, NVIDIA), Fed, BLS/BEA, EIA/OPEC, CME; agencias (Reuters, AP, Bloomberg) e WSJ/FT | Base para decidir |
| **2** | Noticias de mercado com nome: Investing.com (noticias), CNBC, Yahoo Finance, Benzinga, Seeking Alpha, NPR | Confirmar e contextualizar |
| **3** | Agregadores, blogs, sites de SEO/automaticos (ex.: tradingkey, biggo, finwire, stocksdownunder, rollingout) | So como pista. Nunca como base |

## Janela de informacao (regra central)
- **Domingo, segunda (e sabado):** puxar tudo **desde a sexta-feira 00:00 (Brasilia)** ate agora.
- **Terca a sexta:** puxar sempre as **ultimas 24 horas**.
- **Data e hora com fuso sao obrigatorias.** Sem isso a noticia e rejeitada; tudo e convertido para Brasilia.
- Noticia **fora da janela nao explica o movimento de agora**. Se perguntarem "por que o NAS100 esta subindo/caindo?",
  responder so com itens da janela, cada um com data, hora e "ha X horas". Se nao houver nenhum: dizer
  "nenhuma noticia dentro da janela", e nao voltar a noticias de 5 dias atras.
- A janela e calculada pelo codigo (`python scripts/calendar_db.py window` e `news`), nao por memoria do modelo.
- Motivo: assistentes de IA costumam devolver noticias antigas para explicar um movimento forte de agora.
- Fuso: Brasilia fixo em UTC-3 (sem horario de verao desde 2019). Feriado dos EUA na segunda ainda nao tratado.

## Regras
1. **Data e hora de publicacao obrigatorias** (com fuso). Sem data: descartar. O banco recusa noticia sem data.
2. **Confirmacao:** noticia de alto impacto so conta com 2 fontes independentes de nivel 1 ou 2.
3. **Diferenciar:** *confirmado pela empresa/orgao* x *reportado por veiculo* x *rumor*. Registrar em `confidence`.
4. **Persistencia:** `pontual` (passa em horas) x `regime` (muda o cenario por dias). Registrar e justificar.
5. **Categorias que movem o NAS:** petroleo/Brent e geopolitica, juros/Fed, IA e tecnologia (OpenAI, NVIDIA, semicondutores), resultados de gigantes, dados macro.
6. **Janela:** tudo desde o ultimo fechamento e do fim de semana; em dia normal, ultimas 24-48 h.
7. **Acesso:** Investing so pela extensao do navegador (sem scraper). Outros: leitura de pagina/busca; nao usar pagina sem data.

## Regra do gap e do vies
- No reinicio (domingo ou overnight), medir o gap entre o ultimo fechamento e a abertura.
- Gap >= 1 x ATR(H1) (H) **ou** noticia de alto impacto depois de o vies ser definido => **vies = STALE (vencido)**.
- Com vies STALE: **sem sinal** ate a usuaria confirmar ou redefinir o vies com a nova analise.
- Registrar no diario: noticia, gap, vies antes e depois.

## Modelo de briefing de noticias
```
Janela: de ____ ate ____ (BRT)   Gap: ____ (__ x ATR H1)
Noticias (nivel | hora | fonte | confianca | persistencia | impacto no NAS):
Petroleo/Brent e geopolitica: ____
IA/tecnologia/semicondutores: ____
Fed/juros: ____
Vies anterior: ____  ->  vies agora: (mantido / VENCIDO) + motivo
```

## Observacao do teste de hoje (30/09/2026)
A busca trouxe itens de datas misturadas (meados e fim de setembro) e de sites de pesos muito diferentes. Isso e
exatamente por que as regras 1 e 2 existem.
