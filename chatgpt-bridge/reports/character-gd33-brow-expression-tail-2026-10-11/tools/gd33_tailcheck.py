"""GD33: project the imgR (+x) stations of a brow3d json into the solved prof_faceL camera (2x px) and compare with the user's profile mask
path (reference px mapped into the model frame: about the lateral canthus, scale 1/K; REF canthus / model canthus read on the grid crops)."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import project
a = sys.argv[sys.argv.index('--')+1:]; CAMS, NPZ = a[0], a[1]; FILES = a[2:]; K = float(os.environ.get('PK', '1.087'))
CR = np.array([247.5, 390.0]); CM = np.array([252.0, 397.0]); C = json.load(open(CAMS))['prof_faceL']
P = np.load(NPZ)['path']; ref = CM+(P[:, [0, 2]]-CR)/K; rt = CM+(P[:, [0, 1]]-CR)/K; rb = CM+(P[:, [0, 3]]-CR)/K
print('REF(mapped) centre: ' + ' '.join('(%.0f,%.0f)' % tuple(p) for p in ref[::14]) + ' tip (%.0f,%.0f)' % tuple(ref[-1]))
for f in FILES:
    B = json.load(open(f)); q = project(C, np.array([s['cen'] for s in B['imgR']]))*2.0
    print('%-18s imgR centre: ' % os.path.basename(f) + ' '.join('(%.0f,%.0f)' % tuple(p) for p in q))
    # vertical gap to the mapped reference centre at the station columns
    gaps = [p[1]-np.interp(p[0], ref[:, 0], ref[:, 1]) for p in q if ref[:, 0].min() <= p[0] <= ref[:, 0].max()]
    print('   dy (model - ref, + = model lower) at stations:', ' '.join('%+.0f' % g for g in gaps))
