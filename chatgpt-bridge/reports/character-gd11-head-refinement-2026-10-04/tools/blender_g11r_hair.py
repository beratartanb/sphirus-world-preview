"""GD11 head refinement hair (h30 = h23 builder + per-side face-lock / temple-lock controls; copy of blender_gd8_hair.py).
GUARDIAN-8 hair (user correction 2026-10-02): side hair mass starts further back / higher (side hairline 86/98 deg + ear-drape off + no
forward side curtain), bun on the lower occiput (not the nape), sparser / airier rear mass with separated overlapping groups, part cover hairs.
Built on GUARDIAN-7:
GUARDIAN-7 hair (user correction 2026-10-02): natural lifted silhouette + loose overlapping lock groups. Built on the GUARDIAN-4
hierarchical builder; changes: continuous lift FIELD (hairline -> crown -> rear-upper roll -> nape; low sides, no wide dome), more and
smaller primary masses, loose convergence + persistent lateral fill (no rope / dreadlock cords, no deep channels), lower lift at the
part edge + root crossover (no symmetric ridges), loose irregular bun loops (no cord rings). Original header:
GUARDIAN-4 hair: HIERARCHICAL LOCK REBUILD (not an id21 tweak). Main groom = primary flow masses -> secondary locks -> tertiary
clumps -> strands (each level its own root offset / partial convergence / depth separation / wave), a root-free part band so the scalp
reads at the part, irregular hairline (v15b), low irregular bun built from the locks (every secondary lock wraps its own loop).
Loose groom (face-framing / temple / ear / nape / flyaway locks) and scalp / collision / Alembic code reused from blender_lk_hair_locks.py (v14-v16).
Head = SPH_HEAD_NPY (DNA order == package order) so roots sit on the GUARDIAN-4 cranium.
usage: blender -b --factory-startup --python blender_gd4_hair.py -- <sculpt_package.json.gz> <out_dir> [seed]"""
import bpy, sys, os, json, gzip, math, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index('--')+1:]; PKG, OUT = argv[0], argv[1]; SEED = int(argv[2]) if len(argv) > 2 else 20260930
os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(SEED); T0 = time.time()
def log(*a): print('[locks %6.1fs]' % (time.time()-T0), *a, flush=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
E = lambda k, d: float(os.environ.get(k, d))
N_MAIN = int(E('SPH_HAIR_N', '38000')); N_PTS = int(E('SPH_HAIR_PTS', '24')); K_LOCKS = int(E('SPH_K_LOCKS', '130'))
P = json.loads(gzip.open(PKG, 'rb').read()); NB, NH = P['NB'], P['NH']
X = np.asarray(P['br_neutral'], np.float64)[NB:] if not os.environ.get('SPH_HEAD_NPY') else np.load(os.environ['SPH_HEAD_NPY']).astype(np.float64); T = np.asarray(P['head']['triangles'], np.int64); MI = np.asarray(P['head']['material_ids'])
HT = T[MI == 0]
BODYX = np.asarray(P['br_neutral'], np.float64)[:NB]; BT = np.asarray(P['body']['triangles'], np.int64)
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t) for t in HT]); bvh_body = BVHTree.FromPolygons([Vector(p) for p in BODYX], [list(t) for t in BT])
a, b, c = X[HT[:, 0]], X[HT[:, 1]], X[HT[:, 2]]; fn = -np.cross(b-a, c-a); area = np.linalg.norm(fn, axis=1)*0.5; fn /= np.maximum(np.linalg.norm(fn, axis=1), 1e-9)[:, None]; cen = (a+b+c)/3
def nearest(p):
    loc, nrm, idx, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), (np.asarray(fn[idx]) if idx is not None else np.array([0, 0, 1.0]))
def push_out(p, gap):
    loc, n = nearest(p); d = float(np.dot(p-loc, n))
    if d < gap: p = p+n*(gap-d)
    lb, nb_, ib, db = bvh_body.find_nearest(Vector(p))
    if lb is not None:
        lb = np.asarray(lb); nrm = -np.asarray(nb_); dd = float(np.dot(p-lb, nrm))
        if dd < gap*0.8 and db < 6: p = p+nrm*(gap*0.8-dd)
    return p
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def resample(pts, n):
    pts = np.asarray(pts); seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < 1e-6: return np.repeat(pts[:1], n, 0)
    t = np.linspace(0, s[-1], n); return np.stack([np.interp(t, s, pts[:, k]) for k in range(3)], 1)
def smooth_poly(pts, it=3):
    p = np.asarray(pts, float).copy()
    for _ in range(it): p[1:-1] = 0.5*p[1:-1]+0.25*(p[:-2]+p[2:])
    return p
# ------------------------------------------------------------------ scalp (same hairline logic as v13, softer temples)
PART_X = E('SPH_PART_X', '1.3')
HL15 = E('SPH_HL_V15', '0') > 0
_TH = np.array([0, 20, 38, 50, 62, 74, 86, 98, 115, 135, 150])          # azimuth from the front (deg)
_ZH = np.array([E('SPH_HL_C', '168.6'), 168.3, 167.8, 168.2, 166.6, 163.8, 160.8, 160.6, 161.4, 158.0, 153.5])   # hairline z (UE cm); 38->50 deg: temporal recession
HL15B = E('SPH_HL_V15B', '0') > 0
if HL15B:   # v15b: temples come forward/down to the reference (v15a left a bald temple wedge between brow and ear), milder recession
    _ZH = np.array([E('SPH_HL_C', '168.6'), 168.3, 167.9, 167.7, E('SPH_HL_T62', '165.4'), E('SPH_HL_T74', '162.6'), E('SPH_HL_T86', '160.6'), E('SPH_HL_T98', '160.4'), E('SPH_HL_T115', '161.4'), 158.0, 153.5])
def hairline_z(x, y):
    th = abs(math.degrees(math.atan2(x, y-2.5)))
    base = float(np.interp(th, _TH, _ZH)) if th <= 150 else None
    jag = E('SPH_HL_JAG', '0.45')*(math.sin(x*2.9+1.1)*0.5+math.sin(x*6.1+0.4)*0.3+math.sin(x*11.3+2.0)*0.2)
    return base, jag, th
