"""GD40 master body pass = contour block-out (A) + muscle atlas (B) + tissue (C), one always-on morph GD40_Body over the current neutral
(accepted_b2 + BR_Neutral v6 + LK_Neutral). Skeleton / height / joints unchanged. PROCEDURAL (no manual brush control).
A  contour block-out from data/shape_plan.json (gd40_contour.py: reference silhouettes aligned by landmarks, per-z ratios on our grid):
   torso (z >= crotch, blended by leg weight): x' = MX + (x-MX) * (1 + CW*(RW_torso-1));  y' = back_t + (y-back_o) * (front_t-back_t)/(front_o-back_o)
     with the target lines = RELIEF transfer: back_t = our glute-apex plane - (reference back relief vs its glute apex) * H; front_t = our
     thigh-front anchor + (reference front line vs its thigh front) * H; blended by CP toward ours (the reference's forward lean is skeletal and
     is NOT copied); bust band / seam band / feet keep ours.
   legs (per leg about the bone axis): x, y scaled by (1 + CW*(RW_leg-1)), (1 + CD*(RD_leg-1)); arms untouched (Guardian slim arms).
B  muscle atlas (surface primitives snapped to the stage-A surface; amplitudes x A_<REGION> env, default 1.0): abdomen columns +
   intersections, linea alba, semilunar lines, obliques, inguinal line, serratus, upper pectoral; erectors, spinal groove, lats, infraspinatus,
   scapular border, lower trapezius, sacral dimples; glute max / medius, infragluteal fold, trochanteric hollow, TFL; quads (rectus femoris,
   vasti), sartorius groove, adductors, hamstrings + groove, IT-band groove; patella + hollows + knee sides; gastrocnemius heads + groove,
   soleus, Achilles, tibialis anterior; deltoid heads + insertion groove, biceps, triceps, forearm extensors.
C  inframammary shelf softened (breast size kept), lower-belly flatten, guards (neck seam band + 1.5 cm around the 92 weld pairs, hands,
   feet), 1 Laplacian pass, LOD1-3 by closest-point barycentric transfer.
usage: blender -b --factory-startup --python gd40_master.py -- <pkg.json.gz> <lk_lod0.json> <lod_dir> <shape_plan.json> <out_dir>
env: CW=0.9 CD=0.8 CP=0.0 (contour strengths; CP > 0 would copy the reference's forward-lean lines) KB=1.0 (atlas global) A_<REGION> (atlas regions) A_IMF=0.6 A_SMOOTH=1"""
import sys, json, gzip, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd40_lib import Body, ss, nrm, MX
a_ = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, LODD, PLAN, OUT = a_[:5]; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d)); CW, CD, CP, KB = E('CW', '0.9'), E('CD', '0.8'), E('CP', '0.0'), E('KB', '1.0')   # CP 0: the reference's forward lean is skeletal; our lumbar relief already matches (see README)
B = Body(PKG, LKJ); NB = B.NB; XR0 = B.XR.copy(); x, y, z = XR0[:, 0], XR0[:, 1], XR0[:, 2]; T = B.T; arm, leg, hand, uarm = B.arm, B.leg, B.hand, B.uarm
pl = json.load(open(PLAN)); zg = np.asarray(pl['z']); HO = pl['H_our']
def cv(k): return np.asarray(pl[k], float)
RWt, RWl, RDt, RDl = cv('RW_torso'), cv('RW_leg'), cv('RD_torso'), cv('RD_leg'); FRo, BKo = cv('front_our'), cv('back_our'); FRt, BKt = cv('front_target'), cv('back_target'); keep = cv('keep')
z_crotch = pl['landmarks_our_z']['crotch']; z_bust = pl['landmarks_our_z']['bust']
# ---- relief transfer for the side lines (ours stays anchored: glute apex plane, thigh front)
above = zg >= z_crotch-0.5; ia = np.nonzero(above & (zg > 76) & (zg < 100))[0]
apex_o = float(BKo[ia].min()); apex_t = float(BKt[ia].min())                   # back-most (most negative y) rows of the glute band: ours / reference-mapped
back_rel = BKt-apex_t; back_goal = apex_o+back_rel                                 # reference relief placed on OUR apex plane
f_anc_o = float(np.interp(pl['anchor_z'], zg, cv('front_leg_our'))); i_anc = int(np.argmin(np.abs(zg-pl['anchor_z'])))
front_goal = f_anc_o+(FRt-FRt[i_anc])                                            # reference front line vs its thigh front, on our thigh front
front_goal = FRo+(front_goal-FRo)*(1-keep); back_goal = BKo+(back_goal-BKo)*(1-keep)
FR_T = FRo+CP*(front_goal-FRo); BK_T = BKo+CP*(back_goal-BKo)
def at(curve, zz): return np.interp(zz, zg, curve)
# ================= A: block-out
wl = ss((leg-0.3)/0.4); wa = ss((arm-0.2)/0.3); P_t = XR0.copy()
tor = (z > z_crotch-6.0)
sx = 1+CW*(at(RWt, z)-1); fo, bo, ft, bt = at(FRo, z), at(BKo, z), at(FR_T, z), at(BK_T, z)
sy = 1+CD*(at(RDt, z)-1); yc_o = 0.5*(fo+bo); yc_t = 0.5*(ft+bt)            # depth scale about the section centre (independent of the posture lines)
P_t[:, 0] = x*sx; P_t[:, 1] = yc_o+(y-yc_o)*sy+(yc_t-yc_o)                  # + posture-line centre shift (0 with CP = 0)
P_l = XR0.copy()
for s_, sg in (('l', 1), ('r', -1)):
    H_, K_, A_ = B.bone(f'thigh_{s_}'), B.bone(f'calf_{s_}'), B.bone(f'foot_{s_}'); side = (np.sign(x) == sg) | (x == 0)
    zz = z.copy(); t1 = np.clip((H_[2]-zz)/(H_[2]-K_[2]), -0.5, 1.0); c1 = H_+t1[:, None]*(K_-H_); t2 = np.clip((K_[2]-zz)/(K_[2]-A_[2]), 0.0, 1.3); c2 = K_+t2[:, None]*(A_-K_)
    c = np.where((zz > K_[2])[:, None], c1, c2); swl = 1+CW*(at(RWl, z)-1); sdl = 1+CD*(at(RDl, z)-1)
    med = ss((np.abs(x)-1.5)/4.0)   # inner thigh near the midline: no lateral scaling (the two legs would collide at the crotch)
    swl_m = 1+(swl-1)*med; sdl = 1+(sdl-1)*np.maximum(med, ss((z_crotch-2.0-z)/4.0))   # the depth scaling also fades at the crotch midline (perineum / gluteal cleft)
    Pl = XR0.copy(); Pl[:, 0] = c[:, 0]+(x-c[:, 0])*swl_m; Pl[:, 1] = c[:, 1]+(y-c[:, 1])*sdl; P_l[side] = Pl[side]
