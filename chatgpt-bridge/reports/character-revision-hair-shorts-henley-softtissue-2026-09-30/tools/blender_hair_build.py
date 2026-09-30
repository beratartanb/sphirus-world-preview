"""SPHIRUS custom hairstyle (concept: THE GUARDIAN): auburn LOW messy bun, gathered strands with a lightly messy crown,
face-framing / temple / ear / nape loose strands, bun escapes and sparse flyaways. Built procedurally on the exact
candidate head surface (UE bind space, cm) and exported as two Alembic grooms:
  hair_main.abc  = scalp coverage + gathered hair + bun            (stable, no simulation)
  hair_loose.abc = face/temple/ear/nape strands, bun escapes, flyaways (light strand simulation in UE)
Alembic points are written as Blender (X, -Z, Y) in cm so that the UE Alembic groom import (no conversion) lands in UE
component space (verified with a 2-strand test on 2026-09-30).
usage: blender -b --factory-startup --python blender_hair_build.py -- <sculpt_package.json.gz> <out_dir> [seed]"""
import bpy, sys, os, json, gzip, math, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index('--')+1:]; PKG, OUT = argv[0], argv[1]; SEED = int(argv[2]) if len(argv) > 2 else 20260930
os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(SEED); T0 = time.time()
def log(*a): print('[hair %6.1fs]' % (time.time()-T0), *a, flush=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
E = lambda k, d: float(os.environ.get(k, d))
N_MAIN = int(E('SPH_HAIR_N', '26000')); N_PTS = int(E('SPH_HAIR_PTS', '22'))
P = json.loads(gzip.open(PKG, 'rb').read()); NB, NH = P['NB'], P['NH']
X = np.asarray(P['br_neutral'], np.float64)[NB:]; T = np.asarray(P['head']['triangles'], np.int64); MI = np.asarray(P['head']['material_ids'])
HT = T[MI == 0]                                                           # head skin section only
BODYX = np.asarray(P['br_neutral'], np.float64)[:NB]; BT = np.asarray(P['body']['triangles'], np.int64)
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t) for t in HT])                  # UE cm space
bvh_body = BVHTree.FromPolygons([Vector(p) for p in BODYX], [list(t) for t in BT])
# outward normals: UE winding gives inward cross products in this right-handed frame -> flip
a, b, c = X[HT[:, 0]], X[HT[:, 1]], X[HT[:, 2]]; fn = -np.cross(b-a, c-a); area = np.linalg.norm(fn, axis=1)*0.5; fn /= np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]
cen = (a+b+c)/3
def nearest(p):
    loc, nrm, idx, d = bvh.find_nearest(Vector(p)); n = np.asarray(fn[idx]) if idx is not None else np.array([0, 0, 1.0])
    return np.asarray(loc), n
def push_out(p, gap):
    """keep a point at least 'gap' cm outside the head (and the body for long strands)"""
    loc, n = nearest(p); d = float(np.dot(p-loc, n))
    if d < gap: p = p+n*(gap-d)
    lb, nb_, ib, db = bvh_body.find_nearest(Vector(p))
    if lb is not None:
        lb = np.asarray(lb); v = p-lb; nrm = np.asarray(nb_); nrm = -nrm   # body normals from UE winding: flip
        dd = float(np.dot(v, nrm))
        if dd < gap*0.8 and db < 6: p = p+nrm*(gap*0.8-dd)
    return p
# ------------------------------------------------------------------------------------------------ scalp / hairline
def scalp_mask(p, n):
    x, y, z = p; ax = abs(x)
    if n[2] < -0.35: return False
    if y > 5.0:   return z > 165.8-2.6*(ax/7.0)**2+0.15*math.sin(x*1.3)       # forehead hairline, lower at temples
    if y > -0.5:  return z > 161.2 and not (ax > 6.3 and z < 162.5)                # above the ears
    return z > 150.6+2.2*(ax/6.0)**2                                              # behind the ears -> nape hairline