def scalp_mask(p, n):
    x, y, z = p; ax = abs(x)
    if n[2] < -0.35: return False
    if HL15:
        zb, jag, th = hairline_z(x, y)
        if zb is not None: return z > zb+jag*(1.0 if th < 80 else 0.4)
        return z > 150.6+2.2*(ax/6.0)**2
    if y > 5.0: return z > 165.8-2.6*(ax/7.0)**2+0.15*math.sin(x*1.3)+E('SPH_HL_JAG', '0.55')*(math.sin(x*2.7+1.1)*0.6+math.sin(x*5.3+0.4)*0.4)
    if y > 0.5: return z > 162.5 and not (ax > 5.0 and z < 164.5)            # sideburn roots thinned (v13v finding)
    if y > -0.5: return z > 161.2 and not (ax > 6.3 and z < 162.5)
    return z > 150.6+2.2*(ax/6.0)**2
ok = np.array([scalp_mask(cen[i], fn[i]) for i in range(len(HT))]); S_T = HT[ok]; S_A = area[ok]; S_N = fn[ok]
S_C = X[S_T].mean(1)
_zb = 165.8-2.6*(np.abs(S_C[:, 0])/7.0)**2+0.15*np.sin(S_C[:, 0]*1.3)+E('SPH_HL_JAG', '0.55')*(np.sin(S_C[:, 0]*2.7+1.1)*0.6+np.sin(S_C[:, 0]*5.3+0.4)*0.4)
_d = S_C[:, 2]-_zb; _front = (S_C[:, 1] > 5.0)
# natural hairline: sparse fine hairs at the edge, density ramps up over ~1.5 cm, then the extra front density (covers the scalp from above)
S_W = S_A*np.where(_front, (0.35+0.65*sstep(_d/0.9))*(1+E('SPH_HL_DENS', '1.2')*sstep((_d-0.5)/1.2)*(1-sstep((_d-4.5)/1.5))), 1.0)
if HL15:
    _hz = np.array([hairline_z(c[0], c[1])[0] or -1e3 for c in S_C]); _th = np.array([hairline_z(c[0], c[1])[2] for c in S_C]); _d2 = S_C[:, 2]-_hz
    S_W = S_A*np.where(_th < 100, (E('SPH_HL_EDGE', '0.22')+(1-E('SPH_HL_EDGE', '0.22'))*sstep(_d2/E('SPH_HL_RAMP', '1.8')))*(1+E('SPH_HL_DENS', '0.8')*sstep((_d2-1.2)/1.5)*(1-sstep((_d2-5.0)/1.5))), 1.0)
if E('SPH_BACK_DENS', '1.0') != 1.0 or E('SPH_SIDEFRONT_DENS', '1.0') != 1.0:
    _bk = sstep((-S_C[:, 1]-1.5)/3.0)*sstep((S_C[:, 2]-153.0)/3.0); S_W = S_W*(1+(E('SPH_BACK_DENS', '1.0')-1)*_bk)
    _sf = sstep((np.abs(S_C[:, 0])-4.6)/1.0)*sstep((S_C[:, 1]+0.5)/2.0)*(1-sstep((S_C[:, 2]-166.0)/1.5)); S_W = S_W*(1+(E('SPH_SIDEFRONT_DENS', '1.0')-1)*_sf)
if E('SPH_NAPE_DENS', '1.0') != 1.0:
    _np = sstep((-S_C[:, 1]-0.5)/2.5)*(1-sstep((S_C[:, 2]-156.5)/2.0)); S_W = S_W*(1+(E('SPH_NAPE_DENS', '1.0')-1)*_np)
def sample_scalp(n):
    tri = rng.choice(len(S_T), size=n, p=S_W/S_W.sum()); u = rng.random(n); v = rng.random(n); m = u+v > 1; u[m], v[m] = 1-u[m], 1-v[m]
    A, B_, C = X[S_T[tri, 0]], X[S_T[tri, 1]], X[S_T[tri, 2]]; return A+(B_-A)*u[:, None]+(C-A)*v[:, None], S_N[tri]
HC = np.array([0.0, 2.5, 160.5])
C_BUN = np.array([E('SPH_BUN_X', '1.2'), E('SPH_BUN_Y', '-8.7'), E('SPH_BUN_Z', '156.4')])
Gs, gn = nearest(C_BUN); AX = C_BUN-Gs; AX /= np.linalg.norm(AX); AX = 0.35*AX+np.array([0.0, -1.0, 0.25]); AX /= np.linalg.norm(AX); U1 = np.cross(AX, [0, 0, 1.0]); U1 /= np.linalg.norm(U1); U2 = np.cross(AX, U1)
R_BUN = E('SPH_BUN_R', '3.1')
def vnoise3(p, f, seed):
    r = np.random.default_rng(seed); out = np.zeros(3)
    for k in range(3):
        for o in range(3):
            fr = f*(1.7**o); ph = r.random(3)*6.28; d = r.normal(0, 1, 3); d /= np.linalg.norm(d); out[k] += math.sin(float(np.dot(p, d))*fr+ph[0])*(0.55**o)
    return out/1.8
