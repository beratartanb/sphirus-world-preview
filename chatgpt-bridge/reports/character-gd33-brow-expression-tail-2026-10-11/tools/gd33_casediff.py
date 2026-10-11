"""GD33: how much each rest-expression case changes the image vs the neutral case (same composition, camera, light): mean |diff| inside the
brow band and the eye band (2x front panel frame, hair hidden), plus the change of the eye-band mean luminance (+ = brighter / more open)."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; U, LB, CASES = a[0], a[1], a[2].split(',')
N = gi.load(f'{U}/{LB}_xneutral_refnh_front.png')[..., :3]; Ln = N @ np.array([0.30, 0.59, 0.11])
BROW = (slice(340, 395), slice(360, 690)); EYE = (slice(395, 445), slice(380, 670))
for c in CASES:
    I = gi.load(f'{U}/{LB}_x{c}_refnh_front.png')[..., :3]; L = I @ np.array([0.30, 0.59, 0.11]); d = np.abs(I-N).max(2)
    print('CASEDIFF %-8s brow mean|d| %.4f  eye mean|d| %.4f  eye px>0.05 %5.2f%%  eye lum %+.4f  brow lum %+.4f' % (c, d[BROW].mean(), d[EYE].mean(), 100*(d[EYE] > 0.05).mean(), L[EYE].mean()-Ln[EYE].mean(), L[BROW].mean()-Ln[BROW].mean()))
