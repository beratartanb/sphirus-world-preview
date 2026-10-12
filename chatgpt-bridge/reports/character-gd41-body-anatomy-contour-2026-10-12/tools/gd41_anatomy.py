"""GD41 anatomy build (user: "work much more on the body anatomy; we are far from a realistic female form and from the references").
One always-on morph GD41_Body over the current neutral (accepted_b2 + BR_Neutral v6 + LK_Neutral). Skeleton / joints unchanged. PROCEDURAL.
Layers (bind space UE cm, x = subject's left rel. midline, y = front, z = up):
 A  contour block-out from data/shape_plan.json (GD40 C8 method: torso width about the midline / depth about the section centre, per-leg
    width / depth about the bone axis; bust, seam band, feet kept)
 S  section shape: the torso section is an ellipse (fill 0.80); an athletic torso is a rounded box (flat abdominal wall, flat oblique planes):
    radial remap of the torso sections (z 94..121) toward a superellipse of exponent SN (2.6) with strength SS
 K  skeletal landmarks: iliac crest ridge, ASIS, PSIS dimples + sacral triangle, costal margin arch + subcostal groove, scapular spines,
    patella + tibial tuberosity + tibia anterior border, malleoli, olecranon + ulna border, greater-trochanter hollow
 M  muscle volumes with real borders (flat-topped superellipse bellies + sigmoid edges): pectoral base, serratus, rectus blocks + tendinous
    intersections + linea alba + semilunar lines, external obliques, inguinal lines; erectors + spinal groove, latissimus wing, infraspinatus,
    teres, mid / lower trapezius, scapular medial border; gluteus maximus (low, full) + fold, gluteus medius, TFL + groove; rectus femoris,
    vastus lateralis, VMO teardrop, sartorius groove, adductor mass, biceps femoris / semitendinosus + groove, IT-band groove; gastrocnemius
    heads + groove, soleus, Achilles, tibialis anterior, peroneals; deltoid heads + insertion, biceps, triceps, brachialis, forearm masses
 B  breast: hemisphere -> teardrop on the pectoral base (upper pole flattened, lower pole fuller, apex lower / lateral, axillary tail blend,
    modest volume); then a concave-only crease fill (normal push, no tangential shrink) along the lower-lateral IMF and the lateral border,
    where the base breast met the chest wall in a hard cut; light IMF Laplacian afterwards
 F  female fat / skin: lateral upper-thigh fullness, lower-belly curve + pubic mound, knee pads; lower-belly flatten (GD40)
 G  guards: head/body weld band (z 134..143, |x| < 15.3: z-band guard only there, the deltoid cap beyond it is free) + 1.5 cm around the
    92 weld pairs, hands, feet, gluteal cleft for glute fields; 1 Laplacian pass; LOD1-3 transfer.
Candidates: D1 first atlas (ASIS knobs, crest belt, adductor crushed the crotch) -> D2 softer landmarks, depth pivot (front plane fixed at the
waist, back fixed at the pelvis), adductor moved down -> D3 amplitudes up ~1.3x, deltoid cap freed from the z guard, breast fill / volume
-> D4 knee pockets softened (sartorius / peripatellar / knee-side wider and shallower), bigger axillary-tail blend, 12 fill iterations
-> D5 lower back: posterior crest ridge removed, PSIS / sacral hollows halved, lumbar erector higher and lighter (UE clay showed a belt band)
-> D6 the band was the depth pivot: front-fixed waist = 2.5 cm back ledge at z 102-108; pivot now ramps back-fixed (pelvis) -> centre (waist) over z 94-108.
usage: blender -b --factory-startup --python gd41_anatomy.py -- <pkg.json.gz> <lk_lod0.json> <lod_dir> <shape_plan.json> <out_dir>
env: CW CD (block-out strengths), SN SS (section shape), KM (global muscle multiplier, 1.0), KK (landmarks), KF (fat), BR (breast reshape 0..1),
     A_<REGION> per-region multipliers (incl. BR_UP / BR_LOW / BR_VOL / BR_TAIL), A_FILL, A_FILL_IT, A_IMF, A_SMOOTH"""