ok = np.array([scalp_mask(cen[i], fn[i]) for i in range(len(HT))])
S_T = HT[ok]; S_A = area[ok]; S_N = fn[ok]; log('scalp triangles', int(ok.sum()), 'area cm2', round(float(S_A.sum()), 1))
def sample_scalp(n):
    tri = rng.choice(len(S_T), size=n, p=S_A/S_A.sum()); u = rng.random(n); v = rng.random(n); m = u+v > 1; u[m], v[m] = 1-u[m], 1-v[m]
    A, B_, C = X[S_T[tri, 0]], X[S_T[tri, 1]], X[S_T[tri, 2]]; return A+(B_-A)*u[:, None]+(C-A)*v[:, None], S_N[tri]
# ------------------------------------------------------------------------------------------------ bun geometry
C_BUN = np.array([E('SPH_BUN_X', '0.6'), E('SPH_BUN_Y', '-9.3'), E('SPH_BUN_Z', '155.6')])   # low: lower occiput / upper nape
Gs, gn = nearest(C_BUN); AX = C_BUN-Gs; AXL = np.linalg.norm(AX); AX /= AXL                    # bun axis: from the scalp outward
U1 = np.cross(AX, [0, 0, 1.0]); U1 /= np.linalg.norm(U1); U2 = np.cross(AX, U1)
HC = np.array([0.0, 2.5, 160.5])    # cranium centre for the strand arcs
R_BUN = E('SPH_BUN_R', '3.9'); log('bun centre', C_BUN.round(2), 'scalp anchor', Gs.round(2), 'axis', AX.round(2), 'stand-off', round(AXL, 2))
N_LOCKS = 18; LOCK_R = 0.55+0.9*rng.random(N_LOCKS); LOCK_C = rng.normal(0, E('SPH_LOCK_C', '1.1'), (N_LOCKS, 3)); LOCK_A0 = rng.random(N_LOCKS)*2*np.pi; LOCK_AX = rng.normal(0, 0.9, N_LOCKS); LOCK_TURN = E('SPH_TURN0', '0.7')+E('SPH_TURN1', '0.8')*rng.random(N_LOCKS)
# ------------------------------------------------------------------------------------------------ helpers
def vnoise3(p, f, seed):
    """cheap smooth 3D noise (sum of sines with random phases) -> vector in [-1, 1]^3"""
    r = np.random.default_rng(seed); out = np.zeros(3)
    for k in range(3):
        for o in range(3):
            fr = f*(1.7**o); ph = r.random(3)*6.28; d = r.normal(0, 1, 3); d /= np.linalg.norm(d)
            out[k] += math.sin(float(np.dot(p, d))*fr+ph[0])*(0.55**o)
    return out/1.8
def resample(pts, n):
    pts = np.asarray(pts); seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < 1e-6: return np.repeat(pts[:1], n, 0)
    t = np.linspace(0, s[-1], n); return np.stack([np.interp(t, s, pts[:, k]) for k in range(3)], 1)
# ------------------------------------------------------------------------------------------------ MAIN: gathered hair + bun
roots, rnorm = sample_scalp(N_MAIN)
fr, fnn = sample_scalp(N_MAIN*3)
front = (fr[:, 1] > 3.0) & (fr[:, 2] < 169.5)
extra = int(N_MAIN*E('SPH_FRONT_EXTRA', '0.35')); roots = np.vstack([roots, fr[front][:extra]]); rnorm = np.vstack([rnorm, fnn[front][:extra]]); N_MAIN = len(roots)
if E('SPH_HAIRLINE_SOFT', '0') > 0.5:   # sparse, irregular hairline: roots near the forehead / temple edge are thinned out
    def edge_margin(p):
        x, y, z = p; ax = abs(x)
        if y > 5.0: return z-(165.8-2.6*(ax/7.0)**2)
        return 9.0
    mg = np.array([edge_margin(p) for p in roots]); keep = rng.random(N_MAIN) < np.clip(0.15+mg/1.8, 0.15, 1.0)
    roots = roots[keep]; rnorm = rnorm[keep]; N_MAIN = len(roots); log('hairline thinning kept', N_MAIN)
