"""stop236.py <label> [...] : V2.36 whole-body STOP audit of one run (LTP side file), per jog release (input released while moving > 200 cm/s).
Body-level measures on the visible mesh (vb_ / vx_), from the release to 2.4 s after it:
  sel      : stop clips the search played (name@entry time, first 3)
  slip     : worst planted-ball slide / drag (contact231) inside the window (cm)
  plant    : last landing time after the release (s) and the capsule stop time (s)
  stagger  : fore-aft distance of the balls 0.6 s after the capsule stopped (cm) and the time both feet stood planted >= 25 cm apart
             while the capsule was still (s) = the 'long open stance'
  back     : largest backward motion (against the travel) of a ball after the capsule stopped (cm) = a pull-back correction step
  trunk    : trunk pitch (pelvis -> neck) at the release / 0.6 s later (deg, + forward) and its fastest change (deg/s) = 'pop upright'
  arms     : hand fore-aft swing (peak-to-peak vs the pelvis) in the 0.6 s before the release and 0.15-0.75 s after it, their ratio
             (1.0 = the arms keep running), the fastest hand drop (cm/s) and the hand height change (cm)
  pelvis   : lowest pelvis height after the release minus its final height (cm)
  apex     : highest ball lift of any step after the release (cm above its own floor)
Prints STOP236 lines (one per release)."""
import sys, os, math, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V232_20261027']
from ltp231 import load
from contact231 import classify
def v(r, k):
    x = r.get(k); return x if isinstance(x, tuple) else None