import sys, json, gzip, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd41_lib import Body, ss, nrm, MX
a_ = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, LODD, PLAN, OUT = a_[:5]; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d)); CW, CD = E('CW', '0.9'), E('CD', '0.8'); SN, SS = E('SN', '2.5'), E('SS', '0.9'); KM, KK, KF, BRS = E('KM', '1.0'), E('KK', '1.0'), E('KF', '1.0'), E('BR', '1.0')
B = Body(PKG, LKJ); NB = B.NB; XR0 = B.XR.copy(); x, y, z = XR0[:, 0], XR0[:, 1], XR0[:, 2]; T = B.T; arm, leg, hand, uarm = B.arm, B.leg, B.hand, B.uarm
pl = json.load(open(PLAN)); zg = np.asarray(pl['z']); cv = lambda k: np.asarray(pl[k], float)
RWt, RWl, RDt, RDl = cv('RW_torso'), cv('RW_leg'), cv('RD_torso'), cv('RD_leg'); FRo, BKo = cv('front_our'), cv('back_our'); z_crotch = pl['landmarks_our_z']['crotch']; z_bust = pl['landmarks_our_z']['bust']
at = lambda curve, zz: np.interp(zz, zg, curve); rep = {}
# ================= A: block-out (GD40 C8)
wl = ss((leg-0.3)/0.4); wa = ss((arm-0.2)/0.3); P_t = XR0.copy()
sx = 1+CW*(at(RWt, z)-1); fo, bo = at(FRo, z), at(BKo, z); sy = 1+CD*(at(RDt, z)-1)
pf = ss((z-94.0)/14.0); pv = pf*(0.5*fo+0.5*bo)+(1-pf)*bo   # depth pivot: back fixed at the pelvis (belly flattens), section centre from the waist up;
# a front-fixed waist (D2-D5) pushed the whole lumbar back line 2.5 cm out between z 102 and 108 = a horizontal ledge (belt band in UE clay)
P_t[:, 0] = x*sx; P_t[:, 1] = pv+(y-pv)*sy
P_l = XR0.copy()
for s_, sg in (('l', 1), ('r', -1)):
    H_, K_, A_ = B.bone(f'thigh_{s_}'), B.bone(f'calf_{s_}'), B.bone(f'foot_{s_}'); side = (np.sign(x) == sg) | (x == 0)
    t1 = np.clip((H_[2]-z)/(H_[2]-K_[2]), -0.5, 1.0); c1 = H_+t1[:, None]*(K_-H_); t2 = np.clip((K_[2]-z)/(K_[2]-A_[2]), 0.0, 1.3); c2 = K_+t2[:, None]*(A_-K_)
    c = np.where((z > K_[2])[:, None], c1, c2); swl = 1+CW*(at(RWl, z)-1); sdl = 1+CD*(at(RDl, z)-1)
    med = ss((np.abs(x)-1.5)/4.0); swl_m = 1+(swl-1)*med; sdl = 1+(sdl-1)*np.maximum(med, ss((z_crotch-2.0-z)/4.0))
    Pl = XR0.copy(); Pl[:, 0] = c[:, 0]+(x-c[:, 0])*swl_m; Pl[:, 1] = c[:, 1]+(y-c[:, 1])*sdl; P_l[side] = Pl[side]
wleg = np.clip(wl*ss((z_crotch+18.0-z)/10.0), 0, 1)
P_A = (1-wleg)[:, None]*P_t+wleg[:, None]*P_l; P_A = (1-wa)[:, None]*P_A+wa[:, None]*XR0; rep['A_max_mm'] = float(np.linalg.norm(P_A-XR0, axis=1).max()*10)
# ================= S: torso section shape (ellipse -> rounded box)
XR = P_A.copy(); noarm = (arm < 0.3) & (leg < 0.6)
for zz in np.arange(93.0, 122.0, 0.5):
    p = B.section(zz, noarm, XR)
    if len(p) < 8: continue
    cx, cy = 0.0, 0.5*(p[:, 1].max()+p[:, 1].min()); a = 0.5*(p[:, 0].max()-p[:, 0].min()); b = 0.5*(p[:, 1].max()-p[:, 1].min())
    band = noarm & (np.abs(z-zz) < 0.25)
    if not band.any(): continue
    dx = XR[band, 0]-cx; dy = XR[band, 1]-cy; th = np.arctan2(dy/b, dx/a); c_, s_ = np.cos(th), np.sin(th)
    r_e = 1.0/np.sqrt((c_/a)**2+(s_/b)**2); r_t = (np.abs(c_/a)**SN+np.abs(s_/b)**SN)**(-1.0/SN)
    wz = ss((zz-93.0)/4.0)*ss((121.0-zz)/3.0); k = 1+SS*wz*(r_t/r_e-1)
    XR[band, 0] = cx+dx*k; XR[band, 1] = cy+dy*k