N_GROUPS = int(E('SPH_BUN_GROUPS', '9'))
G_ANG = np.sort(rng.random(N_GROUPS))*2*np.pi; G_R = 1.9+E('SPH_BUN_RV', '1.9')*rng.random(N_GROUPS); G_TURN = (0.55+0.75*rng.random(N_GROUPS))*E('SPH_BUN_TURN', '1.0')
G_TILT = rng.normal(0, 0.45, (N_GROUPS, 2)); G_AX = rng.normal(0.2, 1.0, N_GROUPS); G_C = rng.normal(0, E('SPH_BUN_CJ', '0.9'), (N_GROUPS, 3))*np.array([1.0, 0.8, 0.45]); G_ESC = rng.random(N_GROUPS) < E('SPH_BUN_ESC', '0.35')
V16 = E('SPH_V16', '0') > 0
def region_lift(r):
    x, y, z = r; side = 1.0 if x > PART_X else -1.0; asym = 1.15 if side > 0 else 0.9
    if V16:
        if abs(x) > 4.2 and z > 156.0 and y > -4.5: L = E('SPH_L_SIDE', '3.2')+0.9*rng.random()          # temples / over the ears: the reference's wide side mass
        elif z > 167.5: L = E('SPH_L_TOP', '1.4')+0.5*rng.random()                                       # top: rounded dome, no lumps
        elif y > 3.0 and z > 163.5: L = E('SPH_L_FRONT', '1.1')+0.5*rng.random()
        elif y < -2.0 and z > 157.0: L = 1.0+0.5*rng.random()
        else: L = 0.6+0.5*rng.random()
        return L*asym*E('SPH_LIFT_S', '1.0')
    if z > 168.0: L = 2.2+0.9*rng.random()
    elif y > 3.0 and z > 164.5: L = (0.9+0.6*rng.random())*E('SPH_FRONT_LIFT', '1.0')
    elif abs(x) > 4.5 and z > 161.0 and y > -3.0: L = 1.5+0.9*rng.random()
    elif y < -2.0 and z > 157.0: L = 0.8+0.6*rng.random()
    else: L = 0.4+0.5*rng.random()
    return L*asym*E('SPH_LIFT_S', '1.0')
def lock_path(r, lift, seed, ear_drape, bump, wave_amp, wave_len, gidx):
    """authored lock centreline: scalp arc from the root section to its bun group entry, lifted, draped, waved"""
    rr = np.random.default_rng(seed); dirv = r-Gs; dirv -= AX*np.dot(dirv, AX); ang = math.atan2(float(np.dot(dirv, U2)), float(np.dot(dirv, U1)))
    ga = G_ANG[gidx]; wo = E('SPH_ENTRY_OWN', '0.5'); ea = (1-wo)*ga+wo*ang if abs(ang-ga) < np.pi else ang; er = R_BUN*(0.8+E('SPH_ENTRY_RJ', '0.0')*(rr.random()-0.5))
    entry = C_BUN+G_C[gidx]*0.5*(1-wo)+(U1*math.cos(ea)+U2*math.sin(ea))*er+AX*E('SPH_ENTRY_AJ', '0.0')*(rr.random()-0.5)
    ua = r-HC; ub = entry-HC; la, lb = np.linalg.norm(ua), np.linalg.norm(ub); ua = ua/la; ub = ub/lb
    cab = float(np.dot(ua, ub)); over = max(0.0, -cab-0.2)*1.6; n_s = 28; path = []
    front = sstep((r[1]-1.0)/5.0)
    for k in range(n_s+1):
        t = k/n_s
        if over > 0 or front > 0:
            mid = ua+ub+np.array([0.0, -0.25, 1.0])*max(over, 0.3)
            sd = 1.0 if r[0] > PART_X else -1.0; lat = np.array([sd*0.8, 0.2, 0.5]); lat /= np.linalg.norm(lat); mid = mid/np.linalg.norm(mid); mid = mid*(1-E('SPH_PART_LAT', '0.3')*front)+lat*E('SPH_PART_LAT', '0.3')*front; mid /= np.linalg.norm(mid)
            sp = 0.45; a_, b_, tt = (ua, mid, t/sp) if t < sp else (mid, ub, (t-sp)/(1-sp))
        else: a_, b_, tt = ua, ub, t
        om = math.acos(max(-1.0, min(1.0, float(np.dot(a_, b_))))); d = a_ if om < 1e-4 else (math.sin((1-tt)*om)*a_+math.sin(tt*om)*b_)/math.sin(om)
        q = HC+d*(la*(1-t)+lb*t+0.8); loc, n = nearest(q)
        if E('SPH_FIELD_PATH', '0') > 0:   # lift follows the position along the path (hairline low -> crown / rear-upper high -> nape low)
            h = 0.15+lift_field(np.asarray(loc))*E('LF_PATH_GAIN', '1.0')*sstep(t/0.14)*(1-0.7*sstep((t-0.82)/0.18))+0.25*t+bump*math.sin(math.pi*t)**2
        else: h = 0.15+lift*sstep(t/(0.22+0.16*front))*(math.sin(math.pi*min(1.0, t*1.15))**0.5)*(1-0.55*t)+0.35*t+bump*math.sin(math.pi*t)**2
        nb = n+front*(1-sstep(t/0.35))*np.array([0.0, -0.3, 0.9]); nb /= np.linalg.norm(nb)
        if front > 0 and t < 0.2: q_roll = np.array([0.0, 1.0, 0.35])*front*E('SPH_ROLL', '0.0')*math.sin(math.pi*t/0.2)
        else: q_roll = 0.0
        q = loc+nb*h+q_roll
        if ear_drape > 0: q = q+np.array([0, 0, -ear_drape])*(math.sin(math.pi*min(1.0, t*1.3))**1.4)
        path.append(q)
    path = np.asarray(path); path[-1] = entry; path = smooth_poly(path, 2)
    tg = np.gradient(path, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-6)[:, None]; nr = path-HC; nr /= np.linalg.norm(nr, axis=1)[:, None]; bi = np.cross(tg, nr); bi /= np.maximum(np.linalg.norm(bi, axis=1), 1e-6)[:, None]
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))]); ph = rr.random()*6.28; env = sstep(arc/5.0)*(1-0.6*sstep((arc-arc[-1]+4)/4))
    path = path+bi*(wave_amp*env*np.sin(2*np.pi*arc/wave_len+ph))[:, None]+nr*(0.15*wave_amp*env*np.sin(2*np.pi*arc/wave_len+1.7*ph))[:, None]
    return path, ang
