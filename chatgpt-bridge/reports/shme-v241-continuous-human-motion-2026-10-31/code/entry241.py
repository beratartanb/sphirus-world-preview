"""entry241.py <label>... : V2.41 takeover ENTRY check (offline, LTP). For the first input change while a V2.38 cut plays: the cut clip / time
at the request, the clip / time MM entered, the expected contact K (gen239 contact table: t_(K-1) <= tau < t_K, K counted like the
Tk clip names), the entry time jump (entered time - tau - frames elapsed), and the turn-back latency (request -> the frame the heading
starts to move toward the new side). Prints ENTRY241 lines."""
import sys, os, re, json, glob, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026']
from ltp231 import load, short
ROOT = os.path.join(H, '..', '..')
J = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'Saved/Codex/SHME_V239_20261030/gen239_tk_write_part*.json'))): J.update(json.load(open(f))['clips'])
def contacts(side, p):
    c = J.get('SHM239_Tk_%s_P%02d_K1_Opp' % (side, p)) or J.get('SHM239_Tk_%s_P%02d_K1_Back' % (side, p))
    return [x['t'] for x in c['contacts']] if c else None
def run(lab):
    R = load(lab); prev = None; req = None
    for i, r in enumerate(R):
        cur = (r['lix'], r['liy']); o = short(r['av_Phase27_SelectedObject'])
        if prev is not None and cur != prev and math.hypot(*cur) > 0.3 and o.startswith('SHM238_Cut_'): req = i; break
        prev = cur
    if req is None: return 'ENTRY241 %s no request during a cut' % lab
    r0 = R[req]; cut = short(R[req - 1]['av_Phase27_SelectedObject']); tau = float(R[req - 1]['av_Phase27_SelectedTime']); m = re.match(r'SHM238_Cut_([RL])_P(\d\d)', cut)
    ent = None
    for j in range(req, min(req + 40, len(R))):
        o = short(R[j]['av_Phase27_SelectedObject'])
        if o.startswith('SHM239_Tk_'): ent = j; break
    C = contacts(m.group(1), int(m.group(2))) if m else None
    expK = None
    if C:
        for k in range(1, len(C)):
            if C[k - 1] <= tau + 1e-3 < C[k]: expK = k; break
    if ent is None: return 'ENTRY241 %s cut %s tau %.3f expK %s: NO takeover entered' % (lab, cut, tau, expK)
    eo = short(R[ent]['av_Phase27_SelectedObject']); et = float(R[ent]['av_Phase27_SelectedTime']); k = int(re.search(r'_K(\d)_', eo).group(1))
    jump = et - (tau + (R[ent]['t'] - R[req - 1]['t']))
    hd = lambda r: math.degrees(math.atan2(r['avy'], r['avx'])); h0 = hd(R[req]); sg = None; lat = None; hmax = h0
    side = 1 if m.group(1) == 'R' else -1
    for j in range(req, min(req + 60, len(R))):
        h = hd(R[j])
        if side * (h - hmax) > 0: hmax = h
        if side * (hmax - h) > 3.0: lat = R[j]['t'] - r0['t']; break
    return 'ENTRY241 %s cut %s tau %.3f -> %s @%.3f expK %s gotK %d jump %+.3f s | old-side overshoot %.0f deg, turn-back latency %s s' % (lab, cut, tau, eo, et, expK, k, jump, side * (hmax - h0), '%.2f' % lat if lat is not None else '-')
for lab in sys.argv[1:]:
    try: print(run(lab))
    except Exception as e: print('ENTRY241 %s err %s' % (lab, e))