# clumps: strands follow clump guides (lived-in, not combed); parting slightly off centre (x ~ +1.2) on the crown
N_CL = 700; cl_idx = rng.choice(N_MAIN, N_CL, replace=False); cl_roots = roots[cl_idx]
d2 = ((roots[:, None, :]-cl_roots[None, :, :])**2).sum(-1); clump = d2.argmin(1)
PART_X = E('SPH_PART_X', '1.3'); SWEEP = E('SPH_SWEEP', '0'); LIFT_S = E('SPH_LIFT_SCALE', '1.0'); CROWN_X = E('SPH_CROWN_EXTRA', '0.9'); HF = E('SPH_FRIZZ_HF', '0.12'); V6 = E('SPH_V6', '0') > 0.5
LOOP_P = E('SPH_LOOP_P', '0.05'); EAR_N = int(E('SPH_EAR_N', '60')); FACE_N = int(E('SPH_FACE_N', '70'))
main_strands = []
def strand_to_bun(root, rn, jitter, lift, seed, frizz):
    # target on the bun base ring, in the angular direction the strand comes from
    dirv = root-Gs; dirv -= AX*np.dot(dirv, AX); ang = math.atan2(float(np.dot(dirv, U2)), float(np.dot(dirv, U1)))
    ring = Gs+AX*0.9+(U1*math.cos(ang)+U2*math.sin(ang))*(1.6+0.8*jitter[0])
    path = []; n_s = 18
    for k in range(n_s+1):
        t = k/n_s
        ua = root-HC; ub = ring-HC; la, lb = np.linalg.norm(ua), np.linalg.norm(ub); ua /= la; ub /= lb
        cab = float(np.dot(ua, ub)); bias = max(0.0, -cab-0.2)*1.6
        wf = 0.0
        if SWEEP > 0 and root[1] > 1.0:   # front hair sweeps sideways from the centre part over the temples toward the bun
            x_ = min(1.0, max(0.0, (root[1]-1.0)/5.0)); wf = SWEEP*x_*x_*(3-2*x_)
        if bias > 0 or wf > 0:   # near-opposite root / bun directions: route explicitly over the crown (never down across the face)
            mid = ua+ub+np.array([0.0, -0.25, 1.0])*max(bias, 0.3); mid /= np.linalg.norm(mid)
            if wf > 0:
                sd = 1.0 if root[0] > PART_X else -1.0; lat = np.array([sd*0.8, 0.2, 0.5]); lat /= np.linalg.norm(lat)
                mid = mid*(1-wf)+lat*wf; mid /= np.linalg.norm(mid)
            sp = 0.5-0.12*wf
            a_, b_, tt = (ua, mid, t/sp) if t < sp else (mid, ub, (t-sp)/(1-sp))
        else: a_, b_, tt = ua, ub, t
        om = math.acos(max(-1.0, min(1.0, float(np.dot(a_, b_)))))
        dirv = a_ if om < 1e-4 else (math.sin((1-tt)*om)*a_+math.sin(tt*om)*b_)/math.sin(om)
        q = HC+dirv*((la*(1-t)+lb*t+0.8) if V6 else 20.0)   # arc around the cranium at skull radius (a 20 cm arc snapped onto the neck / forehead)
        # part: strands on either side of the parting first move away from it
        side = 1.0 if root[0] > PART_X else -1.0
        q = q+np.array([side*E('SPH_PART_PUSH', '0.5')*math.sin(math.pi*min(1.0, t*1.6))*max(0, 1-abs(root[0]-PART_X)/E('SPH_PART_W', '2.5')), 0, 0])
        loc, n = nearest(q); h = 0.12+lift*(1-0.6*wf)*(math.sin(math.pi*t)**0.8)+0.45*t
        q = loc+n*h+vnoise3(q, 0.55, seed)*frizz*(0.35+0.9*t)+vnoise3(q, 1.6, seed+7)*HF*frizz+(vnoise3(q, 3.4, seed+11)*HF*0.6*frizz*t if V6 else 0.0)
        path.append(q)
    return np.asarray(path), ang
