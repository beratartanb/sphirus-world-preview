# an_slope2.py <label> [window s]: slope support breakdown from a recorder JSON with ground traces (vidm_patch row['gnd']).
# Per window (default 0.5 s), all cm / deg:
#  grade    terrain slope under the capsule from the traced impact normal (acos nz), sign from capsule travel (+ = uphill)
#  capgap   capsule bottom (actor z - half height) minus traced ground under the capsule centre (> 0 = capsule floating / step offset)
#  hitc     component the capsule stands on (collision owner)
#  mesh     visible mesh component z minus capsule bottom (mesh offset; constant if no smoothing)
#  pelG     visible pelvis height above the traced ground under the capsule centre
#  pelLo    visible pelvis height above the LOWER foot's traced ground (leg-length budget actually used)
#  feet     each ball's height above its own traced ground (contact quality; ~3 cm = sole on ground)
#  footdz   traced ground height difference between the two feet (uphill foot minus downhill foot)
#  knee     support (lower) / other knee angle (thigh-calf-ankle, 180 = straight), trunk pitch (+ = forward lean, from travel)
#  clip     GASP selected animation at the window centre
import sys, json, math, statistics as st
lab = sys.argv[1]; WIN = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
d = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % lab)); R = [r for r in d['rows'] if 'ub' in r and isinstance(r.get('gnd'), dict)]
print('== %s rows %d (with ground traces) of %d, fps %s' % (lab, len(R), len(d['rows']), d.get('fps')))
def ang3(a, b, c):
    v1 = [a[i]-b[i] for i in range(3)]; v2 = [c[i]-b[i] for i in range(3)]
    n1 = math.sqrt(sum(x*x for x in v1)); n2 = math.sqrt(sum(x*x for x in v2)); return math.degrees(math.acos(max(-1, min(1, sum(x*y for x, y in zip(v1, v2))/(n1*n2+1e-9)))))
def m(a): a = [x for x in a if x is not None]; return st.mean(a) if a else float('nan')
def rg(a): a = [x for x in a if x is not None]; return (min(a), max(a)) if a else (float('nan'), float('nan'))
OUT = []
t0 = R[0]['t']; k = 0
while True:
    S = [r for r in R if t0 + k*WIN <= r['t'] < t0 + (k+1)*WIN]; k += 1
    if not S:
        if t0 + k*WIN > R[-1]['t']: break
        continue
    v = m([math.hypot(r['vx'], r['vy']) for r in S])
    dz = S[-1]['z'] - S[0]['z']; dx = math.hypot(S[-1]['x'] - S[0]['x'], S[-1]['y'] - S[0]['y'])
    def grade(r):
        c = r['gnd']['cap']
        if c[2] is None: return None
        g = math.degrees(math.acos(max(-1, min(1, c[2])))); return g
    gr = m([grade(r) for r in S]); sgn = 1 if dz >= 0 else -1
    path = math.degrees(math.atan2(dz, dx)) if dx > 10 else 0.0
    capgap = m([(r['z'] - r['gnd']['cap'][0] - r['gnd']['cap'][1]) if r['gnd']['cap'][1] is not None else None for r in S])
    mesh = m([r['gnd']['mz'][0] - (r['z'] - r['gnd']['cap'][0]) for r in S])
    pelG = [r['ub']['pelvis'][2] - r['gnd']['cap'][1] if r['gnd']['cap'][1] is not None else None for r in S]
    def gfoot(r, i):
        g = r['gnd']['f'][i]; return g[0] if g else None
    pelLo = []; fl = []; fr = []; fdz = []; kl = []; ko = []; tp = []
    for r in S:
        gl, gr_ = gfoot(r, 0), gfoot(r, 1)
        if gl is None or gr_ is None: continue
        lo = min(gl, gr_); pelLo.append(r['ub']['pelvis'][2] - lo)
        fl.append(r['ub']['ball_l'][2] - gl); fr.append(r['ub']['ball_r'][2] - gr_)
        up_is_l = gl > gr_; fdz.append(abs(gl - gr_))
        ka = ang3(r['ub']['thigh_l'][:3], r['ub2']['calf_l'], r['v_foot_l']); kb = ang3(r['ub']['thigh_r'][:3], r['ub2']['calf_r'], r['v_foot_r'])
        kl.append(kb if up_is_l else ka); ko.append(ka if up_is_l else kb)
        p = r['ub']['pelvis']; c = r['ub']['spine_05']; vv = math.hypot(r['vx'], r['vy'])
        if vv > 30: fx, fy = r['vx']/vv, r['vy']/vv
        else: y = math.radians(r['yaw']); fx, fy = math.cos(y), math.sin(y)
        tp.append(math.degrees(math.atan2((c[0]-p[0])*fx + (c[1]-p[1])*fy, c[2]-p[2])))
    hc = S[len(S)//2]['gnd']['cap'][4]; clip = S[len(S)//2].get('gasp', [''])
    clip = clip[0] if isinstance(clip, (list, tuple)) else ''
    row = dict(t=S[0]['t'], v=v, path=path, grade=gr*sgn if gr == gr else gr, capgap=capgap, mesh=mesh, pelG=m(pelG), pelG_rg=rg(pelG), pelLo=m(pelLo), pelLo_rg=rg(pelLo),
               fl=m(fl), fr=m(fr), fminl=rg(fl)[0], fminr=rg(fr)[0], footdz=m(fdz), knee_lo=m(kl), knee_up=m(ko), trunk=m(tp), hit=hc, clip=clip)
    OUT.append(row)
    print(' t %5.1f v %3.0f path %+5.1f grade %+5.1f | capgap %+5.1f mesh %+5.1f | pelG %5.1f (%5.1f..%5.1f) pelLo %5.1f | ball L %+5.1f (min %+5.1f) R %+5.1f (min %+5.1f) footdz %4.1f | knee lo %3.0f up %3.0f | trunk %+5.1f | %-18s %s' % (
        row['t'], v, path, row['grade'], capgap, mesh, row['pelG'], row['pelG_rg'][0], row['pelG_rg'][1], row['pelLo'], row['fl'], row['fminl'], row['fr'], row['fminr'], row['footdz'], row['knee_lo'], row['knee_up'], row['trunk'], str(hc)[:18], str(clip)[:34]))
json.dump(OUT, open('Saved/UE59Work/rec_slope_%s.json' % lab, 'w'))
