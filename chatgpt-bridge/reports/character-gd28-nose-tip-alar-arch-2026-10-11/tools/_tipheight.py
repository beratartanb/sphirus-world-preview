"""Robust nose-tip height: centre row of the front-most contour region (points within D px of the minimum x, 1x panel px) relative to the subnasale
row, normalised by the subnasale->menton height; also its x relative to sn. Prints the model-mm difference to the reference.
usage: -- <ref panel> label=alpha.png [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD28_Identity_20261011/tools'))
import gd13_img as gi; from gd28_contour_lib import ref_mask, alpha_mask, analyse, MMPX
a = sys.argv[sys.argv.index('--')+1:]
def tipc(Q, L, D=0.7):
    seg = Q[:L['sn']]; mx = seg[:, 0].min(); m = seg[:, 0] < mx+D; return seg[m, 1].mean(), mx
RQ, RL, _ = analyse(ref_mask(gi.load(a[0])), 1.0, (225, 255)); ry, rx = tipc(RQ, RL); RH = RQ[RL['me']][1]-RQ[RL['sn']][1]
rr = (ry-RQ[RL['sn']][1])/RH; print('REF tip-centre rel row %.4f (fwd %.4f)' % (rr, (RQ[RL['sn']][0]-rx)/RH))
for s in a[1:]:
    lab, p = s.split('=', 1); Q, L, _ = analyse(alpha_mask(gi.load(p)), 2.0, (225, 255)); y, x = tipc(Q, L); Hh = Q[L['me']][1]-Q[L['sn']][1]; r = (y-Q[L['sn']][1])/Hh
    print('%-6s tip-centre rel row %.4f -> %+.2f mm (+ = LOWER than reference) | fwd %+.2f mm' % (lab, r, (r-rr)*Hh*MMPX, ((Q[L['sn']][0]-x)/Hh-(RQ[RL['sn']][0]-rx)/RH)*Hh*MMPX))
