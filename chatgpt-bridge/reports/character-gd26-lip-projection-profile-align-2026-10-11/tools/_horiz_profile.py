"""Horizontal landmark positions relative to subnasale, normalized by the sn->me vertical distance (camera frame; + = in front of sn). Prints
also the model-mm difference to the reference (ratio diff x candidate sn-me height x 10/14.78). usage: -- <ref panel> label=alpha.png [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD26_Identity_20261011/tools'))
import gd13_img as gi
from gd26_contour_lib import ref_mask, alpha_mask, analyse, MMPX
a = sys.argv[sys.argv.index('--')+1:]; TIPR = (225, 255); KEYS = ['tip', 'ls', 'sto', 'li', 'sm', 'pg', 'gn', 'me']
def rel(Q, L):
    sn = Q[L['sn']]; H = Q[L['me']][1]-sn[1]; return {k: ((sn[0]-Q[L[k]][0])/H, (Q[L[k]][1]-sn[1])/H) for k in KEYS if k in L}, H
RQ, RL, _ = analyse(ref_mask(gi.load(a[0])), 1.0, TIPR); R, RH = rel(RQ, RL)
print('pt    REF fwd/H  down/H | ' + ' | '.join('%s fwd/H  down/H  dFwd_mm dDown_mm' % s.split('=')[0] for s in a[1:]))
C = []
for s in a[1:]:
    lab, p = s.split('=', 1); Q, L, _ = analyse(alpha_mask(gi.load(p)), 2.0, TIPR); C.append(rel(Q, L))
for k in KEYS:
    if k not in R: continue
    row = '%-4s  %+.4f  %+.4f | ' % (k, R[k][0], R[k][1])
    for d, H in C:
        if k in d: row += '%+.4f  %+.4f  %+5.2f  %+5.2f | ' % (d[k][0], d[k][1], (d[k][0]-R[k][0])*H*MMPX, (d[k][1]-R[k][1])*H*MMPX)
    print(row)
print('(fwd/H: horizontal distance in front of subnasale / sn-me height; dFwd_mm > 0 = model point is further FORWARD than the reference proportion)')
