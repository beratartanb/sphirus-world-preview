"""GD46 garment fit: re-settle the g17e Henley in the IN-GAME idle pose (the pattern garment was draped in the A-pose, so the yoke / sleeve volume
of that drape is carried into the arms-down game pose by skinning: 'shoulder pads', nothing hangs). Pipeline (Blender 5.2 python, numpy):
  1. LK body (sculpt package br_neutral + LK_Neutral deltas) + head, posed by offline LBS with the game pose (component-space bones)
  2. g17e Henley posed by the same LBS with its own g17e weights (= what the game shows now; validated against the PIE render readback)
  3. main cloth (part SPH_Henley) welded at UV seams, edge lengths pre-relaxed to the BIND (pattern) lengths (PBD), cuff rows pinned
  4. Blender cloth settle with gravity, body collision, self collision -> settled posed shape; detail pieces follow their nearest cloth vertex
  5. posed delta -> bind-space delta through the inverse blended skinning matrix -> new rest positions (LOD1/2: nearest LOD0 delta)
  6. writes a new garment build dir (outfit_geometry.json.gz + weights copy) for the UE chain + report + clay preview renders
usage: blender -b --factory-startup --python gd46_settle.py -- <g17e_build_dir> <sculpt_package_v6.json.gz> <morph_lk_body_lod0.json> <pose.json|approx> <out_dir>
env: SPH_FRAMES=100 SPH_PRERELAX=1 SPH_PBD_IT=300 SPH_PIN_CUFF_X=45.5 SPH_NECK_PIN=0 SPH_NECK_Z=141 SPH_MASS=0.3 SPH_TENSION=30 SPH_COMPRESSION=30
     SPH_SHEAR=15 SPH_BEND=0.6 SPH_AIR=1.5 SPH_QUALITY=10 SPH_DIST=0.0035 SPH_SELFCOL=1 SPH_GAP=0.35 SPH_RENDER=1 SPH_AB=8 SPH_FW=6 SPH_EL=12 SPH_FRICTION=5"""
