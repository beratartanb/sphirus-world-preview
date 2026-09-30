"""IDENTITY pass: art-directed VOLUME layer on top of the multi-view reconstruction (recon_head.npy). The reconstruction fixes
where features sit; this layer builds the forms 2D landmarks cannot constrain, judged in pixel-aligned clay renders against THE
GUARDIAN: rounder/broader nose tip and alae, softer broader bridge, fuller malar fat pads and filled submalar hollow, jowl,
rounder broader chin, hooded upper lid (fold skin over the lid, orbital sulcus filled), lower-lid bags + tear trough, thinner /
narrower lips, lower mouth corners, lower cranial vault. Displacements along vertex normals / anatomical directions, Gaussian
region masks, eyes / teeth / saliva locked, collar / seam guard. All strengths in cm via env SC_* (0 disables).
usage: blender -b -P blender_id_sculpt.py -- <in.npy> <out.npy>"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import *
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).copy(); OUTP = a[1]; E = lambda k, d: float(os.environ.get(k, d))
P = pkg(); T = np.asarray(P['head']['triangles']); MI = np.asarray(P['head']['material_ids']); NS = 24049
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
N = np.zeros_like(X); fn = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]])
for k in range(3): np.add.at(N, T[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
S = X[:NS]; x, y, z = S[:, 0], S[:, 1], S[:, 2]; sg = np.sign(x+1e-9); ax = np.abs(x); Ns = N[:NS]
eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); ez = 0.5*(eL[2]+eR[2]); ey = 0.5*(eL[1]+eR[1]); ex = 0.5*(abs(eL[0])+abs(eR[0]))
mid = ax < 0.35
def profile(z0, z1, mode='max'):
    m = mid & (z > z0) & (z < z1) & (y > 8); ids = np.nonzero(m)[0]; return ids[np.argmax(y[ids])] if mode == 'max' else ids[np.argmin(y[ids])]
tip = S[profile(157.5, 161.0)]; lipU = S[profile(155.8, 157.6)]
m_ = mid & (z > 153.0) & (z < 156.6) & (y > 9); ids = np.nonzero(m_)[0]; zz = np.round(z[ids]/0.12); prof = {}
for i, b in zip(ids, zz):
    if b not in prof or y[i] > y[prof[b]]: prof[b] = i
pl = sorted(prof.items()); ys = np.array([y[i] for _, i in pl]); zs_ = np.array([z[i] for _, i in pl])
sto_z = zs_[np.argmin(np.where((zs_ > 154.8) & (zs_ < 156.4), ys, 99))]                    # stomion = profile notch between the lips
chin = S[profile(150.5, 154.0)]; frontface = sstep((y-2.0)/2.5)
def g(c, r): d = (S-np.asarray(c))/np.asarray(r); return np.exp(-(d**2).sum(1))
D = np.zeros_like(S); log = {}
def add(name, vec, default):
    k = E('SC_'+name, default)
    if k == 0: return
    D[:] += k*vec; log[name] = round(float(np.linalg.norm(k*vec, axis=1).max()*10), 2)
# ---- nose
bulb = g([0, tip[1]-0.45, tip[2]-0.1], [1.0, 0.8, 0.85])*(y > tip[1]-1.6)
rad = np.stack([x, np.zeros_like(x), z-(tip[2]-0.2)], 1); rad /= np.maximum(np.linalg.norm(rad, axis=1), 1e-6)[:, None]
add('TIP_BULB', bulb[:, None]*rad, '0.14')
add('TIP_DROP', (g([0, tip[1]-0.3, tip[2]], [1.1, 1.2, 0.9])*(y > tip[1]-1.8))[:, None]*np.array([0, -0.3, -1.0]), '0.08')
ala = np.exp(-(((ax-1.5)/0.7)**2+((z-(tip[2]-1.9))/0.75)**2))*sstep((y-(tip[1]-3.2))/0.8)
add('ALAR_FLARE', ala[:, None]*np.stack([sg, -0.2*np.ones_like(x), -0.2*np.ones_like(x)], 1), '0.14')
bridge = np.exp(-(((ax-0.55)/0.45)**2+((z-(0.5*(tip[2]+ez)+0.4))/1.3)**2))*sstep((y-(tip[1]-3.5))/0.8)
add('BRIDGE_WIDE', bridge[:, None]*np.stack([sg, 0.3*np.ones_like(x), np.zeros_like(x)], 1), '0.07')
# ---- midface
malar = np.exp(-(((ax-E('SC_MALAR_X', '3.0'))/1.7)**2+((z-(ez-2.3))/1.5)**2+((y-(ey+0.8))/2.5)**2))*frontface
add('MALAR', malar[:, None]*Ns, '0.28')
submal = np.exp(-(((ax-4.6)/1.4)**2+((z-(sto_z+1.3))/1.5)**2))*frontface*(ax > 2.0)
add('SUBMALAR', submal[:, None]*Ns, '0.22')
jowl = np.exp(-(((ax-3.9)/1.2)**2+((z-(sto_z-1.9))/1.1)**2))*frontface
add('JOWL', jowl[:, None]*(Ns+np.array([0, 0, -0.4])), '0.16')
zyg = np.exp(-(((ax-E('SC_ZYG_X', '4.9'))/1.2)**2+((z-(ez-1.3))/0.9)**2))*sstep((y-(ey-2.5))/1.5)
add('ZYGOMA', zyg[:, None]*(Ns+np.stack([0.4*sg, np.zeros_like(x), np.zeros_like(x)], 1)), '0.0')
gon = np.exp(-(((ax-5.7)/1.1)**2+((z-(sto_z-3.1))/1.3)**2+((y-1.0)/2.2)**2))
add('JAW_ANGLE', gon[:, None]*np.stack([sg, np.zeros_like(x), -0.2*np.ones_like(x)], 1), '0.0')
# ---- chin / mouth
chinw = np.exp(-(((ax-1.9)/1.0)**2+((z-(chin[2]-0.2))/1.2)**2))*sstep((y-(chin[1]-2.5))/0.8)
add('CHIN_WIDE', chinw[:, None]*np.stack([sg, np.zeros_like(x), np.zeros_like(x)], 1), '0.14')
chint = np.exp(-((x/1.0)**2+((z-chin[2])/0.9)**2))*sstep((y-(chin[1]-1.5))/0.6)
add('CHIN_TIP', chint[:, None]*np.array([0, -1.0, 0]), '0.06')
lipm = np.exp(-(x/2.4)**4)*sstep((y-(lipU[1]-1.6))/0.6)
lower = lipm*sstep((sto_z-z)/0.25)*(1-sstep((sto_z-1.05-z)/0.4))
add('LIP_LOWER_BACK', lower[:, None]*np.array([0, -1.0, 0.25]), '0.10')
upper = lipm*sstep((z-sto_z)/0.25)*(1-sstep((z-(sto_z+0.9))/0.35))
add('LIP_UPPER_BACK', upper[:, None]*np.array([0, -1.0, -0.2]), '0.06')
lband = lipm*sstep((sto_z-z)/0.15)*(1-sstep((sto_z-E('SC_LL_H', '1.25')-z)/0.35))
lfrac = np.clip((sto_z-z)/E('SC_LL_H', '1.25'), 0, 1)
add('LOWER_LIP_THIN', (lband*lfrac)[:, None]*np.array([0, -0.35, 1.0]), '0.0')             # lower vermilion border rolls up / in toward the stomion
phil = np.exp(-(x/1.1)**2)*sstep((z-(sto_z+0.5))/0.35)*(1-sstep((z-(sto_z+1.7))/0.4))*sstep((y-(lipU[1]-1.6))/0.6)
add('PHILTRUM_BACK', phil[:, None]*np.array([0, -1.0, 0]), '0.0')
corner = np.exp(-(((ax-2.35)/0.8)**2+((z-sto_z)/0.7)**2))*sstep((y-(lipU[1]-3.5))/1.0)
add('MOUTH_NARROW', corner[:, None]*np.stack([-sg, np.zeros_like(x), np.zeros_like(x)], 1), '0.12')
add('CORNER_DOWN', corner[:, None]*np.array([0, 0, -1.0]), '0.08')
# ---- eyes / brows
for ec in (eL, eR):
    s_ = np.sign(ec[0]); dx = x-ec[0]
    hood = np.exp(-(((dx-s_*0.35)/1.8)**2+((z-(ec[2]+1.05))/0.45)**2))*sstep((y-(ec[1]-0.3))/0.6)
    add('HOOD', hood[:, None]*np.array([0, 0.35, -1.0]), '0.16')
    sulcus = np.exp(-((dx/1.6)**2+((z-(ec[2]+1.45))/0.5)**2))*sstep((y-(ec[1]-0.8))/0.6)
    add('SULCUS_FILL', sulcus[:, None]*Ns, '0.14')
    bag = np.exp(-(((dx-s_*0.1)/1.2)**2+((z-(ec[2]-1.05))/0.35)**2))*sstep((y-(ec[1]-0.3))/0.6)
    add('LID_BAG', bag[:, None]*Ns, '0.08')
    trough = np.exp(-(((dx+s_*0.6)/0.9)**2+((z-(ec[2]-1.45))/0.25)**2))*sstep((y-(ec[1]-0.3))/0.6)
    add('TEAR_TROUGH', -trough[:, None]*Ns, '0.06')
# ---- lid apertures: upper-lid margin rotated down about the eyeball centre (stays on the globe), lower lid slightly up
import math
for ec in (eL, eR):
    dx = x-ec[0]; v = S-ec; r = np.linalg.norm(v, axis=1)
    lidw = np.exp(-(dx/1.45)**4)*sstep((z-(ec[2]-0.1))/0.25)*(1-sstep((z-(ec[2]+1.05))/0.45))*sstep((y-(ec[1]-0.2))/0.4)*(1-sstep((r-1.9)/0.4))
    ph = math.radians(E('SC_LID_ROT', '0'))*lidw
    ny = v[:, 1]*np.cos(ph)+v[:, 2]*np.sin(ph); nz = -v[:, 1]*np.sin(ph)+v[:, 2]*np.cos(ph)
    rot = np.stack([np.zeros(len(S)), ny-v[:, 1], nz-v[:, 2]], 1)
    if E('SC_LID_ROT', '0'): D[:] += rot; log['LID_ROT'] = round(float(np.linalg.norm(rot, axis=1).max()*10), 2)
    low = np.exp(-((dx/1.3)**4)-((z-(ec[2]-0.62))/0.3)**2)*sstep((y-(ec[1]-0.2))/0.5)*(1-sstep((r-1.9)/0.4))
    add('LOWER_LID_UP', low[:, None]*np.array([0, 0.2, 1.0]), '0.0')
# ---- cranium: lower the vault above the forehead (face untouched below z 167)
vault = sstep((z-E('SC_VAULT_Z0', '167.0'))/E('SC_VAULT_W', '7.0'))
add('VAULT', vault[:, None]*np.array([0, 0, -1.0]), '0.8')
guard = sstep((z-146.5)/2.0)[:, None]; D *= guard
X[:NS] += D
# lid-attached meshes follow the nearest lid skin displacement (eyeshell, lashes, eyeEdge, cartilage)
att = np.arange(SEG['eyeshell'][0], SEG['cartilage'][1])
from mathutils.kdtree import KDTree
kd = KDTree(NS)
for i, p in enumerate(S): kd.insert(p.tolist(), i)
kd.balance()
for i in att:
    _, j, _ = kd.find(X[i].tolist()); X[i] += D[j]
np.save(OUTP, X); print('SCULPT', json.dumps(log), 'stomion_z', round(float(sto_z), 2), 'tip', np.round(tip, 2).tolist(), 'chin', np.round(chin, 2).tolist())
