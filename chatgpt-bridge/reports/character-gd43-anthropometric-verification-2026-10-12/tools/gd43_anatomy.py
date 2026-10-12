"""GD43 anatomy build (user: "work much more on the body anatomy; we are far from a realistic female form and from the references").
One always-on morph GD43_Body over the current neutral (accepted_b2 + BR_Neutral v6 + LK_Neutral). Skeleton / joints unchanged. PROCEDURAL.
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
 B3 breast sculpt on the existing mass (GD43): apex push along a breast axis (BR_ALPHA lateral, BR_BETA down), sternal valley, IMF fold
    groove + lower-pole overhang, upper-pole flatten, lateral tail, areola + nipple; env BR_APEX/LOW/UP/TAIL/VAL/IMF (cm), BR_XC/ZC, BR_R*,
    BR_ARE, BR_NIP (E1 remove-shelf + explicit dome rejected: cones on a flat plate, upper-rim crease at the seam guard)
 F  female fat / skin: lateral upper-thigh fullness, lower-belly curve + pubic mound, knee pads; lower-belly flatten (GD40)
 G  guards: head/body weld band (z 134..143, |x| < 15.3: z-band guard only there, the deltoid cap beyond it is free) + 1.5 cm around the
    92 weld pairs, hands, feet, gluteal cleft for glute fields; 1 Laplacian pass; LOD1-3 transfer.
Candidates: D1 first atlas (ASIS knobs, crest belt, adductor crushed the crotch) -> D2 softer landmarks, depth pivot (front plane fixed at the
waist, back fixed at the pelvis), adductor moved down -> D3 amplitudes up ~1.3x, deltoid cap freed from the z guard, breast fill / volume
-> D4 knee pockets softened (sartorius / peripatellar / knee-side wider and shallower), bigger axillary-tail blend, 12 fill iterations
-> D5 lower back: posterior crest ridge removed, PSIS / sacral hollows halved, lumbar erector higher and lighter (UE clay showed a belt band)
-> D6 the band was the depth pivot: front-fixed waist = 2.5 cm back ledge at z 102-108; pivot now ramps back-fixed (pelvis) -> centre (waist) over z 94-108.
usage: blender -b --factory-startup --python gd43_anatomy.py -- <pkg.json.gz> <lk_lod0.json> <lod_dir> <shape_plan.json> <out_dir>
env: CW CD (block-out strengths), SN SS (section shape), KM (global muscle multiplier, 1.0), KK (landmarks), KF (fat), BR (breast reshape 0..1),
     A_<REGION> per-region multipliers (incl. BR_UP / BR_LOW / BR_VOL / BR_TAIL), A_FILL, A_FILL_IT, A_IMF, A_SMOOTH"""
import sys, json, gzip, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd43_lib import Body, ss, nrm, MX
a_ = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, LODD, PLAN, OUT = a_[:5]; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d)); CW, CD = E('CW', '0.9'), E('CD', '0.8'); SN, SS = E('SN', '2.5'), E('SS', '0.9'); KM, KK, KF, BRS = E('KM', '1.0'), E('KK', '1.0'), E('KF', '1.0'), E('BR', '1.0')
B = Body(PKG, LKJ); NB = B.NB; XR0 = B.XR.copy(); x, y, z = XR0[:, 0], XR0[:, 1], XR0[:, 2]; T = B.T; leg, hand, uarm = B.leg, B.hand, B.uarm
W8 = B.P['weights']; clav = np.asarray([sum(w for b_, w in W8[v].items() if b_.startswith('clavicle')) for v in range(NB)]); larm = np.asarray([sum(w for b_, w in W8[v].items() if b_.startswith('lowerarm')) for v in range(NB)]); arm = B.arm-clav   # true arm: the clavicle weights (0.4-0.6 on the breast, 0.2-0.4 on the upper back) are torso
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
belly('deltoid_lateral', U_+0.18*ua+1.2*lat, lat, ua, 5.5, 4.6, 7.0*gA_, mask=ALL)   # GD43: shoulder breadth at the acromion was at the norm ceiling
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
# ================= B3: breast sculpt on the current mass (GD43 E2+). The base breast is a wide flat mass (4-5 cm thick laterally at x 12, 2.5-3 cm at
# x 6, 1.3 cm at the sternum, top near x 4-8) and the clavicle skin weights hid it from GD41. E1 (remove-shelf + explicit dome) made cones on a flat
# plate; this version shapes the existing mass with smooth bells along explicit directions: apex push (lateral-forward), sternal valley, IMF fold groove
# + lower-pole overhang, upper-pole flatten, lateral tail; areola / nipple after smoothing. All amplitudes in cm via env BR_* (BR = global).
yc_c = 3.0; th = np.arctan2(xa, ya-yc_c); front = np.cos(th) > 0.1
CHEST = front & (arm < 0.45) & (leg < 0.3) & (za > 112) & (za < 136)
def gb(xc, zc, rx_m, rx_l, rz_d, rz_u, p=2.0, q=1.5):   # anisotropic bell in (x, z): radii medial / lateral / down / up, zero slope at the rim
    dx = xa-xc; dz = za-zc; rx = np.where(dx > 0, rx_l, rx_m); rz = np.where(dz > 0, rz_u, rz_d); s = np.sqrt((dx/rx)**2+(dz/rz)**2); return np.clip(1-np.clip(s, 0, 1)**p, 0, 1)**q