import bpy, bmesh, sys, os, json, gzip, math, time, shutil
import numpy as np
from mathutils import Vector, kdtree
from mathutils.bvhtree import BVHTree
T0 = time.time()
def log(*a): print('[gd46 %6.1fs]' % (time.time()-T0), *a, flush=True)
def E(k, d): return float(os.environ.get(k, d))
a = sys.argv[sys.argv.index('--')+1:]; GDIR, PKG, LKJ, POSE, OUT = a[:5]; os.makedirs(OUT, exist_ok=True)
S = 0.01
def bl(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]*S, -p[..., 1]*S, p[..., 2]*S], -1)
def ue(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]/S, -p[..., 1]/S, p[..., 2]/S], -1)
def ss(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
# ------------------------------------------------------------------ inputs
GEO = json.loads(gzip.open(os.path.join(GDIR, 'outfit_geometry.json.gz'), 'rb').read()); WTS = json.loads(gzip.open(os.path.join(GDIR, 'outfit_weights.json.gz'), 'rb').read())
P = json.loads(gzip.open(PKG, 'rb').read()); NB, NH = P['NB'], P['NH']
XB = np.asarray(P['br_neutral'], np.float64).copy()
for k_, v in json.load(open(LKJ))['Body']['LK_Neutral'].items(): XB[int(k_)] += v          # current LK neutral = b2 + v6 + LK_Neutral
TB = np.asarray([list(t) for t in P['body']['triangles']]+[[x+NB, y+NB, z+NB] for x, y, z in P['head']['triangles']], np.int64)
SK = P['skeleton']['Body']; BIND = SK['bind']; PARENTS = SK['parents']; BONES = list(BIND.keys()); BI = {b: i for i, b in enumerate(BONES)}
def qmat(q):
    x, y, z, w = q; return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def qmul(a_, b_):
    ax, ay, az, aw = a_; bx, by, bz, bw = b_
    return (aw*bx+ax*bw+ay*bz-az*by, aw*by-ax*bz+ay*bw+az*bx, aw*bz+ax*by-ay*bx+az*bw, aw*bw-ax*bx-ay*by-az*bz)
def qaxis(ax, deg):
    h = math.radians(deg)/2; n = math.sqrt(sum(c*c for c in ax)); return (ax[0]/n*math.sin(h), ax[1]/n*math.sin(h), ax[2]/n*math.sin(h), math.cos(h))
def q_from_to(u, v):
    u = np.asarray(u, float); v = np.asarray(v, float); u /= np.linalg.norm(u); v /= np.linalg.norm(v); c = np.cross(u, v); d = float(np.dot(u, v))
    if np.linalg.norm(c) < 1e-9: return (0.0, 0.0, 0.0, 1.0)
    ang = math.degrees(math.atan2(np.linalg.norm(c), d)); return qaxis(tuple(c), ang)
def mats_of(tbl):
    R = np.zeros((len(BONES), 3, 3)); t = np.zeros((len(BONES), 3)); missing = []
    for i, b in enumerate(BONES):
        v = tbl.get(b)
        if v is None: v = BIND[b]; missing.append(b)
        R[i] = qmat(v['rotation'])*np.asarray(v.get('scale', [1, 1, 1]), float)[None, :]; t[i] = np.asarray(v['translation'], float)
    return R, t, missing
# ------------------------------------------------------------------ pose
def children_of(root):
    out = []; stack = [root]
    while stack:
        b = stack.pop(); out.append(b); stack += [c for c, p in PARENTS.items() if p == b]
    return out
def approx_pose():
    """arms-down relaxed idle from the bind: upperarm chain rotated rigidly about the shoulder to an abduction/forward target, forearm flexed"""
    AB, FW, EL = E('SPH_AB', '8'), E('SPH_FW', '6'), E('SPH_EL', '12'); pose = {b: dict(BIND[b]) for b in BONES}; moved = {}
    def rigid(bone, q, origin):
        for c in children_of(bone):
            v = pose[c]; tt = np.asarray(v['translation'], float); pose[c] = {'translation': list(origin+qmat(q)@(tt-origin)), 'rotation': list(qmul(q, tuple(v['rotation']))), 'scale': v.get('scale', [1, 1, 1])}
    for side, sx in (('l', 1.0), ('r', -1.0)):
        ua = 'upperarm_'+side; hd = 'hand_'+side; o = np.asarray(BIND[ua]['translation'], float); d0 = np.asarray(BIND[hd]['translation'], float)-o
        d1 = np.array([sx*math.sin(math.radians(AB)), math.sin(math.radians(FW)), -math.cos(math.radians(AB))]); q = q_from_to(d0, d1); rigid(ua, q, o)
        la = 'lowerarm_'+side; o2 = np.asarray(pose[la]['translation'], float); rigid(la, qaxis((1, 0, 0), EL), o2)
        moved[side] = {'bind_dir': [round(x, 3) for x in d0/np.linalg.norm(d0)], 'target_dir': [round(x, 3) for x in d1/np.linalg.norm(d1)], 'hand_after': [round(x, 2) for x in pose[hd]['translation']]}
    return pose, {'mode': 'approx', 'AB': AB, 'FW': FW, 'EL': EL, 'arms': moved}
if POSE == 'approx': PT, pose_info = approx_pose()
else:
    pj = json.load(open(POSE)); PT = pj['bones'] if 'bones' in pj else pj; pose_info = {'mode': 'file', 'file': POSE, 'n': len(PT)}
Rb, tb, _ = mats_of(BIND); Rp, tp, miss = mats_of(PT); pose_info['missing_in_pose'] = miss[:10]; pose_info['n_missing'] = len(miss)
Rbi = np.linalg.inv(Rb); RM = np.einsum('nij,njk->nik', Rp, Rbi); TM = tp-np.einsum('nij,nj->ni', RM, tb)
def pack_w(wlist, K=8, fallback=None):
    """weights dicts -> (N,K) bone index / weight arrays over the BODY skeleton; influences of unknown bones (facial rig) are dropped and the rest
    renormalised; a vertex with no known bone gets the fallback bone rigidly (head mesh vertices -> 'head')"""
    idx = np.zeros((len(wlist), K), np.int64); w = np.zeros((len(wlist), K)); dropped = 0; nofb = 0
    for i, d in enumerate(wlist):
        items = [(BI[b], float(x)) for b, x in d.items() if b in BI]; dropped += len(d)-len(items); items.sort(key=lambda t: -t[1]); items = items[:K]; s = sum(x for _, x in items) or 1.0
        if not items and fallback is not None: items = [(BI[fallback], 1.0)]; s = 1.0; nofb += 1
        for k, (b, x) in enumerate(items): idx[i, k] = b; w[i, k] = x/s
    if nofb: log('pack_w: fallback bone for', nofb, 'vertices')
    return idx, w, dropped
def lbs(X, idx, w):
    Pp = np.zeros_like(X); A = np.zeros((len(X), 3, 3))
    for k in range(idx.shape[1]):
        Rk = RM[idx[:, k]]; Pp += w[:, k, None]*(np.einsum('nij,nj->ni', Rk, X)+TM[idx[:, k]]); A += w[:, k, None, None]*Rk
    return Pp, A
bidx, bw, bdrop = pack_w(P['weights'], fallback='head'); XBP, _ = lbs(XB, bidx, bw); log('body posed', XB.shape, 'dropped weights', bdrop, 'pose', json.dumps(pose_info)[:300])
H = GEO['henley']; XG = np.asarray(H['positions'], np.float64); TG = np.asarray(H['triangles'], np.int64); PART = np.asarray(H['part']); MID = np.asarray(H['material_ids'], np.int64)
gidx, gw, gdrop = pack_w(WTS['henley']); XGP, AG = lbs(XG, gidx, gw); log('henley posed', XG.shape, 'dropped', gdrop)
np.save(os.path.join(OUT, 'henley_posed_start.npy'), XGP); gzip.open(os.path.join(OUT, 'henley_posed_start.json.gz'), 'wt').write(json.dumps({'positions': np.round(XGP, 3).tolist()}))
# ------------------------------------------------------------------ main cloth: weld + pins + pre-relax
main = np.nonzero(PART == 'SPH_Henley')[0]; is_main = np.zeros(len(XG), bool); is_main[main] = True
key = np.round(XG[main]*1000).astype(np.int64); _, first, grp = np.unique(key, axis=0, return_index=True, return_inverse=True); grp = grp.ravel(); NU = len(first)
XU_bind = np.zeros((NU, 3)); np.add.at(XU_bind, grp, XG[main]); cnt = np.bincount(grp, minlength=NU)[:, None]; XU_bind /= cnt
XU = np.zeros((NU, 3)); np.add.at(XU, grp, XGP[main]); XU /= cnt
m2u = -np.ones(len(XG), np.int64); m2u[main] = grp
tri_main = TG[np.all(is_main[TG], axis=1)]; FU = m2u[tri_main]; FU = FU[(FU[:, 0] != FU[:, 1]) & (FU[:, 1] != FU[:, 2]) & (FU[:, 0] != FU[:, 2])]
edges_all = np.sort(np.concatenate([FU[:, [0, 1]], FU[:, [1, 2]], FU[:, [2, 0]]]), axis=1); edges, ecount = np.unique(edges_all, axis=0, return_counts=True); L0 = np.linalg.norm(XU_bind[edges[:, 1]]-XU_bind[edges[:, 0]], axis=1)
bverts = np.unique(edges[ecount == 1].ravel())                                                   # open boundary of the main cloth: neck opening, V, cuffs, hem
def band_pin(sel_mask, band, full):
    """1 within `full` cm of the selected boundary vertices (bind space), smooth to 0 at `band` cm"""
    bv = bverts[sel_mask[bverts]]
    if len(bv) == 0: return np.zeros(NU)
    kd_ = kdtree.KDTree(len(bv))
    for k, i in enumerate(bv): kd_.insert(Vector(XU_bind[i]), k)
    kd_.balance(); dist = np.asarray([kd_.find(Vector(p))[2] for p in XU_bind]); return ss((band-dist)/max(band-full, 1e-3))
NECKP = E('SPH_NECK_PIN', '1.0'); NECKBAND = E('SPH_NECK_BAND', '2.5'); CUFFBAND = E('SPH_CUFF_BAND', '3.0')
neck_sel = (XU_bind[:, 2] > 118) & (np.abs(XU_bind[:, 0]) < 14.0)                                 # neck opening + V edges (the rib binding grips here)
cuff_sel = np.abs(XU_bind[:, 0]) > 40.0                                                         # sleeve ends (cuffs hold at the wrist)
pin = np.maximum(NECKP*band_pin(neck_sel, NECKBAND, 0.6), band_pin(cuff_sel, CUFFBAND, 1.0))
log('cloth unique', NU, 'tris', len(FU), 'boundary verts', len(bverts), 'pinned', int((pin >= 0.999).sum()), 'soft', int(((pin > 0) & (pin < 0.999)).sum()))
def stretch_stats(Xp):
    r = np.linalg.norm(Xp[edges[:, 1]]-Xp[edges[:, 0]], axis=1)/np.maximum(L0, 1e-6); return {'p50': round(float(np.percentile(r, 50)), 4), 'p95': round(float(np.percentile(r, 95)), 4), 'p05': round(float(np.percentile(r, 5)), 4), 'max': round(float(r.max()), 3), 'min': round(float(r.min()), 3), 'over10pct': round(float((np.abs(r-1) > 0.1).mean()), 4)}
rep = {'pose': pose_info, 'n_unique': NU, 'stretch_posed_start': stretch_stats(XU)}
if int(E('SPH_PRERELAX', '1')):
    Xr = XU.copy(); free = (pin < 0.999).astype(float); IT = int(E('SPH_PBD_IT', '300')); deg = np.bincount(edges.ravel(), minlength=NU).astype(float)[:, None]
    for it in range(IT):
        e = Xr[edges[:, 1]]-Xr[edges[:, 0]]; ln = np.linalg.norm(e, axis=1); corr = ((ln-L0)/np.maximum(ln, 1e-6))[:, None]*e
        dP = np.zeros_like(Xr); np.add.at(dP, edges[:, 0], 0.5*corr); np.add.at(dP, edges[:, 1], -0.5*corr); Xr += 0.8*dP/np.maximum(deg, 1)*free[:, None]
    rep['stretch_prerelaxed'] = stretch_stats(Xr); rep['prerelax_move_cm'] = {'mean': round(float(np.linalg.norm(Xr-XU, axis=1).mean()), 3), 'max': round(float(np.linalg.norm(Xr-XU, axis=1).max()), 3)}; XU_start = Xr
else: XU_start = XU.copy()
# ------------------------------------------------------------------ Blender scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene; sc.frame_set(1)
def make_obj(name, V, F):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], [list(f) for f in F]); me.validate(); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); return ob
body = make_obj('BodyPosed', bl(XBP), TB); body.modifiers.new('Collision', 'COLLISION'); body.collision.thickness_outer = 0.0025; body.collision.thickness_inner = E('SPH_INNER', '0.003'); body.collision.cloth_friction = E('SPH_FRICTION', '5')
SHD = os.environ.get('SPH_SHORTS_DIR', '')
if SHD:   # the worn shorts as an extra collider (game shorts = skinned g16c): posed with their own weights, slightly inflated along their normals
    GS = json.loads(gzip.open(os.path.join(SHD, 'outfit_geometry.json.gz'), 'rb').read())['trousers']; WS = json.loads(gzip.open(os.path.join(SHD, 'outfit_weights.json.gz'), 'rb').read())['trousers']
    XS = np.asarray(GS['positions'], np.float64); TS = np.asarray(GS['triangles'], np.int64); sidx, sw, _ = pack_w(WS); XSP, _ = lbs(XS, sidx, sw)
    nS = np.zeros_like(XSP); fn = np.cross(XSP[TS[:, 1]]-XSP[TS[:, 0]], XSP[TS[:, 2]]-XSP[TS[:, 0]])
    for k in range(3): np.add.at(nS, TS[:, k], fn)
    nS /= np.maximum(np.linalg.norm(nS, axis=1), 1e-9)[:, None]; XSP = XSP+nS*E('SPH_SHORTS_INFLATE', '0.25')
    shorts_ob = make_obj('ShortsPosed', bl(XSP), TS); shorts_ob.modifiers.new('Collision', 'COLLISION'); shorts_ob.collision.thickness_outer = 0.0025; shorts_ob.collision.thickness_inner = 0.003; shorts_ob.collision.cloth_friction = E('SPH_FRICTION', '5')
    VV = np.concatenate([XBP, XSP]); TT = np.concatenate([TB, TS+len(XBP)]); rep['shorts_collider'] = {'verts': int(len(XS)), 'z_top': round(float(XSP[:, 2].max()), 2)}
    gzip.open(os.path.join(OUT, 'shorts_posed.json.gz'), 'wt').write(json.dumps({'positions': np.round(XSP, 3).tolist(), 'triangles': TS.tolist()}))