wleg = np.clip(wl*ss((z_crotch+18.0-z)/10.0), 0, 1)   # per-leg map from the hip down (full below z ~88)
P_A = (1-wleg)[:, None]*P_t+wleg[:, None]*P_l; P_A = (1-wa)[:, None]*P_A+wa[:, None]*XR0
DA = P_A-XR0; rep = {'A_max_mm': float(np.linalg.norm(DA, axis=1).max()*10)}
# ================= B: atlas on the stage-A surface
XR = P_A; N = B.normals(XR); xa, ya, za = XR[:, 0], XR[:, 1], XR[:, 2]
TORSO = (arm < 0.3)*(leg < 0.5); LEGM = (leg > 0.4)*(arm < 0.2); ARMM = (arm > 0.4)*(hand < 0.3); GM = ((TORSO+LEGM) > 0) & (np.abs(xa) > 1.2)   # glute fields never touch the gluteal cleft walls
D = np.zeros_like(XR); prims = {}
def snap(c, face, mask, rs=2.0):
    f = nrm(face); d = XR-c; perp = d-np.outer(d@f, f); cand = np.nonzero(mask & (np.linalg.norm(perp, axis=1) < rs))[0]
    if not len(cand): cand = np.nonzero(mask)[0][np.argsort(np.linalg.norm(XR[mask]-c, axis=1))[:1]]
    return XR[cand[np.argmax(XR[cand]@f)]]