BRS = E('BR', '1.0'); apexes = {}; nbv = {}; Dbr = np.zeros_like(XR)
XCA, ZCA = E('BR_XC', '8.5'), E('BR_ZC', '127.0'); al, be = np.radians(E('BR_ALPHA', '20')), np.radians(E('BR_BETA', '8'))
for sg in (1, -1):
    side = CHEST & (xa*sg > -1.5); xs = xa*sg   # xs: lateral-positive coordinate of this side
    dir_ap = nrm([sg*np.sin(al)*np.cos(be), np.cos(al)*np.cos(be), -np.sin(be)])
    def gbs(xc, zc, rx_m, rx_l, rz_d, rz_u, p=2.0, q=1.5):
        dx = xs-xc; dz = za-zc; rx = np.where(dx > 0, rx_l, rx_m); rz = np.where(dz > 0, rz_u, rz_d); s = np.sqrt((dx/rx)**2+(dz/rz)**2); return np.clip(1-np.clip(s, 0, 1)**p, 0, 1)**q*side
    Dbr += (BRS*E('BR_APEX', '2.6')*gbs(XCA, ZCA, E('BR_RM', '5.0'), E('BR_RL', '5.5'), E('BR_RD', '4.5'), E('BR_RU', '5.5'), p=E('BR_P', '2.0'), q=E('BR_Q', '1.5')))[:, None]*dir_ap          # apex: forward + lateral (a normal-facing gate was tried in F7: 15 flips at the gate boundary, reverted)
    Dbr += (BRS*E('BR_LOW', '1.3')*gbs(XCA-0.5, ZCA-2.4, 5.0, 5.0, 1.8, 2.6))[:, None]*nrm([sg*0.15, 0.6, -0.78])                                       # lower pole overhang
    Dbr += (-BRS*E('BR_UP', '0.9')*gbs(XCA-2.0, ZCA+4.0, 5.0, 6.0, 2.5, 2.5))[:, None]*np.array([0, 1.0, 0])                                              # upper pole flattened
    Dbr += (BRS*E('BR_TAIL', '0.5')*gbs(12.5, ZCA+1.0, 2.5, 2.5, 4.0, 4.0))[:, None]*nrm([sg*0.8, 0.6, 0])                                                 # lateral tail
    Dbr += (-BRS*E('BR_LATBACK', '0.0')*gbs(12.6, ZCA, 2.2, 2.6, 4.0, 4.0))[:, None]*nrm([sg*0.45, 0.9, 0])                                              # lateral part back + in: round front instead of a flat shelf
    nbv[sg] = dir_ap
Dbr += (-BRS*E('BR_VAL', '1.4')*np.exp(-(xa/3.2)**2)*gb(0.0, ZCA+0.5, 9.0, 9.0, 5.0, 4.0, p=2.0, q=1.2)*CHEST)[:, None]*np.array([0, 1.0, 0])             # sternal valley (both sides)
D[:] += Dbr
chain('imf_fold', [(2.5, 13.2, 123.6), (6.5, 13.4, 123.0), (10.5, 12.0, 123.2), (13.0, 9.0, 124.5)], [(0, 0.8, -0.6), (0, 0.8, -0.6), (0.3, 0.75, -0.6)], -10.0*BRS*E('BR_IMF', '1.2'), 1.0, mask=CHEST, p=2, K=1.0)
Y = XR+D
for sg in (1, -1):   # apex = the vertex of this side's apex bell region that projects furthest along the breast axis
    region = np.nonzero(CHEST & (xa*sg > 3.0) & (np.abs(za-ZCA) < 4.0))[0]; k = region[np.argmax(Y[region]@nbv[sg])]; apexes[sg] = Y[k].copy()
