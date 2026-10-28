"""tables232.py <tag> <varA> <varB> [--rep=2] [--scen=a,b,...] : same-session comparison table (V2.32). Per scenario and variant, every
repeat's worst planted-ball SLIP / DRAG (contact231, cm), the number of one-frame selection blips (blip232 rule), and for camera scenarios
the realised orbit max (deg), the 3/4 seconds, jerk95 and the body-path difference to varA (cm) - the camera layer must not move the body.
Summary line TABLES233: per variant the median of the per-scenario medians, runs with a worst slide > 20 cm, total blips."""
import sys, os, glob, math, statistics as st
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); sys.path.insert(0, os.path.join(H, '..', 'SHME_V232_20261027')); sys.path.insert(0, os.path.join(H, '..', 'SHME_V231_20261026'))
from ltp231 import load, short   # V2.33 copy of tables232 (labels v233<tag>)
from contact231 import classify
import cam232
LTP = os.path.join(H, '..', '..', 'Saved', 'Codex', 'SHME_V1_20260925', 'LTP')
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}
tag, VA, VB = args[0], args[1], args[2]; REP = int(opt.get('--rep', 2))
scen = opt.get('--scen'); scen = scen.split(',') if scen else sorted(set(os.path.basename(p)[len('v234%s_' % tag):].rsplit('_%s_r' % VA, 1)[0] for p in glob.glob(os.path.join(LTP, 'v234%s_*_%s_r1.ltp' % (tag, VA)))))
def worst(lab):
    try: R = load(lab)
    except Exception: return None, None
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    sel = [short(r.get('av_Phase27_SelectedObject')) for r in R]
    bl = sum(1 for i in range(1, len(sel) - 1) if sel[i] != sel[i - 1] and sel[i] != sel[i + 1] and sel[i - 1] and sel[i + 1])
    return (max(e['drift'] for e in eps) if eps else 0.0), bl
def camm(lab, base):
    try:
        R = cam232.load(lab); A = cam232.load(base) if base else None
    except Exception: return None
    q34 = sum(R[i]['t'] - R[i - 1]['t'] for i in range(1, len(R)) if 25 <= abs(R[i]['alpha']) <= 65 and R[i]['sp'] > 30)
    js = sorted(r.get('jerk', 0.0) for r in R); dp = 0.0
    if A:
        for r in R:
            a = min(A, key=lambda x: abs(x['t'] - r['t']))
            if abs(a['t'] - r['t']) < 0.02: dp = max(dp, math.hypot(r['pos'][0] - a['pos'][0], r['pos'][1] - a['pos'][1]))
    return max(abs(r['beta']) for r in R), q34, js[int(0.95 * len(js))] if js else 0.0, dp
summ = {VA: {'med': [], 'gt20': 0, 'bl': 0, 'n': 0}, VB: {'med': [], 'gt20': 0, 'bl': 0, 'n': 0}}
print('%-20s | %-22s | %-22s | camera %s: orbit 3/4s jerk95 dBody' % ('scenario', VA + ' worst(r1,r2) blips', VB + ' worst(r1,r2) blips', VB))
for s in scen:
    row = {}
    for v in (VA, VB):
        ws = []; bls = 0
        for rp in range(1, REP + 1):
            w, b = worst('v234%s_%s_%s_r%d' % (tag, s, v, rp))
            if w is None: continue
            ws.append(w); bls += b; summ[v]['n'] += 1; summ[v]['gt20'] += w > 20.0
        summ[v]['bl'] += bls
        if ws: summ[v]['med'].append(st.median(ws))
        row[v] = ('%s b%d' % (','.join('%.1f' % x for x in ws), bls)) if ws else '-'
    cm = camm('v234%s_%s_%s_r1' % (tag, s, VB), 'v234%s_%s_%s_r1' % (tag, s, VA)) if s.startswith(('cam', 's29_cam', 'map', 'ins')) else None
    print('%-20s | %-22s | %-22s | %s' % (s[:20], row[VA], row[VB], ('%.1f %.2f %.2f %.1f' % cm) if cm else ''))
print('TABLES233 ' + ' '.join('%s: median %.1f cm, runs>20cm %d/%d, blips %d' % (v, st.median(d['med']) if d['med'] else 0, d['gt20'], d['n'], d['bl']) for v, d in summ.items()))
