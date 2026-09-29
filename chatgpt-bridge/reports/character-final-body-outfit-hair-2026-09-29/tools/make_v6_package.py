"""Derive the v6 body neutral for the garment builder: sculpt_package.json.gz (topology / weights / bind / accepted_b2)
with br_neutral replaced by accepted_b2 + br_morph_v6 deltas (UE bind space, cm). usage: python make_v6_package.py"""
import json, gzip, pathlib
R = pathlib.Path(__file__).resolve().parents[2]; A = R/'Saved/Codex/BodyRealismArtist_20260929/Blender/sculpt_package.json.gz'; CF = R/'Saved/Codex/CharacterFinal_20260929'
P = json.loads(gzip.open(A, 'rb').read()); NB, NH = P['NB'], P['NH']; M = json.loads((CF/'br_morph_v6.json').read_text())
base = P['accepted_b2']; out = [list(p) for p in base]
nb = 0
for k, d in M['Body']['BR_Neutral'].items():
    i = int(k); out[i] = [out[i][j]+d[j] for j in range(3)]; nb += 1
nh = 0
for k, d in M['Head']['BR_Neutral'].items():
    i = NB+int(k); out[i] = [out[i][j]+d[j] for j in range(3)]; nh += 1
mx = max(sum((a-b)**2 for a, b in zip(p, q))**0.5 for p, q in zip(out, P['br_neutral']))
P['br_neutral'] = out; P['version'] = str(P.get('version', '')) + '+v6'
with gzip.open(CF/'sculpt_package_v6.json.gz', 'wt') as f: json.dump(P, f)
print('v6 package written', 'body deltas', nb, 'head deltas', nh, 'max |v6-v5| cm', round(mx, 3))
