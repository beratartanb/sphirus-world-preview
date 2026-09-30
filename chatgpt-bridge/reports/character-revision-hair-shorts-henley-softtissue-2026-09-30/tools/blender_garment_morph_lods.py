"""Merge the garment corrective solves and write one bake file per LOD ({'Henley': {curve: {vid: d}}, 'Shorts': {...}}).
LOD1 / LOD2 (Blender un-subdivide + light detail decimation) take the delta of the nearest LOD0 rest vertex.
usage: blender -b --factory-startup --python blender_garment_morph_lods.py -- <geometry.json.gz> <out_dir> <solve1.json> [<solve2.json> ...]"""
import sys, json, gzip, os
import numpy as np
from mathutils import Vector, kdtree
a = sys.argv[sys.argv.index('--')+1:]; GEO, OUT = a[0], a[1]; SOLVES = a[2:]
G = json.loads(gzip.open(GEO, 'rb').read())
M = {'henley': {}, 'trousers': {}}
for f in SOLVES:
    d = json.load(open(f))
    for g in M:
        for c, v in d.get(g, {}).items():
            if v: M[g][c] = v
NAME = {'henley': 'Henley', 'trousers': 'Shorts'}
# per-curve gain (art direction of the progression, e.g. small opening at 20-30 deg): SPH_GMORPH_SCALE="RV_Bend30:0.4,RV_Bend60:0.8"
SC = {kv.split(':')[0]: float(kv.split(':')[1]) for kv in os.environ.get('SPH_GMORPH_SCALE', '').split(',') if ':' in kv}
for g in M:
    for c in list(M[g]):
        if c in SC: M[g][c] = {i: [round(x*SC[c], 5) for x in d] for i, d in M[g][c].items()}
print('gains', SC)
for L in (0, 1, 2):
    out = {'Henley': {}, 'Shorts': {}}
    for g, curves in M.items():
        key = g if L == 0 else f'{g}_lod{L}'; X0 = np.asarray(G[g]['positions'])
        if L == 0:
            for c, v in curves.items(): out[NAME[g]][c] = v
            continue
        XL = np.asarray(G[key]['positions']); kd = kdtree.KDTree(len(X0))
        for i, p in enumerate(X0): kd.insert(Vector(p), i)
        kd.balance(); near = [kd.find(Vector(p))[1] for p in XL]
        for c, v in curves.items():
            dd = {}
            for j, i0 in enumerate(near):
                if str(i0) in v: dd[str(j)] = v[str(i0)]
            out[NAME[g]][c] = dd
    fn = os.path.join(OUT, f'morph_rv_garments_lod{L}.json'); json.dump(out, open(fn, 'w'))
    print('LOD', L, {k: {c: len(v) for c, v in d.items()} for k, d in out.items()})
print('GMORPH_OK')
