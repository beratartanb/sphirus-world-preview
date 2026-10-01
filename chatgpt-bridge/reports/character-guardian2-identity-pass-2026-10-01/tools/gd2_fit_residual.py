"""GUARDIAN-2: MetaHumanCharacter fit residual = deployed BR_Neutral LOD0 head (deploy_<tag>/neutral_lod0.npy) vs the authored target head
(face/head<TAG>.npy), skin verts above the collar guard, per region (mm). Large residual where the sculpt asked for form = what the
MetaHuman fit (identity model) cannot express -> evidence for / against a BR_Neutral plateau.
usage: blender -b --factory-startup --python gd2_fit_residual.py -- <target.npy> <deploy dir> [<target2.npy> <deploy dir2> ...]"""
import sys, json, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
R = {'cranium/vault': lambda P: P[:, 2] > 167.0, 'forehead/brow': lambda P: (P[:, 2] > 163.0) & (P[:, 2] <= 167.0) & (P[:, 1] > 6),
     'orbits/lids': lambda P: (np.abs(np.abs(P[:, 0]+0.24)-3.1) < 1.8) & (np.abs(P[:, 2]-162.2) < 1.3) & (P[:, 1] > 9),
     'nose': lambda P: (np.abs(P[:, 0]+0.24) < 1.9) & (P[:, 2] > 157.6) & (P[:, 2] < 163.0) & (P[:, 1] > 12.3),
     'midface/cheeks': lambda P: (np.abs(P[:, 0]+0.24) > 2.0) & (np.abs(P[:, 0]+0.24) < 6.5) & (P[:, 2] > 154.0) & (P[:, 2] < 161.0) & (P[:, 1] > 6),
     'mouth/lips': lambda P: (np.abs(P[:, 0]+0.24) < 3.4) & (P[:, 2] > 154.0) & (P[:, 2] < 157.4) & (P[:, 1] > 11.0),
     'jaw/chin': lambda P: (P[:, 2] > 148.5) & (P[:, 2] < 154.0) & (P[:, 1] > 2)}
for tgt, dd in zip(a[0::2], a[1::2]):
    T = np.load(tgt)[:24049]; D = np.load(os.path.join(dd, 'neutral_lod0.npy'))[:24049]; m0 = T[:, 2] > 148.5; D = D-(D[m0]-T[m0]).mean(0); d = np.linalg.norm(D-T, axis=1)*10
    out = {k: [round(float(d[f(T) & m0].mean()), 2), round(float(np.percentile(d[f(T) & m0], 95)), 2)] for k, f in R.items()}
    out['all'] = [round(float(d[m0].mean()), 2), round(float(np.percentile(d[m0], 95)), 2)]
    print('RESID', os.path.basename(tgt), json.dumps(out))