def prim(name, c, face, fiber, a, b, h, p=3.0, mask=None, gate=0.15, mirror=True, depth=5.0):
    mask = TORSO if mask is None else mask; peak = 0.0
    for sgn in ((1, -1) if mirror else (1,)):
        cc = np.array(c, float)*np.array([sgn, 1, 1]); fc = nrm(np.array(face, float)*np.array([sgn, 1, 1])); fb = np.array(fiber, float)*np.array([sgn, 1, 1])
        side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool)); P0 = snap(cc, fc, side); u = nrm(fb-(fb@fc)*fc); v = np.cross(fc, u); d = XR-P0
        r2 = ((d@u)/a)**2+((d@v)/b)**2; w = np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < depth)*side
        amp = (h/10.0)*KB; D[:] += amp*w[:, None]*N; peak = max(peak, abs(amp)*w.max()*10)
    prims[name] = round(float(peak), 2)
def chainprim(name, pts, faces, h, b, mask=None, p=2.0, mirror=True, gate=0.15):
    mask = TORSO if mask is None else mask
    for sgn in ((1, -1) if mirror else (1,)):
        W = np.zeros(NB); side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool))
        for i in range(len(pts)-1):
            p0 = np.array(pts[i], float)*np.array([sgn, 1, 1]); p1 = np.array(pts[i+1], float)*np.array([sgn, 1, 1]); fc = nrm(np.array(faces[i], float)*np.array([sgn, 1, 1]))
            c = 0.5*(p0+p1); P0 = snap(c, fc, side); fb = p1-p0; L = max(np.linalg.norm(fb), 0.5); u = nrm(fb-(fb@fc)*fc); v = np.cross(fc, u); d = XR-P0
            r2 = ((d@u)/(0.62*L))**2+((d@v)/b)**2; W = np.maximum(W, np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < 4.0)*side)
        D[:] += ((h/10.0)*KB)*W[:, None]*N
    prims[name] = round(abs(h*KB), 2)
