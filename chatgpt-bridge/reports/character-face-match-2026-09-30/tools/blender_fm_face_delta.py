"""FACE-MATCH pass (isolated): neutral-shape likeness deltas for the face toward the approved THE GUARDIAN reference, written as
the head part of the existing always-on BR_Neutral morph (collar deltas kept, face deltas added) -> no DNA / joint / expression
morph / skeleton change. Measured targets (same-camera grids, IPD-normalised; see Saved/Codex/CharacterFaceMatch_20260930):
  lips fuller than reference (lip height 0.32 vs 0.21 IPD; mouth width 0.85 vs 0.78)  -> vermilion volume / projection down, mouth a bit narrower
  eyes more open (aperture 0.18 vs 0.12 IPD)                                             -> slight upper-lid hooding + lid margin lowering (sub-mm)
  face rounder / wider below the zygoma (width / brow-chin 1.14 vs 0.95)                -> buccal + jaw-angle narrowing, chin longer / more defined
  nose shorter / broader                                                                -> tip down, alae in, bridge straighter
  brows smooth / high                                                                   -> brow ridge forward, brow skin slightly down
Hard locks: eyeballs / teeth / saliva (material ids 1-4) = 0; collar / seam region (z < 146.5) = original BR_Neutral only.
Lid-attached meshes (eyeshell, eyelashes, eyeEdge, cartilage) receive the same field as the lid skin.
Outputs morph_fm_face_lod{0..7}.json ({'Head': {'BR_Neutral': {idx: [dx, dy, dz]}}}) + landmarks / stats.
usage: blender -b --factory-startup --python blender_fm_face_delta.py -- <sculpt_package_v6.json.gz> <lod_dir> <out_dir> [scale]"""
import sys, os, json, gzip, math
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; PKG, LODD, OUT = a[:3]; K = float(a[3]) if len(a) > 3 else 1.0; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d))
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']
X = np.asarray(P['accepted_b2'], np.float64)[NB:]; BR = np.asarray(P['br_neutral'], np.float64)[NB:]-X
T = np.asarray(P['head']['triangles'], np.int64); MI = np.asarray(P['head']['material_ids'])
vm = np.full(len(X), -1);
for m in range(15): vm[np.unique(T[MI == m])] = np.where(vm[np.unique(T[MI == m])] < 0, m, vm[np.unique(T[MI == m])])
skin = vm == 0; lidmesh = np.isin(vm, [5, 6, 7, 8]); locked = np.isin(vm, [1, 2, 3, 4])
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def g(c, r): d = (X-np.asarray(c))/np.asarray(r); return np.exp(-(d**2).sum(1))
# ---- landmarks (measured on the mesh)
eyeL = X[vm == 3].mean(0); eyeR = X[vm == 4].mean(0); IPD = float(np.linalg.norm(eyeL-eyeR))
S = X[skin]; mid = S[np.abs(S[:, 0]) < 0.35]
def front_y(z, xs=0.0, w=0.35):
    s = S[(np.abs(S[:, 0]-xs) < w) & (np.abs(S[:, 2]-z) < 0.12)]; return float(s[:, 1].max()) if len(s) else np.nan
