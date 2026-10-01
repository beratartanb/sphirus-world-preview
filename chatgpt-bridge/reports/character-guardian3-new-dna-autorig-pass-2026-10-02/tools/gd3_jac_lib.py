"""GUARDIAN-3 shared: load the face-model Jacobian (numpy, Blender python)."""
import numpy as np, json, glob, os
D = 'Saved/Codex/CharacterGuardian3_20261001/jac'
def load(dtype=np.float32):
    B = np.fromfile(D+'/base.f32', np.float32).reshape(-1, 3); c0 = np.asarray(json.load(open(D+'/coef.json')))
    Js = [np.fromfile(f, np.float32).reshape(-1, B.shape[0], 3) for f in sorted(glob.glob(D+'/J_*.f32'))]
    return B, c0, np.concatenate(Js, 0).astype(dtype)
SEGS = {'skin': (0, 24049), 'teeth': (24049, 28295), 'eyeL': (28955, 29725), 'eyeR': (29725, 30495)}
def coef_types(c0):
    """face-model coefficient layout (verified 2026-10-01): c[0] = region count; per region: quaternion(4) scale(1) translation(3) n_pca(1) pca(n)."""
    n = len(c0); T = np.array(['?']*n, dtype=object); T[0] = 'count'; i = 1; reg = []
    while i < n:
        T[i:i+4] = 'quat'; T[i+4] = 'scale'; T[i+5:i+8] = 'trans'; T[i+8] = 'count'; m = int(round(c0[i+8])); T[i+9:i+9+m] = 'pca'; reg.append((i, m)); i += 9+m
    return T, reg
