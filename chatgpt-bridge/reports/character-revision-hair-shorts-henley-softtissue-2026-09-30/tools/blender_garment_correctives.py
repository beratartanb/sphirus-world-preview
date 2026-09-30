"""Garment pose-space correctives (dynamic Henley neckline, SHCB underarm, shorts hip flexion) solved against the DEFORMED body.
Per target pose: garment rest (outfit_geometry.json.gz, UE cm) -> offline linear-blend skinning with the captured component-space
bones (bind = neutral capture) -> collision pre-push out of the captured posed body (render mesh incl. soft-tissue morphs) ->
Blender cloth with world gravity on the free region only (pinned elsewhere) -> relax -> posed delta -> bind-space delta through
the inverse of each vertex's blended skinning rotation. Detail pieces (bands, buttons, cords) follow their nearest cloth vertex.
Side-specific curves take the matching half (smooth ramp across x = 0).
usage: blender -b --factory-startup --python blender_garment_correctives.py -- <geometry.json.gz> <weights.json.gz> <captures_dir> <prefix> <out.json> [poses csv]"""
import bpy, sys, os, json, gzip, math, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; GEO, WTS, CAP, PFX, OUT = a[:5]; ONLY = a[5].split(',') if len(a) > 5 else None
T0 = time.time()
def log(*x): print('[gcorr %6.1fs]' % (time.time()-T0), *x, flush=True)
G = json.loads(gzip.open(GEO, 'rb').read()); W = json.loads(gzip.open(WTS, 'rb').read())
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
def qmat(q):
    x, y, z, w = q; return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def bones(pose):
    d = json.load(open(os.path.join(CAP, f'{PFX}_{pose}_front.json')))['bone_transforms']['Body']
    return {b: (qmat(v['rotation'])*np.asarray(v['scale'])[None, :], np.asarray(v['translation'])) for b, v in d.items()}
BIND = bones('neutral')
def skin(X, Wg, BP):
    """linear blend skinning; returns posed positions and the blended 3x3 per vertex"""
    Mb = {}
    for b in BP:
        if b not in BIND: continue
        Rb, tb = BIND[b]; Rp, tp = BP[b]; Rbi = np.linalg.inv(Rb); R = Rp@Rbi; Mb[b] = (R, tp-R@tb)
    P = np.zeros_like(X); A = np.zeros((len(X), 3, 3))
    for i, (x, ws) in enumerate(zip(X, Wg)):
        for b, w in ws.items():
            if b not in Mb: continue
            R, t = Mb[b]; P[i] += w*(R@x+t); A[i] += w*R
    return P, A
def load_mesh(path):
    d = json.load(gzip.open(path, 'rt')); return np.asarray(d['positions']), np.asarray(d['triangles'], np.int64)
S = 0.01
def bl(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]*S, -p[..., 1]*S, p[..., 2]*S], -1)
def ue(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]/S, -p[..., 1]/S, p[..., 2]/S], -1)
def make_obj(name, V, F):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in bl(V)], [], [tuple(f) for f in F]); me.validate(); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
# pose -> (garment, curve names, free-region function, frames)
def free_bend(X):
    f = sstep((X[:, 1]-2.0)/3.0)*sstep((133.5-X[:, 2])/2.5)*sstep((X[:, 2]-110.0)/4.0)*sstep((13.5-np.abs(X[:, 0]))/3.0); return f
ARM_R = float(os.environ.get('SPH_GC_ARM_R', '12.0'))
def free_arm(X):
    d = np.minimum(np.linalg.norm(X-np.array([14.5, 0.0, 125.5]), axis=1), np.linalg.norm(X-np.array([-14.5, 0.0, 125.5]), axis=1)); f = sstep((ARM_R-d)/5.0)
    if os.environ.get('SPH_GC_ARM_NECK', '0') == '1': f = np.maximum(f, free_bend(X))   # front neckline also free (arm-raise neckline gape)
    return f
def free_hip(X):
    return sstep((91.0-X[:, 2])/5.0)
POSES = [('pl_bend30', 'henley', ['RV_Bend30'], free_bend, 60), ('pl_bend60', 'henley', ['RV_Bend60'], free_bend, 60), ('pl_bend90', 'henley', ['RV_Bend90'], free_bend, 70),
         ('elev90', 'henley', ['RV_Arm090_l', 'RV_Arm090_r'], free_arm, 50), ('elev120', 'henley', ['RV_Arm120_l', 'RV_Arm120_r'], free_arm, 55),
         ('elev150', 'henley', ['RV_Arm150_l', 'RV_Arm150_r'], free_arm, 60), ('elev180', 'henley', ['RV_Arm180_l', 'RV_Arm180_r'], free_arm, 60),
         ('hipflex', 'trousers', ['RV_Hip075_l', 'RV_Hip075_r'], free_hip, 25), ('squat', 'trousers', ['RV_Hip110_l', 'RV_Hip110_r'], free_hip, 25)]
