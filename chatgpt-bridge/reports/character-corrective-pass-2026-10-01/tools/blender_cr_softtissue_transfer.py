"""CORRECTIVE pass: Henley correctives inherit the body's soft-tissue pose morphs (RV_Bend*/RV_Arm*/RV_ArmFwd*/RV_Twist*).
Cause found 2026-10-01: the garment corrective solve collided against posed-body readbacks WITHOUT morph targets, so the breast
'hang' of RV_Bend60/90 (up to 3 cm) pushed the chest through the Henley in crouch / deep bends.
Rule per curve, per Henley LOD0 vertex near the body (<3 cm): body delta d_b = gaussian-weighted mean of nearby body deltas;
along u = d_b/|d_b| the shirt must move at least |d_b|: add max(0, |d_b| - old.u) * u * falloff(dist).
usage: blender -b --factory-startup --python blender_cr_softtissue_transfer.py -- <body_rv.npz> <outfit_geometry.json.gz> <cur_src.json> <cur_out.json>"""
import sys, json, gzip, numpy as np
from mathutils import Vector, kdtree
a = sys.argv[sys.argv.index('--')+1:]; NPZ, GEO, SRC, OUT = a
B = np.load(NPZ); ue = lambda p: np.stack([p[:, 0], -p[:, 1], p[:, 2]], 1)*100.0
rest = ue(B['base']+B['BR_Neutral']+B['LK_Neutral'])
G = json.loads(gzip.open(GEO, 'rb').read()); H = np.asarray(G['henley']['positions']); cur = json.load(open(SRC))
kd = kdtree.KDTree(len(rest))
for i, p in enumerate(rest): kd.insert(Vector(p), i)
kd.balance()
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
near = []; dist = np.zeros(len(H))
for i, p in enumerate(H):
    r = kd.find_range(Vector(p), 3.0); near.append([(j, d) for _, j, d in r]); dist[i] = min([d for _, _, d in r], default=99)
fall = sstep((3.0-dist)/2.0)
CURVES = [k for k in B.files if k.startswith('RV_') and not k.startswith('RV_Hip')]
stats = {}
for c in CURVES:
    D = ue(B[c])/1.0; D = np.stack([D[:, 0], D[:, 1], D[:, 2]], 1)   # deltas: same axis map (ue() includes *100 m->cm)
    old = cur['henley'].get(c, {}); new = dict(old); nadd = 0; mx = 0.0
    for i in range(len(H)):
        if fall[i] <= 0 or not near[i]: continue
        js = np.array([j for j, _ in near[i]]); ws = np.exp(-(np.array([d for _, d in near[i]])/1.0)**2)
        db = (D[js]*ws[:, None]).sum(0)/ws.sum(); m = np.linalg.norm(db)
        if m < 0.02: continue
        u = db/m; o = np.asarray(old.get(str(i), [0.0, 0.0, 0.0])); need = (m-float(o@u))*fall[i]
        if need <= 0.005: continue
        new[str(i)] = [round(float(x), 5) for x in o+need*u]; nadd += 1; mx = max(mx, need)
    cur['henley'][c] = new; stats[c] = {'henley_verts_adjusted': nadd, 'max_added_cm': round(mx, 3), 'verts_total': len(new)}
cur['_stats']['softtissue_transfer'] = stats
json.dump(cur, open(OUT, 'w')); print('STT_OK', json.dumps(stats))