zs = np.arange(149.0, 166.0, 0.1); prof = np.array([front_y(z) for z in zs])
def argmax_in(z0, z1): m = (zs >= z0) & (zs <= z1); i = np.nanargmax(np.where(m, prof, -1e9)); return float(zs[i]), float(prof[i])
def argmin_in(z0, z1): m = (zs >= z0) & (zs <= z1); i = np.nanargmin(np.where(m, prof, 1e9)); return float(zs[i]), float(prof[i])
pronasale = argmax_in(157.5, 161.0); subnasale = argmin_in(156.8, pronasale[0]-0.5)
labsup = argmax_in(155.6, subnasale[0]); stomion = argmin_in(154.6, labsup[0]); labinf = argmax_in(153.4, stomion[0])
labiomental = argmin_in(151.8, labinf[0]); pogonion = argmax_in(150.0, labiomental[0])
sellion = argmin_in(161.5, 164.5); glabella = argmax_in(sellion[0], 165.5)
# measured midline profile (0.25 cm steps, see face_match notes): the automatic windows above collapse on this mesh -> pinned values
pronasale, subnasale, labsup, stomion, labinf, labiomental, pogonion = (159.25, 15.52), (157.5, 13.40), (156.75, 13.61), (156.0, 13.35), (155.25, 13.70), (154.25, 12.75), (153.5, 12.84)
menton_z = 151.2
Mz = stomion[0]; mc = S[(np.abs(S[:, 2]-Mz) < 0.25) & (S[:, 1] > stomion[1]-2.5)]; mouth_half = E('FM_MOUTH_HALF', '2.55')
LM = {'IPD_cm': IPD, 'eyeL': eyeL.tolist(), 'eyeR': eyeR.tolist(), 'pronasale': pronasale, 'subnasale': subnasale, 'labrale_sup': labsup, 'stomion': stomion, 'labrale_inf': labinf,
      'labiomental': labiomental, 'pogonion': pogonion, 'sellion': sellion, 'glabella': glabella, 'mouth_half_width_est': mouth_half}