else: VV, TT = XBP, TB
bvh = BVHTree.FromPolygons([tuple(v) for v in bl(VV)], [list(f) for f in TT])
cl = make_obj('Cloth', bl(XU_start), FU); vg = cl.vertex_groups.new(name='PIN')
for i in range(NU):
    if pin[i] > 0: vg.add([i], float(pin[i]), 'REPLACE')
GAP = E('SPH_GAP', '0.35')*S; moved = 0; inside0 = 0
for v in cl.data.vertices:
    loc, nrm, idx, dist = bvh.find_nearest(v.co)
    if loc is not None:
        sd = (v.co-loc).dot(nrm)
        if sd < 0: inside0 += 1
        if sd < GAP and (pin[v.index] < 0.999 or int(E('SPH_PREPUSH_PINS', '1'))): v.co = loc+nrm*GAP; moved += 1
cl.data.update(); rep['prepush'] = {'moved': moved, 'inside_before': inside0}; log('prepush', moved, 'inside', inside0)
mod = cl.modifiers.new('Cloth', 'CLOTH'); st = mod.settings; cs = mod.collision_settings
st.quality = int(E('SPH_QUALITY', '12')); st.mass = E('SPH_MASS', '0.3'); st.tension_stiffness = E('SPH_TENSION', '30'); st.compression_stiffness = E('SPH_COMPRESSION', '30'); st.shear_stiffness = E('SPH_SHEAR', '15')
st.bending_stiffness = E('SPH_BEND', '0.6'); st.tension_damping = 5; st.compression_damping = 5; st.shear_damping = 5; st.bending_damping = 0.5; st.air_damping = E('SPH_AIR', '3.0'); st.bending_model = 'ANGULAR'
st.vertex_group_mass = 'PIN'; st.pin_stiffness = 1.0
cs.use_collision = True; cs.distance_min = E('SPH_DIST', '0.0035'); cs.collision_quality = 4; cs.use_self_collision = bool(int(E('SPH_SELFCOL', '0'))); cs.self_distance_min = E('SPH_SELFDIST', '0.005'); cs.self_friction = 5
FR = int(E('SPH_FRAMES', '60')); mod.point_cache.frame_start = 1; mod.point_cache.frame_end = FR; sc.frame_end = FR
dg = bpy.context.evaluated_depsgraph_get(); trace = []
for f in range(1, FR+1):
    sc.frame_set(f)
    if f % 20 == 0 or f == FR:
        ev = cl.evaluated_get(bpy.context.evaluated_depsgraph_get()); co = np.zeros(len(ev.data.vertices)*3); ev.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
        mv = np.linalg.norm(co-bl(XU_start), axis=1); trace.append([f, round(float(mv.mean()/S), 3), round(float(mv.max()/S), 3)]); log('frame', f, 'move mean/max cm', trace[-1][1:])
