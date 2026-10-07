"""GD11 pass QQ: MULTI-VIEW SILHOUETTE FIT of a DNA-order head npy to ALL references at once (user decision "C": every reference, conflicts averaged).
Views
  front : solved reference camera (gd_common.topix 'front'), target = ref_picks.json front CONTOUR picks (cheek / jaw / chin / menton)
  close : solved reference camera ('close'), target = ref_picks.json close CONTOUR picks (chin_p*, menton_c, jawbot, farcheek)
  bald  : user's bald profile photo, orthographic side view, similarity from landmarks (tragus, lateral canthus, pronasale), target = dense
          automatic silhouette (front face edge, back of head, crown, under-chin)
  rprof : 6-view reference right profile panel, same model, target = face front edge + under-chin (hair covers the rest)
Per iteration: for every target sample (point r, outward normal n) the model outline point along the ray r + t n is found among projected skin
vertices (band of +-band px); the violation b (cm, in the view plane) becomes a linear constraint J dX = b on that handle vertex (J = projection
Jacobian, cm-normalised). Constraints are spread to the surface with a Gaussian kernel and solved PER VERTEX as a 3x3 regularised least squares
(sum w K J^T J + mu I) dX = sum w K J^T b, so orthogonal demands from different views combine and contradicting demands average.
Frozen: eyes and lids, ears, mouth opening, neck below z 147.5. Writes <out.npy> (full fit) and <out_half.npy> (50 %), prints residuals.
usage: blender -b --python blender_g11rqq_fit.py -- <head.npy> <out.npy> [iters=5] [cap_mm=3]"""
import bpy, sys, os, json, math, numpy as np
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); OUT = a[1]; ITERS = int(a[2]) if len(a) > 2 else 5; CAP = float(a[3])/10 if len(a) > 3 else 0.3
NH = 24049; MX = -0.23; X = X0.copy()
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]; SOFT = SOFT[SOFT < NH]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = X0[:NH]; ax = np.abs(H[:, 0]-MX)
eye = np.zeros(NH)
for sd in (1, -1):
    c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt(((H-c)/np.array([1.9, 2.2, 1.25]))**2 @ np.ones(3)); eye = np.maximum(eye, 1-ss((d-0.75)/0.35))
ear = ss((ax-6.3)/0.4)*ss((H[:, 2]-154.5)/0.6)*(1-ss((H[:, 2]-167.5)/0.6))*(1-ss((H[:, 1]-4.5)/0.8))
mouth = (1-ss((ax-2.4)/0.4))*ss((H[:, 2]-154.6)/0.25)*(1-ss((H[:, 2]-156.1)/0.25))*ss((H[:, 1]-11.6)/0.4)
neck = 1-ss((H[:, 2]-146.2)/2.6)
FREE = (1-eye)*(1-ear)*(1-mouth)*(1-neck)
if os.environ.get('QQ_REGION', 'all') == 'lowerback':   # only the lower face (below the nose) and the back of the head move; nose, eyes, forehead, crown top frozen
    nose = (1-ss((ax-2.2)/0.5))*ss((H[:, 2]-156.3)/0.4)*ss((H[:, 1]-10.8)/0.6)
    lower = 1-ss((H[:, 2]-159.6)/0.8)
    if os.environ.get('QQ_LOWERY'): lower = lower*ss((H[:, 1]-float(os.environ['QQ_LOWERY']))/2.0)   # face side only (keeps the nape / occiput out)
    BZ0, BZ1, BW = [float(v) for v in os.environ.get('QQ_BACKZ', '153.5,169.0,1.2').split(',')]   # back region: z band and fade width (wide fade = no ridge where the frozen crown meets it)
    back = (1-ss((H[:, 1]-1.5)/1.5))*ss((H[:, 2]-BZ0)/1.0)*(1-ss((H[:, 2]-BZ1)/BW))
    FREE = FREE*np.maximum(lower*(1-nose), back)
FREE_S = FREE[SOFT]

def load_img(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; return np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1][..., :3]

# ---------- side (orthographic) views ----------
def model_landmarks(Xc):
    mid = Xc[:NH][(np.abs(Xc[:NH, 0]-MX) < 0.3) & (Xc[:NH, 1] > 6) & (Xc[:NH, 2] > 156) & (Xc[:NH, 2] < 161.5)]; p = mid[np.argmax(mid[:, 1])]
    if os.environ.get('QQ_ALIGN', 'face') == 'face':   # face-only alignment: lateral canthus, pronasale, stomion (ear left free: the ear sits at a different depth in the photo)
        st = Xc[:NH][(np.abs(Xc[:NH, 0]-MX) < 0.3) & (np.abs(Xc[:NH, 2]-155.05) < 0.08) & (Xc[:NH, 1] > 10)]; st = st[np.argmax(st[:, 1])]
        return np.array([[10.73, 162.27], [p[1], p[2]], [st[1], st[2]]])
    return np.array([[3.83, 159.97], [10.73, 162.27], [p[1], p[2]]])
