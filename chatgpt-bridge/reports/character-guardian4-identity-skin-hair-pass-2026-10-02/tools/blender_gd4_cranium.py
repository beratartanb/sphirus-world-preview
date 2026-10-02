"""GUARDIAN-4: cranium large-form metrics of DNA-order heads (project frame, UE cm; skin only).
vertex height above the eye line / above the tragion level, glabella-opisthocranion length, breadth profile (max |x| width per z band above
the eyes), frontal slope (forehead y at heights above the brow), and a 'dome index' = breadth at +8 cm / max breadth (narrow-top read).
usage: blender -b -P blender_gd4_cranium.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; ez = (X[28955:29725, 2].mean()+X[29725:30495, 2].mean())/2; mx = (X[28955:29725, 0].mean()+X[29725:30495, 0].mean())/2
    top = S[S[:, 2] > ez].copy(); vz = S[:, 2].max()
    mid = np.abs(S[:, 0]-mx) < 0.6
    g = S[mid & (np.abs(S[:, 2]-(ez+1.2)) < 0.6)]; gl = g[np.argmax(g[:, 1])]
    o = S[mid & (S[:, 2] > ez-3) & (S[:, 2] < ez+8)]; op = o[np.argmin(o[:, 1])]
    br = {}
    for dz in (0, 2, 4, 6, 8, 10, 11):
        b = S[(np.abs(S[:, 2]-(ez+dz)) < 0.2) & (S[:, 1] < 4.0)]
        if len(b) > 4: br[f'+{dz}'] = round(float(b[:, 0].max()-b[:, 0].min()), 2)
    fr = {}
    for dz in (2, 4, 6, 8):
        f = S[mid & (np.abs(S[:, 2]-(ez+dz)) < 0.3)]
        if len(f): fr[f'+{dz}'] = round(float(f[:, 1].max()), 2)
    # temple: half-width just behind the lateral orbit (y 3..5) at +2..+4
    tp = S[(S[:, 2] > ez+1.5) & (S[:, 2] < ez+4) & (S[:, 1] > 2.5) & (S[:, 1] < 5.0)]
    mb = max(br.values())
    r = {'vertex_above_eyes': round(float(vz-ez), 2), 'length_gl_op': round(float(gl[1]-op[1]), 2), 'breadth': br, 'max_breadth': mb,
         'dome_index_8': round(br.get('+8', 0)/mb, 3), 'dome_index_10': round(br.get('+10', 0)/mb, 3), 'forehead_y': fr,
         'temple_halfwidth_L': round(float(tp[:, 0].max()-mx), 2), 'temple_halfwidth_R': round(float(mx-tp[:, 0].min()), 2)}
    print('CRANIUM', os.path.basename(hp), json.dumps(r))
