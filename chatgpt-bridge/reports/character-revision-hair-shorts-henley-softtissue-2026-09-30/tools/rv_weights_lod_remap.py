"""Garment LOD weights -> only bones the paired body LOD evaluates (body LOD settings bone removal). Weight on a removed
bone moves to its nearest kept ancestor. Pairing (LODSync mapping): garment LOD0 <-> body LOD0/1, LOD1 <-> body LOD2...
LOD0 = body LOD0 (nothing removed), LOD1 = body-LOD1 list, LOD2 = body-LOD3 list (superset of LOD2)."""
import json, gzip, shutil, sys
E = 'Saved/Codex/CharacterRevision_20260930/'; F = E+'outfit_v3i/outfit_weights.json.gz'
d = json.load(open(E+'lod_bone_removal.json')); par = d['parents']; W = json.loads(gzip.open(F, 'rb').read())
shutil.copy(F, E+'outfit_v3i/outfit_weights_pre_lodremap.json.gz')
PAIR = {'': '0', '_lod1': '1', '_lod2': '3'}
rep = {}
for g in ('henley', 'trousers'):
    for suf, L in PAIR.items():
        rem = set(d['removed'][L]); key = g+suf; moved = 0.0
        def keep(b):
            while b in rem: b = par.get(b, 'root')
            return b
        out = []
        for vw in W[key]:
            acc = {}
            for b, w in vw.items():
                k = keep(b)
                if k != b: moved += w
                acc[k] = acc.get(k, 0.0)+w
            s = sum(acc.values()) or 1.0; out.append({b: round(w/s, 6) for b, w in acc.items()})
        W[key] = out; rep[key] = round(moved, 1)
with gzip.open(F, 'wt') as f: json.dump(W, f)
print('REMAP_OK', rep)