t0 = time.time()
for i in range(N_MAIN):
    j = rng.random(3); cr = cl_roots[clump[i]]
    # strands inherit most of the clump root's path shape: blend root toward the clump root after leaving the scalp
    lift = (0.3+0.75*rng.random())*LIFT_S+(CROWN_X if roots[i][2] > 167 else 0.0)        # crown volume, loosely gathered
    fz = 0.6+0.9*rng.random() if rng.random() > 0.08 else 1.8+1.5*rng.random()   # a few strands clearly out of line
    path, ang = strand_to_bun(roots[i], rnorm[i], j, lift, 1000+clump[i], fz)
    cpath, _ = strand_to_bun(cr, rnorm[i], j, lift, 1000+clump[i], 0.4)
    w = np.clip(np.linspace(-0.2, 1.0, len(path)), 0, 1)[:, None]*0.5; path = path*(1-w)+cpath*w
    if (rng.random() < LOOP_P) or (V6 and clump[i] % 23 == 0 and rng.random() < 0.7):   # lifted loop over the crown / sides (lightly messy)
        mid = len(path)//2; bump = np.sin(np.linspace(0, np.pi, len(path)))[:, None]*(0.6+1.2*rng.random()); nrm_ = rnorm[i]; path = path+bump*nrm_[None, :]
    # bun wrap: continue around the bun axis in the lock this strand belongs to
    lk = int(rng.integers(N_LOCKS)); turns = LOCK_TURN[lk]*(0.45+0.6*rng.random()); a0 = ang+LOCK_A0[lk]*0.35; rj = rng.normal(0, 0.55)
    wrap = []; nw = 16
    for k in range(1, nw+1):
        t = k/nw; a_ = a0+2*np.pi*turns*t*(1 if lk % 2 else -1)
        loop = 1.0+0.55*math.sin(math.pi*t)*(1 if lk % 5 == 0 else 0)          # some locks loop outward
        tip = 1.0 if (i % 7) else (1.0+0.9*t*t)                                 # some tips escape instead of tucking in
        r = R_BUN*LOCK_R[lk]*(1.0-0.5*t)*loop*tip+0.9*math.sin(5*t+lk)+0.6*math.sin(11*t+2*lk)
        ax_off = -1.6+3.4*t*(0.4+0.6*rng.random())+LOCK_AX[lk]*0.9+0.6*math.sin(3*a_+lk)
        q = C_BUN+LOCK_C[lk]*(0.3+0.7*t)+AX*ax_off+(U1*math.cos(a_)+U2*math.sin(a_))*(r+rj)+vnoise3(np.array([a_, t, lk]), 1.2, 3000+lk)*0.9+rng.normal(0, 0.15, 3)
        wrap.append(q)
    full = np.vstack([path, np.asarray(wrap)]); full = resample(full, N_PTS)
    for k in range(len(full)): full[k] = push_out(full[k], 0.08 if k < 3 else 0.18)
    main_strands.append(full)
    if i % 5000 == 0: log('main', i, round(time.time()-t0, 1))
log('main strands', len(main_strands))
# ------------------------------------------------------------------------------------------------ LOOSE strands
loose = []
def hang(root, out_dir, length, wave, n=N_PTS, curl=0.0, gap=0.35, seed=0, fwd=0.0):
    """strand leaving the scalp along out_dir, then falling with gravity, wavy, kept off the face/neck"""
    pts = [root]; p = root.copy(); d = out_dir/np.linalg.norm(out_dir); step = length/(n-1)
    for k in range(1, n):
        t = k/(n-1); g = np.array([0, fwd*0.25, -1.0]); g /= np.linalg.norm(g)
        d = d*(1-0.22)+g*0.22; d /= np.linalg.norm(d)
        w = vnoise3(p, 0.45, seed)*wave+np.array([math.sin(t*6.5+seed)*curl, 0, 0])
        p = p+d*step+w*step*0.6; p = push_out(p, gap if t > 0.1 else 0.1); pts.append(p.copy())
    return np.asarray(pts)
def lock(center, radius, count, out_dir, length, wave, curl, seed, fwd=0.0, jitter_len=0.25):
    rs = []
    for k in range(count):
        o = rng.normal(0, radius, 3); q, n = nearest(center+o); q = q+n*0.1
        L = length*(1+rng.normal(0, jitter_len)); rs.append(hang(q, out_dir+rng.normal(0, 0.25, 3), max(2.0, L), wave, curl=curl, seed=seed+k % 3, fwd=fwd))
    return rs