ev = cl.evaluated_get(bpy.context.evaluated_depsgraph_get()); co = np.zeros(len(ev.data.vertices)*3); ev.data.vertices.foreach_get('co', co); XU_set_bl = co.reshape(-1, 3).copy(); XU_set = ue(XU_set_bl)
rep['trace'] = trace; rep['stretch_settled_raw'] = stretch_stats(XU_set)
# ---------------------------------------------------------------- post: fold repair + edge relax + clearance (PBD-style, pins fixed)
def tri_normals(Xp): n = np.cross(Xp[FU[:, 1]]-Xp[FU[:, 0]], Xp[FU[:, 2]]-Xp[FU[:, 0]]); return n/np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
N_start = tri_normals(XU_start); freev = (pin < 0.999)
nbr_a = np.concatenate([edges[:, 0], edges[:, 1]]); nbr_b = np.concatenate([edges[:, 1], edges[:, 0]]); deg_all = np.bincount(nbr_a, minlength=NU).astype(float)
def flipped_mask(Xp): return np.einsum('ij,ij->i', N_start, tri_normals(Xp)) < 0.0
def pushout(Xp, gap_cm):
    moved = 0
    for i in np.nonzero(freev)[0]:
        q_ = Vector(bl(Xp[i])); loc, nrm, idx, dist = bvh.find_nearest(q_)
        if loc is not None:
            sdv = (q_-loc).dot(nrm)
            if sdv < gap_cm*S: Xp[i] = ue(np.asarray(loc+nrm*(gap_cm*S))); moved += 1
    return moved