def bun_loop(gidx, start, n=18, off=np.zeros(2), lock_seed=0):
    """continuation of a lock inside its bun loop group: wraps around the bun axis with the group's radius / tilt / tension;
    escaping groups leave the loop with a curling end, the others tuck into the centre"""
    rr = np.random.default_rng(lock_seed); c = C_BUN+G_C[gidx]; ax = AX+U1*G_TILT[gidx, 0]+U2*G_TILT[gidx, 1]; ax /= np.linalg.norm(ax)
    u1 = np.cross(ax, [0, 0, 1.0]); u1 /= np.linalg.norm(u1); u2 = np.cross(ax, u1); d0 = start-c; a0 = math.atan2(float(np.dot(d0, u2)), float(np.dot(d0, u1))); r0 = np.linalg.norm(d0-ax*np.dot(d0, ax))
    turns = G_TURN[gidx]*(0.85+0.3*rr.random()); sgn = 1 if gidx % 2 else -1; pts = []
    for k in range(1, n+1):
        u = k/n; a_ = a0+sgn*2*np.pi*turns*u; R = r0+(G_R[gidx]-r0)*sstep(u/0.25)
        if G_ESC[gidx] and u > 0.7: R = R+(u-0.7)/0.3*(1.4+1.2*rr.random())
        elif u > 0.75: R = R*(1-0.55*(u-0.75)/0.25)
        R = R+off[0]; axo = G_AX[gidx]*0.6+(-0.5+1.1*u)+off[1]
        pts.append(c+ax*axo+(u1*math.cos(a_)+u2*math.sin(a_))*R+vnoise3(np.array([a_, u, gidx]), 1.0, 900+gidx)*0.45)
    return np.asarray(pts)
# ------------------------------------------------------------------ GUARDIAN-4 main groom: PRIMARY masses -> SECONDARY locks -> TERTIARY clumps
# primary  (~16): big flow masses (part side, crown, temples / over the ears, nape), authored scalp->bun path (lock_path)
# secondary(~120): visible locks inside a mass: own root offset converging only partly, own lift (depth separation between locks) and wave
# tertiary (~700): clumps inside a lock: tighter convergence, small twist wave; strands clump hard to their tertiary toward the tip
# part     : narrow root-free band along the part line on top / front so the scalp reads; clusters never straddle the part
roots, rnorm = sample_scalp(N_MAIN)
PW = E('SPH_PART_W', '0.30'); pd = roots[:, 0]-PART_X; onpart = (roots[:, 1] > E('SPH_PART_Y0', '-3.0')) & (roots[:, 2] > 163.5)
keep = ~(onpart & (np.abs(pd) < PW*(1+0.5*np.sin(roots[:, 1]*1.7))) & (rng.random(len(roots)) < 0.9)); roots, rnorm = roots[keep], rnorm[keep]
SIDE = np.where(roots[:, 0] > PART_X, 1.0, -1.0); FEAT = roots+np.stack([SIDE*np.where(roots[:, 1] > E('SPH_PART_Y0', '-4.0'), 4.0, 0.0), np.zeros(len(roots)), np.zeros(len(roots))], 1)
def kmeans(F_, k, it=10):
    k = max(1, min(k, len(F_))); c = F_[rng.choice(len(F_), k, replace=False)].copy()
    for _ in range(it):
        lab_ = ((F_[:, None, :]-c[None])**2).sum(2).argmin(1)
        for j in range(k):
            m = lab_ == j
            if m.any(): c[j] = F_[m].mean(0)
    return ((F_[:, None, :]-c[None])**2).sum(2).argmin(1)
def frame(cl):
    tg = np.gradient(cl, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-6)[:, None]; nr = cl-HC; nr /= np.linalg.norm(nr, axis=1)[:, None]
    bi = np.cross(tg, nr); bi /= np.maximum(np.linalg.norm(bi, axis=1), 1e-6)[:, None]; nr = np.cross(bi, tg); return tg, nr, bi
def child_path(par, root, conv, conv_s, depth, wamp, wlen, ph, twist=0.0):
    """child centreline in the parent's frame: root offset (nr, bi) converging by 'conv' after 'conv_s', + depth bulge, + own wave"""
    tg, nr, bi = frame(par); d0 = root-par[0]; c0 = np.array([np.dot(d0, nr[0]), np.dot(d0, bi[0])]); s = np.linspace(0, 1, len(par))
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(par, axis=0), axis=1))]); env = sstep(arc/3.0)*(1-0.5*sstep((arc-arc[-1]+3)/3))
    w = sstep(s/conv_s)*conv; off = c0[None]*(1-w)[:, None]
    if twist: a_ = twist*s*2*np.pi; ca, sa = np.cos(a_), np.sin(a_); off = np.stack([off[:, 0]*ca-off[:, 1]*sa, off[:, 0]*sa+off[:, 1]*ca], 1)
    on = off[:, 0]+depth*np.sin(np.pi*np.clip(s*1.15, 0, 1))**0.7; ob = off[:, 1]+wamp*env*np.sin(2*np.pi*arc/wlen+ph)
    p = par+nr*on[:, None]+bi*ob[:, None]; p = p+(root-p[0])[None]*(1-sstep(s/0.12))[:, None]; return p
def lift_field(r):
    """stand-off (cm) by position: hairline rise -> crown -> rear-upper roll -> nape; sides kept low; lower right at the part edge"""
    x, y, z = r; ax = abs(x-PART_X)
    top = sstep((z-164.5)/3.5); back = sstep((-y-0.5)/3.5)*sstep((z-157.5)/3.0); front = sstep((y-2.5)/3.0)*sstep((z-163.0)/2.0)
    side = sstep((abs(x)-4.4)/1.2)*(1-sstep((z-168.5)/2.0)); nape = 1-sstep((z-156.5)/2.5)
    top = top*(1-E('LF_TOPFRONT_CUT', '0.0')*sstep((y-2.5)/4.5))
    L = E('LF_BASE', '0.45')+E('LF_TOP', '1.5')*top+E('LF_BACK', '1.4')*back*(1-0.4*nape)+E('LF_FRONT', '0.9')*front-E('LF_SIDE', '0.35')*side-0.3*nape
    L *= (0.55+0.45*sstep((ax-0.2)/1.4) if y > -1.0 else 1.0) if E('LF_PARTDIP', '1') > 0 else 1.0
    L *= E('LF_ASYM', '1.0') if x > PART_X else 2.0-E('LF_ASYM', '1.0')
    return max(0.25, L)
