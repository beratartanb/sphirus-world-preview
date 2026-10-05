"""GD11 hair pass P: REGION DIAGNOSIS of a built hair (strand geometry, main groom only unless LOOSE=1) on the build head.
Per region and side: (a) root density roots/cm2 inside the hairline part of the region, (b) surface COVERAGE = share of region surface samples
that have hair within 2.5 cm along the normal (column radius 0.3 cm), (c) LAYERS = mean number of distinct strands in a covered column,
(d) stand-off of the lowest / outermost hair above the surface (cm), (e) flow direction of the hair passing over the region
(unit vector split: back / down / outward), (f) where that hair is ROOTED (share rooted in the region itself vs top / front / elsewhere).
usage: blender -b --factory-startup --python blender_g11rp_cover.py -- <out.json> <head.npy> <hair_dir> [<hair_dir> ...]"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEAD, DIRS = a[0], a[1], a[2:]; MX = -0.23; CY = 2.5
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
fnr = np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]]); ar = 0.5*np.linalg.norm(fnr, axis=1); fnr = -fnr/np.maximum(np.linalg.norm(fnr, axis=1), 1e-9)[:, None]; cen = X[TT].mean(1)
def az(p): return np.degrees(np.arctan2(np.abs(p[..., 0]-MX), p[..., 1]-CY))
REG = {'forehead_corner': (22, 48, 164.0, 169.0), 'temple': (48, 76, 161.0, 166.5), 'above_ear': (76, 106, 163.5, 168.0), 'behind_ear': (106, 138, 157.0, 164.0), 'nape': (138, 180, 152.5, 158.5), 'side_upper': (60, 120, 168.0, 172.0), 'top': (0, 180, 172.0, 999)}
rng = np.random.default_rng(3); res = {}
for hd in DIRS:
    d = np.load(os.path.join(hd, 'strands.npz')); M = d['main']
    if os.environ.get('LOOSE') == '1': M = np.concatenate([M, d['loose']]) if len(d['loose']) else M
    tg = json.load(open(os.path.join(hd, 'strand_tags.json')))['main']
    # dense resample of every strand (every ~0.25 cm) into a voxel hash -> strand ids
    S = M.astype(float); n, k, _ = S.shape; tt = np.linspace(0, 1, k*4); idx = np.clip((tt*(k-1)).astype(int), 0, k-2); f = tt*(k-1)-idx
    D = S[:, idx]*(1-f)[None, :, None]+S[:, idx+1]*f[None, :, None]; pts = D.reshape(-1, 3); sid = np.repeat(np.arange(n), k*4); V = 0.3
    key = np.floor(pts/V).astype(np.int64); h = key[:, 0]*73856093 ^ key[:, 1]*19349663 ^ key[:, 2]*83492791; order = np.argsort(h); hs = h[order]
    tgt = np.gradient(D, axis=1).reshape(-1, 3); tgt /= np.maximum(np.linalg.norm(tgt, axis=1), 1e-9)[:, None]
    roots = S[:, 0]; raz = az(roots); out = {}
    for name, (a0, a1, z0, z1) in REG.items():
        for side, sg in (('L', 1), ('R', -1)):
            m = (az(cen) >= a0) & (az(cen) < a1) & (cen[:, 2] >= z0) & (cen[:, 2] < z1) & (np.sign(cen[:, 0]-MX) == sg) & (fnr[:, 2] > -0.6)
            if name != 'top': m &= (np.abs(cen[:, 0]-MX) < 7.6)      # skip the ear pinna
            area = float(ar[m].sum()); ids = np.nonzero(m)[0]
            if len(ids) == 0: continue
            pick = rng.choice(ids, size=min(260, len(ids)), p=ar[ids]/ar[ids].sum()); cov = 0; lay = []; so_in = []; so_out = []; dirs = []; rooted = []
            for i in pick:
                c = cen[i]; nrm = fnr[i]; col = []; 
                for s in np.arange(0.1, 2.6, 0.3):
                    q = np.floor((c+nrm*s)/V).astype(np.int64); hh = q[0]*73856093 ^ q[1]*19349663 ^ q[2]*83492791; lo = np.searchsorted(hs, hh, 'left'); hi = np.searchsorted(hs, hh, 'right')
                    if hi > lo: col.append((s, order[lo:hi]))
                if not col: continue
                cov += 1; allp = np.concatenate([c_[1] for c_ in col]); st = np.unique(sid[allp]); lay.append(len(st)); so_in.append(col[0][0]); so_out.append(col[-1][0])
                t_ = tgt[allp].mean(0); t_ /= max(np.linalg.norm(t_), 1e-9); dirs.append([-t_[1], -t_[2], sg*t_[0]]); rr = roots[st]
                rooted.append([float(((az(rr) >= a0) & (az(rr) < a1) & (rr[:, 2] >= z0) & (rr[:, 2] < z1)).mean()), float((rr[:, 2] > 171).mean()), float(((rr[:, 1] > 4.5) & (rr[:, 2] <= 171)).mean())])
            rm = (raz >= a0) & (raz < a1) & (roots[:, 2] >= z0) & (roots[:, 2] < z1) & (np.sign(roots[:, 0]-MX) == sg)
            out[f'{name}_{side}'] = {'area_cm2': round(area, 1), 'roots': int(rm.sum()), 'roots_per_cm2': round(float(rm.sum())/max(area, 1e-6), 1), 'coverage': round(cov/len(pick), 2), 'layers': round(float(np.mean(lay)), 1) if lay else 0,
                                     'standoff_inner_cm': round(float(np.mean(so_in)), 2) if so_in else None, 'standoff_outer_cm': round(float(np.mean(so_out)), 2) if so_out else None,
                                     'flow_back_down_out': [round(float(v), 2) for v in np.mean(dirs, 0)] if dirs else None, 'rooted_here_top_front': [round(float(v), 2) for v in np.mean(rooted, 0)] if rooted else None}
    res[os.path.basename(hd)] = out
    print('COVER', os.path.basename(hd)); [print('  %-18s' % k_, json.dumps(v_)) for k_, v_ in out.items()]
json.dump(res, open(OUT, 'w'), indent=1); print('COVER_OK')
