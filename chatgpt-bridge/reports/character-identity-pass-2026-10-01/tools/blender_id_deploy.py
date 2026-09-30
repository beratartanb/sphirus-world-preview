"""IDENTITY pass: MetaHuman-state geometry -> BR_Neutral morph files for the rigged derivative face (all LODs).
identity delta per LOD = s*R(export_new_L - export_base_L) (MetaHumanCharacter exports of the fitted state vs the unedited import;
same LOD vertex order as SKM_RV_FaceMesh, verified per LOD), + the original collar deltas (br_neutral - accepted_b2, barycentric per
LOD), seam guard (z < 146.5 cm: collar only). Eyes / teeth / saliva deltas zeroed on LOD0 (joint-driven meshes stay on their joints).
usage: blender -b -P blender_id_deploy.py -- <new export name> <out_dir> [base export name]"""
import sys, os, json, gzip
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import *
a = sys.argv[sys.argv.index('--')+1:]; NEW, OUT = a[0], a[1]; BASE = a[2] if len(a) > 2 else 'MHC_ID_Base'; os.makedirs(OUT, exist_ok=True)
LODD = 'Saved/Codex/CharacterShoulderFix_20260928/HighElevCorrective_20260929'
P = pkg(); T = np.asarray(P['head']['triangles']); X = head_base(); BR = head_brn()-X
B0, N0 = export_lod(BASE, 0), export_lod(NEW, 0); Tf = umeyama(B0[:24049], X[:24049]); s, R, t = Tf
def sstep(v): v = np.clip(v, 0, 1); return v*v*(3-2*v)
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(tt) for tt in T])
def bary_transfer(PL, F):
    out = np.zeros((len(PL), 3))
    for vi, p in enumerate(PL):
        loc, nrm, fi, dist = bvh.find_nearest(Vector(p))
        if fi is None or dist > 1.0: continue
        tri = T[fi]; A_, B_, C_ = X[tri]; q = np.asarray(loc); v0, v1, v2 = B_-A_, C_-A_, q-A_; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01 or 1e-12
        bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; out[vi] = (1-bv-bw)*F[tri[0]]+bv*F[tri[1]]+bw*F[tri[2]]
    return out
info = json.load(open(os.path.join(LODD, 'lod_info.json')))['Head']; rep = {}
for L in range(info['lods']):
    PL = X if L == 0 else np.asarray(json.load(gzip.open(os.path.join(LODD, f'lod_Head_{L}.json.gz'), 'rt'))['positions'])
    BL, NL = export_lod(BASE, L), export_lod(NEW, L)
    order_err = float(np.linalg.norm(apply(Tf, BL)-PL, axis=1).mean()) if len(BL) == len(PL) else 1e9
    if len(BL) == len(PL) and order_err < 1.0: dId = s*((NL-BL)@R.T); how = 'direct'
    else: dId = bary_transfer(PL, s*((N0-B0)@R.T)); how = 'barycentric'
    if L == 0: dId[SEG['teeth'][0]:SEG['eyeR'][1]] = 0.0
    g = sstep((PL[:, 2]-146.5)/2.0)[:, None]; dId *= g
    col = BR if L == 0 else bary_transfer(PL, BR)
    TOT = col+dId; m = np.linalg.norm(TOT, axis=1); ids = np.nonzero(m > 1e-5)[0]
    json.dump({'Body': {}, 'Head': {'BR_Neutral': {str(int(i)): [round(float(v), 5) for v in TOT[i]] for i in ids}}}, open(os.path.join(OUT, f'morph_fm_face_lod{L}.json'), 'w'))
    rep[L] = {'how': how, 'order_err_mm': round(order_err*10, 2), 'id_max_mm': round(float(np.linalg.norm(dId, axis=1).max()*10), 2), 'verts': int(len(ids))}
    if L == 0: np.save(os.path.join(OUT, 'neutral_lod0.npy'), X+TOT)
# seam normals: body vertex normal at each weld pair -> override for the head boundary vertex (LOD0, package index)
NBODY = np.asarray(P['br_neutral'])[:P['NB']]; TB = np.asarray(P['body']['triangles']); Nb = np.zeros_like(NBODY); fb = -np.cross(NBODY[TB[:, 1]]-NBODY[TB[:, 0]], NBODY[TB[:, 2]]-NBODY[TB[:, 0]])
for k in range(3): np.add.at(Nb, TB[:, k], fb)
Nb /= np.maximum(np.linalg.norm(Nb, axis=1), 1e-9)[:, None]; Wp = np.asarray(P['weld_pairs'])
json.dump({str(int(h-P['NB'])): [round(float(v), 6) for v in Nb[b]] for b, h in Wp}, open(os.path.join(OUT, 'seam_normals_lod0.json'), 'w'))
json.dump(rep, open(os.path.join(OUT, 'deploy.json'), 'w'), indent=1); print('DEPLOY', json.dumps(rep))