def sim2(A, B):   # least squares similarity A(model y,-z) -> B(px)
    mA, mB = A.mean(0), B.mean(0); A0, B0 = A-mA, B-mB; U, S, Vt = np.linalg.svd(B0.T@A0); D = np.diag([1, np.sign(np.linalg.det(U@Vt))]); Rm = U@D@Vt
    s = np.trace(np.diag(S)@D)/(A0**2).sum(); return s, Rm, mB-s*(Rm@mA)
class Side:
    def __init__(s, name, img, lm_px, mask_fn, regions, weight):
        s.name, s.R = name, load_img(img); s.h, s.w = s.R.shape[:2]; s.lm = np.array(lm_px, float); s.M = mask_fn(s.R); s.regions = regions; s.weight = weight
    def setup(s, Xc):
        A = model_landmarks(Xc).copy(); A[:, 1] *= -1; s.s, s.Rm, s.t = sim2(A, s.lm)
    def proj(s, P): Q = np.stack([P[:, 1], -P[:, 2]], -1); return (Q@s.Rm.T)*s.s+s.t
    def J(s): return s.s*s.Rm@np.array([[0.0, 1.0, 0.0], [0.0, 0.0, -1.0]])   # px per cm (2x3)
    def samples(s):
        M, out = s.M, []
        rows = np.nonzero(M.any(1))[0]
        def zrow(z): return int(round(s.proj(np.array([[0, 5.0, z]]))[0, 1]))
        def ycol(y): return int(round(s.proj(np.array([[0, y, 160.0]]))[0, 0]))
        for kind, lo, hi in s.regions:
            if kind == 'front':        # rows: rightmost mask pixel, normal +x (face points right)
                for y in range(zrow(hi), zrow(lo), 4):
                    c = np.nonzero(M[y])[0]
                    if len(c): out.append((np.array([c.max(), y], float), np.array([1.0, 0.0])))
            if kind == 'back':
                for y in range(zrow(hi), zrow(lo), 4):
                    c = np.nonzero(M[y])[0]
                    if len(c): out.append((np.array([c.min(), y], float), np.array([-1.0, 0.0])))
            if kind == 'top':          # columns: topmost mask pixel, normal -y (up)
                for x in range(ycol(lo), ycol(hi), 4):
                    r = np.nonzero(M[:, x])[0]
                    if len(r) and r.min() < zrow(163.0): out.append((np.array([x, r.min()], float), np.array([0.0, -1.0])))   # head top only (not the shoulder)
            if kind == 'under':        # columns between neck front and chin: first mask pixel scanning upward from below the chin
                z0, z1 = zrow(153.5), zrow(lo-4.0)   # scan down from inside the chin; the first background pixel = under-chin edge (skip if the neck continues)
                for x in range(ycol(hi[0]), ycol(hi[1]), 4):
                    if not M[z0, x]: continue
                    col = M[z0:z1, x]; r = np.nonzero(~col)[0]
                    if len(r): out.append((np.array([x, z0+r[0]-1], float), np.array([0.0, 1.0])))
        return out
def mask_gray(R):
    bg = np.median(np.concatenate([R[:20].reshape(-1, 3), R[:, -20:].reshape(-1, 3)]), 0); m = np.linalg.norm(R-bg, axis=-1) > 0.08
    for _ in range(2): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    return m
def mask_chroma(R):
    ch = R.max(-1)-R.min(-1); bg = np.median(np.concatenate([ch[:20].ravel(), ch[:, -20:].ravel()])); m = ch > bg+0.06
    for _ in range(2): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    return m
BALD = Side('bald', 'Saved/Codex/GD11_MalarSkullOO_20261007/data/ref_bald_profile.png', [[452, 505], [700, 425], [0, 0]] if os.environ.get('QQ_ALIGN', 'face') != 'face' else [[700, 425], [0, 0], [850, 657]], mask_gray,
            [('front', 150.2, 166.5), ('back', 154.5, 168.0), ('top', -6.0, 9.0), ('under', 151.6, (3.5, 10.0))], 1.0)
RPROF = Side('rprof', 'Saved/Codex/GD11_LikenessW_20261006/ref/ref6_rprof.png', [[240.7, 230.0], [341.7, 184.0], [0, 0]] if os.environ.get('QQ_ALIGN', 'face') != 'face' else [[341.7, 184.0], [0, 0], [395.0, 271.0]], mask_chroma,
             [('front', 150.2, 161.5), ('under', 151.6, (4.0, 10.0))], 0.6)
