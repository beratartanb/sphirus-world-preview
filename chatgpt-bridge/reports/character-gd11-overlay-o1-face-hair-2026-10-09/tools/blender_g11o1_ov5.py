"""pass O1: 5-VIEW OVERLAY of a candidate on the 6-view reference panels (front, r34, l34, rprof, lprof), SAME image-based method on both sides.
Alignment: MetaHuman tracker curves on the reference panel and on the candidate capture crop (blender_g11o1_prep.py + ue_gd14_track.py);
least-squares similarity (scale, rotation, shift) capture -> panel from anchors that this pass does not edit:
  front / 3/4: both eye-opening centroids + both mouth corners; profiles: near-eye centroid + mouth corner + lip front point.
Lines extracted from BOTH images (reference panel and warped candidate capture) with the same code:
  outer face contour per row (skin key sampled on the cheek of each image; front both sides, 3/4 nose side and ear side, profile front edge),
  jaw-bottom line per column (strongest downward darkening under the jaw; front and 3/4), under-chin edge per column (profiles, background below),
  landmark rows: brow line (darkest band above the eyes), eye line, nose base (philtrum top), mouth line, chin base.
Rows are banded by t = (y - eye line) / (mouth line - eye line) of the REFERENCE: brow -0.45..-0.15, zygomatic 0.15..0.35, cheek mass 0.35..0.6,
lower cheek 0.6..0.9, mouth 0.9..1.1, jaw body 1.1..1.45; jaw-bottom columns by u = |x - chin centre| / half face width: chin base <0.12,
chin side 0.12..0.35, jaw body 0.35..0.7. mm from the candidate camera scale (px per cm at the face) * similarity scale.
Signs: contour + = candidate OUTSIDE the reference (wider / more forward); jaw-bottom / under-chin / landmark rows + = candidate LOWER.
Writes <out_dir>/<label>_<view>.png (reference+lines | 50 % blend+lines | candidate+lines; cyan = reference, magenta = candidate) and <label>_ov5.json.
CANDIDATE contours (outer face contour, profile front edge, under-chin) come from the GEOMETRY: rendered head = postrig + (head - base), projected
with the capture camera and the same similarity (keying the UE skin fails on shaded cheeks); jaw-bottom and brow lines are image-based on both.
Profiles are superimposed on nasion (deepest point of the front edge between brow and eye rows) + near-eye centroid + mouth corner.
usage: blender -b --python blender_g11o1_ov5.py -- <tracks.json> <cand track prefix> <crop dir> <capture dir> <capture prefix> <out dir> <label> <head.npy> <base.npy> <postrig.npy>"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; TRK, CT, TD, CD, CP, OD, LAB = a[:7]; TR = json.load(open(TRK)); os.makedirs(OD, exist_ok=True)
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import SEG
NH = 24049; MX = -0.23; GEO = np.load(a[9])[:NH]+(np.load(a[7])[:NH]-np.load(a[8])[:NH])
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]; Gs = GEO[SOFT]; axs = np.abs(Gs[:, 0]+0.23)
KEEP = ~((axs > 6.2) & (Gs[:, 1] < 4.6) & (Gs[:, 2] > 154.0) & (Gs[:, 2] < 168.0)) & (Gs[:, 1] > -3.0) & (Gs[:, 2] > 145.0)
for sd in (1, -1): KEEP &= np.linalg.norm(Gs-np.array([-0.23+sd*2.97, 10.5, 162.25]), axis=1) > 1.3
KV = np.zeros(NH, bool); KV[SOFT[KEEP]] = True
from id_common import pkg
TRI = np.asarray(pkg()["head"]["triangles"]); TRI = TRI[(TRI < NH).all(1)]; TRI = TRI[KV[TRI].all(1)]
NS = 4; BW = np.array([(i/NS, j/NS, 1-i/NS-j/NS) for i in range(NS+1) for j in range(NS+1-i)])   # barycentric samples: dense silhouette (vertex spacing ~2.5 mm)
Gs = np.einsum("sk,tkc->tsc", BW, GEO[TRI]).reshape(-1, 3)
mid = GEO[(np.abs(GEO[:, 0]-MX) < 0.12) & (GEO[:, 1] > 5.0)]; zb = np.round(mid[:, 2]/0.05).astype(int); PROF = {}
for zi, yv in zip(zb, mid[:, 1]): PROF[zi] = max(PROF.get(zi, -1e9), yv)
PZ = np.array(sorted(PROF))*0.05; PY = np.array([PROF[k] for k in sorted(PROF)])
def plm3():   # candidate profile landmarks from the 3D midline: nasion, pronasale, subnasale
    g = (PZ > 163.5) & (PZ < 167.0); zg = PZ[g][np.argmax(PY[g])]; n_ = (PZ > 160.5) & (PZ < zg); zn = PZ[n_][np.argmin(PY[n_])]
    p_ = (PZ > 155.5) & (PZ < 161.0); zp = PZ[p_][np.argmax(PY[p_])]; sub = np.nonzero((PZ < zp) & (PZ > 154.5))[0][::-1]; best = 1e9; zs = zp
    for i in sub:
        if PY[i] < best: best, zs = PY[i], PZ[i]
        elif PY[i] > best+0.08: break
    P = np.array([[MX, PROF[int(round(z/0.05))], z] for z in (zn, zp, zs)]); print("PLM3 nasion z %.2f y %.2f | prn z %.2f y %.2f | sn z %.2f y %.2f" % (zn, P[0, 1], zp, P[1, 1], zs, P[2, 1])); return P
R6 = 'Saved/Codex/GD11_LikenessW_20261006/ref/ref6_%s.png'
VIEWS = [('front', 'front_f', 0), ('r34', 'q3R_f', 1), ('l34', 'q3L_f', -1), ('rprof', 'profR', 1), ('lprof', 'profL', -1)]
ONLY = os.environ.get('OV5_VIEWS', '').split(',') if os.environ.get('OV5_VIEWS') else None
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.array(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3].copy(); bpy.data.images.remove(im); return x
def save(O, p):
    h, w = O.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(O, 0, 1); o = bpy.data.images.new('o', w, h); o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel())
    o.filepath_raw = os.path.abspath(p); o.file_format = 'PNG'; o.save(); bpy.data.images.remove(o)
def basis(cam):
    x, y, z, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
    return np.array([x, y, z], float), np.array([cy*cp, sy*cp, sp]), np.array([-sy, cy, 0.0]), np.array([-cy*sp, -sy*sp, cp])
def cproj(cam, fov, W, H, P):
    o, f, r, u = basis(cam); t = math.tan(math.radians(fov)/2); d = np.asarray(P, float)-o; dd = d@f; return np.stack([(0.5+0.5*(d@r)/dd/t)*W, (0.5-0.5*(d@u)/dd/t)*H], -1)
def curves(tag): return {k: np.asarray(v, float) for k, v in TR[tag]['curves'].items()}
def anchors(c, prof, side):
    eyes = []
    for s in ('l', 'r'):
        P = np.vstack([c['crv_eyelid_upper_'+s], c['crv_eyelid_lower_'+s]]); eyes.append((np.ptp(P[:, 0]), P.mean(0)))
    L = np.vstack([c[k] for k in c if k.startswith('crv_lip_') and 'outer' in k])
    if prof:
        e = max(eyes, key=lambda q: q[0])[1]; return np.array([e, L[np.argmin(L[:, 0]*side)], L[np.argmax(L[:, 0]*side)]])
    E = sorted([q[1] for q in eyes], key=lambda p: p[0]); return np.array([E[0], E[1], L[np.argmin(L[:, 0])], L[np.argmax(L[:, 0])]])
def sim(A, B):
    mA, mB = A.mean(0), B.mean(0); A0, B0 = A-mA, B-mB; U, S, Vt = np.linalg.svd(B0.T@A0); D = np.diag([1, np.sign(np.linalg.det(U@Vt))]); Rm = U@D@Vt
    s = np.trace(np.diag(S)@D)/(A0**2).sum(); return s, Rm, mB-s*(Rm@mA)
def bilinear(C, src):
    h, w = C.shape[:2]; x = np.clip(src[:, 0]-0.5, 0, w-1.001); y = np.clip(src[:, 1]-0.5, 0, h-1.001); x0 = x.astype(int); y0 = y.astype(int); fx = (x-x0)[:, None]; fy = (y-y0)[:, None]
    return C[y0, x0]*(1-fx)*(1-fy)+C[y0, x0+1]*fx*(1-fy)+C[y0+1, x0]*(1-fx)*fy+C[y0+1, x0+1]*fx*fy
def box(img, k):   # separable box blur
    o = img.copy()
    for ax_ in (0, 1):
        c = np.cumsum(np.pad(o, [(k, k) if i == ax_ else (0, 0) for i in range(o.ndim)], mode='edge'), axis=ax_)
        o = (np.take(c, range(2*k, c.shape[ax_]), axis=ax_)-np.take(c, range(0, c.shape[ax_]-2*k), axis=ax_))/(2*k)
    return o
def lines(I, c, prof, side, t_ref=None):
    """extract contour / jaw / landmark lines from image I (reference frame) with its own tracker curves c (reference-frame px)"""
    h, w = I.shape[:2]; mx = I.max(-1); mn = I.min(-1); S = I.sum(-1)+1e-6; cr = I[..., 0]/S; cg = I[..., 1]/S; chroma = mx-mn
    A = anchors(c, prof, side)
    if prof: E = A[:1]; Mc = A[1:2]; ey = A[0, 1]; my = A[1, 1]
    else: E = A[:2]; Mc = A[2:]; ey = E[:, 1].mean(); my = Mc[:, 1].mean()
    if not prof:
        inner = np.vstack([c[k] for k in c if k.startswith('crv_lip_') and 'inner' in k]); my = inner[:, 1].mean()
    d = my-ey
    # skin sample on the cheek(s)
    pts = []
    if side == 0: pts = [(E[0, 0], ey+0.5*d), (E[1, 0], ey+0.5*d)]
    elif not prof: pts = [(E[0, 0] if side > 0 else E[1, 0], ey+0.5*d)]
    else: pts = [(Mc[0, 0]-side*0.35*d, ey+0.55*d)]
    smp = np.vstack([np.c_[cr[int(y)-4:int(y)+5, int(x)-4:int(x)+5].ravel(), cg[int(y)-4:int(y)+5, int(x)-4:int(x)+5].ravel(), mx[int(y)-4:int(y)+5, int(x)-4:int(x)+5].ravel()] for x, y in pts])
    c0 = np.median(smp, 0); TOL = float(os.environ.get('OV5_TOL', '0.045'))
    skin = (np.hypot(cr-c0[0], cg-c0[1]) < TOL) & (mx > 0.38*c0[2]) & (mx < 1.8*c0[2])
    bgc = np.median(np.r_[chroma[:15, :15].ravel(), chroma[:15, -15:].ravel()]); lum = I.mean(-1); bgl = np.median(np.r_[lum[:15, :15].ravel(), lum[:15, -15:].ravel()])
    subj = (chroma > bgc+0.04) | (np.abs(lum-bgl) > 0.12)   # non-background (profile front edge: the nose bridge highlight fails the skin key)
    for _ in range(1): skin = skin & (np.roll(skin, 1, 1) | np.roll(skin, -1, 1))
    out = dict(ey=ey, my=my, d=d, E=E.tolist(), M=Mc.tolist(), skinpts=pts)
    # outer contour rows
    cont = {}
    def walk(y, x, dirn, tol=3):
        x = int(x); n = 0
        while 0 <= x < w and not skin[y, x] and n < int(0.35*d): x += dirn; n += 1
        if not (0 <= x < w) or not skin[y, x]: return None
        gap = 0
        while 0 < x+dirn < w-1 and (skin[y, x+dirn] or gap < tol):
            gap = 0 if skin[y, x+dirn] else gap+1; x += dirn
        return x-dirn*gap
    RUN = int(os.environ.get('OV5_RUN', '7'))
    def from_border(y, dirn, lim, M=None):   # dirn +1: scan from left border rightward; first run of RUN mask px (hair strands are thinner)
        M = skin if M is None else M
        xs = range(0, w-RUN) if dirn > 0 else range(w-1, RUN-1, -1)
        for x in xs:
            if (dirn > 0 and x > lim) or (dirn < 0 and x < lim): return None
            if dirn > 0 and M[y, x:x+RUN].all(): return x
            if dirn < 0 and M[y, x-RUN+1:x+1].all(): return x
        return None
    y0 = int(ey-1.45*d); y1 = int(my+1.5*d)
    for y in range(max(y0, 2), min(y1, h-2)):
        row = {}
        if side == 0:
            row['L'] = walk(y, E[0, 0], -1); row['R'] = walk(y, E[1, 0], +1)
        elif not prof:
            row['far'] = from_border(y, -side, E[:, 0].mean())
        else:
            row['far'] = from_border(y, -side, E[0, 0]-side*0.2*d, subj)
        cont[y] = row
    out['cont'] = cont
    # jaw-bottom line (front / 3/4): strongest darkening going down under the jaw, per column
    jaw = {}
    if not prof:
        L = box(box(I.mean(-1), 2).T, 1).T; g = np.zeros_like(L); g[3:-3] = L[6:]-L[:-6]
        cx = Mc[:, 0].mean(); hw = 1.2*d
        for x in range(int(cx-hw), int(cx+hw)):
            if not 0 <= x < w: continue
            ya, yb = int(my+0.3*d), min(int(my+1.5*d), h-4)
            col = g[ya:yb, x].copy(); ok = skin[ya-3:yb-3, x] | skin[max(ya-6, 0):yb-6, x]
            col[~ok] = 0
            if col.min() < -0.03: jaw[x] = ya+int(np.argmin(col))
        out['cx'] = cx
    out['jaw'] = jaw
    # under-chin edge (profiles): first background pixel below the chin, per column
    und = {}
    if prof:
        fr = [v['far'] for y, v in cont.items() if v.get('far') is not None and my+0.5*d < y < my+1.3*d]
        cfx = (max(fr) if side > 0 else min(fr)) if fr else Mc[0, 0]+side*0.3*d
        for x in range(int(min(cfx, cfx-side*1.4*d)), int(max(cfx, cfx-side*1.4*d))):
            ya = int(my+0.4*d); yb = min(int(my+2.0*d), h-1); col = subj[ya:yb, x] | skin[ya:yb, x]
            if not col[0]: continue
            r = np.nonzero(~col)[0]
            if len(r): und[x] = ya+int(r[0])
        out['cfx'] = cfx
    out['und'] = und
    # landmark rows
    L2 = box(I.mean(-1), 2); bl = []
    for e in E:
        for x in range(int(e[0]-0.25*d), int(e[0]+0.25*d)):
            ya, yb = int(ey-0.62*d), int(ey-0.14*d)
            if 0 <= x < w and ya > 0: bl.append(ya+int(np.argmin(L2[ya:yb, x])))
    out['brow'] = float(np.median(bl)) if bl else None
    ph = [c[k] for k in c if 'philtrum' in k]
    out['nosebase'] = float(np.vstack(ph)[:, 1].min()) if ph and not prof else None
    if not prof and jaw:
        cc = [jaw[x] for x in jaw if abs(x-out['cx']) < 0.12*d]; out['chin'] = float(np.median(cc)) if cc else None
    elif prof and und:
        xs = sorted(und, key=lambda x: -x*side)[:max(len(und)//8, 1)]; out['chin'] = float(np.median([und[x] for x in xs]))
    else: out['chin'] = None
    return out
REPORT = {}; YAW = {}
def nasion(edge, ey, d, side):   # edge: {row: x}; most posterior front-edge point between brow and eye rows
    ys = sorted(y for y, x in edge.items() if x is not None and ey-0.5*d <= y <= ey+0.1*d)
    if len(ys) < 5: return None
    xs = np.array([edge[y] for y in ys], float); xm = np.array([np.median(xs[max(i-3, 0):i+4]) for i in range(len(xs))])   # median filter: hair strands at the brow
    yv = np.array(ys, float); g = np.nonzero(yv <= ey-0.15*d)[0]
    gi = int(g[np.argmax(xm[g]*side)]) if len(g) else 0   # glabella: most anterior point above the eye; nasion: deepest point below it
    i = gi+int(np.argmin(xm[gi:]*side)); print('GLABELLA row %d x %.1f' % (ys[gi], xm[gi])); print('NASION row %d x %.1f (rows %d..%d, eye %.0f)' % (ys[i], xm[i], ys[0], ys[-1], ey)); return np.array([xm[i], ys[i]], float)
def nose_lm(edge, ey, d, side):   # pronasale (most anterior point between eye and mouth rows) and subnasale (deepest point between it and the upper lip)
    ys = sorted(y for y, x in edge.items() if x is not None and ey <= y <= ey+0.95*d)
    xs = np.array([edge[y] for y in ys], float); xm = np.array([np.median(xs[max(i-2, 0):i+3]) for i in range(len(xs))]); yv = np.array(ys, float)
    p = int(np.argmax(np.where(yv <= ey+0.75*d, xm*side, -1e9))); m = np.nonzero((yv > yv[p]) & (yv <= ey+0.85*d))[0]
    sn = p; best = xm[p]*side   # first local minimum below the nose tip (the upper lip may slant further back than subnasale)
    for i in m:
        if xm[i]*side < best: best, sn = xm[i]*side, int(i)
        elif xm[i]*side > best+max(1.5, 0.012*d): break
    print('NOSE prn row %d x %.1f | sn row %d x %.1f' % (ys[p], xm[p], ys[sn], xm[sn])); return np.array([xm[p], ys[p]], float), np.array([xm[sn], ys[sn]], float)
def gedge(q, rows, fn, axis=1):   # per-row (axis 1) or per-column (axis 0) extreme of the dense projected samples
    rows = list(rows); r0 = min(rows); idx = np.round(q[:, axis]).astype(int)-r0; ok = (idx >= 0) & (idx < max(rows)-r0+1); v = q[ok, 1-axis]; idx = idx[ok]
    big = fn is np.max; acc = np.full(max(rows)-r0+1, -1e9 if big else 1e9); (np.maximum if big else np.minimum).at(acc, idx, v)
    return {y: (int(round(acc[y-r0])) if abs(acc[y-r0]) < 1e8 else None) for y in rows}
for rv, cv, side in VIEWS:
    if ONLY and rv not in ONLY: continue
    prof = 'prof' in rv
    R = load(R6 % rv); h, w = R.shape[:2]
    MIR = rv == 'l34' and os.environ.get('OV5_MIRROR_L34', '1') == '1'   # the 6-view sheet shows BOTH 3/4 panels from the same side: mirror l34 for the left 3/4
    if MIR: R = R[:, ::-1].copy()
    CJ = json.load(open(os.path.join(CD, '%s_%s_custom.json' % (CP, cv)))); C = load(os.path.join(CD, '%s_%s_custom.png' % (CP, cv))); cam, fov = CJ['cam'], float(CJ['fov'])
    KJ = json.load(open(os.path.join(TD, '%s_%s.json' % (CT, cv)))); k = KJ['side']/KJ['out']
    cr_ = curves('ref6_'+rv)
    if MIR: cr_ = {(n[:-2]+{'_l': '_r', '_r': '_l'}[n[-2:]] if n[-2:] in ('_l', '_r') else n): np.c_[w-p[:, 0], p[:, 1]] for n, p in cr_.items()}   # mirrored: left / right curve names swap
    cc_ ={n: np.c_[KJ['x0']+p[:, 0]*k, KJ['y0']+p[:, 1]*k] for n, p in curves('%s_%s' % (CT, cv)).items()}
    LR = lines(R, cr_, prof, side); d = LR['d']; ey = LR['ey']
    qc = cproj(cam, fov, C.shape[1], C.shape[0], Gs)   # candidate geometry in capture px
    Ar = anchors(cr_, prof, side); Ac = anchors(cc_, prof, side)
    if prof:
        # upper-face superimposition on the profile line: nasion + pronasale + subnasale (reference: background-keyed edge, candidate: geometry);
        # candidate eye / mouth rows from the 3D eye centre and stomion height (the tracker is unreliable on the candidate profile)
        er = {y: v.get('far') for y, v in LR['cont'].items()}; nr = nasion(er, ey, d, side); pr_, sr_ = nose_lm(er, ey, d, side)
        # profile panels are drawn ~13 % smaller than front / 3/4 -> free scale; rotation 0 (level cameras); scale from the eye -> stomion height
        # (same rule as front / 3/4: eyes + mouth), horizontal position from nasion. Candidate: near-eye centre / stomion / nasion from 3D.
        Pc = cproj(cam, fov, C.shape[1], C.shape[0], np.vstack([[[MX-side*2.97, 10.5, 162.25], [MX, 12.0, 155.05]], plm3()]))
        inner = np.vstack([cr_[k_] for k_ in cr_ if k_.startswith('crv_lip_') and 'inner' in k_]); myr = inner[:, 1].mean()
        s = (myr-ey)/(Pc[1, 1]-Pc[0, 1]); Rm = np.eye(2); t = np.array([nr[0]-s*Pc[2, 0], 0.5*((ey-s*Pc[0, 1])+(myr-s*Pc[1, 1]))])
        Ar = np.array([[np.nan, ey], [np.nan, myr], nr, pr_, sr_]); Ac = Pc
        res = np.r_[np.abs(Pc[:2, 1]*s+t[1]-Ar[:2, 1]), np.linalg.norm(Pc[2:]*s+t-Ar[2:], axis=1)]
        print('PROFALIGN', rv, 'scale %.4f | nasion res %.1f px, pronasale dx %+.1f dy %+.1f px, subnasale dx %+.1f dy %+.1f px' % ((s, res[2])+tuple((Pc[3]*s+t-pr_))+tuple((Pc[4]*s+t-sr_))))
    else:
        s, Rm, t = sim(Ac, Ar); res = np.linalg.norm((Ac@Rm.T)*s+t-Ar, axis=1)
    yy, xx = np.mgrid[0:h, 0:w]; dst = np.stack([xx.ravel()+0.5, yy.ravel()+0.5], 1); src = ((dst-t)@Rm)/s; Cw = bilinear(C, src).reshape(h, w, 3)
    cw_ = {n: (p@Rm.T)*s+t for n, p in cc_.items()}; q = (qc@Rm.T)*s+t
    P2 = cproj(cam, fov, C.shape[1], C.shape[0], np.array([[MX, 10.0, 157.0], [MX, 10.0, 159.0]])); pxcm = np.linalg.norm(P2[1]-P2[0])/2*s   # ref px per cm
    LC = lines(Cw, cw_, prof, side)   # image-based: jaw-bottom, brow, landmark rows
    rows = list(LR['cont'].keys())
    if side == 0: gl, gr = gedge(q, rows, np.min), gedge(q, rows, np.max); LC['cont'] = {y: {'L': gl[y], 'R': gr[y]} for y in rows}
    else: gf = gedge(q, rows, np.max if side > 0 else np.min); LC['cont'] = {y: {'far': gf[y]} for y in rows}
    if prof:
        ok = (Gs[:, 2] > 148.0) & (Gs[:, 1] > 1.0); und = {x: v for x, v in gedge(q[ok], LR['und'].keys(), np.max, axis=0).items() if v is not None} if LR['und'] else {}
        LC['und'] = und
        xs = sorted(und, key=lambda x: -x*side)[:max(len(und)//8, 1)]; LC['chin'] = float(np.median([und[x] for x in xs])) if und else None
    if not prof:   # rough yaw from the eye spacing / eye-mouth height ratio (reference vs candidate; front view = 0 deg)
        YAW.setdefault('ratio', {})[rv] = dict(ref=float(np.ptp(Ar[:2, 0])/d), cand=float(np.ptp(Ac[:2, 0])/(np.mean(Ac[2:, 1])-np.mean(Ac[:2, 1]))))
    def tband(y): return (y-ey)/d
    BANDS = [('forehead', -1.2, -0.5), ('brow', -0.45, -0.15), ('zygomatic', 0.15, 0.35), ('cheek_mass', 0.35, 0.6), ('lower_cheek', 0.6, 0.9), ('mouth', 0.9, 1.1), ('jaw_body', 1.1, 1.45)]
    rep = dict(view=rv, anchor_res_px=res.round(1).tolist(), scale=round(s, 5), t=[round(float(v), 3) for v in t], rot_deg=round(math.degrees(math.atan2(Rm[1, 0], Rm[0, 0])), 2), px_per_cm=round(pxcm, 2), contour={}, jaw={}, under={}, rows={})
    for key, sgn in (('L', -1), ('R', 1), ('far', side)):
        for nm, b0, b1 in BANDS:
            dd = [(LC['cont'][y][key]-LR['cont'][y][key])*sgn for y in LR['cont'] if b0 <= tband(y) < b1 and LR['cont'][y].get(key) is not None and LC['cont'].get(y, {}).get(key) is not None]
            if len(dd) >= 3: rep['contour'].setdefault(key, {})[nm] = round(float(np.median(dd))/pxcm*10, 1)
    if LR['jaw'] and LC['jaw']:
        hw = max(abs(x-LR['cx']) for x in LR['jaw'])
        for nm, u0, u1 in (('chin_base', 0, 0.12), ('chin_side', 0.12, 0.35), ('jaw_body', 0.35, 0.7), ('jaw_back', 0.7, 1.01)):
            for sd, sg in (('L', -1), ('R', 1)):
                dd = [LC['jaw'][x]-LR['jaw'][x] for x in LR['jaw'] if x in LC['jaw'] and u0 <= abs(x-LR['cx'])/hw < u1 and (x-LR['cx'])*sg >= 0]
                if len(dd) >= 3: rep['jaw'][nm+'_'+sd] = round(float(np.median(dd))/pxcm*10, 1)
    if LR['und'] and LC['und']:
        xs = sorted(set(LR['und']) & set(LC['und']), key=lambda x: -x*side); n = len(xs)
        for nm, f0, f1 in (('chin_front', 0, 0.25), ('under_chin', 0.25, 0.6), ('submandibular', 0.6, 1.0)):
            dd = [LC['und'][x]-LR['und'][x] for x in xs[int(f0*n):max(int(f1*n), int(f0*n)+1)]]
            if dd: rep['under'][nm] = round(float(np.median(dd))/pxcm*10, 1)
    for nm in ('brow', 'nosebase', 'chin'):
        if LR.get(nm) is not None and LC.get(nm) is not None: rep['rows'][nm] = round((LC[nm]-LR[nm])/pxcm*10, 1)
    if not prof:   # inner lines from the same tracker on both images: mean offset (dx + = toward image right, dy + = down) and shape rms after removing it, mm
        def rs_(P, n=40):
            P = np.asarray(P, float); sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; tt = np.linspace(0, sl[-1], n); return np.c_[np.interp(tt, sl, P[:, 0]), np.interp(tt, sl, P[:, 1])]
        cv_ = {}
        for kname in sorted(cr_):
            if kname not in cw_ or 'eyelid' in kname: continue
            r_ = rs_(cr_[kname]); c_ = rs_(cw_[kname])
            if np.linalg.norm(r_[0]-c_[-1]) < np.linalg.norm(r_[0]-c_[0]): c_ = c_[::-1]
            dv = (c_-r_).mean(0); shp = np.sqrt((((c_-dv)-r_)**2).sum(1).mean())
            cv_[kname.replace('crv_', '')] = dict(dx=round(float(dv[0])/pxcm*10, 1), dy=round(float(dv[1])/pxcm*10, 1), shape=round(float(shp)/pxcm*10, 1), dlen=round(float(np.ptp(c_[:, 1])-np.ptp(r_[:, 1]))/pxcm*10, 1))
        rep['curves'] = cv_
    rep['rows']['eye'] = round((LC['ey']-LR['ey'])/pxcm*10, 1); rep['rows']['mouth'] = round((LC['my']-LR['my'])/pxcm*10, 1)
    rep['chin_height_mm'] = dict(ref=round((LR['chin']-LR['my'])/pxcm*10, 1) if LR.get('chin') else None, cand=round((LC['chin']-LC['my'])/pxcm*10, 1) if LC.get('chin') else None)
    if os.environ.get('OV5_HAIR') == '1':   # HAIR SILHOUETTE (same alignment): background-keyed head+hair mass, flyaways removed by a 2 px opening
        def hsil(I):
            mx_ = I.max(-1); chroma_ = mx_-I.min(-1); lum_ = I.mean(-1)
            bc = np.median(np.r_[chroma_[:12, :12].ravel(), chroma_[:12, -12:].ravel()]); bl = np.median(np.r_[lum_[:12, :12].ravel(), lum_[:12, -12:].ravel()])
            m = (chroma_ > bc+0.05) | (np.abs(lum_-bl) > 0.10)
            for _ in range(2): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
            for _ in range(2): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
            return m
        MR, MC = hsil(R), hsil(Cw)
        if not prof: MC[int(LR['my']+1.2*d):] = MR[int(LR['my']+1.2*d):] = False   # the studio floor plate sits below the chin in the captures
        def extents(M):
            ex = {}
            for y in range(max(int(ey-3.4*d), 0), min(int(ey+1.6*d), h)):
                c_ = np.nonzero(M[y])[0]
                if len(c_): ex[y] = (int(c_.min()), int(c_.max()))
            top = min(ex) if ex else None; return ex, top
        ER, TR_ = extents(MR); EC, TC_ = extents(MC)
        HB = [('crown', -2.6, -1.6), ('upper_side', -1.6, -0.8), ('temple_eartop', -0.8, 0.0), ('ear', 0.0, 0.6), ('below_ear_nape', 0.6, 1.4)]
        hr = {'top_mm': round((TR_-TC_)/pxcm*10, 1) if TR_ is not None and TC_ is not None else None}
        keys = (('left', 0, -1), ('right', 1, 1)) if side == 0 else ((('back' if prof else 'ear_side'), 0 if side > 0 else 1, -side), (('front' if prof else 'nose_side'), 1 if side > 0 else 0, side))
        for nm_, j, sg in keys:
            for bn, b0, b1 in HB:
                dd = [(EC[y][j]-ER[y][j])*sg for y in ER if y in EC and b0 <= (y-ey)/d < b1]
                if len(dd) >= 3: hr.setdefault(nm_, {})[bn] = round(float(np.median(dd))/pxcm*10, 1)
        rep['hair'] = hr; print('OV5HAIR', rv, json.dumps(hr))
        def edge(M):
            e = M & ~(np.roll(M, 1, 0) & np.roll(M, -1, 0) & np.roll(M, 1, 1) & np.roll(M, -1, 1)); return e | np.roll(e, 1, 1)
        eR, eC = edge(MR), edge(MC)
        H1 = R.copy(); H1[eR] = (0.1, 0.95, 1.0); H1[eC] = (1.0, 0.15, 0.85)
        H2 = 0.5*R+0.5*Cw; H2[eR] = (0.1, 0.95, 1.0); H2[eC] = (1.0, 0.15, 0.85)
        H3 = Cw.copy(); H3[eR] = (0.1, 0.95, 1.0); H3[eC] = (1.0, 0.15, 0.85)
        for HH in (H1, H2, H3):
            for yy_ in (int(ey), int(ey-1.6*d), int(ey-0.8*d), int(ey+0.6*d)):
                if 0 <= yy_ < h: HH[yy_, ::4] = (1, 1, 0)
        ya_ = max(int(ey-3.4*d), 0); yb_ = min(int(ey+1.7*d), h)
        Oh = np.concatenate([H1[ya_:yb_], np.ones((yb_-ya_, 4, 3)), H2[ya_:yb_], np.ones((yb_-ya_, 4, 3)), H3[ya_:yb_]], 1)
        save(np.repeat(np.repeat(Oh, 2, 0), 2, 1), os.path.join(OD, '%s_%s_hair.png' % (LAB, rv)))
    REPORT[rv] = rep; print('OV5', rv, json.dumps(rep))
    KS = ('cont', 'jaw', 'und', 'ey', 'my', 'd', 'brow', 'chin', 'nosebase')
    json.dump(dict(ref={k_: v for k_, v in LR.items() if k_ in KS}, cand={k_: v for k_, v in LC.items() if k_ in KS}, pxcm=pxcm),
              open(os.path.join(OD, '%s_%s_lines.json' % (LAB, rv)), 'w'), default=lambda o: o.item() if hasattr(o, 'item') else str(o))
    def draw(O, Lx, col):
        for y, row in Lx['cont'].items():
            for kx, x in row.items():
                if x is not None and 0 <= x < w: O[y:y+2, max(x-1, 0):x+1] = col
        for x, y in Lx['jaw'].items(): O[max(y-1, 0):y+1, x:x+1] = col
        for x, y in Lx['und'].items():
            if 0 <= y < h and 0 <= x < w: O[max(y-1, 0):y+1, x:x+1] = col
        xa = int(min(e[0] for e in Lx['E'])-0.9*d); xb = int(max(e[0] for e in Lx['E'])+0.9*d)
        for nm, dash in (('brow', 6), ('ey', 0), ('nosebase', 4), ('my', 0), ('chin', 3)):
            y = Lx.get(nm)
            if y is None: continue
            y = int(round(y)); xs_ = np.arange(max(xa, 0), min(xb, w))
            if dash: xs_ = xs_[(xs_//dash) % 2 == 0]
            if 0 <= y < h: O[y, xs_] = col
    CY, CM = (0.1, 0.95, 1.0), (1.0, 0.15, 0.85)
    P1 = R.copy(); draw(P1, LR, CY); draw(P1, LC, CM)
    P2_ = 0.5*R+0.5*Cw; draw(P2_, LR, CY); draw(P2_, LC, CM)
    P3 = Cw.copy(); draw(P3, LR, CY); draw(P3, LC, CM)
    ya = max(int(ey-1.7*d), 0); yb = min(int(LR['my']+1.9*d), h); xc = float(np.mean([e[0] for e in LR['E']])); xa = max(int(xc-2.4*d), 0); xb = min(int(xc+2.4*d), w)
    if prof: xa = max(int(xc-2.6*d+side*0.8*d), 0); xb = min(int(xc+2.6*d+side*0.8*d), w)
    O = np.concatenate([P1[ya:yb, xa:xb], np.ones((yb-ya, 4, 3)), P2_[ya:yb, xa:xb], np.ones((yb-ya, 4, 3)), P3[ya:yb, xa:xb]], 1)
    O = np.repeat(np.repeat(O, 2, 0), 2, 1); save(O, os.path.join(OD, '%s_%s.png' % (LAB, rv)))
if 'ratio' in YAW and 'front' in YAW['ratio']:
    f = YAW['ratio']['front']
    for v_, r_ in YAW['ratio'].items(): REPORT[v_]['yaw_est_deg'] = dict(ref=round(math.degrees(math.acos(min(r_['ref']/f['ref'], 1))), 1), cand=round(math.degrees(math.acos(min(r_['cand']/f['cand'], 1))), 1))
    print('YAW', {v_: REPORT[v_].get('yaw_est_deg') for v_ in YAW['ratio']})
json.dump(REPORT, open(os.path.join(OD, LAB+'_ov5.json'), 'w'), indent=1); print('OV5_OK')
