"""GD28 nose-tip contour: traces the profile silhouette in BOTH directions from the nose tip (up the dorsum and down to the subnasale) for the
reference panel and a candidate alpha render, maps the candidate onto the reference with the exact 2-point similarity of two anchors
(default: a dorsum point UP px above the tip along the arc, and the subnasale), then prints per candidate point the signed distance to the
reference outline in model mm (+ = move OUT) with the 3D skin vertex forming it, plus the tangent-angle profile (curvature) around the tip.
usage: -- <ref panel> <cand alpha 2x> <cams json> <head.npy> [UP px=28] [step px=1.5]"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD28_Identity_20261011/tools'))
import gd13_img as gi; from gd13_common import NS, MX, project
from gd28_contour_lib import ref_mask, alpha_mask, trace, landmarks, MMPX
a = sys.argv[sys.argv.index('--')+1:]; REFP, CANDP, CAMS, HEAD = a[:4]; UP = float(a[4]) if len(a) > 4 else 28.0; STEP = float(a[5]) if len(a) > 5 else 1.5
def both(m, scale, tiprows=(225, 255)):
    r0, r1 = [int(round(r*scale)) for r in tiprows]
    cols = [np.nonzero(m[r])[0] for r in range(r0, r1)]; xs = [c.min() if c.size else 1e9 for c in cols]; r = r0+int(np.argmin(xs)); start = (r, int(min(xs)))
    A = trace(m, start, int(900*scale), True); Bq = trace(m, start, int(900*scale), False)
    down, up = (A, Bq) if A[min(15, len(A)-1), 0] > start[0] else (Bq, A)
    P = np.r_[up[::-1][:-1], down][:, ::-1]/scale; t0 = len(up)-1
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]; s = np.arange(0, seg[-1], 0.5)
    Q = np.c_[np.interp(s, seg, P[:, 0]), np.interp(s, seg, P[:, 1])]; k = np.exp(-0.5*(np.arange(-6, 7)*0.5/1.2)**2); k /= k.sum(); Qp = np.pad(Q, ((6, 6), (0, 0)), mode='edge')
    Q = np.c_[np.convolve(Qp[:, 0], k, 'valid'), np.convolve(Qp[:, 1], k, 'valid')]; ti = int(np.searchsorted(s, seg[t0]))
    i = ti; L = landmarks(Q[ti:]); sn = ti+L['sn']; tip = ti+int(np.argmin(Q[ti:ti+60, 0])); return Q, tip, sn
RM = ref_mask(gi.load(REFP)); RQ, Rt, Rs = both(RM, 1.0); CQ, Ct, Cs = both(alpha_mask(gi.load(CANDP)), 2.0)
def at_arc(Q, i0, d):   # index at arc distance d before i0 (d>0 = upward)
    ar = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; return int(np.argmin(np.abs(ar-(ar[i0]-d))))
Ru = at_arc(RQ, Rt, UP); scale_c = np.linalg.norm(CQ[Cs]-CQ[Ct])/np.linalg.norm(RQ[Rs]-RQ[Rt]); Cu = at_arc(CQ, Ct, UP*scale_c)
P0, P1, Q0, Q1 = [complex(*v) for v in (CQ[Cu], CQ[Cs], RQ[Ru], RQ[Rs])]; mm = (Q1-Q0)/(P1-P0); tt = Q0-mm*P0; s = abs(mm)
W = mm*(CQ[:, 0]+1j*CQ[:, 1])+tt; CA = np.c_[W.real, W.imag]
C = json.load(open(CAMS))['prof_faceL']; X = np.load(HEAD); S = X[:NS]; P = project(C, S); nose = (S[:, 1] > 11.5) & (S[:, 2] > 156.8) & (S[:, 2] < 163.0)
print('anchors: dorsum point %.0f px above tip + subnasale | scale %.3f rot %.1f deg | ref tip (%.1f,%.1f) cand tip mapped (%.1f,%.1f) -> tip offset mm (+x back, +y down): %+.2f %+.2f' % (
    UP, s, math.degrees(math.atan2(mm.imag, mm.real)), RQ[Rt][0], RQ[Rt][1], CA[Ct][0], CA[Ct][1], (CA[Ct][0]-RQ[Rt][0])/s*MMPX, (CA[Ct][1]-RQ[Rt][1])/s*MMPX))
ar = np.r_[0, np.cumsum(np.linalg.norm(np.diff(CQ, axis=0), axis=1))]; last = -1e9
print('  arc_from_tip   z       y      x-MX   need_mm (+ = OUT)')
for i in range(Cu, Cs+1):
    if ar[i]-last < STEP: continue
    last = ar[i]; p = CA[i]; d = np.linalg.norm(RQ-p, axis=1); j = int(np.argmin(d)); r, c = int(round(p[1])), int(round(p[0]))
    inside = RM[r, c] if (0 <= r < RM.shape[0] and 0 <= c < RM.shape[1]) else False; need = (d[j] if inside else -d[j])/s*MMPX
    q = nose & (np.abs(P[:, 0]-CQ[i, 0]) < 1.5) & (np.abs(P[:, 1]-CQ[i, 1]) < 1.5)
    src = '   .      .     .  '
    if q.any(): k = np.nonzero(q)[0][np.argmin(np.linalg.norm(P[q]-CQ[i], axis=1))]; src = '%7.2f %6.2f %+5.2f' % (S[k, 2], S[k, 1], S[k, 0]-MX)
    print('  %+7.1f   %s   %+5.2f' % ((ar[i]-ar[Ct])/s, src, need))
# tangent-angle profile around the tip (deg from vertical-down, + = turning back), sampled at arc offsets normalized by the tip-sn chord
def tang(Q, ti, si, ups):
    ar = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; L = np.linalg.norm(Q[si]-Q[ti]); T = np.gradient(Q, axis=0); ang = np.degrees(np.arctan2(T[:, 0], T[:, 1]))
    return [float(np.interp(ar[ti]+f*L, ar, ang)) for f in ups]
F = [-0.8, -0.6, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.6]
print('tangent angle (deg) at arc offsets f x |tip-sn| (neg = above tip):  ' + ' '.join('%5.1f' % f for f in F))
print('  REF ' + ' '.join('%5.0f' % v for v in tang(RQ, Rt, Rs, F))); print('  CAN ' + ' '.join('%5.0f' % v for v in tang(CA, Ct, Cs, F)))