rep['S_max_mm'] = float(np.linalg.norm(XR-P_A, axis=1).max()*10)
# ================= primitives on the current surface
N = B.normals(XR); xa, ya, za = XR[:, 0], XR[:, 1], XR[:, 2]
TORSO = (arm < 0.3)*(leg < 0.5); LEGM = (leg > 0.4)*(arm < 0.2); ARMM = (arm > 0.4)*(hand < 0.3); GM = ((TORSO+LEGM) > 0) & (np.abs(xa) > 1.2); ALL = (hand < 0.3)
D = np.zeros_like(XR); prims = {}
def snap(c, face, mask, rs=2.0):
    f = nrm(face); d = XR-c; perp = d-np.outer(d@f, f); cand = np.nonzero(mask & (np.linalg.norm(perp, axis=1) < rs))[0]
    if not len(cand): cand = np.nonzero(mask)[0][np.argsort(np.linalg.norm(XR[mask]-c, axis=1))[:1]]
    return XR[cand[np.argmax(XR[cand]@f)]]
def frame(cc, face, fiber):
    fc = nrm(face); fb = np.asarray(fiber, float); u = nrm(fb-(fb@fc)*fc); v = np.cross(fc, u); return fc, u, v
def belly(name, c, face, fiber, a, b, h, p=3.0, mask=None, gate=0.15, mirror=True, depth=5.0, K=None):
    mask = TORSO if mask is None else mask; K = KM if K is None else K; peak = 0.0
    for sgn in ((1, -1) if mirror else (1,)):
        cc = np.array(c, float)*np.array([sgn, 1, 1]); fc, u, v = frame(cc, np.array(face, float)*np.array([sgn, 1, 1]), np.array(fiber, float)*np.array([sgn, 1, 1]))
        side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool)); P0 = snap(cc, fc, side); d = XR-P0
        r2 = ((d@u)/a)**2+((d@v)/b)**2; w = np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < depth)*side
        amp = (h/10.0)*K; D[:] += amp*w[:, None]*N; peak = max(peak, abs(amp)*w.max()*10)
    prims[name] = round(float(peak), 2)
def chain(name, pts, faces, h, b, mask=None, p=2.0, mirror=True, gate=0.15, K=None):
    mask = TORSO if mask is None else mask; K = KM if K is None else K
    for sgn in ((1, -1) if mirror else (1,)):
        W = np.zeros(NB); side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool))
        for i in range(len(pts)-1):
            p0 = np.array(pts[i], float)*np.array([sgn, 1, 1]); p1 = np.array(pts[i+1], float)*np.array([sgn, 1, 1]); fc, u, v = frame(0, np.array(faces[min(i, len(faces)-1)], float)*np.array([sgn, 1, 1]), p1-p0)
            c = 0.5*(p0+p1); P0 = snap(c, fc, side); L = max(np.linalg.norm(p1-p0), 0.5); d = XR-P0
            r2 = ((d@u)/(0.62*L))**2+((d@v)/b)**2; W = np.maximum(W, np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < 4.0)*side)
        D[:] += ((h/10.0)*K)*W[:, None]*N
    prims[name] = round(abs(h*K), 2)
def edge(name, c, face, fiber, L, w, h, reach, mask=None, mirror=True, gate=0.15, K=None):
    """muscle border: plateau h on the +v side of the line (c, fiber), sigmoid of width w across, fading over `reach` on the + side and over 0.3 L at the ends"""
    mask = TORSO if mask is None else mask; K = KM if K is None else K
    for sgn in ((1, -1) if mirror else (1,)):
        cc = np.array(c, float)*np.array([sgn, 1, 1]); fc, u, v = frame(cc, np.array(face, float)*np.array([sgn, 1, 1]), np.array(fiber, float)*np.array([sgn, 1, 1]))
        side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool)); P0 = snap(cc, fc, side); d = XR-P0; du, dv = d@u, d@v
        if sgn < 0: dv = -dv   # mirrored frame flips v (cross product handedness)
        wgt = ss((0.5*L-np.abs(du))/(0.3*L))*ss((dv+0.5*w)/w)*ss((reach-dv)/(0.6*reach))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < 5.0)*side
        D[:] += ((h/10.0)*K)*wgt[:, None]*N
    prims[name] = round(abs(h*K), 2)
def blob(name, c, r, h, mask=None, mirror=True, p=2.0, K=None):
    mask = ALL if mask is None else mask; K = KK if K is None else K
    for sgn in ((1, -1) if mirror else (1,)):
        cc = np.array(c, float)*np.array([sgn, 1, 1]); side = mask & ((xa*sgn > -0.5) if mirror else np.ones(NB, bool))
        i0 = np.nonzero(side)[0]; P0 = XR[i0[np.argmin(np.linalg.norm(XR[i0]-cc, axis=1))]]; d = np.linalg.norm(XR-P0, axis=1)
        w = np.exp(-((d/r)**p))*side; D[:] += ((h/10.0)*K)*w[:, None]*N
    prims[name] = round(abs(h*K), 2)
