"""relphase231.py <label>... : release -> re-press classification (j30_rel_<ms> family: S released at <ms>/1000 s, re-pressed 0.15 s later).
Brake phase at the RELEASE frame (V2.31 brief, item 7):
  BRAKE_NO_SUPPORT  braking (speed falling, old travel), no foot planted yet in the authored brake (SHM228_Brake, no new contact)
  BRAKE_FOOT        braking with the brake foot planted (a contact flag rose after the request)
  NEAR_ZERO         |speed| < 40 cm/s
  NEW_PUSH          already moving in the NEW direction (velocity against the facing for an F_B request)
  STANDING          idle entry / speed < 5 cm/s for >= 0.2 s
Outcome after the RE-PRESS: the clip family serving the next 0.5 s (authored SHM226 / slow SHM231S / AAMS start / stop / idle), the worst
planted-foot SLIP/DRAG (contact231) in [re-press - 0.1, re-press + 1.0], idle entry inside the window. Prints RELPHASE231 lines."""
import sys, os, re, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
from contact231 import classify
def fam(o):
    if o.startswith('SHM226_JogRev'): return 'AUTH'
    if o.startswith('SHM231S'): return 'SLOW'
    if o.startswith('SHM231L'): return 'LOAD'
    if 'Start' in o: return 'START'
    if 'Stop' in o: return 'STOP'
    if 'Idle' in o: return 'IDLE'
    return o[:18]
for lab in sys.argv[1:]:
    m = re.search(r'j30_rel_(\d+)', lab)
    if not m: continue
    t_rel = int(m.group(1)) / 1000.0 + 2.0; t_rep = t_rel + 0.15   # key times are relative to the move start (2.0 s)
    R = load(lab); R = [r for r in R if isinstance(r.get('mh_root'), tuple)]
    k = min(range(len(R)), key=lambda i: abs(R[i]['t'] - t_rel))
    def vf(i):
        a, b = R[i - 1], R[i]; dt = (b['t'] - a['t']) or 1e-3; y = math.radians(b.get('ay', 0.0))
        return ((b['mh_root'][0] - a['mh_root'][0]) * math.cos(y) + (b['mh_root'][1] - a['mh_root'][1]) * math.sin(y)) / dt
    v = vf(k); req = next((i for i in range(len(R)) if R[i]['t'] >= 5.0 - 0.01), 0)   # the F_B request at 5.0
    # support established = a VISIBLE ball that came down after the request and is still (on its floor level, < 25 cm/s) at the release frame
    # (the component contact flags flipped between identical runs)
    cont = False
    for s_ in 'lr':
        zs_ = sorted(r['vb_ball_' + s_][2] for r in R); zf_ = zs_[len(zs_) // 20] + 1.5
        low = [R[i]['vb_ball_' + s_][2] < zf_ for i in range(len(R))]
        if low[k] and any(not low[i] for i in range(req, k)) and all(low[i] for i in range(max(req, k - 2), k + 1)):
            a_, b_ = R[k - 1]['vb_ball_' + s_], R[k]['vb_ball_' + s_]
            if math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / max(R[k]['t'] - R[k - 1]['t'], 1e-3) < 25.0: cont = True
    still = all(abs(vf(i)) < 5.0 for i in range(max(1, k - 6), k + 1))
    if still or str(R[k].get('av_SHM_IdleHold')) == 'True': ph = 'STANDING'
    elif v < -5.0: ph = 'NEW_PUSH'
    elif abs(v) < 40.0: ph = 'NEAR_ZERO'
    elif cont: ph = 'BRAKE_FOOT'
    else: ph = 'BRAKE_NO_SUPPORT'
    seq = []
    for r in R:
        if t_rep <= r['t'] <= t_rep + 0.5:
            f = fam(short(r.get('av_Phase27_SelectedObject')))
            if not seq or seq[-1] != f: seq.append(f)
    eps = [e for e in classify(R, t_rep - 0.1, t_rep + 1.0) if e['cls'] in ('SLIP', 'DRAG')]
    w = max(eps, key=lambda e: e['drift']) if eps else None
    idle = any(str(r.get('av_SHM_IdleEntry')) == 'True' for r in R if t_rel <= r['t'] <= t_rep + 0.5)
    print('RELPHASE231 %-34s rel %.2f v %5.0f %-16s -> %-26s worst %5.1f %s idle=%s' % (lab[-34:], t_rel - 2.0, v, ph, '>'.join(seq)[:26], w['drift'] if w else 0.0, (w['clip'][:26] if w else ''), idle))