POST_IT = int(E('SPH_POST_IT', '12')); Xf = XU_set.copy(); post = []
for it in range(POST_IT):
    fl = flipped_mask(Xf); fv = np.zeros(NU, bool); fv[FU[fl].ravel()] = True; ring = fv.copy(); ring[nbr_b[fv[nbr_a]]] = True   # folded verts + 1-ring
    if fl.sum() == 0 and it > 2: break
    lap = np.zeros_like(Xf); np.add.at(lap, nbr_a, Xf[nbr_b]); lap /= np.maximum(deg_all, 1)[:, None]
    sm = ring & freev; Xf[sm] = 0.5*Xf[sm]+0.5*lap[sm]                                                  # umbrella smoothing on folds only
    for k in range(25):                                                                                 # edge-length projection (pattern lengths)
        e = Xf[edges[:, 1]]-Xf[edges[:, 0]]; ln = np.linalg.norm(e, axis=1); corr = ((ln-L0)/np.maximum(ln, 1e-6))[:, None]*e
        dP = np.zeros_like(Xf); np.add.at(dP, edges[:, 0], 0.5*corr); np.add.at(dP, edges[:, 1], -0.5*corr); Xf += 0.7*dP/np.maximum(deg_all, 1)[:, None]*freev[:, None]
    mv = pushout(Xf, E('SPH_GAP', '0.35')); post.append([it, int(fl.sum()), mv])