G = lambda k, d: E('A_'+k, d); fr = (0, 1, 0); bk = (0, -1, 0)
# ---------------- torso front
belly('ribcage_lower', (0, 14.5, 117.5), fr, (1, 0, 0), 9.0, 3.0, 1.5*G('RIB', '1'), p=2, mirror=False)
chain('costal_margin', [(0.5, 14.3, 119.0), (5.0, 14.0, 116.3), (9.0, 12.8, 112.8), (12.3, 10.2, 109.3)], [fr, (0.3, 1, 0), (0.6, 0.8, 0)], 2.0*G('RIB', '1'), 1.4, K=KK)
chain('subcostal_groove', [(1.0, 14.2, 117.2), (5.5, 13.8, 114.6), (9.2, 12.6, 111.2), (12.2, 10.0, 107.9)], [fr, (0.3, 1, 0), (0.6, 0.8, 0)], -1.5*G('RIB', '1'), 1.1, K=KK)
gA = G('ABS', '1')
for zc, f_, bb in ((118.0, 0.7, 2.2), (112.6, 1.0, 2.5), (107.0, 0.8, 2.6)): belly(f'rectus_{zc:.0f}', (3.3, 14, zc), fr, (0, 0, 1), 2.8, bb, 3.5*gA*f_, p=2.5)
for zc, f_ in ((115.4, 1.0), (109.8, 0.85)): belly(f'rectus_intersect_{zc:.0f}', (3.3, 14, zc), fr, (1, 0, -0.08), 2.7, 0.7, -1.8*gA*f_, p=2)
belly('linea_alba', (0, 14, 112.0), fr, (0, 0, 1), 9.0, 0.55, -2.2*gA, p=2, mirror=False)
chain('semilunar', [(7.2, 14, 121.0), (7.0, 14, 113.0), (6.4, 14, 105.0), (5.4, 14.2, 98.0)], [fr, (0.25, 1, 0), (0.3, 1, 0)], -1.8*gA, 0.8)
belly('ext_oblique', (11.5, 10.5, 105.0), (0.68, 0.73, 0), (-0.45, 0.2, -1), 6.0, 3.6, 4.0*G('OBL', '1'), p=2.5)
chain('flank_tuck', [(13.4, 8.5, 102.5), (14.2, 3.5, 104.0), (13.4, -1.5, 104.5)], [(0.9, 0.4, 0), (1, 0, 0), (0.9, -0.4, 0)], -2.0*G('OBL', '1'), 1.6)   # waist indentation above the crest
chain('inguinal_line', [(12.0, 13, 96.5), (9.0, 14, 92.5), (6.0, 14.3, 89.0), (3.5, 14.5, 86.5)], [(0.45, 1, 0), fr, fr], -2.5*G('OBL', '1'), 1.0, mask=TORSO*(leg < 0.7))
for i, zc in enumerate((122.0, 119.0, 116.0)): belly(f'serratus_{i}', (13.0, 5.0, zc), (0.8, 0.6, 0), (0.3, 0.75, -0.6), 1.7, 0.8, 2.0*G('SERR', '1'))
belly('pectoral_base', (6.5, 12.3, 133.3), fr, (1, 0, -0.15), 5.0, 2.3, 3.5*G('PEC', '1'))
belly('lower_belly_flatten', (0, 15, 100.0), fr, (0, 0, 1), 5.0, 8.0, -7.0*G('BELLY', '1'), p=2, mirror=False, K=1.0)
# ---------------- pelvis landmarks
chain('iliac_crest', [(11.8, 12.3, 96.5), (13.5, 8.0, 99.5), (13.9, 3.0, 101.5), (12.6, -2.0, 102.0)], [(0.6, 0.8, 0), (0.95, 0.3, 0), (1, 0, 0)], 2.5*G('CREST', '1'), 1.8, K=KK)   # anterior + lateral crest only: the posterior ridge made a belt band across the lower back
blob('asis', (11.8, 12.3, 96.5), 2.2, 1.5*G('CREST', '1'))
blob('psis_dimple', (4.3, -6.8, 100.2), 1.6, -1.5*G('CREST', '1'))
belly('sacral_triangle', (0, -7.5, 96.0), bk, (0, 0, 1), 4.0, 3.5, -1.5*G('CREST', '1'), p=3, mirror=False, K=KK)
blob('pubic_mound', (0, 15.2, 87.5), 2.4, 2.0*G('BELLY', '1'), mirror=False, K=KF)
# ---------------- back
belly('erector_lumbar', (3.4, -5, 107.0), bk, (0, 0, 1), 8.0, 2.3, 4.0*G('BACK', '1'), p=2.5)
belly('erector_thoracic', (3.0, -5.5, 118.0), bk, (0, 0, 1), 8.0, 1.9, 3.0*G('BACK', '1'), p=2.5)
belly('spinal_groove', (0, -5, 113.0), bk, (0, 0, 1), 16.0, 1.1, -3.5*G('BACK', '1'), p=2, mirror=False)
belly('lats', (12.3, -3.5, 117.5), (0.6, -0.8, 0), (0.35, 0, 1), 8.5, 4.0, 5.0*G('BACK', '1'), p=2.5)
chain('scapular_spine', [(4.5, -7.0, 129.5), (9.0, -6.2, 131.5), (13.5, -4.5, 133.5)], [bk, (0.3, -0.95, 0)], 3.0*G('BACK', '1'), 1.0, K=KK)
belly('infraspinatus', (9.5, -6.2, 126.0), bk, (0.3, 0, 1), 3.9, 3.6, 4.5*G('BACK', '1'))
blob('teres', (12.6, -5.0, 124.5), 2.0, 3.0*G('BACK', '1'), K=KM)
belly('scapula_medial_border', (5.8, -7, 126.0), bk, (0, 0, 1), 5.0, 0.8, -2.5*G('BACK', '1'), p=2)
belly('mid_trapezius', (3.2, -6.5, 131.5), bk, (0.4, 0, 1), 4.0, 3.0, 3.0*G('BACK', '1'))
belly('lower_trapezius', (3.6, -7, 122.5), bk, (0.45, 0, 1), 6.0, 2.0, 2.5*G('BACK', '1'))
# ---------------- glutes / hip
belly('glute_max', (7.6, -8, float(E('A_GLUTE_Z', '86.5'))), bk, (0.3, 0, 1), 6.5, 7.0, 11.0*G('GLUTE', '1'), mask=GM, p=3)
belly('glute_lower_fullness', (6.6, -7.5, 83.0), (0, -0.9, -0.45), (1, 0, 0), 5.0, 2.8, 5.0*G('GLUTE', '1'), mask=GM)
chain('infragluteal_fold', [(2.6, -6, 81.8), (6.5, -7, 82.4), (10.5, -6.3, 83.2), (13.0, -4.5, 84.8)], [(0, -0.85, -0.5)]*3, -5.5*G('GLUTE', '1'), 0.9, mask=GM)
belly('glute_medius', (13.0, -4.5, 95.5), (0.75, -0.66, 0), (0, 0, 1), 4.0, 3.5, 5.5*G('GLUTE', '1'), mask=GM)
belly('trochanteric_hollow', (15.3, 1, 85.0), (1, 0, 0), (0, 0, 1), 3.2, 2.8, -5.0*G('HIP', '1'), mask=GM, p=2, K=KK)
belly('tfl', (12.6, 6.5, 90.0), (0.7, 0.7, 0), (0.1, -0.2, -1), 4.0, 2.2, 5.0*G('HIP', '1'), mask=GM)
belly('glute_tfl_groove', (14.6, 2.5, 90.5), (1, 0, 0), (0.05, -0.1, -1), 5.0, 0.8, -2.5*G('HIP', '1'), mask=GM, p=2)
# ---------------- legs
H_, K_, A_ = B.bone('thigh_l'), B.bone('calf_l'), B.bone('foot_l'); ax_t = K_-H_; Lt = np.linalg.norm(ax_t); ax_c = A_-K_; Lc = np.linalg.norm(ax_c)
atp = lambda t: H_+t*ax_t; acp = lambda s: K_+s*ax_c; gL, gC, gK = G('THIGH', '1'), G('CALF', '1'), G('KNEE', '1')
belly('rectus_femoris', atp(0.45)+[0, 6, 0], fr, ax_t, 0.30*Lt, 2.8, 6.0*gL, mask=LEGM)
belly('vastus_lateralis', atp(0.55)+[4.5, 4, 0], (0.75, 0.65, 0), ax_t, 0.30*Lt, 3.4, 8.0*gL, mask=LEGM)
belly('vastus_medialis', atp(0.86)+[-3, 4, 0], (-0.6, 0.8, 0), ax_t, 0.12*Lt, 3.2, 8.5*gL, mask=LEGM)
chain('sartorius_groove', [atp(0.10)+[3.5, 5, 0], atp(0.35)+[1.5, 6, 0], atp(0.60)+[-1.5, 5, 0], atp(0.85)+[-4.0, 2, 0]], [(0.4, 1, 0), (0, 1, 0), (-0.5, 0.85, 0)], -2.0*gL, 1.5, mask=LEGM)
belly('adductors', atp(0.34)+[-4.5, 0.5, 0], (-1, 0.3, 0), ax_t, 0.18*Lt, 3.4, 4.5*gL, mask=LEGM & (np.abs(xa) > 2.5))
belly('biceps_femoris', atp(0.55)+[2.8, -5, 0], (0.5, -0.86, 0), ax_t, 0.30*Lt, 3.0, 7.0*gL, mask=LEGM)
belly('semitendinosus', atp(0.55)+[-2.8, -5, 0], (-0.5, -0.86, 0), ax_t, 0.30*Lt, 3.0, 7.0*gL, mask=LEGM)
belly('hamstring_groove', atp(0.62)+[0, -6, 0], bk, ax_t, 0.22*Lt, 0.8, -3.0*gL, mask=LEGM, p=2)
belly('it_band_groove', atp(0.60)+[6, -1, 0], (1, -0.15, 0), ax_t, 0.24*Lt, 0.9, -3.5*gL, mask=LEGM, p=2)
belly('patella', K_+[0, 5, 3.0], fr, (0, 0, 1), 2.4, 2.2, 4.0*gK, mask=LEGM, p=4, K=KK)
belly('peripatellar_hollow_lat', K_+[2.8, 4, 2.0], (0.6, 0.8, 0), (0, 0, 1), 2.6, 1.6, -2.5*gK, mask=LEGM, p=2, K=KK)
belly('peripatellar_hollow_med', K_+[-2.8, 4, 2.0], (-0.6, 0.8, 0), (0, 0, 1), 2.6, 1.6, -2.5*gK, mask=LEGM, p=2, K=KK)
belly('knee_side_lat', K_+[5, 0, 1.0], (1, 0, 0), (0, 0, 1), 3.5, 3.5, -1.5*gK, mask=LEGM, p=2, K=KK)
belly('knee_side_med', K_+[-5, 0, 1.0], (-1, 0, 0), (0, 0, 1), 3.5, 3.5, -1.5*gK, mask=LEGM, p=2, K=KK)
blob('tibial_tuberosity', K_+[0.3, 4.6, -4.5], 1.3, 2.5*gK)
chain('tibia_anterior_border', [acp(0.12)+[0.6, 4.7, 0], acp(0.45)+[-0.3, 4.4, 0], acp(0.85)+[-1.2, 3.9, 0]], [fr, (-0.2, 1, 0)], 2.0*gC, 1.0, mask=LEGM, K=KK)
belly('gastroc_medial', acp(0.27)+[-2.8, -4, 0], (-0.55, -0.83, 0), ax_c, 7.0, 3.4, 9.0*gC, mask=LEGM)
belly('gastroc_lateral', acp(0.24)+[2.8, -4, 0], (0.55, -0.83, 0), ax_c, 6.0, 3.0, 7.0*gC, mask=LEGM)
belly('gastroc_groove', acp(0.30)+[0, -5, 0], bk, ax_c, 5.5, 0.8, -3.0*gC, mask=LEGM, p=2)
belly('soleus_lat', acp(0.50)+[3.5, -1, 0], (0.95, -0.3, 0), ax_c, 5.0, 2.2, 4.5*gC, mask=LEGM)
belly('soleus_med', acp(0.50)+[-3.5, -1, 0], (-0.95, -0.3, 0), ax_c, 5.0, 2.2, 4.5*gC, mask=LEGM)
belly('achilles_slim_lat', acp(0.78)+[2.5, -1, 0], (1, -0.2, 0), ax_c, 4.0, 2.6, -3.5*gC, mask=LEGM, p=2)
belly('achilles_slim_med', acp(0.78)+[-2.5, -1, 0], (-1, -0.2, 0), ax_c, 4.0, 2.6, -3.5*gC, mask=LEGM, p=2)
belly('tibialis_anterior', acp(0.30)+[2.6, 4, 0], (0.55, 0.83, 0), ax_c, 7.0, 1.9, 4.0*gC, mask=LEGM)
belly('peroneals', acp(0.45)+[3.8, 0.5, 0], (1, 0.1, 0), ax_c, 6.0, 1.6, 3.0*gC, mask=LEGM)
blob('malleolus_med', acp(0.93)+[-3.0, 0.2, 0], 1.5, 2.5*gC)
blob('malleolus_lat', acp(0.95)+[3.3, -0.6, 0], 1.5, 2.5*gC)
# ---------------- arms
U_, El_, Hd_ = B.bone('upperarm_l'), B.bone('lowerarm_l'), B.bone('hand_l'); ua = El_-U_; la = Hd_-El_; lat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(ua))*nrm(ua)); gA_ = G('ARM', '1')
belly('deltoid_lateral', U_+0.18*ua+1.2*lat, lat, ua, 5.5, 4.6, 10.0*gA_, mask=ALL)
belly('deltoid_anterior', U_+0.18*ua+[0, 3, 0], fr, ua, 4.2, 2.5, 6.0*gA_, mask=ALL)
belly('deltoid_posterior', U_+0.18*ua+[0, -3, 0], bk, ua, 4.2, 2.5, 6.0*gA_, mask=ALL)
belly('deltoid_insertion_groove', U_+0.50*ua+1.0*lat, lat, ua, 2.2, 1.9, -2.5*gA_, mask=ARMM, p=2)
belly('biceps', U_+0.58*ua+[0, 2.6, 0], fr, ua, 7.0, 2.3, 5.5*gA_, mask=ARMM)
belly('triceps', U_+0.45*ua+[0, -2.6, 0], bk, ua, 8.0, 2.8, 6.5*gA_, mask=ARMM)
belly('brachialis', U_+0.72*ua+1.0*lat, lat, ua, 3.5, 1.8, 3.0*gA_, mask=ARMM)
blob('olecranon', El_-0.6*nrm(ua)*0+np.array([0, -2.8, 0]), 1.4, 2.5*gA_, mask=ARMM)
flat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(la))*nrm(la)); fmed = -flat
belly('forearm_extensors', El_+0.22*la+1.0*flat, flat, la, 5.5, 2.3, 4.5*gA_, mask=ARMM)
belly('forearm_flexors', El_+0.30*la+1.0*fmed+[0, 1.0, 0], fmed, la, 6.0, 2.4, 4.0*gA_, mask=ARMM)
# ---------------- female fat / skin
belly('lateral_thigh_fullness', (12.5, 3.0, 79.0), (1, 0.1, 0), (0, 0, 1), 7.0, 4.0, 4.0*G('FAT', '1'), mask=LEGM+TORSO > 0, p=2, K=KF)
blob('lower_belly_curve', (0, 15.4, 93.0), 5.0, 2.0*G('FAT', '1'), mirror=False, K=KF)
blob('knee_pad_med', K_+[-2.5, 3.5, 5.0], 2.0, 1.5*G('FAT', '1'), K=KF)
# ---------------- B: breast teardrop (size kept)
AP = {k: np.asarray(v)-np.array([MX, 0, 0]) for k, v in B.P['breast_apex'].items()}
def bmass(A):
    C = A+np.array([0.0, -2.0, -1.5]); d = XR-C; g = np.exp(-((d[:, 0]/5.6)**2+(d[:, 1]/4.4)**2+(d[:, 2]/5.4)**2))
    return g*ss((XR[:, 1]-(A[1]-6.0))/4.5)*ss((np.sign(A[0])*XR[:, 0]-0.8)/1.6)*(arm < 0.25)
