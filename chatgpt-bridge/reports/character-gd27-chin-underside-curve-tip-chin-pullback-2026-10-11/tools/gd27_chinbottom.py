"""GD27 chin-bottom / submental residuals: the candidate outline is mapped onto the reference with the least-squares similarity on ALL common
landmarks (tip, sn, ls, sto, li, sm, pg) - the global profile frame - and every candidate outline point from START (a landmark, e.g. pg) along
the arc for LEN panel px (past the chin turn into the submental line) gets its signed distance to the reference outline in model mm
(+ = must move OUT toward the background, i.e. down for the underside) and the 3D skin vertex that forms it (solved prof_faceL camera).
usage: -- <ref panel> <cand alpha 2x> <cams json> <head.npy> <START> <LEN px> [step px=2]"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD27_Identity_20261011/tools'))
import gd13_img as gi; from gd13_common import NS, MX, project
from gd27_contour_lib import ref_mask, alpha_mask, analyse, similarity, MMPX
a = sys.argv[sys.argv.index('--')+1:]; REFP, CANDP, CAMS, HEAD, START = a[:5]; LEN = float(a[5]); STEP = float(a[6]) if len(a) > 6 else 2.0
TIPR = (225, 255); RM = ref_mask(gi.load(REFP)); RQ, RL, _ = analyse(RM, 1.0, TIPR); CQ, CL, _ = analyse(alpha_mask(gi.load(CANDP)), 2.0, TIPR)
keys = [k for k in ('tip', 'sn', 'ls', 'sto', 'li', 'sm', 'pg') if k in RL and k in CL]
s, R, t = similarity(np.array([CQ[CL[k]] for k in keys]), np.array([RQ[RL[k]] for k in keys])); CA = (s*(R@CQ.T)).T+t
C = json.load(open(CAMS))['prof_faceL']; X = np.load(HEAD); S = X[:NS]; P = project(C, S); front = (S[:, 1] > 8.0) & (S[:, 2] > 149.5) & (S[:, 2] < 160.5)
arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(CQ, axis=0), axis=1))]; i0 = CL[START]; last = -1e9
print('global similarity on %s: scale %.3f rot %.1f deg' % (','.join(keys), s, math.degrees(math.atan2(R[1, 0], R[0, 0]))))
print('  arc   z       y      x-MX   need_mm   (+ = move OUT/down)')
for i in range(i0, len(CQ)):
    if arc[i]-arc[i0] > LEN: break
    if arc[i]-last < STEP: continue
    last = arc[i]; p = CA[i]; d = np.linalg.norm(RQ-p, axis=1); j = int(np.argmin(d)); r, c = int(round(p[1])), int(round(p[0]))
    inside = RM[r, c] if (0 <= r < RM.shape[0] and 0 <= c < RM.shape[1]) else False; need = (d[j] if inside else -d[j])/s*MMPX
    q = front & (np.abs(P[:, 0]-CQ[i, 0]) < 1.5) & (np.abs(P[:, 1]-CQ[i, 1]) < 1.5)
    src = ('%7.2f %6.2f %+5.2f' % (S[k, 2], S[k, 1], S[k, 0]-MX)) if q.any() and (k := np.nonzero(q)[0][np.argmin(np.linalg.norm(P[q]-CQ[i], axis=1))]) is not None else '   .      .     .  '
    print('%6.1f %s   %+5.2f' % (arc[i]-arc[i0], src, need))