PARAMS = {'henley': dict(mass=0.3, tension=30, bend=1.5, shear=15), 'trousers': dict(mass=0.1, tension=60, bend=7.0, shear=25)}
MAINPART = {'henley': 'SPH_Henley', 'trousers': 'SPH_Trousers'}
out = {'henley': {}, 'trousers': {}, '_stats': {}}
sc = bpy.context.scene
for pose, gname, curves, freefn, frames in POSES:
    if ONLY and pose not in ONLY: continue
    g = G[gname]; X = np.asarray(g['positions']); F = np.asarray(g['triangles'], np.int64); part = np.asarray(g['part']); Wg = W[gname]
    main = part == MAINPART[gname]
    BP = bones(pose); P, A = skin(X, Wg, BP)
    # sanity: compare with the render dump of the same capture (nearest-distance)
    gpath = os.path.join(CAP, 'posed_geometry', f'{PFX}_{pose}_{"Henley" if gname == "henley" else "Shorts"}.json.gz')
    rep = {}
    if os.path.exists(gpath):
        RV_, _ = load_mesh(gpath); tb = BVHTree.FromPolygons([Vector(p) for p in RV_], [list(t) for t in _])
        dd = [tb.find_nearest(Vector(p))[3] for p in P[::7]]; rep['lbs_vs_render_mean_cm'] = float(np.mean(dd)); rep['lbs_vs_render_p95_cm'] = float(np.percentile(dd, 95))
    # body collider (posed body + head render meshes)
    BV, BT = load_mesh(os.path.join(CAP, 'posed_geometry', f'{PFX}_{pose}_Body.json.gz'))
    body = make_obj('Body_'+pose, BV, BT); cm = body.modifiers.new('Collision', 'COLLISION'); body.collision.thickness_outer = 0.003; body.collision.cloth_friction = 5.0
    bvh = BVHTree.FromPolygons([Vector(p) for p in bl(BV)], [list(t) for t in BT])
    # cloth object: main panels only
    mid = np.nonzero(main)[0]; remap = -np.ones(len(X), np.int64); remap[mid] = np.arange(len(mid))
    Fm = np.asarray([remap[f] for f in F if main[f].all()])
    # weld UV-seam duplicates (same bind position) so the cloth is one continuous sheet; results are scattered back
    from mathutils import kdtree
    Xm0 = X[mid]; kdw = kdtree.KDTree(len(Xm0))
    for k, q in enumerate(Xm0): kdw.insert(Vector(q), k)
    kdw.balance(); par = list(range(len(Xm0)))
    def root(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for k, q in enumerate(Xm0):
        for (_, j, _) in kdw.find_range(Vector(q), 0.01):
            ri, rj = root(k), root(j)
            if ri != rj: par[max(ri, rj)] = min(ri, rj)
    rts = np.asarray([root(k) for k in range(len(Xm0))]); U, grp = np.unique(rts, return_inverse=True); grp = grp.ravel()
    FmU = grp[Fm]; FmU = FmU[(FmU[:, 0] != FmU[:, 1]) & (FmU[:, 1] != FmU[:, 2]) & (FmU[:, 0] != FmU[:, 2])]
    PU = P[mid][U]
    cl = make_obj('Cloth_'+pose, PU, FmU)
    free = freefn(Xm0[U])
    if gname == 'trousers':   # contact corrective: only cloth close to / inside the posed body is free
        dd_ = np.array([(lambda r: (Vector(bl(PU[k]))-r[0]).dot(r[1])/S if r[0] is not None else 9.0)(bvh.find_nearest(Vector(bl(PU[k])))) for k in range(len(PU))])
        free = free*sstep((2.5-dd_)/1.5)
    pin = 1.0-free
    vg = cl.vertex_groups.new(name='PIN')
    for i, w in enumerate(pin): vg.add([i], float(w), 'REPLACE')
    # pre-push: vertices inside the posed body are moved out along the body normal (+0.35 cm), only in the free region
    me = cl.data; moved = 0
    for i, v in enumerate(me.vertices):
        if free[i] < 0.05: continue
        loc, nrm, idx, dist = bvh.find_nearest(v.co)
        if loc is None: continue
        # BVH built in the Blender frame (y mirrored): UE winding already yields outward normals here
        if (v.co-loc).dot(nrm) < 0.0035: v.co = loc+nrm*0.0035; moved += 1
    me.update()
    REST = os.environ.get('SPH_GC_REST', '0') == '1' and gname == 'henley'
    if REST:   # cloth rest lengths from the bind (unposed) garment: skinning stretch / folds relax toward the sewn shape
        cl.shape_key_add(name='Basis', from_mix=False); kr = cl.shape_key_add(name='REST', from_mix=False); XB = bl(Xm0[U])
        for k in range(len(XB)): kr.data[k].co = Vector(XB[k])
        kr.value = 0.0
    mod = cl.modifiers.new('Cloth', 'CLOTH'); st = mod.settings; cs = mod.collision_settings; pr = PARAMS[gname]
    if REST: st.rest_shape_key = kr
    GR = {kv.split(':')[0]: float(kv.split(':')[1]) for kv in os.environ.get('SPH_GC_GRAV', '').split(',') if ':' in kv}
    if pose in GR: st.effector_weights.gravity = GR[pose]   # art-directed gravity per pose (small neckline opening at 20-30 deg)
    st.quality = 10; st.mass = pr['mass']; st.tension_stiffness = pr['tension']; st.compression_stiffness = pr['tension']*0.5; st.shear_stiffness = pr['shear']; st.bending_stiffness = pr['bend']
    st.air_damping = 3.0; st.vertex_group_mass = 'PIN'; st.pin_stiffness = 1.0; st.bending_model = 'ANGULAR'
    cs.use_collision = True; cs.distance_min = 0.004; cs.collision_quality = 4; cs.use_self_collision = False
    mod.point_cache.frame_start = 1; mod.point_cache.frame_end = frames; sc.frame_start = 1; sc.frame_end = frames
    for f_ in range(1, frames+1): sc.frame_set(f_)
    dg = bpy.context.evaluated_depsgraph_get(); ev = cl.evaluated_get(dg); co = np.zeros(len(ev.data.vertices)*3); ev.data.vertices.foreach_get('co', co)
    Sm = ue(co.reshape(-1, 3)); cl.modifiers.remove(mod); sc.frame_set(1)
    # light relax of the result inside the free region, then blend to the skinned position by the pin weight
    Sm = PU*pin[:, None]+Sm*(1-pin[:, None])
    dmain = (Sm-PU)[grp]; pin = pin[grp]; free = free[grp]; nrm_ = np.linalg.norm(dmain, axis=1); lim = float(os.environ.get('SPH_GC_LIM_H', '3.5')) if gname == 'henley' else 2.5
    dmain = dmain*np.minimum(1.0, lim/np.maximum(nrm_, 1e-6))[:, None]   # clamp (no explosive solver output)
    D = np.zeros_like(X); D[mid] = dmain
    # detail pieces follow their nearest main vertex
    det = np.nonzero(~main)[0]
    if len(det):
        from mathutils import kdtree
        kd = kdtree.KDTree(len(mid))
        for k, p in enumerate(X[mid]): kd.insert(Vector(p), k)
        kd.balance()
        for i in det: D[i] = dmain[kd.find(Vector(X[i]))[1]]
    # posed -> bind space
    Db = np.zeros_like(D)
    for i in np.nonzero(np.linalg.norm(D, axis=1) > 1e-4)[0]:
        try: Db[i] = np.linalg.solve(A[i], D[i])
        except np.linalg.LinAlgError: Db[i] = D[i]
    for c in curves:
        if c.endswith('_l'): wside = sstep((X[:, 0]+1.0)/2.0)
        elif c.endswith('_r'): wside = sstep((1.0-X[:, 0])/2.0)
        else: wside = np.ones(len(X))
        Dc = Db*wside[:, None]; mag = np.linalg.norm(Dc, axis=1); ids = np.nonzero(mag > 0.01)[0]
        out[gname][c] = {str(int(i)): [round(float(v), 5) for v in Dc[i]] for i in ids}
    rep.update({'free_verts': int((free > 0.05).sum()), 'prepush': moved, 'max_posed_delta_cm': float(np.linalg.norm(D, axis=1).max()), 'p95_posed_delta_cm': float(np.percentile(np.linalg.norm(D[mid][free > 0.05], axis=1), 95)) if (free > 0.05).any() else 0.0})
    out['_stats'][pose] = rep; log(pose, gname, curves, json.dumps({k: round(v, 3) if isinstance(v, float) else v for k, v in rep.items()}))
    bpy.data.objects.remove(cl, do_unlink=True); bpy.data.objects.remove(body, do_unlink=True)
json.dump(out, open(OUT, 'w')); log('GCORR_OK', {k: list(v.keys()) for k, v in out.items() if k != '_stats'})