for s_, A in AP.items():
    m = bmass(A); sg = np.sign(A[0]); upper = ss((za-A[2]-0.5)/3.0); lower = ss((A[2]-0.8-za)/3.0)
    D[:] += BRS*(-0.35*G('BR_UP', '1'))*(m*upper)[:, None]*N                                   # upper pole flattened (sloping plane from the pectoral)
    D[:] += BRS*(0.55*G('BR_LOW', '1'))*(m*lower)[:, None]*(0.7*N+np.array([0, 0.15, -0.55]))    # lower pole fuller, hanging
    D[:] += BRS*(0.40*G('BR_VOL', '1'))*m[:, None]*N                                               # modest overall volume (reference bust is fuller)
    D[:] += BRS*(0.5)*m[:, None]*np.array([sg*0.55, 0.0, -0.45])                                   # apex lower / lateral
    tail = np.exp(-((sg*xa-12.8)/3.0)**2-((za-126.5)/4.5)**2)*ss((N[:, 1]+0.3)/0.6)*(arm < 0.35)*TORSO
    D[:] += BRS*(0.45*G('BR_TAIL', '1'))*tail[:, None]*N                                            # axillary tail: lateral wall blends into the chest
    med = np.exp(-((sg*xa-2.0)/1.6)**2-((za-126.5)/3.0)**2)*ss((N[:, 1]-0.3)/0.4)*TORSO
    D[:] += BRS*(-0.10)*med[:, None]*N                                                              # cleavage: the two masses do not merge
