"""GD46: offline LBS vs PIE render readback (component space): nearest-point distances PIE->offline for Henley and body.
usage: blender -b --python gd46_validate.py -- <build_dir> <pie_posed_meshes.json.gz> <sculpt_package.json.gz>"""
import sys, json, gzip, numpy as np
from mathutils import Vector, kdtree
a = sys.argv[sys.argv.index('--')+1:]; BD, PM, PKG = a
pie = json.loads(gzip.open(PM, 'rt').read()); out = {}
for nm, f in (('Henley', 'henley_posed_start.json.gz'), ('Manny', 'body_posed.json.gz')):
    X = np.asarray(json.loads(gzip.open(BD + '/' + f, 'rt').read())['positions'])
    if nm == 'Manny': X = X[:json.loads(gzip.open(PKG, 'rb').read())['NB']]
    kd = kdtree.KDTree(len(X))
    for i, p in enumerate(X): kd.insert(Vector(p), i)
    kd.balance(); Q = np.asarray(pie[nm]['positions']); d = np.asarray([kd.find(Vector(q))[2] for q in Q])
    out[nm] = {'n_pie': len(Q), 'n_off': len(X), 'p50': round(float(np.percentile(d, 50)), 3), 'p95': round(float(np.percentile(d, 95)), 3), 'max': round(float(d.max()), 3)}
print('VALIDATE', json.dumps(out))
