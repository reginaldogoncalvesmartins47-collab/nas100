"""Backtest do indicador 'Structure Volume Profile Setups' (Pine v6) portado 1:1 para Python.
Dados: data/nas100_m5_mt5.csv (M5, tick volume). Uso: python -I scripts/backtest_structure_vp.py
Fidelidade: mesma ordem de operacoes por barra do Pine (pivos -> rompimentos -> void -> setup novo -> fill/TP/SL na mesma barra, SL antes de TP).
Limites: sessionBreak aproximado por buraco >5 min ate a proxima barra; pivothigh com empate so a direita; volume = tick volume.
"""
import csv, datetime as dt, math, os, statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load():
    T, O, H, L, C, V, S = [], [], [], [], [], [], []
    for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'nas100_m5_mt5.csv')), delimiter='\t'):
        T.append(dt.datetime.strptime(r['<DATE>'] + ' ' + r['<TIME>'], '%Y.%m.%d %H:%M:%S'))
        O.append(float(r['<OPEN>'])); H.append(float(r['<HIGH>'])); L.append(float(r['<LOW>'])); C.append(float(r['<CLOSE>']))
        V.append(float(r['<TICKVOL>']) or 1.0); S.append(float(r['<SPREAD>']) / 10.0)
    return T, O, H, L, C, V, S

def atr_series(H, L, C, n=14):
    out, rma = [], None
    trs = []
    for i in range(len(C)):
        tr = H[i] - L[i] if i == 0 else max(H[i] - L[i], abs(H[i] - C[i - 1]), abs(L[i] - C[i - 1]))
        trs.append(tr)
        if i < n - 1:
            out.append(None)
        elif i == n - 1:
            rma = sum(trs) / n; out.append(rma)
        else:
            rma = (rma * (n - 1) + tr) / n; out.append(rma)
    return out

def htf_dir_series(T, C, minutes=60, ema_len=50):
    """direcao do EMA50 do timeframe maior, usando so barras HTF fechadas (dir[1])."""
    buckets, order = {}, []
    for i, t in enumerate(T):
        k = t.replace(minute=0, second=0) if minutes == 60 else t
        if k not in buckets: buckets[k] = []; order.append(k)
        buckets[k].append(i)
    k_ = 2 / (ema_len + 1); ema = None; dirs = {}; prev = 0
    for k in order:
        c = C[buckets[k][-1]]
        ema = c if ema is None else c * k_ + ema * (1 - k_)
        dirs[k] = prev  # valor confirmado da barra HTF anterior
        prev = 1 if c > ema else -1
    return [dirs[t.replace(minute=0, second=0)] for t in T]