rep['B_max_mm'] = float(np.linalg.norm(D, axis=1).max()*10)
# crease fill: the base breast meets the chest wall in a hard cut along the lower-lateral IMF and the lateral border (Laplacian concavity up to 1.9 mm);
# push concave vertices out along the normal only (no tangential shrink), lower-medial fold kept softer than the lateral border
Y = XR+D; wfill = np.zeros(NB)
for s_, A in AP.items():
    sg = np.sign(A[0]); dx = (xa-A[0])*sg; dz = za-A[2]; r = np.sqrt(dx**2+dz**2)
    reg = ss((9.5-r)/2.0)*ss((ya-(A[1]-9.5))/2.5)*(1-ss((arm-0.2)/0.15))*ss((np.abs(xa)-2.0)/1.5)*(0.55+0.45*ss((dx-0.5)/2.0))*ss((3.0-dz)/2.0); wfill = np.maximum(wfill, reg)
wfill *= E('A_FILL', '1.0')
for _ in range(int(E('A_FILL_IT', '12'))):
    Nn = B.normals(Y); M = np.asarray([Y[n].mean(0) if len(n) else Y[i] for i, n in enumerate(B.NBR)]); cc_ = np.einsum('ij,ij->i', M-Y, Nn)
    Y += (0.5*wfill*np.maximum(cc_, 0.0))[:, None]*Nn