FACE_LOCKS = [((-7.2, 6.8, 163.8), (-0.55, -0.1, -0.8), 16), ((7.0, 7.0, 164.0), (0.55, -0.1, -0.8), 14), ((-7.6, 4.8, 162.4), (-0.5, -0.2, -0.85), 19),
              ((7.5, 5.0, 162.3), (0.5, -0.2, -0.85), 18), ((-5.9, 8.9, 165.6), (-0.45, 0.05, -0.8), 9), ((5.6, 9.0, 165.8), (0.45, 0.05, -0.8), 8)]
EYE_BOX = lambda q: (abs(q[0]) < 6.4 and q[1] > 6.0 and 152.0 < q[2] < 166.0)
for i, (c_, d_, L) in enumerate(FACE_LOCKS):
    for st in lock(np.array(c_), 0.8, FACE_N, np.array(d_, float), L, 0.7, 0.5, 100+i, fwd=-0.2):
        for k in range(len(st)):
            if EYE_BOX(st[k]): st[k][0] = math.copysign(6.6+0.6*(6.4-abs(st[k][0]))+0.3*((k*7919+i*104729) % 10)/10.0, st[k][0])          # keep tendrils outside the eye / cheek window
        loose.append(st)
for sx in (-1, 1):                                       # over / behind the ears
    loose += lock(np.array([sx*7.0, 1.6, 162.0]), 0.9, EAR_N, np.array([sx*0.7, -0.2, -0.5]), 13, 0.7, 0.5, 200+sx)
    loose += lock(np.array([sx*6.3, -2.2, 158.5]), 0.9, 26, np.array([sx*0.5, -0.4, -0.6]), 10, 0.6, 0.6, 210+sx)
for k in range(9):                                       # nape wisps
    xx = -4.5+9.0*k/8+rng.normal(0, 0.4); z0 = 150.9+2.2*(abs(xx)/6.0)**2
    loose += lock(np.array([xx, -2.4, z0+0.6]), 0.5, 14, np.array([0.1*xx, -0.5, -0.8]), 6.5+3*rng.random(), 0.7, 0.8, 300+k)
for k in range(26):                                      # escapes around the bun: short loops
    a_ = rng.random()*2*np.pi; q = C_BUN+(U1*math.cos(a_)+U2*math.sin(a_))*R_BUN*0.9+AX*rng.normal(0, 1.0)
    out = (q-C_BUN); out /= np.linalg.norm(out)
    for m in range(10):
        pts = []; L = 3+4*rng.random()
        for s in np.linspace(0, 1, N_PTS):
            pts.append(q+out*math.sin(math.pi*s)*L*0.35+np.cross(out, AX)*(s-0.5)*L+np.array([0, 0, -0.8*s*L*0.3])+rng.normal(0, 0.05, 3))
        loose.append(np.asarray(pts))
for k in range(900):                                     # sparse fine flyaways: crown and bun
    if k < 700: q, n = sample_scalp(1); q, n = q[0], n[0]; q = q+n*0.6
    else: a_ = rng.random()*2*np.pi; q = C_BUN+(U1*math.cos(a_)+U2*math.sin(a_))*R_BUN; n = (q-C_BUN)/np.linalg.norm(q-C_BUN)
    L = 2+4*rng.random(); d_ = n+rng.normal(0, 0.8, 3); d_ /= np.linalg.norm(d_); b_ = np.cross(d_, rng.normal(0, 1, 3)); b_ /= np.linalg.norm(b_)
    loose.append(np.asarray([q+d_*L*s+b_*math.sin(s*math.pi)*L*0.25 for s in np.linspace(0, 1, 10)]))

