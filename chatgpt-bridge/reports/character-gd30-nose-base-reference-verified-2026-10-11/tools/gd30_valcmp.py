"""GD30 reference verification of nose-base feature lines: the same valley detector (Hessian of Gaussian-smoothed luminance, dark lines) is run on the
reference panel ROI and on candidate renders that are in the same solved-camera 2x panel frame; the reference lines are drawn red, each candidate's
lines cyan, over the grey reference (S x zoom, labelled grid). Probes measure feature positions identically on both: for a probe
'name:row:r0-r1:c0-c1' the column of the strongest valley inside c0..c1 is found on every row r0..r1 (vertical feature, e.g. the alar-facial crease),
for 'name:col:c0-c1:r0-r1' the row of the strongest valley on every column (horizontal feature, e.g. the lobule bottom edge); printed as REF mean,
candidate mean and candidate-REF in panel px and mm (mm per px given). A probe sample counts only where the valley strength is above THR on both.
Optional env GD30_ANCHOR=prof: every candidate valley map is mapped into the reference frame with the exact 2-point similarity of its
nose tip and subnasale (silhouette landmarks, same method as gd28_nosecontour) - removes the profile panel's ~5-13 % scale / offset.
usage: -- <out.jpg> <ref panel> <x0,x1,y0,y1> <S> <sigma> <mm_per_px> <probes ;-separated or -> label=render2x.png[|alpha2x.png] [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD30_Identity_20261011/tools')); from gd30_contour_lib import ref_mask, alpha_mask, trace, landmarks
ANCH = os.environ.get('GD30_ANCHOR', '')
a = sys.argv[sys.argv.index('--')+1:]; OUT, REF = a[0], a[1]; x0, x1, y0, y1 = [int(v) for v in a[2].split(',')]; S = int(a[3]); SIG = float(a[4]); MMPX = float(a[5])
PROBES = [] if a[6] == '-' else [p for p in a[6].split(';') if p]; CANDS = a[7:]; THR = 0.18
def gblur(A, s):
    r = int(3*s+1); k = np.exp(-0.5*(np.arange(-r, r+1)/s)**2); k /= k.sum(); P = np.pad(A, r, mode='edge')
    P = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 0, P); return np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 1, P)
def valley(path, sc, alpha=None):
    I = gi.load(path); C = I[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc), :3]; L = C.mean(-1)
    G = gblur(L, SIG*sc); gy, gx = np.gradient(G); gyy, gyx = np.gradient(gy); gxy, gxx = np.gradient(gx)
    tr = gxx+gyy; det = gxx*gyy-gxy*gyx; lam = np.maximum(tr/2+np.sqrt(np.maximum(tr**2/4-det, 0)), 0)
    if alpha is not None:
        A = gi.load(alpha)[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc), 3]; Ab = gblur(A, 2.0*sc); lam = lam*(Ab > 0.98)   # drop the silhouette edge
    lam = lam/max(np.percentile(lam[lam > 0], 98), 1e-9)
    if sc != 1: lam = gi.resize(np.dstack([lam]*3+[np.ones(lam.shape)]), x1-x0, y1-y0)[..., 0]   # to 1x panel px
    return np.clip(lam, 0, 1.5), C

def tipsn(m, scale, tiprows=(225, 255)):
    r0, r1 = [int(round(r*scale)) for r in tiprows]
    cols = [np.nonzero(m[r])[0] for r in range(r0, r1)]; xs = [c.min() if c.size else 1e9 for c in cols]; r = r0+int(np.argmin(xs)); start = (r, int(min(xs)))
    A = trace(m, start, int(900*scale), True); Bq = trace(m, start, int(900*scale), False)
    down, up = (A, Bq) if A[min(15, len(A)-1), 0] > start[0] else (Bq, A)
    P = np.r_[up[::-1][:-1], down][:, ::-1]/scale; t0 = len(up)-1
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; s = np.arange(0, seg[-1], 0.5)
    Q = np.c_[np.interp(s, seg, P[:, 0]), np.interp(s, seg, P[:, 1])]; k = np.exp(-0.5*(np.arange(-6, 7)*0.5/1.2)**2); k /= k.sum(); Qp = np.pad(Q, ((6, 6), (0, 0)), mode='edge')
    Q = np.c_[np.convolve(Qp[:, 0], k, 'valid'), np.convolve(Qp[:, 1], k, 'valid')]; ti = int(np.searchsorted(s, seg[t0]))
    L = landmarks(Q[ti:]); sn = ti+L['sn']; tip = ti+int(np.argmin(Q[ti:ti+60, 0])); return complex(*Q[tip]), complex(*Q[sn])
def warp_to_ref(Vm, mm, tt):
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(float); Pz = (xx+1j*yy-tt)/mm; cx = Pz.real-x0; cy = Pz.imag-y0
    ix = np.clip(np.floor(cx).astype(int), 0, Vm.shape[1]-2); iy = np.clip(np.floor(cy).astype(int), 0, Vm.shape[0]-2); fx = np.clip(cx-ix, 0, 1); fy = np.clip(cy-iy, 0, 1)
    out = Vm[iy, ix]*(1-fx)*(1-fy)+Vm[iy, ix+1]*fx*(1-fy)+Vm[iy+1, ix]*(1-fx)*fy+Vm[iy+1, ix+1]*fx*fy
    return np.where((cx >= 0) & (cx <= Vm.shape[1]-1) & (cy >= 0) & (cy <= Vm.shape[0]-1), out, 0.0)
RV, RC = valley(REF, 1)
if ANCH == 'prof': RT, RS = tipsn(ref_mask(gi.load(REF)), 1.0)
CV = []
for c in CANDS:
    lb, spec = c.split('=', 1); p = spec.split('|'); v, _ = valley(p[0], 2, p[1] if len(p) > 1 else None)
    if ANCH == 'prof' and len(p) > 1:
        CT, CS = tipsn(alpha_mask(gi.load(p[1])), 2.0); mm = (RS-RT)/(CS-CT); tt = RT-mm*CT; v = warp_to_ref(v, mm, tt)
        print('ANCHOR %-10s scale %.3f rot %.1f deg | ref tip (%.1f,%.1f) sn (%.1f,%.1f) cand tip (%.1f,%.1f) sn (%.1f,%.1f)' % (lb, abs(mm), np.degrees(np.angle(mm)), RT.real, RT.imag, RS.real, RS.imag, CT.real, CT.imag, CS.real, CS.imag))
    CV.append((lb, v))
def probe(Vm, pr):
    nm, ax, r1, r2 = pr.split(':'); a0, a1 = [int(t) for t in r1.split('-')]; b0, b1 = [int(t) for t in r2.split('-')]; out = {}
    for k in range(a0, a1+1):
        if ax == 'row':
            seg = Vm[k-y0, b0-x0:b1-x0+1]
        else:
            seg = Vm[b0-y0:b1-y0+1, k-x0]
        j = int(np.argmax(seg)); out[k] = (b0+j, seg[j])
    return out
print('probe            REF mean   ' + '   '.join('%-14s' % lb for lb, _ in CV))
for pr in PROBES:
    R = probe(RV, pr); row = '%-14s' % pr.split(':')[0]; good = [k for k, (p, s) in R.items() if s > THR]
    row += '  %6.1f     ' % np.mean([R[k][0] for k in good]) if good else '     -     '
    for lb, V in CV:
        Cp = probe(V, pr); g = [k for k in good if Cp[k][1] > THR]
        if g: d = np.mean([Cp[k][0]-R[k][0] for k in g]); row += '%6.1f (%+.1f px %+.2f mm n%d)  ' % (np.mean([Cp[k][0] for k in g]), d, d*MMPX, len(g))
        else: row += '      -                     '
    print(row)
W, H = (x1-x0)*S, (y1-y0)*S
base = gi.resize(np.dstack([RC, np.ones(RC.shape[:2])]), W, H); g = base[..., :3].mean(-1, keepdims=True)*0.5+0.3
tiles = []
for lb, V in [('REF', None)]+CV:
    T = np.zeros((H, W, 4)); T[..., 3] = 1; T[..., :3] = g
    Rz = gi.resize(np.dstack([RV]*3+[np.ones(RV.shape)]), W, H)[..., 0]; T[..., :3] = T[..., :3]*(1-np.clip(Rz, 0, 1)[..., None])+np.array([1.0, 0.1, 0.05])*np.clip(Rz, 0, 1)[..., None]
    if V is not None:
        Cz = np.clip(gi.resize(np.dstack([V]*3+[np.ones(V.shape)]), W, H)[..., 0], 0, 1); m = Cz > 0.30; T[m, :3] = T[m, :3]*0.25+np.array([0.1, 0.95, 1.0])*0.75*Cz[m, None]
    for X in range(x0, x1+1):
        if X % 5 == 0: T[:, min((X-x0)*S, W-1), :3] = T[:, min((X-x0)*S, W-1), :3]*0.6+(0.4 if X % 10 == 0 else 0.2)
    for Y in range(y0, y1+1):
        if Y % 5 == 0: T[min((Y-y0)*S, H-1), :, :3] = T[min((Y-y0)*S, H-1), :, :3]*0.6+(0.4 if Y % 10 == 0 else 0.2)
    tiles.append(T)
O = np.zeros((H, len(tiles)*(W+6)-6, 4)); O[..., 3] = 1
for i, T in enumerate(tiles): O[:, i*(W+6):i*(W+6)+W] = T
gi.save(OUT, O); print('VALCMP_OK', OUT)
