# an_armloco6.py <label> ...: arm path vs body during locomotion, by speed band (idle < 30, walk 30-250, jog 250-480, sprint > 480; backward
# when GR_Back). Per band: mean upper-arm abduction (frontal plane), elbow flexion, palm-thigh clearance from the posture layer (CA_CL / CA_CR,
# palm to the tapered thigh surface; < 0 = inside), share of frames with clearance < 0 and < 1 cm, the posture arm servo (PS_DAL / PS_DAR).
import json, sys, math
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def norm(a):
    m = math.sqrt(dot(a, a)) or 1.0; return [x / m for x in a]
A6 = ('CA_L', 'CA_R', 'CA_CL', 'CA_CR', 'PS_DAL', 'PS_DAR', 'PS_PAL', 'PS_PAR', 'PS_AbdL', 'PS_AbdR', 'PS_AbdClipA', 'AW_AL', 'AW_AR', 'PS_CPL', 'PS_CPR', 'PS_CYL', 'PS_CYR', 'PS_C3', 'PS_C5', 'PS_CN', 'PS_Eff')
for lab in sys.argv[1:]:
    R = json.load(open('C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']; B = {}
    for r in R:
        h = r.get('hook', {}); p = h.get('pv'); a6 = h.get('arm6')
        if not p or not a6: continue
        v = math.hypot(r['vx'], r['vy']); band = 'idle' if v < 30 else 'walk' if v < 250 else 'jog' if v < 480 else 'sprint'
        if h.get('GR_Back') and v >= 30: band = 'back_' + band
        d = dict(zip(A6, a6)); rt = norm([p['thigh_r'][0] - p['thigh_l'][0], p['thigh_r'][1] - p['thigh_l'][1], 0.0])
        for s, sg in (('l', -1.0), ('r', 1.0)):
            u = norm(sub(p['lowerarm_' + s], p['upperarm_' + s])); f = norm(sub(p['hand_' + s], p['lowerarm_' + s]))
            e = B.setdefault(band, {'abd': [], 'elbow': [], 'clr': []})
            e['abd'].append(math.degrees(math.atan2(dot(u, [x * sg for x in rt]), -u[2]))); e['elbow'].append(math.degrees(math.acos(max(-1, min(1, dot(u, f))))))
            e['clr'].append(d['CA_CL' if s == 'l' else 'CA_CR'])
    print('==', lab)
    for k in ('idle', 'walk', 'jog', 'sprint', 'back_walk', 'back_jog', 'back_sprint'):
        if k not in B: continue
        e = B[k]; c = sorted(e['clr']); n = len(c)
        print('  %-11s n%4d abd %.1f elbow %.1f | clearance p5 %.1f min %.1f  <0: %.0f%%  <1cm: %.0f%%' % (k, n // 2, sum(e['abd']) / n, sum(e['elbow']) / n, c[int(n * .05)], c[0], 100 * sum(1 for x in c if x < 0) / n, 100 * sum(1 for x in c if x < 1) / n))
