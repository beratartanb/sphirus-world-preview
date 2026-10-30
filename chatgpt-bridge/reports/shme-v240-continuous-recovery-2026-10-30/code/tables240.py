"""tables240.py <out.md> [tag=reg] [var=tk] [fps tags comma list] : V2.40 tables from the LTP side files of ONE editor session.
(1) worst planted-ball slide (contact231, owner clip) + upper-body pops + database-not-ready frames, production o vs the candidate;
(2) control stages of every input change (tk239: request -> first body reaction -> first support -> velocity transfer -> stable heading);
(3) body alignment after a takeover (balance238 on the second request: pelvis / chest / head yaw minus the velocity heading at +1.2 / +1.8 s);
(4) external effect: max residual, latched Ext frames, recovery families, for the push scenarios and a no-push planned cut;
(5) frame-rate modes (worst slide o / var, worst pop) for the given tags."""
import sys, os, json, math, subprocess
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V238_20261030', H + '/../SHME_V239_20261030', H]
from ltp231 import load
from tables238 import cell, runs, worst, nodb, pops
from balance238 import analyse
PY = sys.executable
SC = ['j40_rlw', 'j40_lrw', 'j39_rl', 'j39_rw', 'j39_rl_e', 'j39_rl_l', 'j39_lr', 'j39_lw', 'j38_cc90', 'mtf_jog', 'jlean', 'j38_c90r', 'j38_c90l', 'j38_c90rb', 'j38_c90lb',
      'j38_c45r', 'j38_c135r', 'w38_c90r', 's38_c90r', 'j36_rsm', 'j36_stop', 'j36_stopr', 'j34_chain1', 'j35_rev', 'j30_rel_3450', 'j36_sside', 'jstart',
      'e29_chain', 'c29_combo', 'jdiag', 'wdiag', 'wstart', 'cam32_j90', 'chain_jogcut', 'ad_jog', 'mt_jog', 'j39_push_plan', 'j39_push_jog']
TK = ['j40_rlw', 'j40_lrw', 'j39_rl', 'j39_rw', 'j39_rl_e', 'j39_rl_l', 'j39_lr', 'j39_lw', 'j38_cc90']
def stages(lab):
    try: o = subprocess.run([PY, os.path.join(H, '..', 'SHME_V239_20261030', 'tk239.py'), lab, '5.3', '12'], capture_output=True, text=True, timeout=120).stdout
    except Exception: return []
    out = []
    for ln in o.splitlines():
        if ln.strip().startswith('input'):
            head, js = ln.split(': ', 1); out.append((head.strip(), json.loads(js)))
    return out
def second_req(lab):
    R = runs(lab)
    if R is None: return None
    prev = None
    for r in R:
        if r['t'] < 5.5: prev = (r['lix'], r['liy']); continue
        cur = (r['lix'], r['liy'])
        if prev is not None and cur != prev and math.hypot(*cur) > 0.3: return r['t']
        prev = cur
    return None
if __name__ == '__main__':
    a = sys.argv[1:]; out = a[0]; tag = a[1] if len(a) > 1 else 'reg'; var = a[2] if len(a) > 2 else 'tk'; ft = [x for x in (a[3].split(',') if len(a) > 3 else []) if x]
    L = ['## 1. Worst planted-ball slide (cm, owner) and upper-body pops (count / worst m/s2), fixed 30 FPS: production o vs %s; * = database-not-ready frames' % var, '',
         '| scenario | o | o owner | o pops | %s | %s owner | %s pops |' % (var, var, var), '|---|---|---|---|---|---|---|']
    for s in SC:
        x = cell('v240%s_%s_o_r1' % (tag, s)); y = cell('v240%s_%s_%s_r1' % (tag, s, var))
        L.append('| %s | %s | %s | %s | %s | %s | %s |' % (s, x[0], x[1], x[2], y[0], y[1], y[2]))
    L += ['', '## 2. Control stages after each input change (s after the request frame; tk239)', '', '| scenario | variant | input | first body reaction | first support | velocity transfer | stable heading |', '|---|---|---|---|---|---|---|']
    for s in TK:
        for v in ('o', var):
            for head, st in stages('v240%s_%s_%s_r1' % (tag, s, v)):
                b = st.get('body'); L.append('| %s | %s | %s | %s | %s | %s | %s |' % (s, v, head.replace('input ', ''), '-' if b is None else '%s (%s)' % (b[0], b[1]), st.get('support', '-'), st.get('transfer', '-'), st.get('stable', '-')))
    L += ['', '## 3. Body alignment after the second request (yaw minus the velocity heading, deg; balance238)', '', '| scenario | variant | second request s | pelvis / chest / head @+1.2 | @+1.8 | speed @+1.8 |', '|---|---|---|---|---|---|']
    for s in TK:
        for v in ('o', var):
            lab = 'v240%s_%s_%s_r1' % (tag, s, v); t2 = second_req(lab)
            if t2 is None: L.append('| %s | %s | - |' % (s, v)); continue
            try: A = analyse(lab, t2, 2.0, 0.2)
            except Exception as e: L.append('| %s | %s | %.2f | err %s |' % (s, v, t2, str(e)[:40])); continue
            rows = A['rows']
            def at(tt):
                r = min(rows, key=lambda q: abs(q['t'] - tt))
                f = lambda k: '-' if r.get(k) is None or r.get('hd') is None else str(int(round(((r[k] - r['hd']) + 180) % 360 - 180)))
                return '%s / %s / %s' % (f('pel'), f('chest'), f('head')), r['spd']
            a1, _ = at(1.2); a2, sp = at(1.8)
            L.append('| %s | %s | %.2f | %s | %s | %s |' % (s, v, t2, a1, a2, sp))
    L += ['', '## 4. External effect vs planned velocity change', '', '| run | max residual cm/s | Ext frames | families seen | worst slide |', '|---|---|---|---|---|']
    for s in ('j39_push_plan', 'j39_push_jog', 'j38_c90r', 'j39_rl'):
        for v in ('o', var):
            lab = 'v240%s_%s_%s_r1' % (tag, s, v); R = runs(lab)
            if R is None: continue
            rs = [r for r in R if r['t'] > 2.5]
            L.append('| %s %s | %.0f | %d | %s | %.1f |' % (s, v, max(float(r.get('av_SHM239_Resid') or 0) for r in rs), sum(1 for r in rs if r.get('av_SHM239_Ext') in (True, 'True')),
                     sorted(set(int(round(float(r.get('av_SHM_Family') or 0))) for r in rs)), worst(R)[0]))
    if ft:
        FS = ['j39_rl', 'j39_rw', 'j39_lr', 'j38_cc90', 'mtf_jog', 'jlean', 'j38_c90r', 'j38_c90l', 'j39_push_plan']
        L += ['', '## 5. Frame-rate modes: worst slide cm o / %s (worst pop m/s2 o / %s)' % (var, var), '', '| scenario | ' + ' | '.join([tag] + ft) + ' |', '|---' * (len(ft) + 2) + '|']
        for s in FS:
            cs = []
            for t in [tag] + ft:
                x = cell('v240%s_%s_o_r1' % (t, s)); y = cell('v240%s_%s_%s_r1' % (t, s, var))
                px = x[2].split(' / ')[-1] if x[2] != '-' else '-'; py_ = y[2].split(' / ')[-1] if y[2] != '-' else '-'
                cs.append('%s / %s (%s / %s)' % (x[0], y[0], px, py_))
            L.append('| %s | %s |' % (s, ' | '.join(cs)))
    open(out, 'w', encoding='utf8').write('\n'.join(L) + '\n'); print('\n'.join(L))