if V6:
    TEND = []
    for sx in (-1, 1):
        for k in range(9):
            y0 = 7.6-1.2*k+rng.normal(0, 0.3); z0 = 165.0-0.75*k+rng.normal(0, 0.3); x0 = sx*(6.4+0.18*k)
            TEND.append(((x0, y0, z0), (sx*0.35, 0.15-0.05*k, -0.9), 11.0+10.0*rng.random(), int(E('SPH_TEND_N', '10'))+int(12*rng.random())))
    for i, (c_, d_, L, n_) in enumerate(TEND):
        for st in lock(np.array(c_), 0.35, n_, np.array(d_, float), L, 1.1, 1.6, 500+i, fwd=0.15, jitter_len=0.3):
            for k in range(len(st)):
                if EYE_BOX(st[k]): st[k][0] = math.copysign(6.7+0.6*(6.4-abs(st[k][0]))+0.3*((k*7919+i*104729) % 10)/10.0, st[k][0])
            loose.append(st)
    # hairline baby hairs: short, fine, lying back over the scalp edge
    fr2, fn2 = sample_scalp(40000); sel = np.nonzero(((fr2[:, 1] > 3.0) & (fr2[:, 2] < 167.5)) | ((fr2[:, 1] < -0.5) & (fr2[:, 2] < 153.5)))[0][:int(E('SPH_BABY_N', '1400'))]
    for i_ in sel:
        q = fr2[i_]+fn2[i_]*0.05; up = np.array([0, -0.6, 0.8]) if q[1] > 0 else np.array([0, 0.3, 0.9]); d_ = up+rng.normal(0, 0.45, 3); d_ -= fn2[i_]*np.dot(d_, fn2[i_])*0.7; d_ /= np.linalg.norm(d_)
        L = 0.6+1.8*rng.random(); pts = [push_out(q+d_*L*s+fn2[i_]*0.25*math.sin(math.pi*s)+rng.normal(0, 0.04, 3), 0.05) for s in np.linspace(0, 1, 8)]
        (main_strands if E('SPH_BABY_MAIN', '0') > 0.5 else loose).append(resample(np.asarray(pts), N_PTS) if E('SPH_BABY_MAIN', '0') > 0.5 else np.asarray(pts))   # baby hairs are not simulated (they fell into a fringe)
    # extra loose loops coming out of the bun (messy, not a clean round bun)
    for k in range(40):
        a_ = rng.random()*2*np.pi; q = C_BUN+(U1*math.cos(a_)+U2*math.sin(a_))*R_BUN*(0.6+0.4*rng.random())+AX*rng.normal(0.3, 0.9)
        out = q-C_BUN; out /= np.linalg.norm(out); side = np.cross(out, AX); L = 4+6*rng.random(); nn = 6+int(10*rng.random())
        for m in range(nn):
            off = rng.normal(0, 0.25, 3); pts = []
            for s in np.linspace(0, 1, N_PTS):
                pts.append(q+off+out*math.sin(math.pi*s)*L*(0.3+0.2*rng.random())+side*(s-0.5)*L*0.8+np.array([0, 0, -1.2*s*s*L*0.35])+vnoise3(q+s, 0.9, 700+k)*0.35)
            loose.append(np.asarray(pts))
    log('v6 extras: tendril locks', len(TEND), 'baby hairs', len(sel))
log('loose strands', len(loose))
# ------------------------------------------------------------------------------------------------ export
def export(strands, name, npts=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    for s in strands:
        sp = cu.splines.new('POLY'); sp.points.add(len(s)-1)
        for i, (x, y, z) in enumerate(s): sp.points[i].co = (x, -z, y, 1)            # Alembic Y-up -> UE (X, Y, Z) cm
    ob = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.scene.objects: o.select_set(o == ob)
    fp = os.path.join(OUT, name+'.abc'); bpy.ops.wm.alembic_export(filepath=fp, selected=True, start=1, end=1, curves_as_mesh=False, global_scale=1.0)
    bpy.data.objects.remove(ob, do_unlink=True); log('exported', fp, len(strands))
export(main_strands, 'hair_main'); export(loose, 'hair_loose')
# preview geometry (JSON, UE cm) for Blender/QA renders and the report
stats = {'main_strands': len(main_strands), 'loose_strands': len(loose), 'points_per_strand': N_PTS, 'bun_centre': C_BUN.tolist(), 'bun_radius': R_BUN, 'bun_axis': AX.tolist(), 'part_x': PART_X, 'seed': SEED,
         'scalp_area_cm2': float(S_A.sum()), 'root_density_per_cm2': N_MAIN/float(S_A.sum())}
open(os.path.join(OUT, 'hair_build.json'), 'w').write(json.dumps(stats, indent=1)); log('HAIR_OK', json.dumps(stats))
