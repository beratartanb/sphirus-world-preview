"""Garment deformation QA over captured posed geometry (real UE skinning + morphs + SHCB helper), numpy/BVH in Blender:
per pose: garment-vs-body signed clearance (penetration count/depth by region), garment self/trouser-shirt layering,
triangle stretch vs neutral, degenerate/flipped triangles. blender -b --python this.py -- <captures_dir> <label> <out.json>"""
import bpy, sys, os, json, gzip
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
argv = sys.argv[sys.argv.index('--')+1:]; CAP, LABEL, OUT = argv
PG = os.path.join(CAP, 'posed_geometry')
def load(name, part):
    p = os.path.join(PG, f'{name}_{part}.json.gz')
    if not os.path.exists(p): return None
    d = json.loads(gzip.open(p, 'rb').read()); return np.asarray(d['positions'], np.float64), np.asarray(d['triangles'], np.int64)
def tri_normals(P, T):
    n = np.cross(P[T[:, 1]]-P[T[:, 0]], P[T[:, 2]]-P[T[:, 0]]); a = np.linalg.norm(n, axis=1); return n/np.maximum(a, 1e-12)[:, None], a*0.5
def edge_len(P, T):
    e = np.concatenate([P[T[:, 1]]-P[T[:, 0]], P[T[:, 2]]-P[T[:, 1]], P[T[:, 0]]-P[T[:, 2]]]); return np.linalg.norm(e, axis=1)
def bvh(P, T): return BVHTree.FromPolygons([Vector(p*0.01) for p in P], [[int(t[0]), int(t[2]), int(t[1])] for t in T])  # UE winding -> outward normals in a right-handed frame
def signed_dist(bv, P, Tn=None):
    out = np.zeros(len(P))
    for i, p in enumerate(P):
        loc, nrm, idx, dist = bv.find_nearest(Vector(p*0.01))
        if loc is None: out[i] = 99; continue
        out[i] = dist*100*(1 if (Vector(p*0.01)-loc).dot(nrm) >= 0 else -1)
    return out
cases = json.load(open(os.path.join(CAP, LABEL+'_results.json')))
names = [c['name'] for c in cases if c.get('measure')]
ref = {}
res = {'label': LABEL, 'poses': {}}
for nm in names:
    body = load(nm, 'Body'); head = load(nm, 'Head'); hen = load(nm, 'Henley'); trs = load(nm, 'Shorts')
    if body is None or hen is None or trs is None: res['poses'][nm] = 'missing'; continue
    BP, BT = body; HP, HT = head if head else (np.zeros((0, 3)), np.zeros((0, 3), np.int64))
    # body mesh only: the head mesh has interior surfaces (mouth, eye sockets) that produce false 'inside' results
    AP = BP; AT = BT
    bv = bvh(AP, AT); row = {}
    for gname, (GP, GT) in (('henley', hen), ('shorts', trs)):
        d = signed_dist(bv, GP); pen = (d < -0.05) & (GP[:, 2] < 143.5)   # the body mesh ends at the neck seam (~143): collar vertices above it have no reference surface
        # region split by height band of the neutral garment (approx): use current z
        z = GP[:, 2]
        bands = {'upper': z > 118, 'mid': (z <= 118) & (z > 92), 'lower': (z <= 92) & (z > 45), 'low': z <= 45}
        row[gname] = {'verts': int(len(GP)), 'penetrating': int(pen.sum()), 'pen_ratio': round(float(pen.mean()), 4), 'max_penetration_cm': round(float(-d[pen].min()), 3) if pen.any() else 0.0,
                      'clearance_p5_cm': round(float(np.percentile(d, 5)), 3), 'clearance_median_cm': round(float(np.median(d)), 3),
                      'bands': {k: {'n': int(m.sum()), 'pen': int((pen & m).sum()), 'maxpen': round(float(-d[pen & m].min()), 3) if (pen & m).any() else 0.0} for k, m in bands.items() if m.any()}}
        n, a = tri_normals(GP, GT); row[gname]['degenerate_tris'] = int((a < 1e-4).sum()); row[gname]['finite'] = bool(np.isfinite(GP).all())
        rk = (gname, len(GT))
        if rk not in ref: ref[rk] = (GP.copy(), GT.copy(), edge_len(GP, GT), n.copy())
        else:
            e0 = ref[rk][2]; e = edge_len(GP, GT); s = e/np.maximum(e0, 1e-6)
            row[gname]['stretch_p99'] = round(float(np.percentile(s, 99)), 3); row[gname]['stretch_max'] = round(float(s.max()), 3); row[gname]['compress_p01'] = round(float(np.percentile(s, 1)), 3)
            row[gname]['flipped_vs_ref'] = int(((n*ref[rk][3]).sum(1) < 0).sum())
    # shirt-over-trousers layering: shirt verts below the waistband top must stay outside the trousers (except the tucked front)
    tb = bvh(trs[0], trs[1]); hz = hen[0][:, 2]; sel = (hz < 105.0) & (hz > 92)
    if sel.any():
        d2 = signed_dist(tb, hen[0][sel]); inside = (d2 < -0.1) & (d2 > -3.0)   # only shirt vertices actually near the trouser surface
        row['shirt_inside_shorts_verts'] = int(inside.sum()); row['shirt_inside_shorts_max_cm'] = round(float(-d2[inside].min()), 3) if inside.any() else 0.0
    res['poses'][nm] = row; print(nm, json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk in ('penetrating', 'max_penetration_cm', 'clearance_p5_cm', 'stretch_p99')}) for k, v in row.items()}), flush=True)
json.dump(res, open(OUT, 'w'), indent=1); print('EVAL_OK')
