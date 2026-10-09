"""2 x 4 identity check: reference panel crops (top) over candidate renders in the same solved cameras (bottom), face-framed crops (2x px)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import gd13_img as gi; from gd13_common import ROOT
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; LAB = a[1]; RD = a[2]
CROP = {'front': (240, 260, 740, 830), 'q3_faceR': (380, 250, 880, 820), 'q3_faceL': (120, 250, 620, 820), 'prof_faceL': (60, 220, 560, 790)}
top, bot = [], []
for v, (x0, y0, x1, y1) in CROP.items():
    R = gi.load(f'{ROOT}/SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_{v}.png'); R = gi.resize(R, R.shape[1]*2, R.shape[0]*2)
    C = gi.load(f'{RD}/{LAB}_REF_{v}_skinA.png'); W, H = 420, int(420*(y1-y0)/(x1-x0))
    top.append(gi.resize(R[y0:y1, x0:x1], W, H)); bot.append(gi.resize(C[y0:y1, x0:x1], W, H))
gi.save(OUT, np.concatenate([np.concatenate(top, 1), np.concatenate(bot, 1)], 0)); print('QUAD_OK')
