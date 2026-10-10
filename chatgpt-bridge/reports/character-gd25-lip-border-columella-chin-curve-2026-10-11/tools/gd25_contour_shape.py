"""GD25 profile contour SHAPE analysis (scale-free). Traces the outer silhouette of the lower face from the nose tip down past the chin in the solved
profile panel: reference photo (background key, per-row background = median of the leftmost 30 px, |diff| > 0.10, 3x3 opening against hair strands)
and candidate alpha renders (2x, traced at 2x and scaled to panel px). Moore-neighbour boundary tracing, arc-length resampling, light smoothing.
Landmarks by alternating extrema of x along the arc: tip (start), subnasale sn (max), labrale superius ls (min), stomion sto (max), labrale
inferius li (min), sulcus sm (max), pogonion pg (min); then the chin turn: gn = tangent 45 deg down-back, me = tangent 75 deg (near horizontal).
Per segment A->B: chord length, signed sag profile d(t)/chord at t = 0.1..0.9 (+ = bulging outward into the background), max sag and its t;
angle of each chord. Candidates are similarity-aligned (scale + rotation + translation) to the reference on tip/sn/ls/sto/li/sm/pg; residuals
are reported in ref px and in model mm (1 panel px = 10/14.78 mm at the head, divided by the fitted scale).
usage: -- <ref panel png> <out overlay jpg> <out json> label=alpha.png [label2=alpha2.png ...]   (alpha renders 2x the panel size)"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; REFP, OUTI, OUTJ = a[0], a[1], a[2]; CANDS = [s.split('=', 1) for s in a[3:]]
MMPX = 10.0/14.78
NB = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
def opening(m):
    e = m.copy()
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1): e &= np.roll(np.roll(m, dr, 0), dc, 1)
    d = e.copy()
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1): d |= np.roll(np.roll(e, dr, 0), dc, 1)
    return d
def ref_mask(I):
    rgb = I[..., :3]; bg = np.median(rgb[:, :30], axis=1); d = np.abs(rgb-bg[:, None, :]).max(-1); return opening(d > 0.10)
def alpha_mask(I): return opening(I[..., 3] > 0.5)
def trace(m, start, maxn, cw):
    order = NB if cw else NB[::-1]; p = start; b = (start[0], start[1]-1); pts = [p]
    for _ in range(maxn):
        k = order.index((b[0]-p[0], b[1]-p[1])); found = None
        for j in range(1, 9):
            q = order[(k+j) % 8]; c = (p[0]+q[0], p[1]+q[1])
            if 0 <= c[0] < m.shape[0] and 0 <= c[1] < m.shape[1] and m[c]: found = c; pv = order[(k+j-1) % 8]; break
        if found is None: break
        b = (p[0]+pv[0], p[1]+pv[1]); p = found; pts.append(p)
        if p == start and len(pts) > 3: break
    return np.array(pts, float)
def outline(m, scale, tiprows):
    r0, r1 = [int(round(r*scale)) for r in tiprows]
    cols = [np.nonzero(m[r])[0] for r in range(r0, r1)]; xs = [c.min() if c.size else 1e9 for c in cols]; r = r0+int(np.argmin(xs)); start = (r, int(min(xs)))
    for cw in (True, False):
        P = trace(m, start, int(900*scale), cw)
        if P[min(15, len(P)-1), 0] > start[0]: break   # must walk downward (toward the lips)
    P = P[:, ::-1]/scale   # (x, y) in panel px
    # resample by arc length (0.5 px) + smooth (gaussian sigma 1.2 px)
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; s = np.arange(0, seg[-1], 0.5)
    Q = np.c_[np.interp(s, seg, P[:, 0]), np.interp(s, seg, P[:, 1])]
    k = np.exp(-0.5*(np.arange(-6, 7)*0.5/1.2)**2); k /= k.sum(); Qp = np.pad(Q, ((6, 6), (0, 0)), mode='edge')
    Q = np.c_[np.convolve(Qp[:, 0], k, 'valid'), np.convolve(Qp[:, 1], k, 'valid')]
    return Q
def extrema(x, prom=1.0):
    E = []   # alternating extrema with prominence filter, starting with a max (subnasale) after the tip
    i0 = 0; cur = 'max'; i = 0; n = len(x)
    best = 0
    while i < n:
        if cur == 'max':
            if x[i] > x[best]: best = i
            if x[best]-x[i] > prom: E.append(('max', best)); cur = 'min'; best = i
        else:
            if x[i] < x[best]: best = i
            if x[i]-x[best] > prom: E.append(('min', best)); cur = 'max'; best = i
        i += 1
    return E
def landmarks(Q):
    x = Q[:, 0]; E = extrema(x, 1.0); names = ['sn', 'ls', 'sto', 'li', 'sm', 'pg']; L = {'tip': 0}
    for nm, (kind, i) in zip(names, E): L[nm] = i
    if 'pg' in L:
        T = np.gradient(Q, axis=0); ang = np.degrees(np.arctan2(T[:, 0], T[:, 1]))   # 0 = straight down, +90 = moving back (+x)
        j = L['pg']; gn = me = None
        for i in range(j, len(Q)):
            if gn is None and ang[i] > 45: gn = i
            if ang[i] > 75: me = i; break
        if gn is not None: L['gn'] = gn
        if me is not None: L['me'] = me
    return L
def outward_sign(mask, scale, A, B):
    c = (A+B)/2; d = (B-A)/np.linalg.norm(B-A); n = np.array([-d[1], d[0]])
    for sgn in (1, -1):
        p = (c+sgn*n*3)*scale; r, cc = int(round(p[1])), int(round(p[0]))
        if 0 <= r < mask.shape[0] and 0 <= cc < mask.shape[1] and not mask[r, cc]: return sgn*n
    return n
def seg_shape(Q, i, j, nout):
    A, B = Q[i], Q[j]; ch = np.linalg.norm(B-A); P = Q[i:j+1]; sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    d = (P-A)@nout; t = np.linspace(0.1, 0.9, 9); dd = np.interp(t*sl[-1], sl, d)
    k = int(np.argmax(np.abs(d))); ang = math.degrees(math.atan2(B[0]-A[0], B[1]-A[1]))
    return dict(chord=float(ch), sag=[round(float(v/ch), 4) for v in dd], max_sag=round(float(d[k]/ch), 4), t_max=round(float(sl[k]/sl[-1]), 3), angle=round(ang, 1), arc=float(sl[-1]))
SEGS = [('tip', 'sn'), ('sn', 'ls'), ('ls', 'sto'), ('sto', 'li'), ('li', 'sm'), ('sm', 'pg'), ('pg', 'gn'), ('gn', 'me'), ('pg', 'me')]
def analyse(mask, scale, tiprows):
    Q = outline(mask, scale, tiprows); L = landmarks(Q); S = {}
    for A, B in SEGS:
        if A in L and B in L and L[B] > L[A]+2: S[A+'-'+B] = seg_shape(Q, L[A], L[B], outward_sign(mask, scale, Q[L[A]], Q[L[B]]))
    return Q, L, S
def similarity(src, dst):   # Umeyama: dst ~ s R src + t
    ms, md = src.mean(0), dst.mean(0); X, Y = src-ms, dst-md; U, D, Vt = np.linalg.svd(Y.T@X); R = U@Vt
    if np.linalg.det(R) < 0: U[:, -1] *= -1; R = U@Vt
    s = (D.sum())/(X**2).sum(); t = md-s*R@ms; return s, R, t
RI = gi.load(REFP); RM = ref_mask(RI); TIPR = (225, 255)
RQ, RL, RS = analyse(RM, 1.0, TIPR); OUT = {'ref': {'landmarks': {k: [round(float(v), 1) for v in RQ[i]] for k, i in RL.items()}, 'segments': RS}}
print('REF   ' + ' '.join('%s(%.1f,%.1f)' % (k, RQ[i][0], RQ[i][1]) for k, i in RL.items()))
ALIGN = ['tip', 'sn', 'ls', 'sto', 'li', 'sm', 'pg']; CQ = {}
for lab, p in CANDS:
    I = gi.load(p); M = alpha_mask(I); Q, L, S = analyse(M, 2.0, TIPR)
    keys = [k for k in ALIGN if k in L and k in RL]; s, R, t = similarity(np.array([Q[L[k]] for k in keys]), np.array([RQ[RL[k]] for k in keys]))
    Qa = (s*(R@Q.T)).T+t; CQ[lab] = (Qa, L)
    res = {k: [round(float(v), 2) for v in (Qa[L[k]]-RQ[RL[k]])] for k in L if k in RL}
    res_mm = {k: [round(v/s*MMPX, 2) for v in r] for k, r in res.items()}
    OUT[lab] = {'scale_ref_per_cand': round(float(s), 4), 'rot_deg': round(math.degrees(math.atan2(R[1, 0], R[0, 0])), 2), 'landmarks': {k: [round(float(v), 1) for v in Q[i]] for k, i in L.items()},
                'residual_refpx(+x=back,+y=down)': res, 'residual_mm_model': res_mm, 'segments': S}
    print('%-6s scale %.3f rot %.1f | ' % (lab, s, OUT[lab]['rot_deg']) + ' '.join('%s(%+.1f,%+.1f)' % (k, r[0], r[1]) for k, r in res_mm.items()))
print('SEGMENT SHAPE (sag/chord at t=.1..9, + = outward; max sag @t; chord angle deg from vertical, + = going back)')
for sg in [a_+'-'+b_ for a_, b_ in SEGS]:
    rows = []
    for lab, d in [('REF', RS)] + [(l, OUT[l]['segments']) for l, _ in CANDS]:
        if sg in d: v = d[sg]; rows.append('%-6s max %+.3f@%.2f ang %+6.1f chord %5.1f | %s' % (lab, v['max_sag'], v['t_max'], v['angle'], v['chord'], ' '.join('%+.3f' % x for x in v['sag'])))
    if rows: print(' ' + sg); [print('   ' + r) for r in rows]
json.dump(OUT, open(OUTJ, 'w'), indent=1)
# overlay: ref crop 6x, ref outline orange, candidates cyan / magenta / green / yellow, landmarks as squares
x0, x1, y0, y1 = 20, 140, 220, 380; Z = 6; C = RI[y0:y1, x0:x1].copy(); C = gi.resize(C, (x1-x0)*Z, (y1-y0)*Z)
COL = [(1.0, 0.55, 0.0), (0.0, 0.9, 1.0), (1.0, 0.2, 0.9), (0.3, 1.0, 0.3), (1.0, 1.0, 0.2)]
def draw(Q, L, col, sq):
    for x, y in Q:
        c, r = int((x-x0)*Z), int((y-y0)*Z)
        if 1 <= r < C.shape[0]-1 and 1 <= c < C.shape[1]-1: C[r-1:r+2, c-1:c+2, :3] = col
    for k, i in L.items():
        x, y = Q[i]; c, r = int((x-x0)*Z), int((y-y0)*Z)
        if sq <= r < C.shape[0]-sq and sq <= c < C.shape[1]-sq: C[r-sq:r+sq, c-sq:c+sq, :3] = col
draw(RQ, RL, COL[0], 5)
for n, (lab, _) in enumerate(CANDS): draw(CQ[lab][0], CQ[lab][1], COL[1+n % 4], 4)
gi.save(OUTI, C); print('CONTOUR_OK', OUTI)