rep['B_max_mm'] = float(np.linalg.norm(Dbr, axis=1).max()*10); rep['breast'] = {'apex_left': [round(float(v), 2) for v in apexes[1]], 'apex_right': [round(float(v), 2) for v in apexes[-1]]}
# ================= C: anthropometric corrections (GD43) — measured against lean-athletic female norms (gd43_anthro.py): waist section was as deep
# as wide (ratio 1.0; norm 1.2-1.4) from the contaminated reference side silhouette, hips +6 % circumference, upper arm +10 %, wrist -11 %,
# bust points 15 cm apart (norm 18-21.5), knee -2 %. Skeletal deviations (upper arm 10 % short / forearm 3 % long) are reported, not changed.
rowsC = np.arange(78.0, 124.0, 1.0); ycC = []
for zz in rowsC:
    p = B.section(float(zz), (arm < 0.3) & (hand < 0.1), Y)
    ycC.append(0.5*(p[:, 1].max()+p[:, 1].min()) if len(p) >= 8 else np.nan)
ycC = np.asarray(ycC); m_ = np.isnan(ycC); ycC[m_] = np.interp(rowsC[m_], rowsC[~m_], ycC[~m_]); ycv = np.interp(Y[:, 2], rowsC, ycC)
Yc = Y.copy(); zc_ = Y[:, 2]
# waist: breadth x K_WAIST_W, depth x K_WAIST_D about the section centre; band z 103..119 (smooth), torso only, arms excluded
wz = ss((zc_-101.0)/4.0)*ss((121.0-zc_)/4.0)*(1-ss((arm-0.15)/0.2))*(leg < 0.5)
Yc[:, 0] = Y[:, 0]*(1+wz*(E('K_WAIST_W', '1.12')-1)); Yc[:, 1] = ycv+(Y[:, 1]-ycv)*(1+wz*(E('K_WAIST_D', '0.88')-1))
# hips: lateral soft tissue over the trochanters / TFL pushed inward (bell at the widest point), glute apex a little back-to-front
NY = B.normals(Y)
for sg in (1, -1):
    hw = np.exp(-((Y[:, 0]*sg-18.5)/5.0)**2-((zc_-88.0)/6.5)**2-((Y[:, 1]-2.0)/7.0)**2)*(Y[:, 0]*sg > 9.0)*(hand < 0.1)*ss((NY[:, 0]*sg-0.3)/0.4)
    Yc[:, 0] -= sg*E('HIP_IN', '1.0')*hw
    gw = np.exp(-((Y[:, 0]*sg-8.0)/5.5)**2-((zc_-86.5)/6.0)**2)*(Y[:, 1] < -4.0)*(np.abs(Y[:, 0]) > 1.5)*ss((-NY[:, 1]-0.3)/0.4)*(hand < 0.1)
    Yc[:, 1] += E('GL_BACK', '0.5')*gw