for S in (BALD, RPROF):   # reference pronasale = rightmost mask pixel below the canthus row
    face = os.environ.get('QQ_ALIGN', 'face') == 'face'; ci = 0 if face else 1; pi = 1 if face else 2
    y0 = int(S.lm[ci, 1]); band = S.M[y0:y0+int(S.h*0.12)]
    cols = [np.nonzero(r)[0].max() if r.any() else -1 for r in band]; i = int(np.argmax(cols)); S.lm[pi] = [cols[i], y0+i]
# ---------- solved perspective views (picks) ----------
PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))
PICKS = {v: [(np.array(c['ref'], float), np.array(c['n'], float)/np.linalg.norm(c['n']), c['w']) for c in PK[v]['contours']] for v in ('front', 'close')}
def cm_per_px(view, Xc):
    e = topix(view, np.array([[MX-2.97, 10.5, 162.25], [MX+2.97, 10.5, 162.25]])); return 5.94/np.linalg.norm(e[1]-e[0])

def outline_hit(q, r, n, band):
    t = np.array([-n[1], n[0]]); rel = q-r; s_ = np.abs(rel@t) < band
    if not s_.any(): return None, None
    pr = rel[s_]@n; i = np.argmax(pr); return np.nonzero(s_)[0][i], pr[i]
kd = KDTree(len(SOFT))
for i, v in enumerate(SOFT): kd.insert(H[v].tolist(), i)
kd.balance()
def front_mask(Xc):   # skin vertices that can form a silhouette in the frontal views (exclude back of head / ears / neck)
    Hs = Xc[SOFT]; return (Hs[:, 1] > -1.0) & (Hs[:, 2] > 147.0) & (np.abs(Hs[:, 0]-MX) < 7.2)