K1 = int(E('SPH_K1', '16')); K2 = int(E('SPH_K2', '120')); K3 = int(E('SPH_K3', '700'))
lab1 = kmeans(FEAT, K1); prim = {}; t0 = time.time()
for p in range(K1):
    idx = np.nonzero(lab1 == p)[0]
    if len(idx) == 0: continue
    r = nearest(roots[idx].mean(0))[0]; lift = lift_field(r) if E('SPH_FIELD', '0') > 0 else region_lift(r); side_ear = (abs(r[0]) > 5.0 and -3.5 < r[1] < 4.5 and r[2] < 167.0)
    ear_drape = (2.0+1.3*rng.random())*E('SPH_EAR_D', '1.0') if side_ear else 0.0
    bump = (0.6+0.9*rng.random())*E('SPH_BUMP_SIDE', '1.0') if (rng.random() < E('SPH_MESSY_P', '0.3') and r[2] < 167.0) else 0.0
    dirv = r-Gs; dirv -= AX*np.dot(dirv, AX); ang = math.atan2(float(np.dot(dirv, U2)), float(np.dot(dirv, U1))) % (2*np.pi)
    gidx = int(np.argmin(np.abs(((G_ANG-ang+np.pi) % (2*np.pi))-np.pi)))
    cl, _ = lock_path(r, lift, 3000+p, ear_drape, bump, (0.45+0.4*rng.random())*E('SPH_WAVE', '1.0'), 9.0+4.0*rng.random(), gidx)
    prim[p] = (cl, gidx, idx)
main = []; n_sec = 0; n_ter = 0
for p, (pcl, gidx, idx) in prim.items():
    k2 = max(2, int(round(K2*len(idx)/len(roots)))); lab2 = kmeans(roots[idx], k2)
    for s_ in range(k2):
        sidx = idx[lab2 == s_]
        if len(sidx) == 0: continue
        n_sec += 1; sr = nearest(roots[sidx].mean(0))[0]; sg_ = n_sec*13+7; rs = np.random.default_rng(sg_)
        sdep = ((lift_field(sr)-lift_field(nearest(roots[idx].mean(0))[0]))*0.55+rs.normal(0, E('SPH_SEC_DS', '0.05'))*(1+E('SPH_BACK_VAR', '0.0')*sstep((-sr[1]-1.0)/3.0))) if E('SPH_FIELD', '0') > 0 else rs.normal(E('SPH_SEC_D', '0.12'), E('SPH_SEC_DS', '0.22'))
        scl = child_path(pcl, sr, (0.35+0.25*rs.random())*E('SPH_SEC_CONV', '1.0'), 0.45, sdep, (0.25+0.3*rs.random())*E('SPH_WAVE2', '1.0'), 5.0+3.0*rs.random(), rs.random()*6.28)
        loop_off = np.array([rs.normal(0, 0.5), rs.normal(0, 0.5)]); g2 = gidx if rs.random() > 0.25 else int(rs.integers(N_GROUPS))
        k3 = max(1, int(round(K3*len(sidx)/len(roots)))); lab3 = kmeans(roots[sidx], k3, 6)
        for t_ in range(k3):
            tidx = sidx[lab3 == t_]
            if len(tidx) == 0: continue
            n_ter += 1; tr = nearest(roots[tidx].mean(0))[0]; rt = np.random.default_rng(n_ter*29+5)
            bk_ = sstep((-tr[1]-1.5)/3.0); tcl = child_path(scl, tr, min(0.95, (0.55+0.25*rt.random())*E('SPH_TER_CONV', '1.0')*(1+E('SPH_BACK_CLUMP', '0.0')*bk_)), 0.35, rt.normal(0.0, 0.08), 0.10+0.12*rt.random(), 3.0+2.0*rt.random(), rt.random()*6.28, twist=rt.normal(0, 0.25))
            for i in tidx:
                rr_ = np.random.default_rng(int(i)+17); conv = min(0.98, E('SPH_CONV', '0.7')+E('SPH_CONV_R', '0.25')*rr_.random()) if rr_.random() > 0.05 else 0.2*rr_.random()
                bks_ = sstep((-roots[i][1]-1.5)/3.0); conv = min(0.97, conv*(1+E('SPH_BACK_CLUMP', '0.0')*0.6*bks_)); pts = child_path(tcl, roots[i], conv, 0.3, 0.0, 0.03, 2.5, rr_.random()*6.28)
                if E('SPH_FILL', '0') > 0:   # persistent lateral fill: strands drift sideways along the length so groups overlap (no empty channels)
                    tg_, nr_, bi_ = frame(pts); sfill = np.linspace(0, 1, len(pts)); fl_ = E('SPH_FILL', '0')*(1-E('SPH_BACK_FILLCUT', '0.0')*bks_); pts = pts+bi_*(rr_.normal(0, fl_)*sstep(sfill/0.35))[:, None]+nr_*(rr_.normal(0, fl_*0.35)*sstep(sfill/0.35))[:, None]
                s = np.linspace(0, 1, len(pts)); fz = (0.04+0.06*rr_.random())*E('SPH_FRIZZ', '1.0') if rr_.random() > 0.05 else 0.25+0.3*rr_.random()
                pts = pts+np.asarray([vnoise3(q, 1.6, int(n_ter*7+3))*fz*(0.3+st) for q, st in zip(pts, s)])
                lp = bun_loop(g2, pts[-1], 16, off=loop_off+rr_.normal(0, E('SPH_BUN_JIT', '0.12'), 2), lock_seed=n_sec if E('SPH_BUN_PERLOCK', '1') > 0 else int(i) % 997)
                full = resample(np.vstack([pts, lp]), N_PTS)
                for m in range(len(full)): full[m] = push_out(full[m], 0.08 if m < 2 else 0.18)
                main.append(full)
    log('primary', p, 'strands', len(main), round(time.time()-t0, 1))
