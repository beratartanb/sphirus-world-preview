"""Project the LOD0 SHCA morph deltas onto lower LODs (bind space): closest point on the LOD0 surface ->
barycentric interpolation of the LOD0 per-vertex deltas. Writes morph_data_lod<k>.json per LOD."""
import json, gzip, math, sys
from pathlib import Path
C = Path(__file__).resolve().parents[2]/'Saved/Codex/CharacterShoulderFix_20260928'; S = C/'HighElevCorrective_20260929'
D = json.load(open(C.parent/'CharacterFinal_20260929'/'morph_data_br_all.json')); D165 = {'Body': {}, 'Head': {}}
for p in D: D[p].update(D165[p])
info = json.load(open(S/'lod_info.json'))
def sub(a, b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def closest_bary(p, a, b, c):
    """Ericson, Real-Time Collision Detection 5.1.5 -> barycentric (u,v,w) of closest point"""
    ab = sub(b, a); ac = sub(c, a); ap = sub(p, a)
    d1 = dot(ab, ap); d2 = dot(ac, ap)
    if d1 <= 0 and d2 <= 0: return (1, 0, 0)
    bp = sub(p, b); d3 = dot(ab, bp); d4 = dot(ac, bp)
    if d3 >= 0 and d4 <= d3: return (0, 1, 0)
    vc = d1*d4-d3*d2
    if vc <= 0 and d1 >= 0 and d3 <= 0: v = d1/(d1-d3); return (1-v, v, 0)
    cp = sub(p, c); d5 = dot(ab, cp); d6 = dot(ac, cp)
    if d6 >= 0 and d5 <= d6: return (0, 0, 1)
    vb = d5*d2-d1*d6
    if vb <= 0 and d2 >= 0 and d6 <= 0: w = d2/(d2-d6); return (1-w, 0, w)
    va = d3*d6-d5*d4
    if va <= 0 and (d4-d3) >= 0 and (d5-d6) >= 0: w = (d4-d3)/((d4-d3)+(d5-d6)); return (0, 1-w, w)
    den = 1/(va+vb+vc); v = vb*den; w = vc*den; return (1-v-w, v, w)
out_all = {}
for part in ['Body', 'Head']:
    g0 = json.load(gzip.open(C/f'{part}_source_geometry.json.gz', 'rt')); P0 = g0['positions']; T0 = g0['triangles']
    morphs = D[part]; names = sorted(morphs)
    active = set(int(k) for n in names for k in morphs[n])
    # triangles touching the corrective region (+ their neighbours through shared verts)
    cell = 1.5; grid = {}
    tris = [t for t in T0 if any(v in active for v in t)]
    region = set(v for t in tris for v in t)
    tris = [t for t in T0 if any(v in region for v in t)]
    for t in tris:
        xs = [P0[v] for v in t]
        lo = [math.floor(min(x[i] for x in xs)/cell) for i in range(3)]; hi = [math.floor(max(x[i] for x in xs)/cell) for i in range(3)]
        for i in range(lo[0], hi[0]+1):
            for j in range(lo[1], hi[1]+1):
                for k in range(lo[2], hi[2]+1): grid.setdefault((i, j, k), []).append(t)
    for lod in range(1, info[part]['lods']):
        g = json.load(gzip.open(S/f'lod_{part}_{lod}.json.gz', 'rt')); PL = g['positions']
        res = {n: {} for n in names}; far = 0; nproj = 0; maxdist = 0
        for vi, p in enumerate(PL):
            key = [math.floor(p[i]/cell) for i in range(3)]; cand = []
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    for k in (-1, 0, 1): cand += grid.get((key[0]+i, key[1]+j, key[2]+k), [])
            if not cand: continue
            best = None
            for t in cand:
                a, b, c = (P0[t[0]], P0[t[1]], P0[t[2]]); u, v, w = closest_bary(p, a, b, c)
                q = [u*a[i]+v*b[i]+w*c[i] for i in range(3)]; d = math.dist(p, q)
                if best is None or d < best[0]: best = (d, t, (u, v, w))
            d, t, bw = best
            if d > 1.0: far += 1; continue
            nproj += 1; maxdist = max(maxdist, d)
            for n in names:
                m = morphs[n]; acc = [0.0, 0.0, 0.0]; hit = False
                for vid, wt in zip(t, bw):
                    dd = m.get(str(vid))
                    if dd: hit = True; acc = [acc[i]+wt*dd[i] for i in range(3)]
                if hit and max(abs(x) for x in acc) > 1e-5: res[n][str(vi)] = acc
        out_all[f'{part}_{lod}'] = {'projected': nproj, 'skipped_far': far, 'max_proj_dist_cm': round(maxdist, 3),
                                   'morph_verts': {n: len(x) for n, x in res.items()},
                                   'max_delta_mm': {n: round(max([math.sqrt(dot(x, x)) for x in r.values()] or [0])*10, 2) for n, r in res.items()}}
        (C.parent/'CharacterFinal_20260929'/f'morph_data_br_lod_{part}_{lod}.json').write_text(json.dumps({part: res}))
        print(part, lod, json.dumps(out_all[f'{part}_{lod}']), flush=True)
(C.parent/'CharacterFinal_20260929'/'lod_transfer_br.json').write_text(json.dumps(out_all, indent=1))
