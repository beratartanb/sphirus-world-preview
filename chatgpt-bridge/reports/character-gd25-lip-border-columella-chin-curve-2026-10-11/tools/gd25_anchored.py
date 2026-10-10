"""GD25 anchored contour residuals: reference vs candidate profile silhouette compared LOCALLY - the candidate outline is mapped onto the reference
with the exact 2-point similarity defined by two landmarks (e.g. tip+sn for the nose underside, sn+sto for the upper lip, sto+sm for the lower
lip, sm+gn / sm+me for the chin), then every candidate outline point between (and a margin beyond) the anchors gets its signed distance to the
reference outline (+ = candidate OUTSIDE the reference, i.e. it must move inward; - = must move outward), converted to model mm (/scale * 10/14.78).
Each candidate outline point is also mapped back to the 3D skin vertex that forms it (nearest projected vertex with the solved prof_faceL camera),
so the table reads: 3D z / y / x-MX of the silhouette source and the required normal move.
usage: -- <ref panel> <cand alpha 2x> <cams json> <head.npy> <A> <B> <margin landmarks before,after e.g. 0,0> [step px=1.5]"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD25_Identity_20261011/tools'))
import gd13_img as gi; from gd13_common import NS, MX, project
from gd25_contour_lib import ref_mask, alpha_mask, analyse, MMPX
a = sys.argv[sys.argv.index('--')+1:]; REFP, CANDP, CAMS, HEAD, LA, LB = a[:6]; MB, MA = [float(v) for v in a[6].split(',')]; STEP = float(a[7]) if len(a) > 7 else 1.5
TIPR = (225, 255); RQ, RL, _ = analyse(ref_mask(gi.load(REFP)), 1.0, TIPR); CI = gi.load(CANDP); CQ, CL, _ = analyse(alpha_mask(CI), 2.0, TIPR)
for k in (LA, LB): assert k in RL and k in CL, k
def sim2(p0, p1, q0, q1):   # complex similarity mapping p -> q
    P0, P1, Q0, Q1 = [complex(*v) for v in (p0, p1, q0, q1)]; m = (Q1-Q0)/(P1-P0); return m, Q0-m*P0
m, t = sim2(CQ[CL[LA]], CQ[CL[LB]], RQ[RL[LA]], RQ[RL[LB]]); s = abs(m)
Z = CQ[:, 0]+1j*CQ[:, 1]; W = m*Z+t; CA = np.c_[W.real, W.imag]
# signed distance of mapped candidate points to the reference polyline (sign: + if the candidate point lies on the background side)
RM = ref_mask(gi.load(REFP))
def sdist(p):
    d = np.linalg.norm(RQ-p, axis=1); j = int(np.argmin(d)); r, c = int(round(p[1])), int(round(p[0]))
    inside = RM[r, c] if (0 <= r < RM.shape[0] and 0 <= c < RM.shape[1]) else False
    return (-d[j] if inside else d[j]), j
C = json.load(open(CAMS))['prof_faceL']; X = np.load(HEAD); S = X[:NS]; P = project(C, S); front = (S[:, 1] > 9.0) & (S[:, 2] > 150.5) & (S[:, 2] < 160.5)
iA, iB = CL[LA], CL[LB]; L = iB-iA; i0 = max(0, int(iA-MB*L)); i1 = min(len(CQ)-1, int(iB+MA*L))
print('anchors %s-%s  scale ref/cand %.3f  rot %.1f deg | cand pts %d..%d' % (LA, LB, s, math.degrees(math.atan2(m.imag, m.real)), i0, i1))
print(' t     z       y     x-MX   need_mm (+ = move OUT toward background, - = move IN)   ref_px')
last = -1e9; arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(CQ, axis=0), axis=1))]
for i in range(i0, i1+1):
    if arc[i]-last < STEP: continue
    last = arc[i]; d, j = sdist(CA[i]); need = -d/s*MMPX   # candidate outside (d>0) -> must move inward (negative)
    q = front & (np.abs(P[:, 0]-CQ[i, 0]) < 1.5) & (np.abs(P[:, 1]-CQ[i, 1]) < 1.5)
    if q.any():
        k = np.nonzero(q)[0][np.argmin(np.linalg.norm(P[q]-CQ[i], axis=1))]; xs = '%7.2f %6.2f %+5.2f' % (S[k, 2], S[k, 1], S[k, 0]-MX)
    else: xs = '   .      .     .  '
    print('%5.2f %s   %+5.2f   %+5.1f' % ((i-iA)/L, xs, need, d))