log('hierarchy', 'primary', len(prim), 'secondary', n_sec, 'tertiary', n_ter)
NPC = int(E('SPH_PART_COVER', '0')); npc_ = 0
while npc_ < NPC:
    q, n = sample_scalp(1); q, n = q[0], n[0]
    if not (abs(q[0]-PART_X) < 1.1 and q[1] > -2.5 and q[2] > 164.5): continue
    sd = -1.0 if q[0] > PART_X else 1.0; dv = np.array([sd*(0.5+0.6*rng.random()), -0.6-0.6*rng.random(), 0.0]); dv -= n*np.dot(dv, n); dv /= np.linalg.norm(dv)
    Lc = 1.6+1.8*rng.random(); pts = [push_out(q+dv*Lc*s_+n*(0.05+0.18*s_), 0.05) for s_ in np.linspace(0, 1, 8)]; main.append(resample(np.asarray(pts), N_PTS)); npc_ += 1
NBABY = int(E('SPH_BABY', '0')); nb_ = 0
while nb_ < NBABY:
    q, n = sample_scalp(1); q, n = q[0], n[0]
    if HL15:                                                                                   # v15: band just above the authored hairline
        zb_, _, th_ = hairline_z(q[0], q[1])
        if zb_ is None or th_ > 100 or not (q[2] < zb_+E('SPH_BABY_BAND', '1.0')): continue
    elif not (q[1] > 3.0 and q[2] < 168.5-2.6*(abs(q[0])/7.0)**2): continue                    # front hairline band only
    back = np.array([0.0, -1.0, 0.55])+np.array([np.sign(q[0]-PART_X)*0.35, 0.0, 0.0]); back -= n*np.dot(back, n); back /= np.linalg.norm(back)
    L = 1.8+2.2*rng.random(); side = np.cross(n, back); ph = rng.random()*6.28
    pts = [q+back*L*s_+n*(0.06+0.22*s_)+side*0.25*math.sin(ph+6.0*s_) for s_ in np.linspace(0, 1, 10)]
    pts = [push_out(p_, 0.06) for p_ in pts]; main.append(resample(np.asarray(pts), N_PTS)); nb_ += 1
log('main strands', len(main))
# ------------------------------------------------------------------ loose groom: authored locks
loose = []
def contour(z, sg):
    """outer face contour (front half) at height z on side sg: x, y of the most lateral head point in front of the ear"""
    s = X[(np.abs(X[:, 2]-z) < 0.6) & (X[:, 1] > 1.5) & (X[:, 0]*sg > 0)]
    if len(s) == 0: return np.array([sg*6.0, 3.0])
    p = s[np.argmax(s[:, 0]*sg)]; return np.array([p[0], p[1]])
def wave_lock(ctrl, n_str, lock_r, amp, wl, seed, taper=0.6, spread_tip=1.5, stray=0.08):
    """thick wavy lock from a hand-placed control polyline: smoothed centreline + S-wave, clumped strands, a few strays"""
    rr = np.random.default_rng(seed); cl = resample(smooth_poly(resample(np.asarray(ctrl, float), 40), 6), N_PTS)
    amp = amp*E('SPH_LOOSE_AMP', '1.0'); wl = wl*E('SPH_LOOSE_WL', '1.0'); spread_tip = spread_tip*E('SPH_LOOSE_SPREAD', '1.0'); n_str = int(n_str*E('SPH_LOOSE_N', '1.0'))
    tg = np.gradient(cl, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-6)[:, None]
    rad_ = np.stack([cl[:, 0], (cl[:, 1]-3.0)*0.35, np.zeros(len(cl))], 1); rad_ /= np.maximum(np.linalg.norm(rad_, axis=1), 1e-6)[:, None]
    side = rad_-tg*np.sum(rad_*tg, 1)[:, None]; side /= np.maximum(np.linalg.norm(side, axis=1), 1e-6)[:, None]; up = np.cross(side, tg)
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(cl, axis=0), axis=1))]); ph = rr.random()*6.28; env = sstep(arc/3.0)
    cl = cl+side*(amp*env*np.sin(2*np.pi*arc/wl+ph))[:, None]+up*(0.1*amp*env*np.sin(2*np.pi*arc/wl+2.0*ph))[:, None]
    out = []; s = np.linspace(0, 1, N_PTS)
    for k in range(n_str):
        a_ = rr.random()*2*np.pi; rad = lock_r*math.sqrt(rr.random()); o1, o2 = rad*math.cos(a_), rad*math.sin(a_)
        tipw = 1+spread_tip*sstep((s-0.6)/0.4)*rr.random(); L_ = 0.8+0.2*rr.random() if rr.random() > stray else 0.5+0.5*rr.random()
        st = cl+side*(o1*tipw*(1-0.3*s*taper))[:, None]+up*(o2*tipw*(1-0.3*s*taper))[:, None]+np.asarray([vnoise3(p, 2.2, seed*31+k % 5)*0.06 for p in cl])
        if rr.random() < stray: st = st+side*(np.linspace(0, 1, N_PTS)**2*rr.normal(0, 1.2))[:, None]
        st = resample(st[:max(6, int(N_PTS*L_))], N_PTS)
        for m in range(N_PTS): st[m] = push_out(st[m], 0.2+1.0*sstep(m/5.0))
        out.append(st)
    return out
