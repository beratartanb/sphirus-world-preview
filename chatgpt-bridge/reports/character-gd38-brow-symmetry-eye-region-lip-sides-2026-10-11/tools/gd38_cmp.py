"""GD38 assembly check (copy of gd33_cmp.py): saved BP_GD38 in L_GD38_Eval_G31 (ue/g33_refS_*) vs the harness capture of the same composition and rest pose (ue/e6_xlid60_ref_*).
captures of the same composition (GD31 ue/cg31c4S_ref_<view>.png, read-only), both warped onto the same 2x panel frame. Region = the face
crop of the report boards (FACE rects) and the full frame. Values 0..1 per channel (sRGB). Also writes an amplified |diff| image per view.
usage: blender -b --factory-startup --python gd32_cmp.py -- <gd32 ue dir> <gd31 ue dir> <label> <out txt> <diff dir>"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; D32, D31, LB, OUT, DD = a
FACE = {'front': [240, 260, 740, 830], 'q3_faceR': [380, 250, 880, 820], 'q3_faceL': [120, 250, 620, 820], 'prof_faceL': [60, 220, 560, 790]}
lines = ['view       region  mean|d|  p95|d|  p99|d|  px>0.05   px>0.10']
for v, r in FACE.items():
    A = gi.load(f'{D32}/{LB}_refS_{v}.png')[..., :3]; B = gi.load(f'{D31}/'+os.environ.get('CMPB', 'e6_xlid60_ref')+f'_{v}.png')[..., :3]
    if A.shape != B.shape: lines.append(f'{v} SHAPE MISMATCH {A.shape} {B.shape}'); continue
    d = np.abs(A-B).max(2)
    for nm, m in (('face', d[r[1]:r[3], r[0]:r[2]]), ('frame', d)):
        lines.append('%-10s %-6s  %.4f   %.4f  %.4f  %6.2f %%  %6.2f %%' % (v, nm, m.mean(), np.percentile(m, 95), np.percentile(m, 99), 100*(m > 0.05).mean(), 100*(m > 0.10).mean()))
    E = np.clip(d*5, 0, 1); gi.save(f'{DD}/diff5x_{v}.png', np.dstack([E, E, E, np.ones_like(E)]))
open(OUT, 'w').write('\n'.join(lines)+'\n'); print('\n'.join(lines)); print('CMP_OK')