def held(r): return abs(float(r.get('lix', 0) or 0)) + abs(float(r.get('liy', 0) or 0)) > 0.1
def audit(lab):
    R = load(lab); outs = []
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    for i in range(1, len(R)):
        if not (held(R[i - 1]) and not held(R[i]) and float(R[i - 1].get('Speed2D', 0)) > 200): continue
        t0 = R[i]['t']; W = [r for r in R if t0 - 0.6 <= r['t'] <= t0 + 2.4]
        after = [r for r in W if r['t'] >= t0]
        if any(held(r) for r in after[3:]):        # a re-press inside the window: report only up to it
            cut = next(r['t'] for r in after[3:] if held(r)); after = [r for r in after if r['t'] < cut]
        if len(after) < 10: continue
        p0 = v(R[i - 3], 'vb_pelvis'); p1 = v(R[i], 'vb_pelvis')
        fw = (p1[0] - p0[0], p1[1] - p0[1]); n = math.hypot(*fw) or 1.0; fw = (fw[0] / n, fw[1] / n)
        along = lambda p: p[0] * fw[0] + p[1] * fw[1]
        tstop = next((r['t'] for r in after if float(r.get('Speed2D', 0)) < 1.0), None)
        sel = []
        for r in after:
            c = str(r.get('av_Phase27_SelectedObject', '')); c = c.split('.')[-1].split("'")[0] if c else ''
            if not sel or sel[-1][0] != c: sel.append((c, round(float(r.get('av_Phase27_SelectedTime', 0) or 0), 2), round(r['t'] - t0, 2)))
        slip = max([e['drift'] for e in eps if t0 - 0.05 <= e['t'] <= after[-1]['t']] or [0.0])
        # landings + apex per ball
        bz0 = {s: min(v(r, 'vb_ball_' + s)[2] for r in W if v(r, 'vb_ball_' + s)) for s in 'lr'}
        lands = []; apex = 0.0; back = 0.0
        for s in 'lr':
            prev = None
            for r in after:
                b = v(r, 'vb_ball_' + s)
                if not b: continue
                low = b[2] < bz0[s] + 1.5
                if prev is not None and low and not prev: lands.append(round(r['t'] - t0, 2))
                prev = low; apex = max(apex, b[2] - bz0[s])
            if tstop is not None:
                post = [v(r, 'vb_ball_' + s) for r in after if r['t'] >= tstop and v(r, 'vb_ball_' + s)]
                if post:
                    mx = max(along(b) for b in post[:3]); back = max(back, max(mx - along(b) for b in post))
        stg = None; open_t = 0.0
        if tstop is not None:
            r6 = min(after, key=lambda r: abs(r['t'] - (tstop + 0.6)))
            if v(r6, 'vb_ball_l') and v(r6, 'vb_ball_r'): stg = round(abs(along(v(r6, 'vb_ball_l')) - along(v(r6, 'vb_ball_r'))), 1)
            for a, b in zip(after, after[1:]):
                if a['t'] < tstop: continue
                bl, br = v(a, 'vb_ball_l'), v(a, 'vb_ball_r')
                if bl and br and bl[2] < bz0['l'] + 1.5 and br[2] < bz0['r'] + 1.5 and abs(along(bl) - along(br)) >= 25.0: open_t += b['t'] - a['t']
        def pitch(r):
            pv, nk = v(r, 'vb_pelvis'), v(r, 'vx_neck_01')
            if not pv or not nk: return None
            d = (nk[0] - pv[0], nk[1] - pv[1], nk[2] - pv[2]); return math.degrees(math.atan2(along(d), d[2]))
        pt = [(r['t'], pitch(r)) for r in after if pitch(r) is not None]
        prate = max([abs(b[1] - a[1]) / max(b[0] - a[0], 1e-3) for a, b in zip(pt, pt[1:])] or [0.0])
        p_rel = pt[0][1] if pt else None; p_6 = next((p for tt, p in pt if tt >= t0 + 0.6), None)
        def hand_rel(r, s):
            h, pv = v(r, 'vx_hand_' + s), v(r, 'vb_pelvis')
            return (along(h) - along(pv), h[2] - pv[2]) if h and pv else None
        def pp(rows):
            vals = [hand_rel(r, s)[0] for r in rows for s in 'lr' if hand_rel(r, s)]
            per = []
            for s in 'lr':
                xs = [hand_rel(r, s)[0] for r in rows if hand_rel(r, s)]
                if xs: per.append(max(xs) - min(xs))
            return max(per) if per else 0.0
        before = [r for r in W if t0 - 0.6 <= r['t'] < t0]; mid = [r for r in after if t0 + 0.15 <= r['t'] <= t0 + 0.75]
        swb, swa = pp(before), pp(mid)
        hz = [(r['t'], 0.5 * (v(r, 'vx_hand_l')[2] + v(r, 'vx_hand_r')[2])) for r in after if v(r, 'vx_hand_l') and v(r, 'vx_hand_r')]
        hdrop = max([(a[1] - b[1]) / max(b[0] - a[0], 1e-3) for a, b in zip(hz, hz[1:])] or [0.0])
        pz = [v(r, 'vb_pelvis')[2] for r in after if v(r, 'vb_pelvis')]
        outs.append({'label': lab, 't_release': round(t0, 2), 'sel': sel[:4], 'slip': round(slip, 1), 'lands': sorted(lands)[:6],
                     'last_land': max(lands) if lands else None, 't_stop': round(tstop - t0, 2) if tstop else None, 'stagger_cm': stg, 'open_stance_s': round(open_t, 2),
                     'back_cm': round(back, 1), 'trunk_deg': [round(p_rel, 1) if p_rel is not None else None, round(p_6, 1) if p_6 is not None else None], 'trunk_rate': round(prate, 0),
                     'arm_pp': [round(swb, 1), round(swa, 1), round(swa / swb, 2) if swb > 1 else None], 'hand_drop_cms': round(hdrop, 0),
                     'hand_dz': round(hz[-1][1] - hz[0][1], 1) if hz else None, 'pelvis_dip': round(min(pz) - pz[-1], 1) if pz else None, 'apex': round(apex, 1)})
    return outs
if __name__ == '__main__':
    for lab in sys.argv[1:]:
        try:
            for o in audit(lab): print('STOP236 ' + json.dumps(o))
        except Exception as e: print('STOP236 ' + json.dumps({'label': lab, 'err': str(e)[:160]}))