rep['post'] = post; rep['flipped_after_post'] = int(flipped_mask(Xf).sum()); rep['post_move_cm'] = round(float(np.linalg.norm(Xf-XU_set, axis=1).max()), 3)
# displacement-field smoothing (keeps the pattern drape detail of the rest shape, removes sub-cm crumple noise of the settle), then edge relax + clearance
DS = int(E('SPH_DSMOOTH', '0'))
if DS > 0:
    Du = Xf-XU
    for it in range(DS):
        lap = np.zeros_like(Du); np.add.at(lap, nbr_a, Du[nbr_b]); lap /= np.maximum(deg_all, 1)[:, None]; Du[freev] = 0.5*Du[freev]+0.5*lap[freev]
    Xf = XU+Du
    for k in range(40):
        e = Xf[edges[:, 1]]-Xf[edges[:, 0]]; ln = np.linalg.norm(e, axis=1); corr = ((ln-L0)/np.maximum(ln, 1e-6))[:, None]*e
        dP = np.zeros_like(Xf); np.add.at(dP, edges[:, 0], 0.5*corr); np.add.at(dP, edges[:, 1], -0.5*corr); Xf += 0.7*dP/np.maximum(deg_all, 1)[:, None]*freev[:, None]
    rep['dsmooth'] = {'it': DS, 'pushout': pushout(Xf, E('SPH_GAP', '0.35'))}