FACE = []
for sg in (1, -1):
    asym = 1.0 if sg > 0 else 0.85
    for j, (x0, y0, z0, z_end, gap, fwd, n_str) in enumerate([(3.2, 9.0, 167.0, 150.0, 2.4, 0.8, 90), (4.6, 8.3, 166.2, 147.5, 2.1, 0.6, 110), (5.9, 7.2, 165.0, 146.0, 1.9, 0.3, 100),
                                                              (6.8, 5.6, 164.0, 149.5, 1.7, 0.0, 80), (2.2, 9.6, 167.6, 156.0, 2.8, 1.0, 50)]):
        if str(j) in os.environ.get('SPH_FACE_SKIP', '').split(','): continue
        if str(j) in os.environ.get('SPH_FACE_SKIP_'+('L' if sg > 0 else 'R'), '').split(','): continue
        if sg < 0 and j == 4: continue                                          # asymmetric: one short front lock on the part side only
        z_end = z_end+(0.0 if sg > 0 else 1.5)
        if HL15:   # roots at the raised (reference) hairline, not on the forehead
            z0 = hairline_z(sg*x0, y0)[0]+0.7; y0 = float(nearest(np.array([sg*x0, y0, z0]))[0][1])
        ctrl = [np.array([sg*x0, y0, z0])]
        for z in np.linspace(z0-2.5, z_end, 6):
            cx, cy = contour(z, sg); g = 0.6*gap*(0.8+0.4*(z0-z)/(z0-z_end)); ctrl.append(np.array([cx+sg*g, cy+(fwd+0.6)*(0.5+0.5*(z0-z)/(z0-z_end)), z]))
        FACE.append((ctrl, int(float(E('SPH_FACE_MULT', '2.0'))*n_str*asym), 0.62+0.18*j/4, 0.8+0.4*rng.random(), 9.0+2.5*rng.random(), 400+j+(0 if sg > 0 else 50)))
for sg in (1, -1):
    for j, (x0, z0, xe, ze) in enumerate(((1.6, 167.8, 6.6, 157.0), (3.0, 167.4, 7.4, 154.5))):
        if sg < 0 and j == 1: continue
        xs0 = PART_X+sg*x0
        if HL15: z0 = hairline_z(xs0, 8.6)[0]+0.9
        ctrl = [np.array([xs0, 8.6, z0]), np.array([xs0+sg*1.4, 11.2, z0-1.2]), np.array([sg*(xe-1.2), 12.6, z0-4.0]), np.array([sg*xe, 11.0, ze+2.0]), np.array([sg*(xe+0.6), 9.0, ze])]
        FACE.append((ctrl, 45 if j == 0 else 35, 0.32, 0.7, 7.0, 800+j+(0 if sg > 0 else 20)))
for ctrl, n_, lr, amp, wl, sd in FACE: loose += wave_lock(ctrl, n_, lr*E('SPH_FF_R', '1.0'), amp*E('SPH_FF_AMP', '1.0'), wl*E('SPH_FF_WL', '1.0'), sd, spread_tip=E('SPH_FF_SPREAD', '1.5'))
for sg in (1, -1):                                                       # v15c temple locks: from the temporal hairline back over the upper ear
    for j, (thd, dz, n_t) in enumerate(((58, 0.0, 60), (70, -0.8, 70), (82, -1.4, 50))[:int(E('SPH_TEMPLE_LOCKS' if sg > 0 else 'SPH_TEMPLE_LOCKS_R', E('SPH_TEMPLE_LOCKS', '0')))]):
        thd = thd+E('SPH_TEMPLE_BACK_DEG', '0.0')
        yy_ = 2.5+7.0*math.cos(math.radians(thd)); xx_ = sg*7.0*math.sin(math.radians(thd)); zb_ = hairline_z(xx_, yy_)[0]; r0 = nearest(np.array([xx_, yy_, zb_+0.5]))[0]
        TX_ = E('SPH_TEMPLE_X', '1.0'); ctrl = [r0, r0+np.array([sg*0.5, -1.6, -0.4+dz*0.3]), np.array([sg*8.0*TX_, 0.8, zb_-1.6+dz]), np.array([sg*8.3*TX_, -1.8, zb_-3.0+dz]), np.array([sg*7.6*TX_, -4.0, zb_-4.6+dz])]
        loose += wave_lock(ctrl, int(n_t*(1.0 if sg > 0 else 0.85)), 0.45, 0.45, 7.5, 1200+j+(0 if sg > 0 else 40), taper=0.5, spread_tip=1.0)
if E('SPH_V16', '0') > 0:
    # fringe: asymmetric groups from the part falling INTO the forehead region (the reference's broken, crossing front)
    for j, (xs, xe, ze, n_, sd) in enumerate(((1.8, 4.6, 163.4, 70, 1), (0.6, 3.1, 164.8, 45, 1), (-1.2, -4.2, 164.2, 55, -1))):
        z0 = hairline_z(xs, 8.4)[0]+1.2; r0 = nearest(np.array([xs, 8.4, z0]))[0]
        ctrl = [r0, r0+np.array([sd*0.4, 1.4, 0.2]), np.array([sd*(abs(xs)+abs(xe))/2, 11.6, z0-1.6]), np.array([xe, 11.2, ze+0.4]), np.array([xe+sd*0.9, 9.4, ze-1.4])]
        ze = ze-E('SPH_FRINGE_DROP', '0.0'); ctrl[3][2] = ze+0.4; ctrl[4][2] = ze-1.4
        loose += wave_lock(ctrl, int(n_*E('SPH_FRINGE_MULT', '1.0')), 0.45*E('SPH_FRINGE_R', '1.0'), 0.5, 6.5, 1300+j, taper=0.5, spread_tip=1.2)
    # temple + face-framing S-waves: several per side, lengths to cheek / jaw / neck, asymmetric
    FF = [(58, 157.0, 1.2, 70), (66, 152.0, 1.6, 85), (72, 148.0, 1.9, 80), (80, 143.0, 2.2, 70), (88, 139.0, 2.4, 60)]
    for sg in (1, -1):
        for j, (thd, z_end, stand, n_) in enumerate(FF):
            if sg < 0 and j == 4: continue
            if str(j) in os.environ.get('SPH_FF_SKIP_L' if sg > 0 else 'SPH_FF_SKIP_R', '').split(','): continue
            z_end = z_end+(0.0 if sg > 0 else 1.8)
            thd = thd+E('SPH_FF_BACK_DEG', '0.0'); yy_ = 2.5+7.0*math.cos(math.radians(thd)); xx_ = sg*7.0*math.sin(math.radians(thd)); zb_ = hairline_z(xx_, yy_)[0]+0.8; r0 = nearest(np.array([xx_, yy_, zb_]))[0]
            ctrl = [r0, r0+np.array([sg*1.4, 0.3, -1.0])]
            for z in np.linspace(zb_-3.0, z_end, 5):
                cx, cy = contour(min(z, 158.0), sg); f_ = (zb_-z)/(zb_-z_end); ctrl.append(np.array([cx+sg*(stand+0.8*f_), cy-0.8-1.6*f_, z]))
            loose += wave_lock(ctrl, int(n_*E('SPH_FACE_MULT', '2.0')*(1.0 if sg > 0 else 0.85)), 0.55*E('SPH_FF_R', '1.0'), 1.0*E('SPH_FF_AMP', '1.0'), 8.0*E('SPH_FF_WL', '1.0'), 1400+j+(0 if sg > 0 else 60), taper=0.6, spread_tip=1.8*E('SPH_FF_SPREAD', '1.5')/1.5)
    # long side / behind-ear locks reaching the shoulders (the reference's front silhouette: wavy strands down both sides)
    for sg in (1, -1):
        for j, (y0, z0, z_end, n_) in enumerate(((0.5, 162.0, 136.0, 90), (-2.0, 160.5, 134.0, 80), (-4.0, 158.5, 138.0, 60))):
            if str(j) in os.environ.get('SPH_SIDE_SKIP_L' if sg > 0 else 'SPH_SIDE_SKIP_R', '').split(','): continue
            SX_ = E('SPH_SIDE_X', '1.0'); ctrl = [np.array([sg*7.3, y0, z0]), np.array([sg*8.8*SX_, y0-0.4, z0-3.0]), np.array([sg*8.9*SX_, y0-0.6, z0-8.0]), np.array([sg*8.1*SX_, y0-0.4, (z0+z_end)/2-4]), np.array([sg*7.6, y0+0.4, z_end])]
            loose += wave_lock(ctrl, int(n_*(1.0 if sg > 0 else 0.8)), 0.5, 1.1, 7.5, 1500+j+(0 if sg > 0 else 40), taper=0.6, spread_tip=2.0)
