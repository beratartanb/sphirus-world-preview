"""GD11 refinement I copy (of H; +SPH_UNDER_EAR, SPH_NAPE_REPLACE nape_lock / nape_fine) (of G) (+SPH_NAPE_FIX/NAPE_CONV/NAPE_LOOP, SPH_NAPE_G, SPH_FSF) (+ per-strand tags, editable guides.json export / SPH_GUIDES_IN import) of the F copy (+SPH_SDEP_ARC, SPH_FILL_EDGE, SPH_TEMPLE_VEIL) of the E copy (SPH_FLOW_E: arc lift profile, early root ramp, end taper, distributed bun entry, behind-ear join/free) of the D copy of blender_g11rc_hair.py: + LF_TOPBACK_CUT, SPH_BUN_AXS, SPH_BEHIND_EAR (behind-ear loose locks).
GD11 head refinement B hair (h33+: front-root exit angle / gradual rise, clustered edge hairs along the flow; copy of blender_g11r_hair.py).
GD11 head refinement hair (h30 = h23 builder + per-side face-lock / temple-lock controls; copy of blender_gd8_hair.py).
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
import faulthandler as _fh
if os.environ.get('SPH_DEBUG_TB'): _fh.dump_traceback_later(int(os.environ['SPH_DEBUG_TB']), repeat=True, file=sys.stderr)
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
# ---- refinement G: editable guide export / import + per-strand tags ------------------------------------------------------------
GUIDES_OUT = {}; GUIDES_IN = json.load(open(os.environ['SPH_GUIDES_IN'])) if os.environ.get('SPH_GUIDES_IN') else {}
GUIDES_BASE = json.load(open(os.environ['SPH_GUIDES_BASE'])) if os.environ.get('SPH_GUIDES_BASE') else {}
GUIDES_IN2 = json.load(open(os.environ['SPH_GUIDES_IN2'])) if os.environ.get('SPH_GUIDES_IN2') else {}   # I: second edit layer (edits relative to BASE2 = the guides of the build the .blend came from)
GUIDES_BASE2 = json.load(open(os.environ['SPH_GUIDES_BASE2'])) if os.environ.get('SPH_GUIDES_BASE2') else {}
MAIN_TAG = []; LOOSE_TAG = []; GUIDES_EDITED = []
FAMILY = ((400, 460, 'face_frame'), (800, 830, 'face_frame_short'), (1200, 1260, 'temple_lock'), (1300, 1310, 'fringe'), (1400, 1470, 'ff_wave'), (1500, 1550, 'side_long'),
          (600, 640, 'ear_lock'), (700, 710, 'nape_free'), (1700, 1760, 'behind_ear'), (1900, 1950, 'temple_veil'), (2100, 2200, 'front_side_frame'), (2300, 2400, 'nape_free_g'), (2500, 2600, 'under_ear'))
def family_of(seed):
    for a_, b_, n_ in FAMILY:
        if a_ <= seed < b_: return n_
    return 'loose_other'
def guide_ctrl(key, group, ctrl, **meta):
    """record a guide; if the guides file overrides this key, use its control points (only that group changes, all RNG draws stay identical)"""
    if key in GUIDES_IN and 'ctrl' in GUIDES_IN[key]:
        new_ = [np.asarray(p, float) for p in GUIDES_IN[key]['ctrl']]
        ref_ = [np.asarray(p, float) for p in GUIDES_BASE[key]['ctrl']] if (key in GUIDES_BASE and 'ctrl' in GUIDES_BASE[key]) else ctrl   # H: compare with the guide the .blend was EXPORTED from
        same_ = len(new_) == len(ref_) and max(float(np.abs(np.asarray(q)-np.asarray(c)).max()) for q, c in zip(new_, ref_)) < E('SPH_GUIDE_TOL', '0.001')
        if not same_: ctrl = new_; GUIDES_EDITED.append(key)   # H: unedited guides (round-trip float noise < tol) keep the exact computed values
    if key in GUIDES_IN2 and 'ctrl' in GUIDES_IN2[key] and key in GUIDES_BASE2 and 'ctrl' in GUIDES_BASE2[key]:
        n2_ = [np.asarray(p, float) for p in GUIDES_IN2[key]['ctrl']]; b2_ = [np.asarray(p, float) for p in GUIDES_BASE2[key]['ctrl']]
        if not (len(n2_) == len(b2_) and max(float(np.abs(q-c).max()) for q, c in zip(n2_, b2_)) < E('SPH_GUIDE_TOL', '0.001')): ctrl = n2_; GUIDES_EDITED.append(key+'@2')
    GUIDES_OUT[key] = {'group': group, 'ctrl': [[round(float(v), 4) for v in p] for p in ctrl], **meta}; return ctrl
def prim_group(r):
    x, y, z = r
    if y < -2.0 and z < 157.5: return 'nape_to_bun'
    if y < -2.0: return 'back_to_bun'
    if abs(x) > 4.6 and y < 3.5: return 'side_to_bun'
    if y > 3.0: return 'front_to_bun'
    return 'top_to_bun'
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
if E('SPH_NAPE_EDGE', '0') > 0:   # F: soft nape hairline -> density ramps up over SPH_NAPE_EDGE_W cm above the nape hairline curve (no straight 'cut' edge from behind)
    _zn = 151.2+2.2*(np.abs(S_C[:, 0])/6.0)**2+0.35*np.sin(S_C[:, 0]*2.3+0.7)+0.2*np.sin(S_C[:, 0]*5.1)
    _bkn = sstep((-S_C[:, 1]-0.5)/2.0); S_W = S_W*(1-_bkn*(1-(E('SPH_NAPE_EDGE', '0.3')+(1-E('SPH_NAPE_EDGE', '0.3'))*sstep((S_C[:, 2]-_zn)/E('SPH_NAPE_EDGE_W', '1.3')))))
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
for _g in range(N_GROUPS):   # G: editable bun loop groups (centre offset G_C, radius G_R, turns G_TURN)
    _k = f'bun:{_g}'
    if _k in GUIDES_IN:   # H: tolerance as for curves (round-trip noise does not count as an edit)
        BB_ = GUIDES_BASE.get(_k, {'c_off': list(G_C[_g]), 'r': float(G_R[_g]), 'turn': float(G_TURN[_g])})
        if 'c_off' in GUIDES_IN[_k] and np.abs(np.asarray(GUIDES_IN[_k]['c_off'], float)-np.asarray(BB_['c_off'], float)).max() > 1e-3: G_C[_g] = np.asarray(GUIDES_IN[_k]['c_off'], float); GUIDES_EDITED.append(_k+':c_off')
        if 'r' in GUIDES_IN[_k] and abs(float(GUIDES_IN[_k]['r'])-float(BB_['r'])) > 1e-3: G_R[_g] = float(GUIDES_IN[_k]['r']); GUIDES_EDITED.append(_k+':r')
        if 'turn' in GUIDES_IN[_k] and abs(float(GUIDES_IN[_k]['turn'])-float(BB_['turn'])) > 1e-3: G_TURN[_g] = float(GUIDES_IN[_k]['turn']); GUIDES_EDITED.append(_k+':turn')
    if _k in GUIDES_IN2 and _k in GUIDES_BASE2:   # I: layer-2 bun edits
        B2_ = GUIDES_BASE2[_k]
        if np.abs(np.asarray(GUIDES_IN2[_k]['c_off'], float)-np.asarray(B2_['c_off'], float)).max() > 1e-3: G_C[_g] = np.asarray(GUIDES_IN2[_k]['c_off'], float); GUIDES_EDITED.append(_k+':c_off@2')
        if abs(float(GUIDES_IN2[_k]['r'])-float(B2_['r'])) > 1e-3: G_R[_g] = float(GUIDES_IN2[_k]['r']); GUIDES_EDITED.append(_k+':r@2')
        if abs(float(GUIDES_IN2[_k]['turn'])-float(B2_['turn'])) > 1e-3: G_TURN[_g] = float(GUIDES_IN2[_k]['turn']); GUIDES_EDITED.append(_k+':turn@2')
    _c = C_BUN+G_C[_g]; GUIDES_OUT[_k] = {'group': 'bun_loops', 'c_off': [round(float(v), 4) for v in G_C[_g]], 'r': round(float(G_R[_g]), 4), 'turn': round(float(G_TURN[_g]), 4),
        'ctrl': [[round(float(v), 4) for v in (_c+(U1*math.cos(a_)+U2*math.sin(a_))*G_R[_g])] for a_ in np.linspace(0, 2*np.pi, 13)]}
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
    LP_ = math.acos(max(-1.0, min(1.0, cab)))*0.5*(la+lb)   # E: approximate scalp path length (cm) for a distance-based root ramp
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
            rr_ramp = E('SPH_ROOT_RAMP', '0.14')+E('SPH_ROOT_RAMP_FRONT', '0.0')*front
            if FLOW_E:   # E: field along the path, early root ramp, gradual end taper over the last 40 % (no wall / no last-moment drop)
                h = E('SPH_ROOT_H', '0.15')+lift_field_arc(np.asarray(loc))*E('LF_PATH_GAIN', '1.0')*(sstep(t*LP_/E('SPH_RAMP_CM', '3.0')) if E('SPH_RAMP_CM', '0') > 0 else sstep(t/rr_ramp))*(1-E('SPH_END_TAPER', '0.6')*sstep((t-0.6)/0.4))+0.25*t+bump*math.sin(math.pi*t)**2
            else: h = E('SPH_ROOT_H', '0.15')+lift_field(np.asarray(loc))*E('LF_PATH_GAIN', '1.0')*sstep(t/rr_ramp)*(1-0.7*sstep((t-0.82)/0.18))+0.25*t+bump*math.sin(math.pi*t)**2
        else: h = 0.15+lift*sstep(t/(0.22+0.16*front))*(math.sin(math.pi*min(1.0, t*1.15))**0.5)*(1-0.55*t)+0.35*t+bump*math.sin(math.pi*t)**2
        nb = n+front*(1-sstep(t/0.35))*np.array([0.0, -E('SPH_NB_BACK', '0.3'), E('SPH_NB_UP', '0.9')]); nb /= np.linalg.norm(nb)
        if front > 0 and t < 0.2: q_roll = np.array([0.0, 1.0, 0.35])*front*E('SPH_ROLL', '0.0')*math.sin(math.pi*t/0.2)
        else: q_roll = 0.0
        q = loc+nb*h+q_roll
        if ear_drape > 0: q = q+np.array([0, 0, -ear_drape])*(math.sin(math.pi*min(1.0, t*1.3))**1.4)
        path.append(q)
    path = np.asarray(path)
    if FLOW_E:   # E: approach the bun entry over the last ~35 % of the lock (several control points move together) instead of snapping the last point
        tt_ = np.linspace(0, 1, len(path)); w_ = sstep((tt_-E('SPH_ENTRY_T0', '0.62'))/(1-E('SPH_ENTRY_T0', '0.62'))); path = path+w_[:, None]*(entry-path[-1])[None]
    path[-1] = entry; path = smooth_poly(path, 2 if not FLOW_E else 4)
    tg = np.gradient(path, axis=0); tg /= np.maximum(np.linalg.norm(tg, axis=1), 1e-6)[:, None]; nr = path-HC; nr /= np.linalg.norm(nr, axis=1)[:, None]; bi = np.cross(tg, nr); bi /= np.maximum(np.linalg.norm(bi, axis=1), 1e-6)[:, None]
    arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))]); ph = rr.random()*6.28; env = sstep(arc/5.0)*(1-0.6*sstep((arc-arc[-1]+4)/4))
    path = path+bi*(wave_amp*env*np.sin(2*np.pi*arc/wave_len+ph))[:, None]+nr*(0.15*wave_amp*env*np.sin(2*np.pi*arc/wave_len+1.7*ph))[:, None]
    return path, ang
def bun_loop(gidx, start, n=18, off=np.zeros(2), lock_seed=0, rscale=1.0):
    """continuation of a lock inside its bun loop group: wraps around the bun axis with the group's radius / tilt / tension;
    escaping groups leave the loop with a curling end, the others tuck into the centre"""
    rr = np.random.default_rng(lock_seed); c = C_BUN+G_C[gidx]; TL_ = E('SPH_BUN_TILT_L', '0.0'); ax = AX+U1*(G_TILT[gidx, 0]+rr.normal(0, TL_))+U2*(G_TILT[gidx, 1]+rr.normal(0, TL_)); ax /= np.linalg.norm(ax)   # F: per-lock axis wobble (loops cross, no clean spiral)
    u1 = np.cross(ax, [0, 0, 1.0]); u1 /= np.linalg.norm(u1); u2 = np.cross(ax, u1); d0 = start-c; a0 = math.atan2(float(np.dot(d0, u2)), float(np.dot(d0, u1))); r0 = np.linalg.norm(d0-ax*np.dot(d0, ax))
    TV_ = E('SPH_BUN_TURN_VAR', '0.3'); turns = G_TURN[gidx]*(1-TV_/2+TV_*rr.random()); sgn = 1 if gidx % 2 else -1; pts = []   # F: per-lock turn variation
    for k in range(1, n+1):
        u = k/n; a_ = a0+sgn*2*np.pi*turns*u; R = (r0+(G_R[gidx]-r0)*sstep(u/0.25))*(1.0-(1.0-rscale)*sstep(u/0.4))   # G: rscale < 1 tucks the loop into the bun core
        if G_ESC[gidx] and u > 0.7: R = R+(u-0.7)/0.3*(1.4+1.2*rr.random())*E('SPH_BUN_ESC_R', '1.0')   # refinement D: escaping-end flare scale
        elif u > 0.75: R = R*(1-0.55*(u-0.75)/0.25)
        R = R+off[0]; axo = (G_AX[gidx]*0.6+(-0.5+1.1*u))*E('SPH_BUN_AXS', '1.0')+off[1]   # refinement D: SPH_BUN_AXS scales the loops' spread along the bun axis (= backwards)
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
FLOW_E = E('SPH_FLOW_E', '0') > 0
ARC_K = [float(v) for v in os.environ.get('SPH_ARC_KNOTS', '78,1.5,58,2.45,32,2.85,6,2.85,-20,2.45,-45,1.65,-70,0.95,-100,0.5').split(',')]
ARC_T, ARC_L = np.array(ARC_K[0::2])[::-1], np.array(ARC_K[1::2])[::-1]
def lift_field_arc(r):
    """refinement E: stand-off as ONE smooth profile of the angle around the head centre in the side view (0 = vertex, + = front, - = back):
    hairline -> front-top -> crown -> back -> bun level, so the front rises early and the crown is not a separate dome; sides attenuated as before"""
    x, y, z = r; ax = abs(x-PART_X); th = math.degrees(math.atan2(y-HC[1], z-HC[2]))
    L = float(np.interp(th, ARC_T, ARC_L))
    side = sstep((abs(x)-4.4)/1.2)*(1-sstep((z-168.5)/2.0)); nape = 1-sstep((z-156.5)/2.5)
    L = L-E('LF_SIDE', '0.35')*side*(L/2.5)-0.3*nape
    L *= 1.0+E('SPH_PART_VAR', '0.0')*(1 if x > PART_X else -1)*sstep((y-0.0)/4.0)
    if E('SPH_ARC_PARTDIP', '0') > 0 and y > -1.0: L *= 1.0-E('SPH_ARC_PARTDIP', '0')*(1-sstep((ax-0.15)/1.8))   # E: lower lift right at the part so both sides lean in (no dark V)   # mild difference on the two sides of the part (front half only)
    return max(E('SPH_ARC_FLOOR', '0.25'), L)   # F: floor configurable (nape strands may lie closer than 0.25 cm)
def lift_field(r):
    """stand-off (cm) by position: hairline rise -> crown -> rear-upper roll -> nape; sides kept low; lower right at the part edge"""
    x, y, z = r; ax = abs(x-PART_X)
    top = sstep((z-164.5)/3.5); back = sstep((-y-0.5)/3.5)*sstep((z-157.5)/3.0); front = sstep((y-2.5)/3.0)*sstep((z-163.0)/2.0)
    side = sstep((abs(x)-4.4)/1.2)*(1-sstep((z-168.5)/2.0)); nape = 1-sstep((z-156.5)/2.5)
    top = top*(1-E('LF_TOPFRONT_CUT', '0.0')*sstep((y-2.5)/4.5))
    top = top*(1-E('LF_TOPBACK_CUT', '0.0')*sstep((-y-1.0)/4.0))      # refinement D: crown lift reduced only on the BACK half (front / top volume unchanged)
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
    cl = np.asarray(guide_ctrl(f'prim:{p}', prim_group(r), list(cl), root=[round(float(v), 4) for v in r], bun_group=int(gidx), n_roots=int(len(idx))), float)   # G: editable lock centreline
    if GUIDES_IN.get(f'prim:{p}', {}).get('ctrl') and len(cl) != 29: cl = resample(cl, 29)
    if f'prim:{p}' in GUIDES_IN and 'shift' in GUIDES_IN[f'prim:{p}']:   # optional rigid offset of the tail (bun entry) part: [dx, dy, dz] * sstep over the last 40 %
        sh = np.asarray(GUIDES_IN[f'prim:{p}']['shift'], float); tt_ = np.linspace(0, 1, len(cl)); cl = cl+sstep((tt_-0.6)/0.4)[:, None]*sh[None]
    prim[p] = (cl, gidx, idx)
main = []; n_sec = 0; n_ter = 0
for p, (pcl, gidx, idx) in prim.items():
    ptag_ = prim_group(nearest(roots[idx].mean(0))[0])+f':p{p}'
    NF_ = E('SPH_NAPE_CONV', '1.0') if (ptag_.startswith('nape_to_bun') and E('SPH_NAPE_FIX', '0') > 0) else 1.0; NCL_ = 0.0 if NF_ != 1.0 else 1.0   # G: nape locks fan out (low convergence, no back clumping)
    k2 = max(2, int(round(K2*len(idx)/len(roots)))); lab2 = kmeans(roots[idx], k2)
    for s_ in range(k2):
        sidx = idx[lab2 == s_]
        if len(sidx) == 0: continue
        n_sec += 1; sr = nearest(roots[sidx].mean(0))[0]; sg_ = n_sec*13+7; rs = np.random.default_rng(sg_)
        LFA_ = lift_field_arc if (FLOW_E and E('SPH_SDEP_ARC', '0') > 0) else lift_field   # F: secondary depth from the same (active) lift profile as the lock path
        sdep = ((LFA_(sr)-LFA_(nearest(roots[idx].mean(0))[0]))*0.55+rs.normal(0, E('SPH_SEC_DS', '0.05'))*(1+E('SPH_BACK_VAR', '0.0')*sstep((-sr[1]-1.0)/3.0))) if E('SPH_FIELD', '0') > 0 else rs.normal(E('SPH_SEC_D', '0.12'), E('SPH_SEC_DS', '0.22'))
        scl = child_path(pcl, sr, (0.35+0.25*rs.random())*E('SPH_SEC_CONV', '1.0')*NF_, 0.45, sdep, (0.25+0.3*rs.random())*E('SPH_WAVE2', '1.0'), 5.0+3.0*rs.random(), rs.random()*6.28)
        loop_off = np.array([rs.normal(0, 0.5), rs.normal(0, 0.5)]); g2 = gidx if rs.random() > 0.25 else int(rs.integers(N_GROUPS))
        k3 = max(1, int(round(K3*len(sidx)/len(roots)))); lab3 = kmeans(roots[sidx], k3, 6)
        for t_ in range(k3):
            tidx = sidx[lab3 == t_]
            if len(tidx) == 0: continue
            n_ter += 1; tr = nearest(roots[tidx].mean(0))[0]; rt = np.random.default_rng(n_ter*29+5)
            bk_ = sstep((-tr[1]-1.5)/3.0)*NCL_; tcl = child_path(scl, tr, min(0.95, (0.55+0.25*rt.random())*E('SPH_TER_CONV', '1.0')*NF_*(1+E('SPH_BACK_CLUMP', '0.0')*bk_)), 0.35, rt.normal(0.0, 0.08), 0.10+0.12*rt.random(), 3.0+2.0*rt.random(), rt.random()*6.28, twist=rt.normal(0, 0.25))
            for i in tidx:
                rr_ = np.random.default_rng(int(i)+17); conv = min(0.98, E('SPH_CONV', '0.7')+E('SPH_CONV_R', '0.25')*rr_.random()) if rr_.random() > 0.05 else 0.2*rr_.random()
                bks_ = sstep((-roots[i][1]-1.5)/3.0)*NCL_; conv = min(0.97, conv*NF_*(1+E('SPH_BACK_CLUMP', '0.0')*0.6*bks_)); pts = child_path(tcl, roots[i], conv, 0.3, 0.0, 0.03, 2.5, rr_.random()*6.28)
                if E('SPH_FILL', '0') > 0:   # persistent lateral fill: strands drift sideways along the length so groups overlap (no empty channels)
                    tg_, nr_, bi_ = frame(pts); sfill = np.linspace(0, 1, len(pts)); fl_ = E('SPH_FILL', '0')*(1-E('SPH_BACK_FILLCUT', '0.0')*bks_); pts = pts+bi_*(rr_.normal(0, fl_)*sstep(sfill/0.35))[:, None]+nr_*(rr_.normal(0, fl_*0.35)*sstep(sfill/0.35))[:, None]
                s = np.linspace(0, 1, len(pts)); fz = (0.04+0.06*rr_.random())*E('SPH_FRIZZ', '1.0') if rr_.random() > 0.05 else 0.25+0.3*rr_.random()
                pts = pts+np.asarray([vnoise3(q, 1.6, int(n_ter*7+3))*fz*(0.3+st) for q, st in zip(pts, s)])
                lp = bun_loop(g2, pts[-1], 16, off=loop_off+rr_.normal(0, E('SPH_BUN_JIT', '0.12'), 2), lock_seed=n_sec if E('SPH_BUN_PERLOCK', '1') > 0 else int(i) % 997, rscale=(E('SPH_NAPE_LOOP', '1.0') if NF_ != 1.0 else 1.0))
                full = resample(np.vstack([pts, lp]), N_PTS)
                for m in range(len(full)): full[m] = push_out(full[m], 0.08 if m < 2 else 0.18)
                if NF_ != 1.0 and E('SPH_NAPE_FLAT', '0') > 0:   # G: nape hair lies on the scalp below the bun (thin swept-up layer, no hanging slab); released toward the bun entry
                    dmax_ = E('SPH_NAPE_FLAT', '0.25')+0.1*rr_.random(); zl_ = C_BUN[2]-E('SPH_BUN_R', '2.35')
                    for m in range(len(full)):
                        wz_ = 1.0-sstep((full[m][2]-(zl_-1.6))/1.6)
                        if wz_ <= 0: continue
                        loc_, n_ = nearest(full[m]); d_ = float(np.dot(full[m]-loc_, n_))
                        if d_ > dmax_: full[m] = full[m]-n_*(d_-dmax_)*wz_
                main.append(full); MAIN_TAG.append(ptag_)
    log('primary', p, 'strands', len(main), round(time.time()-t0, 1))
log('hierarchy', 'primary', len(prim), 'secondary', n_sec, 'tertiary', n_ter)
N_LOCK_STRANDS = len(main)
if FLOW_E and E('SPH_FRONT_FILL', '0') > 0:
    # E front fill: lock strands are pushed outward (radially from the head centre in the side plane + a little lateral) by
    #   F(theta) * sstep(arc_from_own_root / SPH_FILL_RAMP)  ->  0 at every root (roots stay on the scalp), full after ~ramp cm
    # F is non-zero only in the band behind the frontal hairline (theta 12..55 deg), so the crown / back / bun are untouched.
    FK = [float(v) for v in os.environ.get('SPH_FILL_KNOTS', '12,0,22,0.35,32,0.75,40,1.0,48,0.7,56,0').split(',')]; FT, FV = np.array(FK[0::2]), np.array(FK[1::2])*E('SPH_FRONT_FILL', '1.0')
    C3 = np.array([0.0, 1.5, 161.0]); RAMP = E('SPH_FILL_RAMP', '2.2'); nfill = 0
    for i in range(N_LOCK_STRANDS):
        st = np.asarray(main[i], float); th = np.degrees(np.arctan2(st[:, 1]-C3[1], st[:, 2]-C3[2])); F = np.interp(th, FT, FV, left=0.0, right=0.0)
        if F.max() <= 0: continue
        arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(st, axis=0), axis=1))]); w = F*sstep(arc/RAMP)
        if E('SPH_FILL_EDGE', '0') > 0:   # F: strands rooted right at the hairline get less fill -> they lie lower and blend the edge (coverage kept)
            hz_ = hairline_z(st[0, 0], st[0, 1])[0]
            if hz_ is not None: dl_ = st[0, 2]-hz_; w = w*(E('SPH_FILL_EDGE', '0.4')+(1-E('SPH_FILL_EDGE', '0.4'))*sstep(dl_/E('SPH_FILL_EDGE_W', '1.5')))
        d = st-C3; d[:, 0] *= E('SPH_FILL_LAT', '0.35');   # 0 = no lateral push (keeps the part closed)
        d /= np.maximum(np.linalg.norm(d, axis=1), 1e-6)[:, None]
        main[i] = st+d*w[:, None]; nfill += 1
    log('front fill strands', nfill)
NPC = int(E('SPH_PART_COVER', '0')); npc_ = 0
while npc_ < NPC:
    q, n = sample_scalp(1); q, n = q[0], n[0]
    if not (abs(q[0]-PART_X) < 1.1 and q[1] > -2.5 and q[2] > 164.5): continue
    sd = -1.0 if q[0] > PART_X else 1.0; dv = np.array([sd*(0.5+0.6*rng.random()), -0.6-0.6*rng.random(), 0.0]); dv -= n*np.dot(dv, n); dv /= np.linalg.norm(dv)
    Lc = 1.6+1.8*rng.random(); La_ = lift_field_arc(q)*E('SPH_PC_LIFT', '0.0') if FLOW_E else 0.0; pts = [push_out(q+dv*Lc*s_+n*(0.05+0.18*s_+La_*sstep(s_/0.7)), 0.05) for s_ in np.linspace(0, 1, 8)]; main.append(resample(np.asarray(pts), N_PTS)); npc_ += 1   # F: part-cover hairs rise with the lifted sides (bridge, not a flat layer)
NBABY = int(E('SPH_BABY', '0')); nb_ = 0; CL_N = int(E('SPH_BABY_CLUSTER', '0'))
while nb_ < NBABY:
    q, n = sample_scalp(1); q, n = q[0], n[0]
    if HL15:                                                                                   # v15: band just above the authored hairline
        zb_, _, th_ = hairline_z(q[0], q[1])
        if zb_ is None or th_ > 100 or not (q[2] < zb_+E('SPH_BABY_BAND', '1.0')): continue
    elif not (q[1] > 3.0 and q[2] < 168.5-2.6*(abs(q[0])/7.0)**2): continue                    # front hairline band only
    back = np.array([0.0, -1.0, 0.55])+np.array([np.sign(q[0]-PART_X)*0.35, 0.0, 0.0]); back -= n*np.dot(back, n); back /= np.linalg.norm(back)
    if CL_N > 0:     # a small cluster sharing one flow direction (natural hairline growth), lengths / spread vary inside it
        k_ = int(rng.integers(max(2, CL_N//2), CL_N+1)); side_ = np.cross(n, back); side_ /= np.linalg.norm(side_)
        for _c in range(k_):
            qq = q+side_*rng.normal(0, 0.12)+back*rng.normal(0, 0.06); qq, nn = nearest(qq); nn = np.asarray(nn)
            d_ = back+side_*rng.normal(0, 0.12); d_ -= nn*np.dot(d_, nn); d_ /= np.linalg.norm(d_)
            L = E('SPH_BABY_LMIN', '1.8')+(E('SPH_BABY_LMAX', '4.0')-E('SPH_BABY_LMIN', '1.8'))*rng.random(); ph = rng.random()*6.28
            pts = [qq+d_*L*s_+nn*(0.03+E('SPH_BABY_LIFT', '0.22')*s_)+side_*E('SPH_BABY_WOB', '0.25')*math.sin(ph+4.0*s_)*s_ for s_ in np.linspace(0, 1, 10)]
            pts = [push_out(p_, 0.05) for p_ in pts]; main.append(resample(np.asarray(pts), N_PTS)); nb_ += 1
        continue
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
    fam_ = family_of(seed); ctrl = guide_ctrl(f'{fam_}:{seed}', fam_, ctrl, n_str=int(n_str), lock_r=float(lock_r), amp=float(amp), wl=float(wl))
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
    LOOSE_TAG.extend([f'{fam_}:{seed}']*len(out))
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
if E('SPH_BEHIND_EAR', '0') > 0:   # refinement D: loose, slightly hanging locks just BEHIND the ear that rejoin the nape / bun flow
    # (y0, z0, drop, out, back, n): root behind the ear on the scalp, bulge out (depth from the ear), hang, then turn back/in toward the nape
    BE = {1: [(-2.9, 162.2, 7.5, 0.95, 2.6, 60), (-4.1, 160.6, 5.8, 0.75, 2.0, 42), (-3.4, 163.4, 9.2, 0.85, 3.0, 34)],
          -1: [(-3.1, 161.8, 6.6, 0.85, 2.3, 52), (-4.4, 160.2, 8.4, 0.70, 2.6, 38)]}
    for sg in (1, -1):
        for j, (y0, z0, drop, out, bk, n_) in enumerate(BE[sg]):
            r0 = nearest(np.array([sg*7.0, y0, z0]))[0]; xs = abs(r0[0]); out = out*E('SPH_BE_OUT', '1.0')
            free = FLOW_E and str(j) in os.environ.get('SPH_BE_FREE_'+('L' if sg > 0 else 'R'), '').split(',')
            if not FLOW_E: ctrl = [r0, np.array([sg*(xs+0.35), y0-0.4, z0-0.8]), np.array([sg*(xs+out), y0-0.9, z0-drop*0.45]), np.array([sg*(xs+out*0.8), y0-bk*0.6, z0-drop*0.85]),
                    np.array([sg*(xs+out*0.2), y0-bk, z0-drop])]
            elif free:   # free: leaves behind the ear, eases outward, then simply falls (slightly back), tip below the earlobe
                ctrl = [r0, np.array([sg*(xs+0.3), y0-0.5, z0-0.9]), np.array([sg*(xs+out), y0-1.0, z0-drop*0.4]), np.array([sg*(xs+out*0.9), y0-1.4, z0-drop*0.8]), np.array([sg*(xs+out*0.75), y0-1.6, z0-drop*1.25])]
            else:        # join: leaves behind the ear with a little slack, then curves back and up into the nape / bun flow (no U-hook)
                tgt = np.array([sg*2.6, C_BUN[1]+1.2, C_BUN[2]-2.2])
                ctrl = [r0, np.array([sg*(xs+0.3), y0-0.6, z0-0.9]), np.array([sg*(xs+out*0.9), y0-1.4, z0-drop*0.45]), np.array([sg*(xs+out*0.5)*0.75+0.25*tgt[0], 0.55*(y0-2.6)+0.45*tgt[1], z0-drop*0.6]), tgt]
            ctrl = [np.array([p[0], min(p[1], -2.7), p[2]]) for p in ctrl]                       # never in front of y = -2.7 (keeps clear of the ear)
            loose += wave_lock(ctrl, int(n_*E('SPH_BEHIND_EAR', '1.0')), 0.42, 0.55, 7.0, 1700+j+(0 if sg > 0 else 50), taper=0.55, spread_tip=1.3)
if E('SPH_TEMPLE_VEIL', '0') > 0:   # F: loose temple / upper-ear locks from the side hairline: over the temple, above (or just outside) the ear, back into the side mass
    TV = {1: [(54, 0.0, 0.55, 95, 0.0), (66, -0.4, 0.70, 120, 0.0)],                       # character left: 2 locks
          -1: [(50, 0.3, 0.50, 80, 0.0), (60, -0.2, 0.65, 110, 0.0), (71, -0.6, 0.75, 100, 1.0)]}   # character right: 3, the last drapes over the upper ear rim
    for sg in (1, -1):
        for j, (thd, dz, lr_, n_, over_ear) in enumerate(TV[sg]):
            yy_ = 2.5+7.0*math.cos(math.radians(thd)); xx_ = sg*7.0*math.sin(math.radians(thd)); zb_ = hairline_z(xx_, yy_)[0]
            if zb_ is None: continue
            r0 = nearest(np.array([xx_, yy_, zb_+0.6]))[0]; ax_ = abs(r0[0])
            ztop = 164.8+dz if not over_ear else 163.7
            xo = 9.55 if not over_ear else 9.9                                              # ear outer |x| ~ 8.7 (build head)
            ctrl = [r0, r0+np.array([sg*0.35, -0.7, -0.5]), np.array([sg*(ax_+0.75), 3.6, E('SPH_VEIL_Z', '164.6')+dz*0.5]), np.array([sg*xo, 0.6, ztop]), np.array([sg*(xo-0.9), -2.8, ztop-0.9]),
                    np.array([sg*5.2, C_BUN[1]+1.6, C_BUN[2]+0.3])]
            loose += wave_lock(ctrl, int(n_*E('SPH_TEMPLE_VEIL', '1.0')), lr_, 0.5, 7.0, 1900+j+(0 if sg > 0 else 40), taper=0.5, spread_tip=1.2)
if E('SPH_NAPE_G', '0') > 0:   # G: irregular free nape groups (uneven spacing / length / width; a couple curve sideways) instead of the even 'comb' row
    NG = [(-4.6, 1.4, -0.6, 22, 0.20), (-2.3, 3.6, 0.2, 30, 0.30), (-0.4, 2.1, 0.5, 14, 0.15), (1.6, 4.3, 1.1, 34, 0.32), (3.9, 2.6, 0.7, 18, 0.22), (5.1, 1.6, 1.0, 12, 0.15)]
    for j, (xx, ln, dx, n_, lr_) in enumerate(NG):
        z0 = 151.2+2.2*(abs(xx)/6.0)**2+0.35*math.sin(xx*2.3+0.7)+0.4; r0 = nearest(np.array([xx, -5.4, z0]))[0]
        ctrl = [r0, r0+np.array([dx*0.25, -0.35, -ln*0.3]), r0+np.array([dx*0.7, -0.45, -ln*0.7]), r0+np.array([dx, -0.35, -ln])]
        loose += wave_lock(ctrl, n_, lr_, 0.35, 3.5+ln, 2300+j, taper=0.5, spread_tip=1.2)
if E('SPH_FSF', '0') > 0:   # G: front-side frame families: several roots along the front-side hairline, short / medium / long, thin to medium, asymmetric
    FS = {1: [(38, 162.4, 0.35, 0.9, 0.22, 40), (47, 158.0, 0.45, 1.3, 0.30, 55), (55, 153.5, 0.5, 1.6, 0.38, 70), (63, 160.2, 0.4, 1.1, 0.26, 45), (72, 156.2, 0.55, 1.4, 0.33, 50), (80, 161.0, 0.6, 1.0, 0.20, 30)],
          -1: [(41, 160.8, 0.35, 1.0, 0.24, 45), (52, 155.0, 0.45, 1.5, 0.36, 65), (61, 162.0, 0.4, 0.9, 0.20, 35), (70, 151.5, 0.55, 1.8, 0.30, 55), (78, 158.6, 0.6, 1.2, 0.25, 40)]}
    if os.environ.get('SPH_FSF_TABLE'): FS.update({int(k): [tuple(r) for r in v] for k, v in json.loads(os.environ['SPH_FSF_TABLE']).items()})   # H: per-side front-side family table override
    for sg in (1, -1):
        for j, (thd, z_end, s0, s1, lr_, n_) in enumerate(FS[sg]):
            yy_ = 2.5+7.0*math.cos(math.radians(thd)); xx_ = sg*7.0*math.sin(math.radians(thd)); zb_ = hairline_z(xx_, yy_)[0]
            if zb_ is None: continue
            r0 = nearest(np.array([xx_, yy_, zb_+0.5]))[0]; ctrl = [r0, r0+np.array([sg*0.3, 0.1, -0.6])]
            for z in np.linspace(zb_-1.6, z_end, 4):
                cx, cy = contour(min(z, 163.5), sg); f_ = (zb_-z)/max(zb_-z_end, 0.1); ctrl.append(np.array([cx+sg*(s0+(s1-s0)*f_), cy-0.3-0.9*f_, z]))
            loose += wave_lock(ctrl, int(n_*E('SPH_FSF', '1.0')), lr_, 0.25+0.35*((j*7) % 5)/4, 5.0+1.2*((j*3) % 4), 2100+j+(0 if sg > 0 else 50), taper=0.55, spread_tip=1.3)
if E('SPH_UNDER_EAR', '0') > 0:   # I: under-ear frame - free locks from behind / over the ear that fall past the lobe beside the jaw and upper neck (visible from the front)
    # (kind, root theta, z_end, out, n, lock_r, amp): kind 'b' = behind the ear, 'o' = over the ear rim then behind the lobe; ends lateral of the neck (|x| 6.3-7.8)
    UE = {1: [('b', 108, 153.0, 0.0, 90, 0.42, 0.55), ('o', 90, 156.2, 0.2, 70, 0.36, 0.45), ('b', 118, 150.8, -0.3, 75, 0.38, 0.6)],
          -1: [('b', 110, 152.2, 0.1, 90, 0.44, 0.5), ('o', 88, 155.4, 0.3, 75, 0.38, 0.5), ('b', 102, 156.8, 0.2, 55, 0.30, 0.4), ('b', 121, 151.0, -0.2, 70, 0.36, 0.6)]}
    if os.environ.get('SPH_UNDER_EAR_TABLE'): UE.update({int(k): [tuple(r) for r in v] for k, v in json.loads(os.environ['SPH_UNDER_EAR_TABLE']).items()})
    for sg in (1, -1):
        for j, (kind, thd, z_end, out, n_, lr_, amp_) in enumerate(UE[sg]):
            yy_ = 2.5+7.0*math.cos(math.radians(thd)); xx_ = sg*7.0*math.sin(math.radians(thd)); zb_ = hairline_z(xx_, yy_)[0] or 161.0
            r0 = nearest(np.array([xx_, yy_, zb_+0.6]))[0]
            if kind == 'o': ctrl = [r0, np.array([sg*(abs(r0[0])+0.6), r0[1]-0.4, r0[2]-0.3]), np.array([sg*9.3, 1.4, 161.6]), np.array([sg*9.3, -0.3, 158.8]), np.array([sg*(8.2+out), 0.6, (158.0+z_end)/2]), np.array([sg*(7.4+out), 0.9, z_end])]
            else: ctrl = [r0, np.array([sg*(abs(r0[0])+0.5), r0[1]+0.1, r0[2]-0.9]), np.array([sg*(8.5+out), -0.4, 158.6]), np.array([sg*(8.1+out), 0.4, (158.0+z_end)/2+0.3]), np.array([sg*(7.2+out), 0.7, z_end])]
            loose += wave_lock(ctrl, int(n_*E('SPH_UNDER_EAR', '1.0')), lr_, amp_, 7.0, 2500+j+(0 if sg > 0 else 50), taper=0.55, spread_tip=1.3)
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
if E('SPH_CORNER', '0') > 0:   # H: behind-ear -> nape CORNER family: roots in the band between a softened back hairline and the old one,
    # strands sweep diagonally up/back along the scalp into the lower-lateral side of the bun (fills the L corner; existing strands unchanged)
    MAIN_TAG += ['partcover_or_baby']*(len(main)-len(MAIN_TAG))
    crng = np.random.default_rng(int(E('SPH_CORNER_SEED', '777'))); NCO = int(E('SPH_CORNER_N', '2600'))
    TB = [float(v) for v in os.environ.get('SPH_CORNER_HL', '112,161.0,122,159.2,132,157.4,142,155.6,152,153.4').split(',')]; TBt, TBz = np.array(TB[0::2]), np.array(TB[1::2])
    def zold(th): return float(np.interp(th, _TH, _ZH)) if th <= 150 else 153.5
    for sg in (1, -1):
        # editable side guides: start (behind the ear, low) -> mid (on the scalp, diagonal) -> bun lower-lateral entry
        GU = []
        for gi, (th0, dz, ex, ez) in enumerate(((114, 0.4, 2.4, -1.0), (124, 0.3, 2.0, -1.6), (134, 0.2, 1.5, -2.0), (144, 0.2, 1.0, -2.2))):
            zr = float(np.interp(th0, TBt, TBz))+dz; rr0 = nearest(np.array([sg*7.0*math.sin(math.radians(th0)), 2.5+7.0*math.cos(math.radians(th0)), zr]))[0]
            ent = C_BUN+np.array([sg*ex, 1.3, ez]); mid = nearest(0.5*(rr0+ent)+np.array([0, 0.6, 0.4]))[0]
            ctrl = guide_ctrl(f'corner_to_bun:{sg}:{gi}', 'corner_to_bun', [rr0, mid, ent]); GU.append(np.asarray(ctrl, float))
        n_side = NCO//2; k_ = 0; tries = 0
        while k_ < n_side and tries < n_side*30:
            tries += 1; th = crng.uniform(TBt[0], TBt[-1]); zl_ = float(np.interp(th, TBt, TBz)); z = zl_+(zold(th)+0.8-zl_)*crng.random()**E('SPH_CORNER_BIAS', '1.0')   # bias < 1: roots denser toward the old (upper) hairline
            q, nq = nearest(np.array([sg*7.0*math.sin(math.radians(th)), 2.5+7.0*math.cos(math.radians(th)), z]))
            if q[1] > 1.0: continue
            gw = np.array([1.0/(0.3+abs(th-(114+10*gi))) for gi in range(4)]); gw /= gw.sum(); A_ = sum(w*g for w, g in zip(gw, GU))   # blended guide
            off = q-A_[0]; tt = np.linspace(0, 1, 12)
            pa = [(1-t_)**2*A_[0]+2*(1-t_)*t_*A_[1]+t_**2*A_[2] for t_ in tt]; conv = E('SPH_CORNER_CONV', '0.45')*(0.7+0.6*crng.random())
            pts = []
            for t_, pp in zip(tt, pa):
                pp = pp+off*(1-conv*sstep(t_/0.8)); loc_, n_ = nearest(pp); h_ = 0.08+E('SPH_CORNER_LIFT', '0.35')*sstep(t_/0.5)*(1-0.4*t_)
                pts.append(loc_+n_*h_+crng.normal(0, 0.03, 3))
            gidx = int(np.argmin(np.linalg.norm((C_BUN+G_C)-pts[-1], axis=1)))
            lp = bun_loop(gidx, pts[-1], 10, off=crng.normal(0, 0.2, 2), lock_seed=5000+k_ % 40, rscale=E('SPH_CORNER_LOOP', '0.45'))
            full = resample(np.vstack([np.asarray(pts), lp]), N_PTS)
            for m in range(len(full)): full[m] = push_out(full[m], 0.06 if m < 2 else 0.14)
            main.append(full); MAIN_TAG.append(f'corner_to_bun:s{sg}'); k_ += 1
    log('corner strands', len([t_ for t_ in MAIN_TAG if t_.startswith('corner')]))
MAIN_TAG += ['partcover_or_baby']*(len(main)-len(MAIN_TAG))
if E('SPH_NAPE_REPLACE', '0') > 0:   # I: replace the nape sheet (nape_to_bun + corner_to_bun) by distinct swept-up NAPE LOCKS + fine hairline hairs (other strands untouched)
    keep_ = [not (t_.startswith('nape_to_bun') or t_.startswith('corner_to_bun')) for t_ in MAIN_TAG]; nrem_ = len(keep_)-sum(keep_)
    main = [st for st, k in zip(main, keep_) if k]; MAIN_TAG = [t_ for t_, k in zip(MAIN_TAG, keep_) if k]
    nrng = np.random.default_rng(int(E('SPH_NLOCK_SEED', '4242')))
    def zh_back(x, y):   # soft back hairline: nape curve in the middle, softened behind-ear curve laterally (same as the corner band's lower edge)
        th = abs(math.degrees(math.atan2(x, y-2.5)))
        zc = 151.2+2.2*(abs(x)/6.0)**2+0.35*math.sin(x*2.3+0.7); zs = float(np.interp(th, [112, 122, 132, 142, 152], [161.0, 159.2, 157.4, 155.6, 153.4]))
        w = sstep((abs(x)-3.4)/1.6); return (1-w)*zc+w*zs
    # (x_root, dz above hairline, patch radius, n, entry side shift, lift)
    NL = [(-6.6, 0.9, 0.75, 260, -0.6, 0.30), (-5.4, 0.5, 0.85, 340, -0.3, 0.26), (-4.0, 0.7, 0.70, 300, -0.1, 0.22), (-2.7, 0.4, 0.95, 420, 0.0, 0.20), (-1.2, 0.8, 0.80, 380, 0.2, 0.18),
          (0.3, 0.5, 0.90, 430, 0.3, 0.18), (1.8, 0.9, 0.75, 360, 0.5, 0.20), (3.1, 0.4, 0.95, 420, 0.7, 0.22), (4.5, 0.8, 0.70, 290, 0.9, 0.26), (5.7, 0.5, 0.80, 300, 1.1, 0.28), (6.8, 1.0, 0.65, 220, 1.3, 0.30)]
    if os.environ.get('SPH_NLOCK_TABLE'): NL = [tuple(r) for r in json.loads(os.environ['SPH_NLOCK_TABLE'])]
    nl_n = 0
    for j, (xr, dz, pr, n_, esh, lift) in enumerate(NL):
        yr = -5.6+0.62*abs(xr) if abs(xr) < 5.0 else -5.6+0.62*5.0+0.9*(abs(xr)-5.0)
        zr_ = zh_back(xr, yr)+dz
        if E('SPH_NLOCK_SURF', '0') > 0:   # I: root on the real back scalp surface (most-backward head vertex near (x, z)), not a projection from a guessed point
            sel_ = X[(np.abs(X[:, 0]-xr) < 0.45) & (np.abs(X[:, 2]-zr_) < 0.45) & (X[:, 1] < 1.0)]
            r0 = nearest(sel_[np.argmin(sel_[:, 1])] if len(sel_) else np.array([xr, yr, zr_]))[0]
        else: r0 = nearest(np.array([xr, yr, zr_]))[0]
        SP_ = E('SPH_NLOCK_SPREAD', '0.0'); ent = C_BUN+np.array([0.55*xr*0.45*(1+SP_)+esh*0.3, 1.2-0.3*SP_*abs(xr)/6.0, -1.9+0.12*abs(xr)*(1+1.5*SP_)])   # spread > 0: entries fan over the lower half of the bun
        mid = nearest(0.55*r0+0.45*ent+np.array([0, 0.5, 0.2]))[0]
        G_ = np.asarray(guide_ctrl(f'nape_lock:{j}', 'nape_lock', [r0, mid, ent], patch_r=float(pr), n=int(n_)), float)
        conv_ = E('SPH_NLOCK_CONV', '0.72'); gidx = int(np.argmin(np.linalg.norm((C_BUN+G_C)-G_[-1], axis=1)))
        tt = np.linspace(0, 1, 14)
        for k_ in range(int(n_*E('SPH_NLOCK_N', '1.0'))):
            off_ = nrng.normal(0, pr*0.5, 3); off_[1] *= 0.3; q, nq = nearest(G_[0]+off_)
            pa = [(1-t_)**2*G_[0]+2*(1-t_)*t_*G_[1]+t_**2*G_[2] for t_ in tt]; d0 = q-G_[0]; cv = conv_*(0.75+0.5*nrng.random())
            pts = []
            for t_, pp in zip(tt, pa):
                pp = pp+d0*(1-cv*sstep(t_/0.55)); loc_, n__ = nearest(pp); h_ = 0.05+lift*sstep(t_/0.45)*(1-0.3*t_)
                pts.append(loc_+n__*h_+nrng.normal(0, 0.025, 3))
            lp = bun_loop(gidx, pts[-1], 10, off=nrng.normal(0, 0.2, 2), lock_seed=6000+j, rscale=E('SPH_NLOCK_LOOP', '0.5'))
            full = resample(np.vstack([np.asarray(pts), lp]), N_PTS)
            for m in range(len(full)): full[m] = push_out(full[m], 0.05 if m < 2 else 0.12)
            main.append(full); MAIN_TAG.append(f'nape_lock:{j}'); nl_n += 1
    nf_n = 0
    for k_ in range(int(E('SPH_NAPE_FINE', '0'))):   # fine short hairline hairs (soft start of the nape), small upward-swept wisps
        x_ = nrng.uniform(-7.0, 7.0); y_ = -5.6+0.62*min(abs(x_), 5.0)+0.9*max(abs(x_)-5.0, 0.0); zf_ = zh_back(x_, y_)+nrng.uniform(-0.15, E('SPH_NAPE_FINE_BAND', '0.7'))
        if E('SPH_NLOCK_SURF', '0') > 0:
            sel_ = X[(np.abs(X[:, 0]-x_) < 0.45) & (np.abs(X[:, 2]-zf_) < 0.45) & (X[:, 1] < 1.0)]
            q, nq = nearest(sel_[np.argmin(sel_[:, 1])] if len(sel_) else np.array([x_, y_, zf_]))
        else: q, nq = nearest(np.array([x_, y_, zf_]))
        up = np.array([0.15*np.sign(x_)*nrng.random()+nrng.normal(0, E('SPH_NAPE_FINE_SPREAD', '0.0')), -0.2, 1.0]); up -= nq*np.dot(up, nq); up /= np.linalg.norm(up); L_ = nrng.uniform(0.5, E('SPH_NAPE_FINE_L', '1.5'))
        cu_ = nrng.normal(0, E('SPH_NAPE_FINE_CURL', '0.0'), 3); pts = [push_out(q+up*L_*t_+nq*(0.03+0.10*t_)+cu_*t_*t_+nrng.normal(0, 0.03, 3)*t_, 0.03) for t_ in np.linspace(0, 1, 8)]   # curl: bends the wisp tip
        main.append(resample(np.asarray(pts), N_PTS)); MAIN_TAG.append('nape_fine'); nf_n += 1
    log('nape replace: removed', nrem_, 'nape locks', nl_n, 'fine', nf_n)
if E('SPH_NAPE_THIN', '0') > 0:   # H: probabilistic thinning of nape / corner strands rooted close to the lower back hairline (own RNG; other strands untouched)
    trng = np.random.default_rng(int(E('SPH_THIN_SEED', '991'))); keep = []
    for st, tg_ in zip(main, MAIN_TAG):
        if tg_.startswith('nape_to_bun') or tg_.startswith('corner_to_bun'):
            x0, y0, z0 = st[0]; zh_ = 151.2+2.2*(abs(x0)/6.0)**2+0.35*math.sin(x0*2.3+0.7) if abs(x0) < 4.2 else float(np.interp(abs(math.degrees(math.atan2(x0, y0-2.5))), [112, 122, 132, 142, 152], [161.0, 159.2, 157.4, 155.6, 153.4]))
            pk = E('SPH_NAPE_THIN', '0.3')+(1-E('SPH_NAPE_THIN', '0.3'))*sstep((z0-zh_)/E('SPH_NAPE_THIN_W', '2.2'))
            keep.append(trng.random() < pk)
        else: keep.append(True)
    main = [st for st, k in zip(main, keep) if k]; MAIN_TAG = [t_ for t_, k in zip(MAIN_TAG, keep) if k]; log('nape thinning removed', len(keep)-sum(keep))
MAIN_TAG += ['partcover_or_baby']*(len(main)-len(MAIN_TAG)); LOOSE_TAG += ['fly']*(len(loose)-len(LOOSE_TAG))
json.dump({'main': MAIN_TAG, 'loose': LOOSE_TAG}, open(os.path.join(OUT, 'strand_tags.json'), 'w'))
json.dump({'edited_guides': GUIDES_EDITED}, open(os.path.join(OUT, 'guides_edited.json'), 'w')); log('edited guides', len(GUIDES_EDITED), GUIDES_EDITED[:20])
json.dump({'note': 'refinement G editable guides: prim:* = lock centrelines (29 pts, UE cm, build-head frame), <family>:<seed> = loose lock control polylines, bun:* = bun loop groups (c_off / r / turn). Edit and rebuild with SPH_GUIDES_IN=<this file>.', **GUIDES_OUT}, open(os.path.join(OUT, 'guides.json'), 'w'), indent=0)
export(main, 'hair_main'); export(loose, 'hair_loose'); np.savez_compressed(os.path.join(OUT, 'strands.npz'), main=np.asarray(main, np.float32), loose=np.asarray(loose, np.float32))
stats = {'builder': 'GUARDIAN-8 side/bun/rear architecture', 'primary': len(prim), 'secondary': n_sec, 'tertiary': n_ter, 'main_strands': len(main), 'loose_strands': len(loose), 'locks': K_LOCKS, 'bun_groups': N_GROUPS, 'face_locks': len(FACE), 'points_per_strand': N_PTS, 'bun_centre': C_BUN.tolist(), 'seed': SEED}
open(os.path.join(OUT, 'hair_build.json'), 'w').write(json.dumps(stats, indent=1)); log('HAIR_OK', json.dumps(stats))