rep['flipped_final'] = int(flipped_mask(Xf).sum())
XU_set = Xf; XU_set_bl = bl(XU_set); rep['stretch_settled'] = stretch_stats(XU_set); log('post', post[-3:], 'flipped final', rep['flipped_final'], 'stretch', rep['stretch_settled'])
zb_u = XU_bind[:, 2]; dzu = (XU_set-XU)[:, 2]
rep['dz_cm'] = {nm: round(float(dzu[m_].mean()), 3) for nm, m_ in (('hem_z<100', zb_u < 100), ('mid_100-122', (zb_u >= 100) & (zb_u < 122)), ('upper_122-136', (zb_u >= 122) & (zb_u < 136)), ('yoke_z>136', zb_u >= 136), ('sleeves_|x|>22', np.abs(XU_bind[:, 0]) > 22)) if m_.any()}
sd = []
for i in range(NU):
    loc, nrm, idx, dist = bvh.find_nearest(Vector(XU_set_bl[i])); sd.append((Vector(XU_set_bl[i])-loc).dot(nrm)/S if loc is not None else 9.9)
sd = np.asarray(sd); rep['clearance_cm'] = {'inside_gt_0.1': int((sd < -0.1).sum()), 'inside_any': int((sd < 0).sum()), 'p05': round(float(np.percentile(sd, 5)), 3), 'p50': round(float(np.percentile(sd, 50)), 3), 'p95': round(float(np.percentile(sd, 95)), 3)}
# ------------------------------------------------------------------ back to all garment vertices, details follow, inverse skin
D = np.zeros_like(XG); D[main] = (XU_set-XU)[grp]
det = np.nonzero(~is_main)[0]
if len(det):
    kd = kdtree.KDTree(len(main))
    for k, i in enumerate(main): kd.insert(Vector(XG[i]), k)
    kd.balance()
    for i in det: D[i] = D[main[kd.find(Vector(XG[i]))[1]]]
Db = np.zeros_like(D)
for i in np.nonzero(np.linalg.norm(D, axis=1) > 1e-5)[0]:
    try: Db[i] = np.linalg.solve(AG[i], D[i])
    except np.linalg.LinAlgError: Db[i] = D[i]
XG_new = XG+Db; XGP_new, _ = lbs(XG_new, gidx, gw); rep['roundtrip_cm'] = round(float(np.abs(XGP_new-(XGP+D)).max()), 4)
rep['delta_posed_cm'] = {'mean': round(float(np.linalg.norm(D, axis=1).mean()), 3), 'p95': round(float(np.percentile(np.linalg.norm(D, axis=1), 95)), 3), 'max': round(float(np.linalg.norm(D, axis=1).max()), 3)}
rep['delta_bind_cm'] = {'mean': round(float(np.linalg.norm(Db, axis=1).mean()), 3), 'max': round(float(np.linalg.norm(Db, axis=1).max()), 3)}
zb = XG[main, 2]
for nm, m_ in (('yoke_z>136', zb > 136), ('upper_122-136', (zb > 122) & (zb <= 136)), ('lower_<122', zb <= 122)):
    rep['delta_posed_cm'][nm] = round(float(np.linalg.norm(D[main][m_], axis=1).mean()), 3) if m_.any() else None
