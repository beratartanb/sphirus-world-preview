"""GUARDIAN-4: 3D landmark points (project frame, UE cm) of a DNA-order head from the mesh-bound tracker curves (semantic_j.json, front set):
curve endpoints / mid samples for the eyelids (canthi), lips (corners), brows. usage: blender -b -P blender_gd4_lm3d.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))['front']
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); out = {}
    for k, smp in SEM.items():
        if not any(t in k for t in ('eyelid', 'lip', 'brow')): continue
        P = np.array([np.asarray(w) @ X[np.asarray(i)] for i, w in smp]); out[k] = {'first': np.round(P[0], 3).tolist(), 'last': np.round(P[-1], 3).tolist(), 'mid': np.round(P[len(P)//2], 3).tolist(), 'n': len(P)}
    print('LM3D', os.path.basename(hp), json.dumps(out))