# upper arm: radial x K_UARM about the humerus axis (t 0.15..0.85 smooth); wrist: radial x K_WRIST around the wrist joint; knee: x K_KNEE about the knee joint
for s_, sg in (('l', 1), ('r', -1)):
    U = B.bone(f'upperarm_{s_}'); El = B.bone(f'lowerarm_{s_}'); Hd = B.bone(f'hand_{s_}'); ua = El-U; nua = nrm(ua); la = Hd-El; nla = nrm(la)
    side = (Y[:, 0]*sg > 0)
    t = ((Y-U)@nua)/np.linalg.norm(ua); foot = U+np.outer(t*np.linalg.norm(ua), nua); rvec = Y-foot
    w_ua = ss((t-0.12)/0.12)*ss((0.88-t)/0.12)*(uarm > 0.4)*side*ss((7.0-np.linalg.norm(rvec, axis=1))/1.5); Yc += (w_ua*(E('K_UARM', '0.91')-1))[:, None]*rvec   # only within the arm's own radius: lateral-chest verts carry upperarm weight too (stretch trap)
    tw = ((Y-Hd)@nla)   # cm along the forearm axis from the wrist joint (+ into the hand)
    footw = Hd+np.outer(tw, nla); rw_ = Y-footw; w_wr = np.exp(-((tw+2.0)/4.0)**2)*((larm > 0.3) | (hand > 0.3))*(hand < 0.93)*side*(np.linalg.norm(rw_, axis=1) < 5.0)   # distal forearm + wrist (styloid level)
    Yc += (w_wr*(E('K_WRIST', '1.12')-1))[:, None]*rw_
    K_ = B.bone(f'calf_{s_}'); dk = Y-K_; w_k = np.exp(-(dk[:, 2]/4.0)**2)*(leg > 0.5)*side*(np.linalg.norm(dk[:, :2], axis=1) < 9.0); rk = np.stack([dk[:, 0], dk[:, 1], np.zeros(NB)], 1)
    Yc += (w_k*(E('K_KNEE', '1.035')-1))[:, None]*rk
rep['C_max_mm'] = float(np.linalg.norm(Yc-Y, axis=1).max()*10); Y = Yc
# ================= G: guards, smoothing, output
Dtot = Y-XR0
kd = KDTree(len(B.weld))
for j, i in enumerate(B.weld): kd.insert(tuple(XR0[i]), j)
kd.balance(); dseam = np.array([kd.find(tuple(p))[2] for p in XR0])
gz = 1-(1-ss((138.5-z)/2.0))*ss((16.5-np.abs(x))/1.0)   # z-band guard only over the head/body weld span (|x|<15.3); the deltoid cap beyond it stays free
dwr = np.minimum(((XR0-B.bone('hand_l'))@nrm(B.bone('hand_l')-B.bone('lowerarm_l'))), ((XR0-B.bone('hand_r'))@nrm(B.bone('hand_r')-B.bone('lowerarm_r'))))   # cm past the nearer wrist joint
guard = gz*ss((dseam-1.5)/1.5)*(1-ss((hand-0.2)/0.3)*ss((dwr-2.5)/2.5))*ss((z-11.0)/4.0); Dtot *= guard[:, None]   # hand guard starts 2.5 cm past the wrist joint (wrist band stays editable)
Dtot = B.smooth_field(Dtot, int(E('A_SMOOTH', '1'))); Dtot *= guard[:, None]
Yf = XR0+Dtot
for sg in (1, -1):   # areola disc + nipple on the final surface (after smoothing so the point is not spread), guard applied
    A = apexes[sg]; dd = np.linalg.norm(Yf-A, axis=1); nb = nbv[sg]
    bump = E('BR_ARE', '0.15')*np.exp(-(dd/2.0)**4)+E('BR_NIP', '0.30')*np.exp(-(dd/0.9)**2); Dtot += (bump*guard*CHEST)[:, None]*nb
mag = np.linalg.norm(Dtot, axis=1); ids = np.nonzero(mag > 0.002)[0]
rep.update({'verts': int(len(ids)), 'max_mm': float(mag.max()*10), 'p99_mm': float(np.percentile(mag[ids], 99)*10), 'seam_pairs_max_mm': float(mag[B.weld].max()*10), 'prims_peak_mm': prims,
            'env': {k: v for k, v in os.environ.items() if k.startswith('A_') or k in ('CW', 'CD', 'SN', 'SS', 'KM', 'KK', 'KF', 'BR')}})
json.dump({'Body': {'GD43_Body': {str(int(i)): [round(float(v), 5) for v in Dtot[i]] for i in ids}}, 'Head': {}}, open(os.path.join(OUT, 'morph_gd43_body_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'gd43_body_delta_lod0.npy'), Dtot)
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
    json.dump({'Body': {'GD43_Body': res}, 'Head': {}}, open(os.path.join(OUT, f'morph_gd43_body_lod{lod}.json'), 'w')); rep[f'lod{lod}'] = {'verts': len(res), 'far': far}
json.dump(rep, open(os.path.join(OUT, 'gd43_body_report.json'), 'w'), indent=1)
print('GD43ANAT', json.dumps({k: v for k, v in rep.items() if k not in ('env', 'prims_peak_mm')}))