P_ = pkg(); TRI = np.asarray(P_['head']['triangles']); TRI = TRI[(TRI < NH).all(1)]
pos = -np.ones(NH, int); pos[SOFT] = np.arange(len(SOFT)); E_ = np.r_[TRI[:, [0, 1]], TRI[:, [1, 2]], TRI[:, [2, 0]]]; E_ = np.r_[E_, E_[:, ::-1]]
E_ = E_[(pos[E_[:, 0]] >= 0) & (pos[E_[:, 1]] >= 0)]; EI = pos[E_]; DEG = np.bincount(EI[:, 0], minlength=len(SOFT)).astype(float)
Hm = H[SOFT].copy(); Hm[:, 0] = 2*MX-Hm[:, 0]; MIR = np.array([kd.find(p.tolist())[1] for p in Hm])
STEP, SMOOTH, ROBUST = float(os.environ.get('QQ_STEP', '0.6')), int(os.environ.get('QQ_SMOOTH', '12')), float(os.environ.get('QQ_ROBUST', '1.2'))
CAPT = float(os.environ.get('QQ_CAP_TOTAL', '0.9')); Dacc = np.zeros((len(SOFT), 3))
log = []
for it in range(ITERS):
    Xs = X[SOFT].copy(); cons = []   # (soft index, J_cm (2x3), b_cm (2), weight, sigma)
    resid = {}
    fm = front_mask(X)
    for view in ('front', 'close'):
        q = topix(view, Xs); cpp = cm_per_px(view, X); r_ = []
        for r, n, w in PICKS[view]:
            if n[1] > 0.85: continue   # jaw-bottom picks against the neck shadow: not reproducible on the mesh; the profile views' under-chin samples cover them
            idx, pr = outline_hit(np.where(fm[:, None], q, 1e9), r, n, 3.0)
            if idx is None: continue
            P = Xs[idx]; eps = 0.05; Jn = np.stack([(topix(view, (P+e)[None])[0]-topix(view, (P-e)[None])[0])/(2*eps) for e in np.eye(3)*eps], 1)   # px/cm
            b = -pr*n   # px
            cons.append((idx, Jn*cpp, b*cpp, 1.6*w, 1.4)); r_.append(pr*cpp)
            if os.environ.get('QQ_REPORT') and it == 0: print('PICK', view, 'n=(%.1f,%.1f)' % tuple(n), 'vtx', Xs[idx].round(1).tolist(), 'res_cm %+.2f' % (pr*cpp))
        resid[view] = float(np.sqrt(np.mean(np.square(r_)))) if r_ else 0.0
    for S in (BALD, RPROF):
        S.setup(X); q = S.proj(Xs); q = np.where((Xs[:, 2] > 147.0)[:, None], q, 1e9); smp = S.samples(); Jp = S.J(); cpp = 1.0/S.s; r_ = []   # neck below 147 cannot be a hit
        for r, n in smp:
            idx, pr = outline_hit(q, r, n, 2.5)
            if idx is None: continue
            cons.append((idx, Jp*cpp, -pr*n*cpp, S.weight*14.0/max(len(smp), 1)*6.0, 0.8)); r_.append(pr*cpp)
            if os.environ.get('QQ_REPORT') and it == 0: print('SMP', S.name, 'n=(%.0f,%.0f)' % tuple(n), 'z=%.1f y=%.1f' % (Xs[idx][2], Xs[idx][1]), 'res_cm %+.2f' % (pr*cpp))
        resid[S.name] = float(np.sqrt(np.mean(np.square(r_)))) if r_ else 0.0
        if os.environ.get('QQ_DEBUG') and it == 0:
            O = S.R.copy()
            for qq in q[::3]:
                if qq[0] > 1e8: continue
                xi, yi = int(qq[0]), int(qq[1])
                if 0 <= xi < S.w and 0 <= yi < S.h: O[yi, xi] = (1, 1, 0)
            if os.environ.get('QQ_DEBUG_SIL'):   # model silhouette only (front-most / back-most projected vertex per image row), no vertex cloud
                O = S.R.copy(); qv = q[q[:, 0] < 1e8]; rows = np.round(qv[:, 1]).astype(int)
                for yi in np.unique(rows):
                    if not 0 <= yi < S.h: continue
                    xs = qv[rows == yi, 0]
                    for xi in (int(xs.max()), int(xs.min())):
                        if 0 <= xi < S.w: O[yi, max(xi-1, 0):xi+1] = (1, 0, 1)
            for r, n in smp:
                xi, yi = int(r[0]), int(r[1]); O[max(yi-1, 0):yi+1, max(xi-1, 0):xi+1] = (0.1, 0.9, 1.0)
            for lm in S.lm: xi, yi = int(lm[0]), int(lm[1]); O[max(yi-4, 0):yi+5, max(xi-4, 0):xi+5] = (1, 0, 0)
            O4 = np.concatenate([O, np.ones(O.shape[:2]+(1,), np.float32)], -1)[::-1]; o = bpy.data.images.new('d', S.w, S.h); o.pixels.foreach_set(np.ascontiguousarray(O4).ravel())
            o.filepath_raw = os.path.abspath(os.environ['QQ_DEBUG']+'_'+S.name+'.png'); o.file_format = 'PNG'; o.save(); print('DBG', S.name, 'lm', S.lm.round(1).tolist(), 'scale', round(S.s, 2), 'nsmp', len(smp))
    # gradient step at the handles (min-norm solve per constraint, robust: skip > ROBUST cm) + Laplacian diffusion of the displacement field
    G = np.zeros((len(SOFT), 3)); Wt = np.zeros(len(SOFT))
    for idx, Jc, b, w, sg in cons:
        if np.linalg.norm(b) > ROBUST: continue
        d = np.linalg.pinv(Jc)@b; G[idx] += w*d; Wt[idx] += w
    hd = Wt > 0; G[hd] /= Wt[hd][:, None]
    Dacc = Dacc + STEP*G
    for _ in range(SMOOTH):
        acc = np.zeros_like(Dacc); np.add.at(acc, EI[:, 0], Dacc[EI[:, 1]]); Dacc = Dacc + 0.5*(acc/np.maximum(DEG, 1)[:, None]-Dacc)
        Dacc *= FREE_S[:, None]
    Dm = Dacc[MIR].copy(); Dm[:, 0] *= -1; Dacc = 0.5*(Dacc+Dm)   # left/right symmetric (asymmetry must stay subtle)
    nrm = np.linalg.norm(Dacc, axis=1); Dacc *= np.minimum(1.0, CAPT/np.maximum(nrm, 1e-9))[:, None]
    if it == ITERS-1:
        for _ in range(int(os.environ.get('QQ_POSTSMOOTH', '0'))):   # final low-pass of the accumulated field (removes handle-scale ripples)
            acc = np.zeros_like(Dacc); np.add.at(acc, EI[:, 0], Dacc[EI[:, 1]]); Dacc = Dacc + 0.5*(acc/np.maximum(DEG, 1)[:, None]-Dacc)
            Dacc *= FREE_S[:, None]
    D = Dacc
    X[SOFT] = X0[SOFT]+Dacc
    log.append({'iter': it, 'resid_cm': {k: round(v, 3) for k, v in resid.items()}, 'n_cons': len(cons), 'max_step_mm': round(10*float(np.linalg.norm(D, axis=1).max()), 2)})
    print('FIT', json.dumps(log[-1]))
np.save(OUT, X); Xh = X0.copy(); Xh[:NH] = X0[:NH]+0.5*(X[:NH]-X0[:NH]); np.save(OUT.replace('.npy', '_half.npy'), Xh)
dd = np.linalg.norm(X[:NH]-X0[:NH], axis=1)*10; print('FIT_DONE max %.2f mm mean(face) %.2f mm' % (dd.max(), dd[(H[:, 1] > 2)].mean()))
