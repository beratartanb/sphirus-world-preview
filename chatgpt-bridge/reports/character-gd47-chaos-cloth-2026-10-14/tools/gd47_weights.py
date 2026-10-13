"""GD47: MaxDistance field (cm) for the WHOLE Henley f5 (DynamicMesh LOD0 order of data/henley_f5_mesh.json.gz), bind (A-pose) space.
Main fabric (section 0) = 4 unwelded panels (front, back, 2 sleeves; seams coincident, welded in UE after the weights are set).
  torso: yoke z>=133 -> Y cm, ramp to MID cm at z 120, to HEM cm at z<=100
  sleeves: SLV cm, blended from the torso value at the armhole seam over 6 cm
  pins (0 cm) within 1 cm of the trims: neck binding (ramp to full at NECK_R cm), placket + its two side strips (PLK_R), cuffs (CUFF_R)
  trims / buttons themselves 0 (render-only, driven by the proxy deformer)
usage: blender -b --python gd47_weights.py -- mesh.json.gz out.json [key=value ...]   (Y MID HEM SLV NECK_R PLK_R CUFF_R HIGH)"""
import sys, json, gzip, collections, numpy as np
from mathutils.kdtree import KDTree
a = sys.argv[sys.argv.index('--') + 1:]; d = json.load(gzip.open(a[0], 'rt')); OUT = a[1]
K = {'Y': 1.5, 'MID': 4.0, 'HEM': 7.0, 'SLV': 3.0, 'NECK_R': 7.0, 'PLK_R': 5.0, 'CUFF_R': 5.0, 'HIGH': 8.0, 'Z_YOKE': 133.0, 'Z_MID': 120.0, 'Z_HEM': 100.0, 'CHEST': 99.0, 'CHEST_Y': 5.0, 'CHEST_Z0': 116.0}
for kv in a[2:]: k, v = kv.split('='); K[k] = float(v)
P = np.array(d['P']); T = np.array(d['T']); M = np.array(d['M']); nV = len(P)
def ss(x): x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)
def comps(Ts):
    par = {}
    def f(x):
        while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
        return x
    for t in Ts:
        for v in t[1:]: par[f(v)] = f(t[0])
    g = collections.defaultdict(list)
    for v in np.unique(Ts).tolist(): g[f(v)].append(v)
    return list(g.values())
main = comps(T[M == 0]); trims = comps(T[M == 1])
cen = lambda c: P[c].mean(0)
sleeves = [c for c in main if abs(cen(c)[0]) > 15]; torso = [c for c in main if abs(cen(c)[0]) <= 15]
neck = [c for c in trims if cen(c)[2] > 130 and abs(cen(c)[0]) < 5 and len(c) > 200]
cuffs = [c for c in trims if abs(cen(c)[0]) > 35]
plk = [c for c in trims if cen(c)[1] > 13 and 110 < cen(c)[2] < 132 and len(c) < 200]
hem = [c for c in trims if cen(c)[2] < 102 and abs(cen(c)[0]) < 5]
assert len(sleeves) == 2 and len(torso) == 2 and len(neck) == 1 and len(cuffs) == 2 and len(plk) == 3 and len(hem) == 1, (len(sleeves), len(torso), len(neck), len(cuffs), len(plk), len(hem))
def kd_of(vs):
    kd = KDTree(len(vs)); [kd.insert(P[v].tolist(), i) for i, v in enumerate(vs)]; kd.balance(); return kd
def dist_to(vs, query):
    kd = kd_of(vs); return np.array([kd.find(P[q].tolist())[2] for q in query])
mainv = np.unique(T[M == 0]); W = np.zeros(nV)
sv = set(v for c in sleeves for v in c); tv = [v for c in torso for v in c]
z = P[:, 2]
def torso_field(idx):
    zz = z[idx]; up = K['Y'] + (K['MID'] - K['Y']) * ss((K['Z_YOKE'] - zz) / (K['Z_YOKE'] - K['Z_MID']))
    lo = K['MID'] + (K['HEM'] - K['MID']) * ss((K['Z_MID'] - zz) / (K['Z_MID'] - K['Z_HEM']))
    return np.where(zz >= K['Z_MID'], up, lo)
F = np.zeros(nV); F[tv] = torso_field(np.array(tv))
tva = np.array(tv); ch = (P[tva, 1] > K['CHEST_Y']) * ss((P[tva, 2] - K['CHEST_Z0']) / 4.0); F[tva] = F[tva] * (1 - ch) + np.minimum(F[tva], K['CHEST']) * ch
# armhole seam = sleeve vertices coincident with torso vertices
kd_t = kd_of(tv); arm = [v for v in sv if kd_t.find(P[v].tolist())[2] < 0.01]
sl = np.array(sorted(sv)); da = dist_to(arm, sl); F[sl] = torso_field(sl) * (1 - ss(da / 6.0)) + K['SLV'] * ss(da / 6.0)
def pin(cv, R, idx):
    dd = dist_to(cv, idx); return ss((dd - 1.0) / (R - 1.0))
mv = mainv
r = np.minimum.reduce([pin([v for c in neck for v in c], K['NECK_R'], mv), pin([v for c in plk for v in c], K['PLK_R'], mv), pin([v for c in cuffs for v in c], K['CUFF_R'], mv)])
W[mv] = np.clip(F[mv] * r / K['HIGH'], 0.0, 1.0)
cm = W * K['HIGH']; rep = {'K': K, 'verts': nV, 'main_verts': int(len(mv)), 'armhole_seam_verts': len(arm),
       'pinned_main(<0.05cm)': int((cm[mv] < 0.05).sum()), 'hist_cm': {f'{lo}-{lo+1}': int(((cm[mv] >= lo) & (cm[mv] < lo + 1)).sum()) for lo in range(0, 8)}}
for nm, sel in (('yoke z>133 torso', [v for v in tv if z[v] > 133]), ('torso 110-120', [v for v in tv if 110 < z[v] < 120]), ('hem z<101 torso', [v for v in tv if z[v] < 101]), ('sleeves', list(sv))):
    q = cm[sel]; rep[nm] = [round(float(q.min()), 2), round(float(np.median(q)), 2), round(float(q.max()), 2)]
json.dump({'rep': rep, 'W': [round(float(w), 5) for w in W]}, open(OUT, 'w')); print('GD47_WEIGHTS', json.dumps(rep))
