# Liquidez válida, Fibonacci em TF maior e pontuação de regiões

> Status: conceitos gerais + **hipóteses a calibrar**. Todo número marcado (H) é palpite inicial e deve ser
> testado com dados históricos do NAS100 antes de virar regra fixa.

## 1. O que é liquidez
Liquidez é onde há **ordens acumuladas**: stops de quem está comprado abaixo de fundos e stops/entradas de quem
está vendido acima de topos. O preço tende a ir buscar essas ordens.
- **BSL (buy-side):** acima de topos. **SSL (sell-side):** abaixo de fundos.
- **Externa (ERL):** extremos do range / níveis de TF maior. **Interna (IRL):** desequilíbrios dentro do range.

## 2. Quando uma liquidez é VÁLIDA
Uma liquidez só entra na lista se passar nestes critérios:

| Critério | Regra | Por quê |
|---|---|---|
| Estrutural | É um swing high/low claro (pivô com N barras de cada lado; H: 5 em H1, 10 em M15) | Stops de verdade ficam atrás de pontos óbvios |
| Intacta | Ainda **não foi varrida** | Depois de varrida e aceita, a liquidez foi consumida |
| Hierarquia | Semana > dia > sessão (Ásia/Londres) > intradiário | TF maior = mais ordens |
| Toques | Topos/fundos iguais (equal highs/lows) valem mais; tolerância H: 0,15 x ATR(H1) | Muitos stops no mesmo lugar |
| Alcançável | Dentro de H: 2 x ATR(H1) do preço | Longe demais não influencia o agora |
| Contexto macro | Liquidez **no sentido da macro** = alvo. Liquidez **contra** a macro = zona de reação | Liga liquidez ao viés do dia |

**Varredura válida:** o pavio passa do nível **e o candle fecha de volta** do lado de dentro (ou há deslocamento
claro na direção oposta). Se o preço **fecha além** do nível e fica, é aceitação (rompimento): não é varredura.

**Liquidez inválida/consumida:** já varrida; fechamento além do nível; nível sem estrutura (meio do nada); nível
de TF muito pequeno (ruído de M1/M5).

## 3. Fibonacci em TF maior
- **Desenhar no H1** (H), ancorando no **último movimento relevante**: do pivô de fundo ao pivô de topo (ou o
  inverso) do leg que **quebrou estrutura**. Regra objetiva: usar os pivôs do H1, sem escolher "a olho".
- **Zona de reação:** 0,5 a 0,786 (níveis: 0,5 / 0,618 / 0,786). A zona vale como **região**, não como ponto.
- Fibo em TF pequeno (M1/M5) gera muitas zonas e pouca informação: não usar como região principal.
- Redesenhar só quando um novo leg quebrar estrutura (evita "fibo que muda toda hora").

## 4. Pontuação de regiões (a região NÃO é o gatilho)
O robô **primeiro pontua regiões** e só depois procura gatilho. Uma região é um grupo de níveis dentro de
H: 0,3 x ATR(H1) um do outro.

| Fator | Pontos (H) |
|---|---|
| Zona de Fibo H1 (0,5-0,786) | +1 |
| Máxima/mínima do dia anterior (PDH/PDL) | +1 |
| Máxima/mínima da semana anterior (PWH/PWL) | +2 |
| Máxima/mínima de sessão (Ásia/Londres) | +1 |
| Equal highs/lows | +1 |
| FVG / desequilíbrio não mitigado | +1 |
| Nível redondo (ex.: 30.000) | +0,5 |
| Reação anterior no mesmo lugar | +1 |

- Nota mínima para a região contar: **3 (H)** a favor da macro; **4 (H)** se o trade for **contra a macro**.
- Exemplo (ilustrativo, números inventados): Fibo 0,618 do H1 em 29.480 (+1) coincide com a mínima do dia
  anterior em 29.470 (+1) e equal lows em 29.475 (+1) = nota 3: região válida.

## 5. Da região à entrada
Região pontuada é só o "onde". A entrada exige **tudo** isto:
1. Região com nota mínima.
2. Gatilho: varredura válida + fechamento de volta (ou o critério de confirmação que o usuário definir).
3. Espaço até o alvo (próxima liquidez oposta) com RR mínimo (H: 2:1).
4. Horário de operação e limites de risco (`docs/regras-risco.md`).
5. Contra a macro: nota maior, risco menor e saída mais curta (ex.: meio da faixa).

## 6. Erros comuns
- Tratar o nível como sinal (entrar ao tocar, sem esperar a reação).
- Usar liquidez já varrida.
- Fibo em TF pequeno ou ancorada "a olho".
- Ignorar o contexto da macro.

## 7. Calibração (obrigatória antes de confiar)
Com a base M15 do NAS100: medir, para cada fator, a frequência e a duração da reação; ajustar pontos e nota
mínima; comparar trades com e sem a pontuação. Sem esse teste, os pontos acima são só palpite.