def run(D, swing=5, bos_req=3, rows=30, va_pct=70, sl_mult=1.0, tp_mode='VA', tp_mult=2.0,
        gap_filter=True, side_filter=True, void_choch=True, expiry=0, htf=None, cost_pts=0.0):
    T, O, H, L, C, V, S = D
    n = len(C); ATR = atr_series(H, L, C)
    HD = htf_dir_series(T, C) if htf else None
    sess_break = [i + 1 < n and (T[i + 1] - T[i]).total_seconds() > 300 for i in range(n)]
    is_gap = [i > 0 and ATR[i] is not None and abs(O[i] - C[i - 1]) > ATR[i] for i in range(n)]
    cache_n = 300

    def build(a, b, i):
        first = i - min(i + 1, cache_n) + 1
        s = min(i, max(first, a)); e = min(i, max(s, b))
        top = max(H[s:e + 1]); bot = min(L[s:e + 1]); step = (top - bot) / rows
        vols = [0.0] * rows
        if step > 0:
            for j in range(s, e + 1):
                r1 = max(0, min(rows - 1, int(math.floor((L[j] - bot) / step))))
                r2 = max(0, min(rows - 1, int(math.floor((H[j] - bot) / step))))
                vp = V[j] / (r2 - r1 + 1)
                for r in range(r1, r2 + 1): vols[r] += vp
        mx = max(vols); poc_i = vols.index(mx); target = sum(vols) * va_pct / 100.0
        up = dn = poc_i; acc = vols[poc_i]
        for _ in range(rows):
            if acc >= target or (up >= rows - 1 and dn <= 0): break
            vu = vols[up + 1] if up < rows - 1 else -1.0
            vd = vols[dn - 1] if dn > 0 else -1.0
            if vu >= vd: up += 1; acc += vu
            else: dn -= 1; acc += vd
        return (bot + (poc_i + 0.5) * step, bot + (up + 1) * step, bot + dn * step, step, mx)

    def has_gap(a, b, i):
        first = i - min(i + 1, cache_n) + 1
        s = min(i, max(first, a)); e = min(i, max(s, b))
        return any(is_gap[s:e + 1])

    last_high = last_low = None; high_taken = low_taken = True
    last_high_bar = last_low_bar = None
    trend = 0; bull_bos = bear_bos = 0; choch_bar = None; ext = None; ext_bar = None
    p_dir = 0; p_entry = p_tp = p_sl = None; p_filled = False; p_bar = None; p_idx = None
    trades = []; n_setups = n_void = n_gap_rej = n_side_rej = 0; pend = None

    for i in range(n):
        atr = ATR[i] if ATR[i] is not None else 0.1
        # pivos (confirmados swing barras depois)
        if i >= 2 * swing:
            j = i - swing
            if H[j] > max(H[j - swing:j]) and H[j] >= max(H[j + 1:i + 1]): last_high, last_high_bar, high_taken = H[j], j, False
            if L[j] < min(L[j - swing:j]) and L[j] <= min(L[j + 1:i + 1]): last_low, last_low_bar, low_taken = L[j], j, False
        if trend == 1 and (ext is None or H[i] > ext): ext, ext_bar = H[i], i
        if trend == -1 and (ext is None or L[i] < ext): ext, ext_bar = L[i], i
        can_arm = p_dir == 0 and not (gap_filter and (sess_break[i] or is_gap[i]))
        long_sig = short_sig = choch_ev = False; s0 = e0 = None
        hd = HD[i] if HD else 0

        def try_signal(direction, bos_cnt, htf_ok):
            nonlocal n_gap_rej, n_side_rej
            if bos_cnt >= bos_req and htf_ok and choch_bar is not None and can_arm:
                a = choch_bar; b = ext_bar if ext_bar is not None else i
                if gap_filter and has_gap(a, b, i): n_gap_rej += 1; return None
                poc, _, _, step, mx = build(a, b, i)
                ok = True
                if side_filter:
                    ok = (step > 0 and mx > 0) and ((C[i] > poc) if direction == 1 else (C[i] < poc))
                if not ok: n_side_rej += 1; return None
                return (a, b)
            return None

        if high_taken is False and last_high is not None and C[i] > last_high:
            high_taken = True; is_bos = trend == 1
            if is_bos: bull_bos += 1
            else:
                r = try_signal(-1, bear_bos, (not htf) or hd == -1)
                if r: short_sig, (s0, e0) = True, r
                choch_ev = True; bear_bos = bull_bos = 0; trend = 1; choch_bar = i; ext = H[i]; ext_bar = i
        if low_taken is False and last_low is not None and C[i] < last_low:
            low_taken = True; is_bos = trend == -1
            if is_bos: bear_bos += 1
            else:
                r = try_signal(1, bull_bos, (not htf) or hd == 1)
                if r: long_sig, (s0, e0) = True, r
                choch_ev = True; bull_bos = bear_bos = 0; trend = -1; choch_bar = i; ext = L[i]; ext_bar = i
        # void de pendente
        gap_void = gap_filter and (sess_break[i] or is_gap[i])
        if (( void_choch and choch_ev) or gap_void or (expiry > 0 and p_bar is not None and i - p_bar >= expiry)) and p_dir != 0 and not p_filled:
            p_dir = 0; n_void += 1
        # setup novo
        if long_sig or short_sig:
            d_ = 1 if long_sig else -1
            poc, vah, val, step, mx = build(s0, e0, i)
            if step > 0 and mx > 0:
                tp = (vah if d_ == 1 else val) if tp_mode == 'VA' else (poc + atr * tp_mult if d_ == 1 else poc - atr * tp_mult)
                sl = poc - atr * sl_mult if d_ == 1 else poc + atr * sl_mult
                p_entry, p_tp, p_sl, p_dir, p_bar, p_filled = poc, tp, sl, d_, i, False
                n_setups += 1; p_idx = i
        # fill / TP / SL
        if p_dir != 0 and p_entry is not None:
            if not p_filled and L[i] <= p_entry <= H[i]:
                p_filled = True; fill_i = i
            if p_filled:
                hit = None
                if p_dir == 1:
                    if L[i] <= p_sl: hit = 'SL'
                    elif H[i] >= p_tp: hit = 'TP'
                else:
                    if H[i] >= p_sl: hit = 'SL'
                    elif L[i] <= p_tp: hit = 'TP'
                if hit:
                    risk = abs(p_entry - p_sl); rew = abs(p_tp - p_entry)
                    r = (rew / risk if hit == 'TP' else -1.0) - (cost_pts / risk if risk > 0 else 0)
                    trades.append(dict(t=T[i], d=p_dir, hit=hit, r=r, rr=rew / risk if risk else 0, risk=risk, bars=i - fill_i, setup=T[p_idx]))
                    p_dir = 0; p_filled = False
    return trades, dict(setups=n_setups, voided=n_void, gap_rej=n_gap_rej, side_rej=n_side_rej)

