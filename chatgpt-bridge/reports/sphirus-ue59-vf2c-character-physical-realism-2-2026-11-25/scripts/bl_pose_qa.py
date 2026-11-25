# Blender 5.3 (background): deformation / penetration matrix for the real gameplay poses recorded by pose_rec.py.
# Linear-blend skinning is done here with the recorded component-space bone transforms (delta from the reference pose), so the
# result is the same skinned shape the game shows for body, top and shorts. For every pose: garment vertices under the visible skin
# (count, deepest, where) and skin stretch at shoulder / elbow / hip / knee (edge-length ratio p99). Optional --fix writes a
# refitted garment FBX in which the worst offenders are pushed out in the REST pose.
import bpy, sys, os, json, math, numpy as np, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; FBX, POSE, OUT = a[0], a[1], a[2]; GARMENTS = a[3].split(','); FIX = len(a) > 4 and a[4] == 'fix'
P = json.load(open(POSE)); REF = P['ref']
def mat(t):
    x, y, z, qx, qy, qz, qw, s = t; n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw) or 1.0; qx, qy, qz, qw = qx / n, qy / n, qz / n, qw / n
    R = np.array([[1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)], [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)], [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)]])
    M = np.eye(4); M[:3, :3] = R * s; M[:3, 3] = (x, y, z); return M
REFM = {n: mat(t) for n, t in REF.items()}; REFI = {n: np.linalg.inv(m) for n, m in REFM.items()}
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(path):
    before = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
    new = [o for o in bpy.data.objects if o not in before]; m = [o for o in new if o.type == 'MESH'][0]; arm = [o for o in new if o.type == 'ARMATURE'][0]
    co = np.array([(m.matrix_world @ v.co)[:] for v in m.data.vertices]) * 100.0; co[:, 1] *= -1.0     # Blender m -> UE cm (FBX flips Y)
    gn = [g.name for g in m.vertex_groups]; W = np.zeros((len(co), 8)); Ix = np.zeros((len(co), 8), dtype=int)
    for v in m.data.vertices:
        gs = sorted(((g.weight, g.group) for g in v.groups if g.weight > 0), reverse=True)[:8]; tot = sum(w for w, _ in gs) or 1.0
        for k, (w, gi) in enumerate(gs): W[v.index, k] = w / tot; Ix[v.index, k] = gi
    tris = [tuple(reversed(p.vertices[:])) for p in m.data.polygons]; edges = np.array([e.vertices[:] for e in m.data.edges])   # Y flip mirrors the mesh: reversed winding keeps normals outward
    return dict(obj=m, arm=arm, co=co, gn=gn, W=W, Ix=Ix, polys=tris, edges=edges)
body = load(os.path.join(FBX, 'body.fbx')); G = {os.path.splitext(os.path.basename(p))[0]: load(p) for p in GARMENTS}
# keep only the VISIBLE skin: the body material hides everything under the outfit with a UV mask (T_Sph_Mask_Home, white = visible)
ALLP = list(body['polys'])
MASKP = os.path.join(OUT, 'T_Sph_Mask_Home.png')
if os.path.exists(MASKP):
    img = bpy.data.images.load(MASKP); Wd, Ht = img.size; px = np.array(img.pixels[:]).reshape(Ht, Wd, img.channels)[:, :, 0]
    me = body['obj'].data; uvl = me.uv_layers.active.data; keep = []
    for pi, p in enumerate(me.polygons):
        uvc = np.mean([uvl[li].uv[:] for li in p.loop_indices], axis=0); x = min(Wd - 1, max(0, int((uvc[0] % 1.0) * Wd))); y = min(Ht - 1, max(0, int((uvc[1] % 1.0) * Ht)))
        if px[y, x] > 0.5: keep.append(pi)
    print('PQ body polygons visible through the outfit mask: %d of %d' % (len(keep), len(me.polygons))); body['polys'] = [body['polys'][i] for i in keep]
else: print('PQ no mask file: all body polygons used')
# The skeleton asset's reference pose is the generic MetaHuman one; this character's mesh has its own joint positions (up to 15 cm
# apart). Reference matrices therefore take ROTATION from the skeleton reference pose and TRANSLATION from the mesh armature (FBX rest).
arm = body['arm']; errs = []; dots = []
for b in arm.data.bones:
    if b.name not in REFM: continue
    h = arm.matrix_world @ b.head_local; ue = np.array([h.x * 100, -h.y * 100, h.z * 100]); errs.append(float(np.linalg.norm(ue - REFM[b.name][:3, 3]))); REFM[b.name][:3, 3] = ue
for b, c in (('upperarm_l', 'lowerarm_l'), ('lowerarm_r', 'hand_r'), ('thigh_l', 'calf_l'), ('calf_r', 'foot_r'), ('spine_03', 'spine_04')):
    d = REFM[c][:3, 3] - REFM[b][:3, 3]; d /= np.linalg.norm(d); dots.append(round(float(abs(d @ REFM[b][:3, 0])), 3))
