"""GD13 regional sculpt operators (handle-driven soft deformation, the scripted equivalent of ZBrush Transpose / Maya soft-mod moves) on a
DNA-order head npy. Every operator is anatomically named and placed at landmarks measured on the CURRENT mesh; displacements are smooth
(Wendland C2 kernels, ellipsoidal radii in cm), symmetric by default, gated so they never cross to the other side of a thin structure.
Ops (json list, applied in order):
  move   : {"at": landmark | [x,y,z] | {"lm": name, "off": [dx,dy,dz]}, "r": r | [rx,ry,rz], "d": [dx,dy,dz] cm (dx = toward the outside for
            mirrored pairs), "mask": optional region, "gate": min normal dot (default -1 = off), "sym": true}
  scale  : {"pivot": landmark | [x,y,z], "s": [sx,sy,sz], "at": centre of the weight field, "r": radii, "mask": region}   (d = w (S-1)(x-p))
  relax  : {"at": ..., "r": ..., "iters": n, "k": 0.5, "mask": region}   (Laplacian relax of the displacement accumulated so far: keeps the
            start-head detail, removes only the op-made ripples)
  inflate: {"at": ..., "r": ..., "amt": cm along the vertex normal, "mask"}
Regions: skin, face (no ear / neck), nose, upper_lip, lower_lip, lips, chin, lower_face, cheek, lids, not_lids
Non-skin parts (teeth, eyes, lashes, eye edge, eye shell, cartilage) follow their nearest start-head skin vertex; eyeballs move rigidly.
usage: blender -b --factory-startup --python gd13_sculpt.py -- <in.npy> <ops.json> <out.npy> [base_for_relax.npy]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]).astype(float); OPS = json.load(open(a[1])); OUT = a[2]
X = X0.copy(); XB = np.load(a[3]).astype(float) if len(a) > 3 else X0; S0 = X0[:NS]; AX = np.abs(S0[:, 0]-MX); N0 = skin_normals(X0)
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
# ---------- landmarks on the current mesh
def landmarks(X):
    S = X[:NS]; ax = np.abs(S[:, 0]-MX); mid = (ax < 0.35) & (S[:, 1] > 4.0); L = {}
    def amax(m, f): i = np.nonzero(m)[0]; return S[i[np.argmax(f(S[i]))]].copy()
    def prof(z0, z1):
        out = []
        for zz in np.arange(z0, z1, 0.1):
            m = mid & (np.abs(S[:, 2]-zz) < 0.09)
            if m.any(): i = np.nonzero(m)[0]; out.append(S[i[np.argmax(S[i, 1])]])
        return np.array(out)
    L['eyeL'] = X[SEG['eyeL'][0]:SEG['eyeL'][1]].mean(0); L['eyeR'] = X[SEG['eyeR'][0]:SEG['eyeR'][1]].mean(0); L['eye_L'] = L['eyeL']; L['eye_R'] = L['eyeR']; ez = (L['eyeL'][2]+L['eyeR'][2])/2
    P = prof(ez-12.5, ez+1.5)   # midline front profile below the eyes (to below the chin)
    L['pronasale'] = P[np.argmax(np.where((P[:, 2] > ez-4.5) & (P[:, 2] < ez-1.5), P[:, 1], -1e9))]
    up = prof(ez-1.0, ez+2.2); L['nasion'] = up[np.argmin(up[:, 1])]
    seg = P[(P[:, 2] < L['pronasale'][2]-0.3) & (P[:, 2] > L['pronasale'][2]-2.4)]; L['subnasale'] = seg[np.argmin(seg[:, 1])]
    lip = P[(P[:, 2] < L['subnasale'][2]) & (P[:, 2] > L['subnasale'][2]-1.4)]; L['labrale_sup'] = lip[np.argmax(lip[:, 1])]
    st = P[(P[:, 2] < L['labrale_sup'][2]) & (P[:, 2] > L['labrale_sup'][2]-1.2)]; L['stomion'] = st[np.argmin(st[:, 1])]
    li = P[(P[:, 2] < L['stomion'][2]) & (P[:, 2] > L['stomion'][2]-1.3)]; L['labrale_inf'] = li[np.argmax(li[:, 1])]
    lm = P[(P[:, 2] < L['labrale_inf'][2]) & (P[:, 2] > L['labrale_inf'][2]-1.6)]; L['labiomental'] = lm[np.argmin(lm[:, 1])]
    ch = P[(P[:, 2] < L['labiomental'][2]) & (P[:, 2] > L['labiomental'][2]-3.0)]; L['pogonion'] = ch[np.argmax(ch[:, 1])]
    L['menton'] = amax(mid & (S[:, 1] > L['pogonion'][1]-3.0) & (S[:, 2] < L['pogonion'][2]) & (S[:, 2] > L['pogonion'][2]-3.0), lambda Q: -Q[:, 2])
    for s, sg in (('L', 1), ('R', -1)):
        side = (S[:, 0]-MX)*sg > 0
        L['alar_'+s] = amax(side & (np.abs(S[:, 2]-(L['subnasale'][2]+0.7)) < 0.35) & (ax < 2.6) & (S[:, 1] > L['subnasale'][1]-1.2), lambda Q: np.abs(Q[:, 0]-MX))
        L['cheilion_'+s] = amax(side & (np.abs(S[:, 2]-L['stomion'][2]) < 0.35) & (ax < 3.6) & (S[:, 1] > L['stomion'][1]-2.2), lambda Q: np.abs(Q[:, 0]-MX))
        L['malar_'+s] = amax(side & (np.abs(S[:, 2]-(ez-1.9)) < 0.3) & (np.abs(ax-4.3) < 0.3), lambda Q: Q[:, 1])
        L['zygion_'+s] = amax(side & (np.abs(S[:, 2]-(ez-1.6)) < 0.4) & (S[:, 1] > 3.0), lambda Q: np.abs(Q[:, 0]-MX))
        L['gonion_'+s] = amax(side & (S[:, 2] > L['menton'][2]+1.0) & (S[:, 2] < L['menton'][2]+3.5) & (S[:, 1] > -1.0) & (S[:, 1] < 4.0) & (ax < 6.4), lambda Q: np.abs(Q[:, 0]-MX)-0.3*Q[:, 2])
    JL = X[jaw_line(X)]
    for s, sg in (('L', 1), ('R', -1)):
        k = JL[((JL[:, 0]-MX)*sg > 0)]; L['jawmid_'+s] = k[np.argmin(np.abs(np.abs(k[:, 0]-MX)-3.6))].copy()
    try:
        BFl = bindings('front', mirror_map())
        for s, k in (('L', 'l'), ('R', 'r')):
            P = bind_pts(BFl['crv_eyelid_upper_'+k], X); P = P[~np.isnan(P[:, 0])]; o = np.argsort(np.abs(P[:, 0]-MX))
            L['mcanth_'+s] = P[o[0]].copy(); L['lcanth_'+s] = P[o[-1]].copy()
    except Exception as e: print('canthus landmarks failed', e)
    return L
# ---------- material regions (start head)
ez0 = (X0[SEG['eyeL'][0]:SEG['eyeL'][1], 2].mean()+X0[SEG['eyeR'][0]:SEG['eyeR'][1], 2].mean())/2
L0 = landmarks(X0); EAR = (AX > 6.2) & (S0[:, 1] < 4.6) & (S0[:, 2] > 154) & (S0[:, 2] < 168)
REG = {'skin': np.ones(NS, bool), 'face': ~EAR & (S0[:, 2] > 147.0) & (S0[:, 1] > -1.5)}
REG['nose'] = (AX < 2.6) & (S0[:, 1] > 11.8) & (S0[:, 2] > L0['subnasale'][2]-0.15) & (S0[:, 2] < L0['nasion'][2]+0.6)
mouth_mid = (L0['stomion'][2])
REG['upper_lip'] = (AX < 3.4) & (S0[:, 1] > 10.0) & (S0[:, 2] > mouth_mid) & (S0[:, 2] < L0['subnasale'][2]+0.2)
REG['lower_lip'] = (AX < 3.4) & (S0[:, 1] > 10.0) & (S0[:, 2] <= mouth_mid) & (S0[:, 2] > L0['labiomental'][2]-0.3)
REG['lips'] = REG['upper_lip'] | REG['lower_lip']
REG['chin'] = (AX < 3.6) & (S0[:, 1] > 6.0) & (S0[:, 2] < L0['labiomental'][2]+0.3) & (S0[:, 2] > L0['menton'][2]-1.2)
REG['lower_face'] = REG['face'] & (S0[:, 2] < L0['subnasale'][2]+0.5)
REG['cheek'] = REG['face'] & (AX > 2.2) & (S0[:, 2] < ez0-0.8) & (S0[:, 2] > L0['stomion'][2]-1.5)
lidm = np.zeros(NS, bool)
for k in ('eyeL', 'eyeR'):
    c = L0[k]; d = np.sqrt((((S0-c)/np.array([1.8, 2.2, 1.05]))**2).sum(1)); lidm |= d < 1.0
REG['lids'] = lidm; REG['not_lids'] = ~lidm
def resolve(spec, L, sg=1):
    if isinstance(spec, str): p = L[spec.replace('_S', '_L' if sg > 0 else '_R')].copy()
    elif isinstance(spec, dict):
        p = resolve(spec['lm'], L, sg); off = np.asarray(spec.get('off', [0, 0, 0]), float).copy(); off[0] *= sg; p = p+off
    else: p = np.asarray(spec, float).copy(); p[0] = MX+sg*(p[0]-MX) if sg < 0 else p[0]
    return p
def kern(P, c, r, plateau=None):
    """Wendland C2 bump (localised moves) or, with plateau = feather radii, a flat box field with smooth edges (broad re-proportioning)"""
    r = np.asarray(r if isinstance(r, list) else [r, r, r], float)
    if plateau is not None:
        f = np.asarray(plateau if isinstance(plateau, list) else [plateau]*3, float); return np.prod(ss((r-np.abs(P-c))/f), axis=1)
    q = np.sqrt((((P-c)/r)**2).sum(1)); return np.where(q < 1, (1-q)**4*(4*q+1), 0.0)
LOG = []; MIRR = mirror_map(X0)
for op in OPS:
    L = landmarks(X); H = X[:NS].copy(); N = skin_normals(X); before = H.copy()
    m = REG[op.get('mask', 'skin')].astype(float)
    if op.get('soft_mask'):   # feather a hard material mask over ~n rings
        for _ in range(int(op['soft_mask'])): m = 0.5*m+0.5*lap(m[:, None])[:, 0]
    sides = (1, -1) if op.get('sym', True) else (1,)
    D = np.zeros((NS, 3))
    for sg in sides:
        at = op.get('at', op.get('pivot')); c = resolve(at, L, sg)
        if sg < 0 and abs(c[0]-MX) < 0.25: continue
        if op.get('snap', op['op'] in ('move', 'inflate') and isinstance(at, dict)):   # anchor onto the front-most skin surface at that (x, z)
            cand = np.nonzero((np.abs(H[:, 0]-c[0]) < 0.3) & (np.abs(H[:, 2]-c[2]) < 0.3) & (N[:, 1] > 0.1) & REG['face'])[0]
            if len(cand): c = H[cand[np.argmax(H[cand, 1])]].copy()
        w = kern(H, c, op['r'], op.get('plateau'))*m
        if op.get('gate', -1) > -1:
            j = np.argmin(((H-c)**2).sum(1)); w *= ss((N@N[j]-op['gate'])/0.2)
        t = op['op']
        if t == 'move': d = np.asarray(op['d'], float).copy(); d[0] *= sg; D += w[:, None]*d
        elif t == 'scale':
            p = resolve(op['pivot'], L, sg) if 'pivot' in op else c; s = np.asarray(op['s'], float); D += w[:, None]*((H-p)*(s-1))
        elif t == 'inflate': D += (op['amt']*w)[:, None]*N
        elif t == 'lid':
            # eyelid rotation over the eyeball (partial blink): upper (or lower) lid skin between the mesh-bound margin curve and 'reach' cm away
            # rotates about the eyeball centre around the lateral axis by angle = d / eyeball radius * weight; weight 1 at the margin -> 0 at
            # reach (crease / lid-cheek junction); 'lat' adds lateral bias (hooding) 1 + lat * (lateral position in [-1, 1])
            ek = 'eyeL' if sg > 0 else 'eyeR'; ce = X[SEG[ek][0]:SEG[ek][1]].mean(0); rad = np.linalg.norm(X[SEG[ek][0]:SEG[ek][1]]-ce, axis=1).mean()
            BF_ = bindings('front', MIRR); cname = ('crv_eyelid_upper_' if op['lid'] == 'upper' else 'crv_eyelid_lower_')+('l' if sg > 0 else 'r')
            Pm = bind_pts(BF_[cname], X); Pm = Pm[~np.isnan(Pm[:, 0])]; o = np.argsort(Pm[:, 0]); zm = np.interp(H[:, 0], Pm[o, 0], Pm[o, 2])
            oname = ('crv_eyelid_lower_' if op['lid'] == 'upper' else 'crv_eyelid_upper_')+('l' if sg > 0 else 'r')
            Po = bind_pts(BF_[oname], X); Po = Po[~np.isnan(Po[:, 0])]; oo = np.argsort(Po[:, 0]); zo = np.interp(H[:, 0], Po[oo, 0], Po[oo, 2]); zmid = 0.5*(zm+zo)
            xr = (H[:, 0]-ce[0])*sg; inx = 1-ss(np.abs(xr-op.get('xc', 0.0))/op.get('half', 1.6))   # smooth to 0 at the canthi (no shear)
            hgt = (H[:, 2]-zm) if op['lid'] == 'upper' else (zm-H[:, 2]); side_ok = (H[:, 2] > zmid) if op['lid'] == 'upper' else (H[:, 2] < zmid)
            # whole lid (margin, lid edge, inner surface) moves fully; above the margin the motion fades to 0 at 'reach'
            wl = np.where(hgt <= 0, 1.0, ss(1-hgt/op.get('reach', 0.85)))*side_ok*inx*(H[:, 1] > ce[1]-0.6)*m*(1+op.get('lat', 0.0)*np.clip(xr/1.2, -1, 1))
            ang = -op['d']/rad*wl*(1 if op['lid'] == 'upper' else -1)   # upper: rotate down (front points move -z), lower: up
            rel = H-ce; cy_, sy_ = np.cos(ang), np.sin(ang); ny = cy_*rel[:, 1]-sy_*rel[:, 2]; nz = sy_*rel[:, 1]+cy_*rel[:, 2]
            D[:, 1] += ny-rel[:, 1]; D[:, 2] += nz-rel[:, 2]
        elif t == 'relax':
            W = w if op.get('mask') != 'lids' else m; Y = H.copy()
            for _ in range(op.get('iters', 6)):
                Dv = Y-XB[:NS]; Dv = Dv+(op.get('k', 0.5)*W)[:, None]*(lap(Dv)-Dv); Y = XB[:NS]+Dv
            D += Y-H
            if not op.get('sym', False): break
            H = H+(Y-H)
    X[:NS] = H+D
    dd = np.linalg.norm(D, axis=1)*10; LOG.append(dict(name=op['name'], op=op['op'], max_mm=round(float(dd.max()), 2), verts=int((dd > 0.05).sum()), mean_mm=round(float(dd[dd > 0.05].mean()) if (dd > 0.05).any() else 0, 2)))
    print('OP %-28s %-7s max %.2f mm  verts %d' % (op['name'], op['op'], dd.max(), (dd > 0.05).sum()))
# non-skin follow
NNp = os.path.join(GD, 'data/nearest_skin.npy'); NN = np.load(NNp)
Ds = X[:NS]-X0[:NS]
for k in ('teeth', 'saliva', 'eyeshell', 'lashes', 'eyeEdge', 'cartilage'): i0, i1 = SEG[k]; X[i0:i1] = X0[i0:i1]+Ds[NN[i0:i1]]
for k in ('eyeL', 'eyeR'): i0, i1 = SEG[k]; X[i0:i1] = X0[i0:i1]+Ds[np.unique(NN[i0:i1])].mean(0)
np.save(OUT, X); dd = np.linalg.norm(X[:NS]-X0[:NS], axis=1)*10
json.dump(dict(ops=LOG, total_max_mm=float(dd.max()), moved=int((dd > 0.05).sum()), landmarks_in={k: v.round(3).tolist() for k, v in L0.items()}, landmarks_out={k: v.round(3).tolist() for k, v in landmarks(X).items()}), open(OUT.replace('.npy', '_sculpt.json'), 'w'), indent=1)
print('SCULPT_OK total max %.2f mm moved %d' % (dd.max(), (dd > 0.05).sum()))