G = lambda k, d: E('A_'+k, d); fr = (0, 1, 0); bk = (0, -1, 0)
gA = G('ABS', '1.0')
for zc, f_ in ((118.6, 1.0), (113.0, 1.0), (107.6, 0.55)): prim(f'rectus_block_{zc:.0f}', (3.3, 14, zc), fr, (0, 0, 1), 2.4, 2.1, 1.6*gA*f_)
for zc, f_ in ((115.8, 1.0), (110.2, 0.8)): prim(f'rectus_intersect_{zc:.0f}', (3.3, 14, zc), fr, (1, 0, -0.08), 2.6, 0.55, -1.1*gA*f_, p=2)
prim('linea_alba', (0, 14, 114.5), fr, (0, 0, 1), 7.5, 0.6, -1.6*gA, p=2, mirror=False)
chainprim('semilunar', [(7.0, 14, 121.0), (6.8, 14, 113.0), (6.2, 14, 105.0), (5.3, 14, 98.0)], [fr, (0.25, 1, 0), (0.3, 1, 0)], -1.3*gA, 0.65)
prim('ext_oblique', (11.3, 10, 103.5), (0.65, 0.76, 0), (-0.4, 0, -1), 4.0, 2.4, 2.4*G('OBL', '1.0'))
chainprim('inguinal_line', [(12.0, 13, 96.5), (9.0, 14, 92.5), (6.0, 14, 89.0), (3.5, 14, 86.5)], [(0.45, 1, 0), fr, fr], -2.0*G('OBL', '1.0'), 0.8, mask=TORSO*(leg < 0.7))
for i, zc in enumerate((121.5, 118.6, 115.8)): prim(f'serratus_{i}', (12.9, 5, zc), (0.8, 0.6, 0), (0.3, 0.75, -0.6), 1.5, 0.75, 1.4*G('SERR', '1.0'))
prim('upper_pectoral', (6.5, 12, 133.2), fr, (1, 0, -0.15), 4.0, 1.9, 1.6*G('PEC', '1.0'))
prim('lower_belly_flatten', (0, 15, 100.0), fr, (0, 0, 1), 5.0, 8.0, -7.0*G('BELLY', '1.0'), p=2, mirror=False)
prim('erector', (3.6, -5, 106.0), bk, (0, 0, 1), 11.0, 1.7, 2.8*G('BACK', '1.0'))
prim('spinal_groove', (0, -5, 112.0), bk, (0, 0, 1), 15.0, 0.8, -2.6*G('BACK', '1.0'), p=2, mirror=False)
prim('lats', (12.8, -3, 116.5), (0.6, -0.8, 0), (0.35, 0, 1), 7.5, 3.0, 2.8*G('BACK', '1.0'))
prim('infraspinatus', (9.5, -6, 126.0), bk, (0.3, 0, 1), 3.6, 3.4, 2.8*G('BACK', '1.0'))
prim('scapula_medial_border', (5.8, -7, 126.0), bk, (0, 0, 1), 5.0, 0.8, -1.4*G('BACK', '1.0'), p=2)
prim('lower_trapezius', (3.6, -7, 123.5), bk, (0.45, 0, 1), 6.0, 2.0, 1.2*G('BACK', '1.0'))
prim('sacral_dimples', (3.6, -6, 98.5), bk, (0, 0, 1), 0.9, 0.9, -1.5*G('BACK', '1.0'), p=2)
prim('glute_max', (7.4, -8, float(E('A_GLUTE_Z', '87.5'))), bk, (0, 0, 1), 6.2, float(E('A_GLUTE_B', '6.4')), 7.5*G('GLUTE', '0.7'), mask=GM, p=3)   # the block-out already deepens the hip; the atlas adds shape, not more depth
chainprim('infragluteal_fold', [(3.0, -6, 82.4), (6.0, -7, 82.8), (9.0, -7, 83.2), (11.5, -6, 84.0)], [(0, -0.85, -0.5)]*3, -2.6*G('GLUTE', '1.0'), 0.8, mask=GM)
prim('glute_medius', (12.8, -4, 95.0), (0.75, -0.66, 0), (0, 0, 1), 3.6, 3.0, 2.8*G('GLUTE', '1.0'), mask=GM)
prim('trochanteric_hollow', (15.2, 1, 85.0), (1, 0, 0), (0, 0, 1), 3.0, 2.5, -1.8*G('HOLLOW', '1.0'), mask=GM, p=2)
prim('tfl', (12.5, 6, 89.0), (0.7, 0.7, 0), (0.15, -0.2, -1), 3.6, 1.8, 2.0*G('HIP', '1.0'), mask=GM)
H_, K_, A_ = B.bone('thigh_l'), B.bone('calf_l'), B.bone('foot_l'); ax_t = K_-H_; Lt = np.linalg.norm(ax_t); ax_c = A_-K_
atp = lambda t: H_+t*ax_t; acp = lambda s: K_+s*ax_c; gL, gC, gK = G('THIGH', '1.0'), G('CALF', '1.0'), G('KNEE', '1.0')
prim('rectus_femoris', atp(0.45)+[0, 6, 0], fr, ax_t, 0.30*Lt, 2.7, 3.8*gL, mask=LEGM)
prim('vastus_lateralis', atp(0.56)+[4, 4, 0], (0.72, 0.69, 0), ax_t, 0.30*Lt, 3.1, 4.2*gL, mask=LEGM)
prim('vastus_medialis', atp(0.86)+[-3, 4, 0], (-0.62, 0.78, 0), ax_t, 0.11*Lt, 2.9, 4.2*gL, mask=LEGM)
chainprim('sartorius_groove', [atp(0.10)+[3.5, 5, 0], atp(0.35)+[1.5, 6, 0], atp(0.60)+[-1.5, 5, 0], atp(0.85)+[-4.0, 2, 0]], [(0.4, 1, 0), (0, 1, 0), (-0.5, 0.85, 0)], -1.6*gL, 0.8, mask=LEGM)
prim('adductors', atp(0.25)+[-4, 0, 0], (-1, 0.25, 0), ax_t, 0.18*Lt, 3.4, 2.2*gL, mask=LEGM)
prim('biceps_femoris', atp(0.55)+[2.5, -5, 0], (0.5, -0.86, 0), ax_t, 0.28*Lt, 2.7, 3.3*gL, mask=LEGM)
prim('semitendinosus', atp(0.55)+[-2.5, -5, 0], (-0.5, -0.86, 0), ax_t, 0.28*Lt, 2.7, 3.3*gL, mask=LEGM)
prim('hamstring_groove', atp(0.62)+[0, -6, 0], bk, ax_t, 0.22*Lt, 0.7, -1.2*gL, mask=LEGM, p=2)
prim('it_band_groove', atp(0.62)+[6, -1, 0], (1, -0.15, 0), ax_t, 0.22*Lt, 0.8, -1.4*gL, mask=LEGM, p=2)
prim('patella', K_+[0, 5, 3.0], fr, (0, 0, 1), 2.2, 2.0, 2.4*gK, mask=LEGM, p=4)
prim('peripatellar_hollow_lat', K_+[2.6, 4, 2.0], (0.6, 0.8, 0), (0, 0, 1), 2.4, 1.0, -2.2*gK, mask=LEGM, p=2)
prim('peripatellar_hollow_med', K_+[-2.6, 4, 2.0], (-0.6, 0.8, 0), (0, 0, 1), 2.4, 1.0, -2.2*gK, mask=LEGM, p=2)
prim('knee_side_lat', K_+[5, 0, 1.0], (1, 0, 0), (0, 0, 1), 3.0, 3.0, -2.6*gK, mask=LEGM, p=2)
prim('knee_side_med', K_+[-5, 0, 1.0], (-1, 0, 0), (0, 0, 1), 3.0, 3.0, -2.6*gK, mask=LEGM, p=2)
prim('gastroc_medial', acp(0.27)+[-2.5, -4, 0], (-0.55, -0.83, 0), ax_c, 6.5, 3.1, 5.5*gC, mask=LEGM)
prim('gastroc_lateral', acp(0.24)+[2.5, -4, 0], (0.55, -0.83, 0), ax_c, 5.5, 2.7, 3.8*gC, mask=LEGM)
prim('gastroc_groove', acp(0.30)+[0, -5, 0], bk, ax_c, 5.0, 0.7, -1.4*gC, mask=LEGM, p=2)
prim('soleus_lat', acp(0.50)+[3.5, -1, 0], (0.95, -0.3, 0), ax_c, 5.0, 2.1, 1.7*gC, mask=LEGM)
prim('soleus_med', acp(0.50)+[-3.5, -1, 0], (-0.95, -0.3, 0), ax_c, 5.0, 2.1, 1.7*gC, mask=LEGM)
prim('achilles_slim_lat', acp(0.78)+[2.5, -1, 0], (1, -0.2, 0), ax_c, 4.0, 2.6, -2.2*gC, mask=LEGM, p=2)
prim('achilles_slim_med', acp(0.78)+[-2.5, -1, 0], (-1, -0.2, 0), ax_c, 4.0, 2.6, -2.2*gC, mask=LEGM, p=2)
prim('tibialis_anterior', acp(0.30)+[2.5, 4, 0], (0.55, 0.83, 0), ax_c, 7.0, 1.8, 2.4*gC, mask=LEGM)
U_, El_, Hd_ = B.bone('upperarm_l'), B.bone('lowerarm_l'), B.bone('hand_l'); ua = El_-U_; la = Hd_-El_; lat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(ua))*nrm(ua)); gA_ = G('ARM', '1.0')
prim('deltoid_lateral', U_+0.16*ua+1.2*lat, lat, ua, 5.0, 4.2, 4.0*gA_, mask=ARMM)
prim('deltoid_anterior', U_+0.12*ua+[0, 3, 0], fr, ua, 4.0, 2.2, 2.0*gA_, mask=ARMM)
prim('deltoid_posterior', U_+0.12*ua+[0, -3, 0], bk, ua, 4.0, 2.2, 2.0*gA_, mask=ARMM)
prim('deltoid_insertion_groove', U_+0.42*ua+1.0*lat, lat, ua, 2.0, 1.8, -1.0*gA_, mask=ARMM, p=2)
prim('biceps', U_+0.58*ua+[0, 2.5, 0], fr, ua, 7.0, 2.2, 2.4*gA_, mask=ARMM)
prim('triceps', U_+0.45*ua+[0, -2.5, 0], bk, ua, 8.0, 2.7, 2.8*gA_, mask=ARMM)
flat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(la))*nrm(la)); prim('forearm_extensors', El_+0.22*la+1.0*flat, flat, la, 5.0, 2.2, 1.8*gA_, mask=ARMM)
# ================= C: IMF soften (size kept), guards, smoothing
AP = B.P['breast_apex']; wimf = np.zeros(NB)
for sk_, Ap in AP.items():
    Ap = np.asarray(Ap)-np.array([MX, 0, 0]); dx = xa-Ap[0]; dz = za-Ap[2]
    band = np.exp(-((np.sqrt((dx/6.0)**2+((dz+5.5)/2.2)**2)-1.0)/0.45)**2)*ss((Ap[2]-1.0-za)/2.0)*ss((ya-(Ap[1]-8.0))/3.0)*TORSO; wimf = np.maximum(wimf, band)
