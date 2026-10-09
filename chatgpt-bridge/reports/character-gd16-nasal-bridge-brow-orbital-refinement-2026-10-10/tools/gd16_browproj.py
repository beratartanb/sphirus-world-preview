"""GD16: reference brow stations (front panel-original px: col, top row, bottom row, read on the user's front panel) -> 3D points on the head
skin through the SOLVED front camera (same camera the identity captures are warped with). For every station pixel the front-facing brow-
region skin vertices whose projection lies within a few px are averaged (inverse distance) -> a surface point (project frame cm).
stations json: {"imgL": [[col, top, bottom], ...medial->lateral], "imgR": [...]}  (imgL = subject's RIGHT brow)
usage: blender -b --python gd16_browproj.py -- <head.npy> <cams.json> <stations.json> <out.json>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); from gd13_common import project, depth
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); C = json.load(open(a[1]))['front']; ST = json.load(open(a[2])); OUT = a[3]
NS = 24049; MX = -0.23; S = X[:NS]
m = (S[:, 2] > 161.8) & (S[:, 2] < 168.0) & (S[:, 1] > 9.0) & (np.abs(S[:, 0]-MX) < 7.0); idx = np.nonzero(m)[0]; P2 = project(C, S[idx]); Z = depth(C, S[idx])
def pick(col, row):
    d = np.linalg.norm(P2-np.array([col, row]), axis=1); near = np.argsort(d)[:12]
    zmin = Z[near].min(); near = near[Z[near] < zmin+0.6]                     # front-most layer only (no back-facing / occluded points)
    w = 1.0/np.maximum(d[near], 0.15)**2; p = (S[idx[near]]*w[:, None]).sum(0)/w.sum()
    return p, float(d[near].min())
out = {'camera': 'front (solved, Ec_cams.json)', 'stations_px': ST}
for side, L in ST.items():
    rows = []
    for col, top, bot in L:
        t, et = pick(col, top); b, eb = pick(col, bot); c, ec = pick(col, 0.5*(top+bot))
        rows.append({'col': col, 'top': t.round(4).tolist(), 'cen': c.round(4).tolist(), 'bot': b.round(4).tolist(), 'pick_err_px': round(max(et, eb, ec), 2), 'thick_mm': round(float(np.linalg.norm(t-b))*10, 2)})
    out[side] = rows
json.dump(out, open(OUT, 'w'), indent=1)
for side in ST: print('BROWPROJ', side, ' | '.join('c%d (%.2f,%.2f,%.2f) %.1fmm' % (r['col'], *r['cen'], r['thick_mm']) for r in out[side]))