print('PQ skeleton-vs-mesh joint offset cm: max %.1f mean %.1f | bone X axis along mesh bone direction (1 = same orientation):' % (max(errs), sum(errs) / len(errs)), dots)
assert min(dots) > 0.97, 'rotation convention mismatch'
REFI = {n: np.linalg.inv(m) for n, m in REFM.items()}
def skin(M, D):
    Ds = np.stack([D.get(n, np.eye(4)) for n in M['gn']]); co4 = np.concatenate([M['co'], np.ones((len(M['co']), 1))], axis=1)
    out = np.zeros((len(co4), 3))
    for k in range(8):
        w = M['W'][:, k:k + 1]
        if not w.any(): break
        out += w * np.einsum('nij,nj->ni', Ds[M['Ix'][:, k]], co4)[:, :3]
    return out
def edge_len(M, co): return np.linalg.norm(co[M['edges'][:, 0]] - co[M['edges'][:, 1]], axis=1)
rest_e = edge_len(body, body['co'])
REG = {'shoulder': ('upperarm_l', 14.0), 'elbow': ('lowerarm_l', 9.0), 'hip': ('thigh_l', 13.0), 'knee': ('calf_l', 10.0), 'neck': ('neck_01', 8.0)}
emid = (body['co'][body['edges'][:, 0]] + body['co'][body['edges'][:, 1]]) / 2
REGI = {k: np.where(np.linalg.norm(emid - REFM[b][:3, 3], axis=1) < r)[0] for k, (b, r) in REG.items()}
rows = []; worst = {k: np.zeros(len(body['co'])) for k in G}
VISV = sorted({v for pl in body['polys'] for v in pl}); VTRI = [(pl[0], pl[i], pl[i + 1]) for pl in body['polys'] for i in range(1, len(pl) - 1)]
print('PQ visible skin vertices', len(VISV), 'triangles', len(VTRI))
for s in P['samples']:
    D = {n: mat(t) @ REFI[n] for n, t in s['bones'].items() if n in REFI}
    bc = skin(body, D); bvh = BVHTree.FromPolygons([Vector(v) for v in bc], body['polys'], all_triangles=False)
    row = {'pose': '%s_%d' % (s['label'], s['k']), 'speed': s['speed']}
    e = edge_len(body, bc) / np.maximum(rest_e, 1e-6)
    for k, idx in REGI.items(): row['stretch_' + k] = round(float(np.percentile(np.abs(e[idx] - 1.0), 99)), 3) if len(idx) else None
    # skin-through-cloth test from the VISIBLE skin side: a skin vertex pokes through when the garment surface lies UNDER it
    # (ray from the vertex along the inward normal hits the garment within 3 cm). Open garment hems make an inside/outside test unreliable.
    bvh_all = BVHTree.FromPolygons([Vector(v) for v in bc], ALLP, all_triangles=False)
    vn = np.zeros_like(bc)
    for t in VTRI: 
        n = np.cross(bc[t[1]] - bc[t[0]], bc[t[2]] - bc[t[0]]); vn[t[0]] += n; vn[t[1]] += n; vn[t[2]] += n
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-9)
    for gk, g in G.items():
        gc = skin(g, D); gb = BVHTree.FromPolygons([Vector(v) for v in gc], g['polys'], all_triangles=False); n_in = 0; deep = 0.0; zs = []
        for vi in VISV:
            o = Vector(bc[vi] - vn[vi] * 0.03); hit = gb.ray_cast(o, Vector(-vn[vi]), 3.0)
            if hit[0] is not None and hit[3] > 0.08:
                ex = bvh_all.ray_cast(o, Vector(-vn[vi]), 3.2)     # thin parts (fingers, wrist): the ray leaves the body before it reaches cloth on the far side
                if ex[0] is not None and ex[3] < hit[3]: continue
                n_in += 1; deep = max(deep, hit[3]); zs.append(body['co'][vi, 2]); worst[gk][vi] = max(worst[gk][vi], hit[3])
        row[gk + '_in'] = n_in; row[gk + '_deep_cm'] = round(deep, 2); row[gk + '_z'] = (round(min(zs)), round(max(zs))) if zs else None
    rows.append(row)
json.dump(rows, open(os.path.join(OUT, 'pose_qa.json'), 'w'), indent=1)
gk = list(G.keys())
print('PQ pose                 speed | ' + ' | '.join('%s: skin verts through / deepest cm' % k[:14] for k in gk) + ' | stretch p99: shoulder elbow hip knee neck')
for r in rows:
    print('PQ %-20s %5.0f | ' % (r['pose'], r['speed']) + ' | '.join('%5d /%5.2f' % (r[k + '_in'], r[k + '_deep_cm']) for k in gk) + ' | ' + ' '.join('%.2f' % (r['stretch_' + k] or 0) for k in REG))
for k in gk:
    w = worst[k]; z = body['co'][:, 2]; hot = w > 0.3
    print('PQ worst-case over all poses', k, 'skin verts ever through the cloth', int((w > 0.08).sum()), 'deepest %.2f cm' % w.max(), '| >0.3 cm:', int(hot.sum()), '| >1 cm:', int((w > 1.0).sum()), '| height band of >0.3 cm (rest z cm):', (round(float(z[hot].min())), round(float(z[hot].max()))) if hot.any() else None)
    np.save(os.path.join(OUT, 'worst_skin_' + k + '.npy'), w)