print('LANDMARKS', json.dumps({k: (np.round(v, 2).tolist() if isinstance(v, (list, tuple)) else round(v, 3)) for k, v in LM.items()}))
D = np.zeros_like(X); N = np.zeros_like(X)
fn = np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); fn = -fn
for k in range(3): np.add.at(N, T[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
fwd = np.array([0.0, 1.0, 0.0]); up = np.array([0.0, 0.0, 1.0]); sgx = np.sign(X[:, 0]+1e-9)
# ---- lips: vermilion volume / projection down, slightly narrower mouth
lipz0, lipz1 = labinf[0]-0.9, labsup[0]+0.5
lip = sstep((X[:, 1]-(stomion[1]-0.9))/0.8)*np.exp(-((X[:, 0])/(mouth_half*0.95))**4)*sstep((X[:, 2]-lipz0)/0.4)*sstep((lipz1-X[:, 2])/0.4)
upper = lip*sstep((X[:, 2]-stomion[0])/0.25); lower = lip*sstep((stomion[0]-X[:, 2])/0.25)
D += E('FM_LIP_U', '0.11')*K*upper[:, None]*(-fwd+np.array([0, 0, -0.35]))[None, :]            # upper lip thinner, less everted
D += E('FM_LIP_L', '0.10')*K*lower[:, None]*(-fwd+np.array([0, 0, 0.3]))[None, :]               # lower lip less full
corner = np.exp(-(((np.abs(X[:, 0])-mouth_half)/0.7)**2+((X[:, 2]-Mz)/0.6)**2))*sstep((X[:, 1]-(stomion[1]-3.0))/1.0)
D += E('FM_MOUTH_W', '0.09')*K*corner[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)   # mouth ~0.9 mm narrower per side
# ---- eyes: upper-lid hooding + margin lowering, lower lid up (lid meshes follow)
for ec in (eyeL, eyeR):
    upl = np.exp(-(((X[:, 0]-ec[0])/1.6)**2+((X[:, 2]-(ec[2]+0.75))/0.55)**2))*sstep((X[:, 1]-(ec[1]-0.3))/0.6)
    fold = np.exp(-(((X[:, 0]-ec[0])/1.8)**2+((X[:, 2]-(ec[2]+1.25))/0.45)**2))*sstep((X[:, 1]-(ec[1]-0.5))/0.6)
    lowl = np.exp(-(((X[:, 0]-ec[0])/1.5)**2+((X[:, 2]-(ec[2]-0.7))/0.4)**2))*sstep((X[:, 1]-(ec[1]-0.3))/0.6)
    D += E('FM_LID_U', '0.055')*K*upl[:, None]*(-up)[None, :]
    D += E('FM_FOLD', '0.08')*K*fold[:, None]*(-up*0.8+fwd*0.25)[None, :]
    D += E('FM_LID_L', '0.03')*K*lowl[:, None]*up[None, :]
# ---- brows: ridge forward, brow skin slightly lower (more mature, closer to the eyes)
for ec in (eyeL, eyeR):
    br = np.exp(-(((X[:, 0]-ec[0]*1.1)/2.4)**2+((X[:, 2]-(ec[2]+1.9))/0.7)**2))*sstep((X[:, 1]-(ec[1]+0.5))/0.8)
    D += E('FM_BROW', '0.08')*K*br[:, None]*(-up*0.8+fwd*0.6)[None, :]
# ---- nose: tip a little lower / longer, alae narrower, bridge straighter
tip = g([0, pronasale[1], pronasale[0]], [0.9, 1.2, 0.8])*sstep((X[:, 1]-(pronasale[1]-1.6))/0.6)
D += E('FM_NOSE_TIP', '0.10')*K*tip[:, None]*(-up*0.9+fwd*0.1)[None, :]
ala = np.exp(-(((np.abs(X[:, 0])-1.55)/0.55)**2+((X[:, 2]-(subnasale[0]+0.6))/0.6)**2))*sstep((X[:, 1]-(subnasale[1]-1.0))/0.8)
D += E('FM_ALA', '0.08')*K*ala[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
bridge = np.exp(-((X[:, 0]/0.7)**2+((X[:, 2]-(sellion[0]+0.2))/0.9)**2))*sstep((X[:, 1]-(sellion[1]-0.6))/0.5)
D += E('FM_BRIDGE', '0.06')*K*bridge[:, None]*fwd[None, :]
# ---- cheeks / jaw / chin: narrower below the zygoma, longer and more defined chin
buccal = np.exp(-(((np.abs(X[:, 0])-4.6)/1.4)**2+((X[:, 2]-(Mz+1.2))/1.5)**2))*sstep((X[:, 1]-4.0)/2.0)*skin
D += E('FM_BUCCAL', '0.16')*K*buccal[:, None]*np.stack([-sgx*0.8, -np.ones(len(X))*0.6, np.zeros(len(X))], 1)
jaw = np.exp(-(((np.abs(X[:, 0])-6.3)/1.5)**2+((X[:, 2]-(Mz-2.8))/1.8)**2))*sstep((X[:, 1]+1.0)/2.5)*skin
D += E('FM_JAW', '0.24')*K*jaw[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
chin = np.exp(-((X[:, 0]/1.9)**2+((X[:, 2]-(pogonion[0]-0.8))/1.4)**2))*sstep((X[:, 1]-(pogonion[1]-4.5))/1.0)*skin
D += E('FM_CHIN', '0.13')*K*chin[:, None]*(-up*0.85+fwd*0.45)[None, :]                        # chin a little lower / more projected: longer lower face
chinw = np.exp(-(((np.abs(X[:, 0])-2.3)/0.9)**2+((X[:, 2]-(pogonion[0]-0.4))/1.4)**2))*sstep((X[:, 1]-(pogonion[1]-3.0))/1.0)*skin
D += E('FM_CHIN_W', '0.07')*K*chinw[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
# ---- subtle natural asymmetry (left side slightly fuller cheek / lower brow)
D += E('FM_ASYM', '0.03')*K*(np.exp(-(((X[:, 0]-4.2)/1.5)**2+((X[:, 2]-(Mz+2.5))/1.5)**2))*skin)[:, None]*fwd[None, :]
# ---- v2 (derivative b+): explicit-magnitude likeness block (cm), from the corrected same-scale front / 3/4 measurements:
#   ref lower face ~10% longer below the eyes (eye->subnasale 0.70 vs 0.61 IPD, stomion->menton 0.71 vs 0.62), brows ~0.03 IPD lower,
#   upper lid hooded (lateral), alae 0.47 vs 0.52 IPD, upper vermilion thinner, lower lip less everted, cheeks flatter below the zygoma.
#   Run with K=0 so the v1 fields above are off; each term is scaled by FM2 (global) and its own FM2_* strength.
V2 = E('FM_V2', '0') > 0
if V2:
    G2 = E('FM2', '1.0'); Sn, Ls, St, Li, Lm, Pg = subnasale[0], labsup[0], stomion[0], labinf[0], labiomental[0], pogonion[0]
    ax_ = np.abs(X[:, 0]); zz = X[:, 2]; yy = X[:, 1]; front_face = sstep((yy-2.0)/2.0)
    # lower-face lengthening: everything below the nose moves down on a ramp (0 at the alar base -> full at the lips / chin), soft-tissue chin a bit more
    ramp = sstep((Sn+0.4-zz)/1.4)*front_face*np.exp(-(ax_/6.0)**4)
    D += G2*E('FM2_LOWER', '0.22')*ramp[:, None]*(-up)[None, :]
    chin2 = sstep((Lm+0.3-zz)/1.2)*np.exp(-(ax_/3.2)**2)*front_face
    D += G2*E('FM2_CHIN', '0.18')*chin2[:, None]*(-up*0.9+fwd*0.2)[None, :]
    chinw2 = np.exp(-(((ax_-2.7)/1.1)**2+((zz-(Pg-0.6))/1.3)**2))*sstep((yy-(pogonion[1]-3.5))/1.0)*skin    # broader, squarer chin (candidate tapers to a point)
    D += G2*E('FM2_CHINW', '0.0')*chinw2[:, None]*np.stack([sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
    # nose: tip longer / less upturned (rotate the lobule down), alae narrower, columella down with the tip
    tip2 = np.exp(-((X[:, 0]/1.0)**2+((zz-(pronasale[0]-0.3))/0.9)**2))*sstep((yy-(pronasale[1]-1.8))/0.7)
    D += G2*E('FM2_TIP', '0.14')*tip2[:, None]*(-up)[None, :]
    ala2 = np.exp(-(((ax_-1.6)/0.6)**2+((zz-(Sn+0.5))/0.7)**2))*sstep((yy-(subnasale[1]-1.5))/0.8)
    D += G2*E('FM2_ALA', '0.13')*ala2[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
    # lips: thinner upper vermilion (border rolls in toward the stomion), lower lip less everted, corners 1 mm in
    lipm = np.exp(-(X[:, 0]/(mouth_half*0.9))**4)*sstep((yy-(stomion[1]-1.8))/0.8)
    upv = lipm*sstep((zz-St)/0.25)*(1-sstep((zz-(Ls+0.35))/0.35))
    D += G2*E('FM2_LIPU', '0.13')*upv[:, None]*(-up*E('FM2_LIPU_DN', '0.55')-fwd*0.6)[None, :]
    lov = lipm*sstep((St-zz)/0.25)*(1-sstep((Li-0.45-zz)/0.4))
    D += G2*E('FM2_LIPL', '0.10')*lov[:, None]*(up*0.25-fwd*0.7)[None, :]
    corner2 = np.exp(-(((ax_-mouth_half)/0.8)**2+((zz-St)/0.7)**2))*sstep((yy-(stomion[1]-3.0))/1.0)
    D += G2*E('FM2_MOUTHW', '0.10')*corner2[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
    # eyes: upper lid margin rotated down around the eyeball centre (stays on the globe), lateral hooding of the fold, lower lid up
    for ec in (eyeL, eyeR):
        dx = X[:, 0]-ec[0]; v = X-ec; r = np.linalg.norm(v, axis=1)
        lidw = np.exp(-(dx/1.45)**4)*sstep((zz-(ec[2]-0.1))/0.25)*(1-sstep((zz-(ec[2]+1.05))/0.45))*sstep((yy-(ec[1]-0.2))/0.4)*(1-sstep((r-1.9)/0.4))
        ph = np.radians(E('FM2_LID_DEG', '7.5'))*G2*lidw
        ny = v[:, 1]*np.cos(ph)+v[:, 2]*np.sin(ph); nz = -v[:, 1]*np.sin(ph)+v[:, 2]*np.cos(ph)
        D += np.stack([np.zeros(len(X)), ny-v[:, 1], nz-v[:, 2]], 1)*(lidw > 1e-4)[:, None]
        lat = np.sign(ec[0])
        hood = np.exp(-(((X[:, 0]-(ec[0]+lat*0.45))/1.7)**2+((zz-(ec[2]+1.2))/0.5)**2))*sstep((yy-(ec[1]-0.5))/0.6)
        D += G2*E('FM2_HOOD', '0.16')*hood[:, None]*(-up*0.85+fwd*0.3)[None, :]
        lowl2 = np.exp(-((dx/1.4)**2+((zz-(ec[2]-0.72))/0.35)**2))*sstep((yy-(ec[1]-0.3))/0.6)
        D += G2*E('FM2_LIDL', '0.04')*lowl2[:, None]*up[None, :]
        brow2 = np.exp(-(((X[:, 0]-ec[0]*1.08)/2.6)**2+((zz-(ec[2]+2.0))/0.9)**2))*sstep((yy-(ec[1]+0.3))/0.8)
        D += G2*E('FM2_BROW', '0.18')*brow2[:, None]*(-up*0.9+fwd*0.35)[None, :]
    # cheeks / jaw: flatter below the zygoma, slight malar definition, narrower lower jaw, mild nasolabial
    buc2 = np.exp(-(((ax_-4.4)/1.5)**2+((zz-(St+1.0))/1.6)**2))*sstep((yy-3.5)/2.0)*skin
    D += G2*E('FM2_BUCCAL', '0.20')*buc2[:, None]*np.stack([-sgx*0.7, -np.ones(len(X))*0.7, np.zeros(len(X))], 1)
    mal = np.exp(-(((ax_-4.3)/1.3)**2+((zz-(eyeL[2]-1.9))/0.9)**2))*sstep((yy-5.0)/2.0)*skin
    D += G2*E('FM2_MALAR', '0.06')*mal[:, None]*np.stack([sgx*0.5, np.ones(len(X))*0.8, np.zeros(len(X))], 1)
    jaw2 = np.exp(-(((ax_-6.0)/1.6)**2+((zz-(St-2.6))/1.9)**2))*sstep((yy+1.0)/2.5)*skin
    D += G2*E('FM2_JAW', '0.26')*jaw2[:, None]*np.stack([-sgx, np.zeros(len(X)), np.zeros(len(X))], 1)
    nl = np.exp(-(((ax_-2.6)/0.9)**2+((zz-(Sn-0.2))/1.0)**2))*sstep((yy-8.0)/2.0)*skin
    D += G2*E('FM2_NL', '0.05')*nl[:, None]*fwd[None, :]
    D += G2*E('FM2_ASYM', '0.04')*(np.exp(-(((X[:, 0]-4.2)/1.5)**2+((zz-(St+2.5))/1.5)**2))*skin)[:, None]*fwd[None, :]
    # soft-tissue ageing (derivative c+): nasolabial fold (groove + cheek mass lateral to it), tear trough + lower-lid bag, marionette
    def line_w(p0, p1, wid):   # distance of each vertex (x-z plane, per side) to a segment; returns weight and the lateral offset sign
        out = np.zeros(len(X)); side_ = np.zeros(len(X))
        for sg_ in (1.0, -1.0):
            a0 = np.array([sg_*p0[0], p0[1]]); a1 = np.array([sg_*p1[0], p1[1]]); q = np.stack([X[:, 0], zz], 1); dv = a1-a0
            t = np.clip(((q-a0)@dv)/(dv@dv), 0, 1); c = a0+t[:, None]*dv; d = np.linalg.norm(q-c, axis=1); w = np.exp(-(d/wid)**2)*np.clip(np.sin(np.pi*t), 0, 1)**0.5*(np.sign(X[:, 0]) == sg_)
            lat = (q[:, 0]-c[:, 0])*sg_; out += w; side_ += w*np.sign(lat)
        return out, side_
    frontal = sstep((yy-6.0)/2.0)*skin
    nlw, _ = line_w((1.85, Sn+0.35), (mouth_half+0.35, St-0.5), 0.22)
    D -= G2*E('FM2_NLF', '0.0')*(nlw*frontal)[:, None]*N                                                   # fold groove
    nlm, _ = line_w((2.5, Sn+0.2), (mouth_half+0.95, St-0.2), 0.45)
    D += G2*E('FM2_NLM', '0.0')*(nlm*frontal)[:, None]*(fwd*0.8+up*0.2)[None, :]                          # cheek mass over the fold
    for ec in (eyeL, eyeR):
        sg_ = np.sign(ec[0]); tt, _ = line_w((abs(ec[0])-1.25, ec[2]-0.85), (abs(ec[0])+0.3, ec[2]-1.55), 0.2)
        tt = tt*(np.sign(X[:, 0]) == sg_)*sstep((yy-(ec[1]-0.2))/0.6)*skin
        D -= G2*E('FM2_TEAR', '0.0')*tt[:, None]*N
        bag = np.exp(-(((X[:, 0]-ec[0]-sg_*0.1)/1.1)**2+((zz-(ec[2]-0.95))/0.32)**2))*sstep((yy-(ec[1]-0.2))/0.6)*skin
        D += G2*E('FM2_BAG', '0.0')*bag[:, None]*(fwd*0.9+up*0.2)[None, :]
    mrw, _ = line_w((mouth_half+0.2, St-0.4), (mouth_half+0.5, St-2.2), 0.2)
    D -= G2*E('FM2_MAR', '0.0')*(mrw*sstep((yy-8.0)/2.0)*skin)[:, None]*N
    D[lidmesh] = D[lidmesh]  # lid meshes (eyeshell / lashes / edge / caruncle) take the same field as the lid skin
# ---- locks: eyeballs / teeth / saliva zero; seam / collar only original BR
D[locked] = 0.0
guard = sstep((X[:, 2]-E('FM_GUARD_Z', '146.5'))/2.0); D *= guard[:, None]
mag = np.linalg.norm(D, axis=1); print('FACE_DELTA verts>0.002', int((mag > 0.002).sum()), 'max mm %.2f' % (mag.max()*10), 'p99 mm %.2f' % (np.percentile(mag[mag > 0.002], 99)*10))
reg = {n: float((np.linalg.norm(v, axis=1)).max()*10) for n, v in [('lips', D*(lip > 0.05)[:, None]), ('eyes', D*((np.linalg.norm(X-eyeL, axis=1) < 3) | (np.linalg.norm(X-eyeR, axis=1) < 3))[:, None]), ('jaw', D*(jaw > 0.05)[:, None])]}
print('REGION_MAX_MM', json.dumps({k: round(v, 2) for k, v in reg.items()}))
TOT = BR+D
def put(DD, idx=None):
    m = np.linalg.norm(DD, axis=1); ids = np.nonzero(m > 1e-5)[0]; return {str(int(i)): [round(float(x), 5) for x in DD[i]] for i in ids}
json.dump({'Body': {}, 'Head': {'BR_Neutral': put(TOT)}}, open(os.path.join(OUT, 'morph_fm_face_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'face_delta_lod0.npy'), D); json.dump(LM, open(os.path.join(OUT, 'face_landmarks.json'), 'w'), indent=1)
# ---- LOD transfer (closest point on LOD0 -> barycentric of the TOTAL delta)
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t) for t in T])
info = json.load(open(os.path.join(LODD, 'lod_info.json')))['Head']
for lod in range(1, info['lods']):
    f = os.path.join(LODD, f'lod_Head_{lod}.json.gz')
    if not os.path.exists(f): print('no lod file', lod); continue
    PL = np.asarray(json.load(gzip.open(f, 'rt'))['positions']); res = {}; far = 0
    for vi, p in enumerate(PL):
        loc, nrm, fi, dist = bvh.find_nearest(Vector(p))
        if fi is None or dist > 1.0: far += 1; continue
        t = T[fi]; A_, B_, C_ = X[t[0]], X[t[1]], X[t[2]]; q = np.asarray(loc)
        v0, v1, v2 = B_-A_, C_-A_, q-A_; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01 or 1e-12
        bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; bu = 1-bv-bw; dd = bu*TOT[t[0]]+bv*TOT[t[1]]+bw*TOT[t[2]]
        if np.linalg.norm(dd) > 1e-5: res[str(vi)] = [round(float(x), 5) for x in dd]
    json.dump({'Body': {}, 'Head': {'BR_Neutral': res}}, open(os.path.join(OUT, f'morph_fm_face_lod{lod}.json'), 'w')); print('LOD', lod, 'verts', len(res), 'far', far)
print('FACEDELTA_OK')
