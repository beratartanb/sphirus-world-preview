"""GD33 lid read-out helper: per image and eye, the iris centre (darkest 7x7 mean in the eye window, below the lash band) and the luminance /
saturation profile of the 5 columns through it (rows 380..460, 2x front frame), plus the visible-iris height = rows of the central run whose
saturation > SATI and luminance < 0.75 x skin (iris tissue, excluding near-black lashes lum < 0.10 x skin is NOT required: the run is cut at the
first lash-dark row). Prints the run and the profile so the lid margins can be checked by eye.
usage: blender -b --factory-startup --python gd33_lidprofile.py -- label=image ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; SATI = float(os.environ.get('SATI', '0.28'))
EYES = {'imgL': (395, 475, 395, 450), 'imgR': (565, 650, 395, 450)}
for it in a:
    lab, p = it.split('=', 1)
    if p == 'REF': I = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png'); I = gi.resize(I, I.shape[1]*2, I.shape[0]*2)
    else: I = gi.load(p)
    I = I[..., :3]; L = I @ np.array([0.30, 0.59, 0.11]); mx = I.max(2); mn = I.min(2); S = (mx-mn)/np.maximum(mx, 1e-4)
    for side, (c0, c1, r0, r1) in EYES.items():
        W_ = L[r0:r1, c0:c1]; k = np.ones(7)/7; B = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, W_); B = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, B)
        B[:4] = B[-4:] = 9; B[:, :4] = B[:, -4:] = 9; r, c = np.unravel_index(np.argmin(B), B.shape); pr, pc = r0+r, c0+c
        sk = np.percentile(L[370:470, c0:c1], 90); lp = L[370:470, pc-2:pc+3].mean(1)/sk; sp = S[370:470, pc-2:pc+3].mean(1)
        iris = (sp > SATI) & (lp < 0.75); i = pr-370; top = i; bot = i
        while top > 0 and iris[top-1]: top -= 1
        while bot < len(iris)-1 and iris[bot+1]: bot += 1
        print('LID %-10s %s pupil (%d,%d) iris run rows %d..%d = %d px' % (lab, side, pc, pr, 370+top, 370+bot, bot-top+1))
        print('   lum ' + ' '.join('%02d' % int(100*v) for v in lp[10:90:2]))
        print('   sat ' + ' '.join('%02d' % int(100*v) for v in sp[10:90:2]))