rep['fill_max_mm'] = float(np.linalg.norm(Y-XR-D, axis=1).max()*10)
# IMF soften (light, after the fill)
wimf = np.zeros(NB)
for s_, A in AP.items():
    dx = xa-A[0]; dz = za-A[2]; band = np.exp(-((np.sqrt((dx/6.0)**2+((dz+5.5)/2.2)**2)-1.0)/0.45)**2)*ss((A[2]-1.0-za)/2.0)*ss((ya-(A[1]-8.0))/3.0)*TORSO; wimf = np.maximum(wimf, band)
for _ in range(int(10*E('A_IMF', '0.2'))):
    M = np.asarray([Y[n].mean(0) if len(n) else Y[i] for i, n in enumerate(B.NBR)]); Y += (0.5*wimf)[:, None]*(M-Y)
# ================= G: guards, smoothing, output
Dtot = Y-XR0
kd = KDTree(len(B.weld))
for j, i in enumerate(B.weld): kd.insert(tuple(XR0[i]), j)
kd.balance(); dseam = np.array([kd.find(tuple(p))[2] for p in XR0])
gz = 1-(1-ss((138.5-z)/2.0))*ss((16.5-np.abs(x))/1.0)   # z-band guard only over the head/body weld span (|x|<15.3); the deltoid cap beyond it stays free
guard = gz*ss((dseam-1.5)/1.5)*(1-ss((hand-0.2)/0.3))*ss((z-11.0)/4.0); Dtot *= guard[:, None]
Dtot = B.smooth_field(Dtot, int(E('A_SMOOTH', '1'))); Dtot *= guard[:, None]
mag = np.linalg.norm(Dtot, axis=1); ids = np.nonzero(mag > 0.002)[0]
rep.update({'verts': int(len(ids)), 'max_mm': float(mag.max()*10), 'p99_mm': float(np.percentile(mag[ids], 99)*10), 'seam_pairs_max_mm': float(mag[B.weld].max()*10), 'prims_peak_mm': prims,
            'env': {k: v for k, v in os.environ.items() if k.startswith('A_') or k in ('CW', 'CD', 'SN', 'SS', 'KM', 'KK', 'KF', 'BR')}})
json.dump({'Body': {'GD41_Body': {str(int(i)): [round(float(v), 5) for v in Dtot[i]] for i in ids}}, 'Head': {}}, open(os.path.join(OUT, 'morph_gd41_body_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'gd41_body_delta_lod0.npy'), Dtot)
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
    json.dump({'Body': {'GD41_Body': res}, 'Head': {}}, open(os.path.join(OUT, f'morph_gd41_body_lod{lod}.json'), 'w')); rep[f'lod{lod}'] = {'verts': len(res), 'far': far}
json.dump(rep, open(os.path.join(OUT, 'gd41_body_report.json'), 'w'), indent=1)
print('GD41ANAT', json.dumps({k: v for k, v in rep.items() if k not in ('env', 'prims_peak_mm')}))