for sg in (1, -1):                                                       # ear locks: over / behind the ear
    for j, (y0, z0, dz, dx) in enumerate([(1.5, 163.0, 10.0, 1.8), (-1.5, 162.0, 8.0, 1.2), (-3.5, 160.0, 7.0, 0.8)]):
        if str(j) in os.environ.get('SPH_EARLOCK_SKIP', '').split(','): continue
        EX_ = E('SPH_EAR_X', '1.0'); ctrl = [np.array([sg*7.2, y0, z0]), np.array([sg*(8.3+dx)*EX_, y0-0.6, z0-dz*0.4]), np.array([sg*(8.0+dx)*EX_, y0-1.2, z0-dz*0.8]), np.array([sg*(7.4+dx)*EX_, y0-1.5, z0-dz])]
        loose += wave_lock(ctrl, 50, 0.4, 0.6, 8.0, 600+j+(0 if sg > 0 else 30))
NAPE_ = ((-3.9, 3.2, -0.8), (-1.0, 2.2, 0.4), (2.1, 3.8, 0.9), (4.2, 2.6, 1.2), (-2.6, 2.8, -0.4), (0.6, 3.4, 0.2), (3.2, 2.0, 0.7), (-4.8, 2.4, -1.0))[:int(E('SPH_NAPE_N', '4'))]
for j, (xx, dz, dx) in enumerate(NAPE_):   # nape escapes: short, uneven
    z0 = 151.2+2.2*(abs(xx)/6.0)**2; ctrl = [np.array([xx, -5.2, z0+0.8]), np.array([xx+dx*0.5, -6.1, z0-dz*0.5]), np.array([xx+dx, -5.9, z0-dz])]
    loose += wave_lock(ctrl, 16, 0.3, 0.35, 3.5, 700+j)
for k in range(int(E('SPH_FLY_N', '2000'))):                              # sparse crown / part flyaways
    q, n = sample_scalp(1); q, n = q[0], n[0]
    if q[2] < 165.0 and rng.random() < 0.7: continue
    q = q+n*0.5; L = (2.0+4.0*rng.random())*E('SPH_FLY_L', '1.0'); d_ = n+rng.normal(0, 0.9, 3); d_ /= np.linalg.norm(d_); b_ = np.cross(d_, rng.normal(0, 1, 3)); b_ /= np.linalg.norm(b_)
    loose.append(resample(np.asarray([q+d_*L*s_+b_*math.sin(s_*math.pi*1.3)*L*0.3 for s_ in np.linspace(0, 1, 10)]), N_PTS))
log('loose strands', len(loose), 'face locks', len(FACE))
def export(strands, name):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    for s in strands:
        sp = cu.splines.new('POLY'); sp.points.add(len(s)-1)
        for i, (x, y, z) in enumerate(s): sp.points[i].co = (x, -z, y, 1)
    ob = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(ob)
    for o in bpy.context.scene.objects: o.select_set(o == ob)
    fp = os.path.join(OUT, name+'.abc'); bpy.ops.wm.alembic_export(filepath=fp, selected=True, start=1, end=1, curves_as_mesh=False, global_scale=1.0)
    bpy.data.objects.remove(ob, do_unlink=True); log('exported', fp, len(strands))
export(main, 'hair_main'); export(loose, 'hair_loose'); np.savez_compressed(os.path.join(OUT, 'strands.npz'), main=np.asarray(main, np.float32), loose=np.asarray(loose, np.float32))
stats = {'builder': 'GUARDIAN-8 side/bun/rear architecture', 'primary': len(prim), 'secondary': n_sec, 'tertiary': n_ter, 'main_strands': len(main), 'loose_strands': len(loose), 'locks': K_LOCKS, 'bun_groups': N_GROUPS, 'face_locks': len(FACE), 'points_per_strand': N_PTS, 'bun_centre': C_BUN.tolist(), 'seed': SEED}
open(os.path.join(OUT, 'hair_build.json'), 'w').write(json.dumps(stats, indent=1)); log('HAIR_OK', json.dumps(stats))