Y = XR+D
for _ in range(int(10*E('A_IMF', '0.3'))):
    M = np.asarray([Y[n].mean(0) if len(n) else Y[i] for i, n in enumerate(B.NBR)]); Y += (0.5*wimf)[:, None]*(M-Y)
Dtot = Y-XR0
kd = KDTree(len(B.weld))
for j, i in enumerate(B.weld): kd.insert(tuple(XR0[i]), j)
kd.balance(); dseam = np.array([kd.find(tuple(p))[2] for p in XR0])
guard = ss((138.5-z)/2.0)*ss((dseam-1.5)/1.5)*(1-ss((hand-0.2)/0.3))*ss((z-11.0)/4.0); Dtot *= guard[:, None]
Dtot = B.smooth_field(Dtot, int(E('A_SMOOTH', '1'))); Dtot *= guard[:, None]
mag = np.linalg.norm(Dtot, axis=1); ids = np.nonzero(mag > 0.002)[0]
rep.update({'CW': CW, 'CD': CD, 'CP': CP, 'KB': KB, 'verts': int(len(ids)), 'max_mm': float(mag.max()*10), 'p99_mm': float(np.percentile(mag[ids], 99)*10), 'seam_pairs_max_mm': float(mag[B.weld].max()*10),
            'glute_apex_plane_our': apex_o, 'B_atlas_max_mm': float(np.linalg.norm(D, axis=1).max()*10), 'prims_peak_mm': prims, 'env': {k: v for k, v in os.environ.items() if k.startswith('A_') or k in ('CW', 'CD', 'CP', 'KB')}})