# LOD1/2: nearest LOD0 bind vertex delta
kd0 = kdtree.KDTree(len(XG))
for i in range(len(XG)): kd0.insert(Vector(XG[i]), i)
kd0.balance(); NEW = {'henley': XG_new}
for ln in ('henley_lod1', 'henley_lod2'):
    XL = np.asarray(GEO[ln]['positions'], np.float64); DL = np.asarray([Db[kd0.find(Vector(p))[1]] for p in XL]); NEW[ln] = XL+DL
# ------------------------------------------------------------------ outputs
G2 = json.loads(json.dumps(GEO))
for ln, X_ in NEW.items(): G2[ln]['positions'] = np.round(X_, 4).tolist()
G2['facts']['gd46_settle'] = {'source_build': os.path.basename(os.path.normpath(GDIR)), 'pose': pose_info.get('mode'), 'frames': FR}
gzip.open(os.path.join(OUT, 'outfit_geometry.json.gz'), 'wt').write(json.dumps(G2)); gzip.open(os.path.join(OUT, 'outfit_geometry_raw.json.gz'), 'wt').write(json.dumps(G2))
shutil.copy(os.path.join(GDIR, 'outfit_weights.json.gz'), os.path.join(OUT, 'outfit_weights.json.gz'))
gzip.open(os.path.join(OUT, 'henley_posed_settled.json.gz'), 'wt').write(json.dumps({'positions': np.round(XGP+D, 3).tolist()})); gzip.open(os.path.join(OUT, 'body_posed.json.gz'), 'wt').write(json.dumps({'positions': np.round(XBP, 3).tolist()}))
json.dump(PT, open(os.path.join(OUT, 'pose_used.json'), 'w'))
# ------------------------------------------------------------------ clay previews (Workbench): posed body + start garment / settled garment
if int(E('SPH_RENDER', '1')):
    cl.modifiers.remove(mod); sc.frame_set(1)
    for o in (body, cl): o.hide_render = True
    gar0 = make_obj('GarmentStart', bl(XGP), TG); gar1 = make_obj('GarmentSettled', bl(XGP+D), TG); bodyr = make_obj('BodyR', bl(XBP), TB)
    def mat(name, col):
        m = bpy.data.materials.new(name); m.diffuse_color = col; return m
    mb = mat('M_Body', (0.45, 0.42, 0.40, 1.0)); mg = mat('M_Garment', (0.92, 0.92, 0.90, 1.0)); bodyr.data.materials.append(mb); gar0.data.materials.append(mg); gar1.data.materials.append(mg)
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'; sc.display.shading.show_shadows = True; sc.display.shading.show_cavity = True
    sc.render.resolution_x = 900; sc.render.resolution_y = 1200; sc.render.resolution_percentage = 100; sc.render.image_settings.file_format = 'PNG'
    cam_data = bpy.data.cameras.new('Cam'); cam_data.lens = 60; cam = bpy.data.objects.new('Cam', cam_data); sc.collection.objects.link(cam); sc.camera = cam
    tgt = Vector(bl(np.array([0.0, 0.0, 122.0])))
    def shoot(tag, az_deg, dist=3.4, h=1.32):
        ang = math.radians(az_deg); pos = Vector((dist*math.sin(ang), -dist*math.cos(ang), h)); cam.location = pos; d = tgt-pos; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(OUT, 'preview_%s.png' % tag); bpy.ops.render.render(write_still=True)
    for st_, g in (('start', gar0), ('settled', gar1)):
        gar0.hide_render = g is not gar0; gar1.hide_render = g is not gar1
        for az, nm in ((0, 'front'), (90, 'side'), (180, 'back'), (40, 'front34')): shoot('%s_%s' % (st_, nm), az)
    log('previews written')
json.dump(rep, open(os.path.join(OUT, 'settle_report.json'), 'w'), indent=1); log('GD46_SETTLE_OK', json.dumps(rep)[:1500])