def report(name, res):
    trades, info = res
    n = len(trades)
    if not n: print(f'{name:38s} sem trades | {info}'); return
    w = [t for t in trades if t['hit'] == 'TP']; rs = [t['r'] for t in trades]
    gp = sum(r for r in rs if r > 0); gl = -sum(r for r in rs if r < 0)
    eq = peak = dd = 0.0
    for r in rs:
        eq += r; peak = max(peak, eq); dd = max(dd, peak - eq)
    print(f"{name:38s} setups {info['setups']:4d} canc {info['voided']:4d} | trades {n:4d} win {len(w)/n*100:5.1f}% "
          f"| R medio {sum(rs)/n:+.2f} | soma {sum(rs):+7.1f}R | PF {gp/gl if gl else float('inf'):.2f} | DD {dd:.1f}R | RR medio {st.mean(t['rr'] for t in trades):.1f} | risco medio {st.mean(t['risk'] for t in trades):.1f}pts")

if __name__ == '__main__':
    D = load()
    print(f'{len(D[0])} velas M5, {D[0][0]} a {D[0][-1]}\n')
    report('PADRAO do indicador (como esta)', run(D))
    report('padrao + custo 1,5 pts/trade', run(D, cost_pts=1.5))
    report('stop 2 ATR', run(D, sl_mult=2.0))
    report('stop 3 ATR', run(D, sl_mult=3.0))
    report('alvo ATR 2x / stop 1x', run(D, tp_mode='ATR', tp_mult=2.0))
    report('alvo ATR 1x / stop 1x', run(D, tp_mode='ATR', tp_mult=1.0))
    report('filtro HTF 1h', run(D, htf=True))
    report('sem cancelar no CHoCH', run(D, void_choch=False, expiry=60))
    report('bos_req 2', run(D, bos_req=2))
    report('swing 8', run(D, swing=8))
    tr = run(D)[0]
    for name, f in (('so COMPRA', lambda t: t['d'] == 1), ('so VENDA', lambda t: t['d'] == -1)):
        sub = [t for t in tr if f(t)]
        if sub: print(f"{name:12s} n {len(sub)} win {sum(t['hit']=='TP' for t in sub)/len(sub)*100:.1f}% R medio {sum(t['r'] for t in sub)/len(sub):+.2f}")
    by = {}
    for t in tr: by.setdefault(t['t'].strftime('%Y-%m'), []).append(t['r'])
    print('por mes (padrao):', {k: (len(v), round(sum(v), 1)) for k, v in sorted(by.items())})