json.dump({'Body': {'GD40_Body': {str(int(i)): [round(float(v), 5) for v in Dtot[i]] for i in ids}}, 'Head': {}}, open(os.path.join(OUT, 'morph_gd40_body_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'gd40_body_delta_lod0.npy'), Dtot)
X0 = B.X; bvh = BVHTree.FromPolygons([Vector(p) for p in X0], [list(t_) for t_ in T])
for lod in (1, 2, 3):
    gl = json.load(gzip.open(os.path.join(LODD, f'lod_Body_{lod}.json.gz'), 'rt')); PL = np.asarray(gl['positions']); res = {}; far = 0
    for vi, p in enumerate(PL):
        loc, nr_, fi, dist = bvh.find_nearest(Vector(p))
        if fi is None or dist > 1.0: far += 1; continue
        tri = T[fi]; A0, B0, C0 = X0[tri[0]], X0[tri[1]], X0[tri[2]]; qq = np.asarray(loc)
        v0, v1, v2 = B0-A0, C0-A0, qq-A0; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01 or 1e-12
        bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; bu = 1-bv-bw; dd_ = bu*Dtot[tri[0]]+bv*Dtot[tri[1]]+bw*Dtot[tri[2]]
        if np.linalg.norm(dd_) > 0.002: res[str(vi)] = [round(float(v), 5) for v in dd_]
    json.dump({'Body': {'GD40_Body': res}, 'Head': {}}, open(os.path.join(OUT, f'morph_gd40_body_lod{lod}.json'), 'w')); rep[f'lod{lod}'] = {'verts': len(res), 'far': far}
json.dump(rep, open(os.path.join(OUT, 'gd40_body_report.json'), 'w'), indent=1)
print('GD40MASTER', json.dumps({k: v for k, v in rep.items() if k not in ('env', 'prims_peak_mm')}))
