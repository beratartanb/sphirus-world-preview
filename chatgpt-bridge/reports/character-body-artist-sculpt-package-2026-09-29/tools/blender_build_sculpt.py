"""Build the SPHIRUS artist-sculpt .blend from sculpt_package.json.gz (Blender 5.2, background).
usage: blender -b --factory-startup --python blender_build_sculpt.py -- <package.json.gz> <out.blend> <tools.py> <readme.md>
Creates exact-topology meshes (vertex order = UE source-model LOD0 ids: body 0..NB-1, head NB..), UVs, material slots,
skin-weight vertex groups, protection/region groups, mask, face sets, reference shape keys, locked-head display,
reference objects, skeleton reference, anatomical guides, measurement rings and sculpt cameras.
No geometry is modified: every shape key is copied from the package."""
import bpy, sys, gzip, json, math, hashlib
import numpy as np
from mathutils import Vector, Quaternion, Matrix

argv = sys.argv[sys.argv.index('--')+1:]
PKG, OUT, TOOLS, README = argv[:4]
P = json.loads(gzip.open(PKG, 'rb').read())
NB, NH = P['NB'], P['NH']; NV = NB+NH
S = 0.01
def bl(p): return (p[0]*S, -p[1]*S, p[2]*S)          # UE cm -> Blender m (handedness flip on Y)
def blv(arr): a = np.asarray(arr, dtype=np.float64); return np.stack([a[:, 0]*S, -a[:, 1]*S, a[:, 2]*S], 1)

# ---------------- clean scene ----------------
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene
sc.unit_settings.system = 'METRIC'; sc.unit_settings.length_unit = 'CENTIMETERS'; sc.unit_settings.scale_length = 1.0
def coll(name, parent=None):
    c = bpy.data.collections.new(name); (parent or sc.collection).children.link(c); return c
C_SCULPT = coll('SPH_SCULPT'); C_REF = coll('SPH_REFERENCE_READONLY'); C_GUIDE = coll('SPH_GUIDES_REFERENCE_ONLY')
C_MEAS = coll('SPH_MEASURE_RINGS'); C_CAM = coll('SPH_CAMERAS'); C_SKEL = coll('SPH_SKELETON_REFERENCE')

# ---------------- topology ----------------
tris = [list(t) for t in P['body']['triangles']] + [[a+NB, b+NB, c+NB] for a, b, c in P['head']['triangles']]
uvs = P['body']['uv'] + P['head']['uv']
mats_body = P['body']['materials']; mats_head = P['head']['materials']
matidx = list(P['body']['material_ids']) + [m+len(mats_body) for m in P['head']['material_ids']]
topo_hash = hashlib.sha256(json.dumps(tris, separators=(',', ':')).encode()).hexdigest()
def make_mesh(name, coords, with_uv=True, with_mats=True):
    me = bpy.data.meshes.new(name)
    me.vertices.add(NV); me.vertices.foreach_set('co', blv(coords).astype(np.float32).ravel())
    nt = len(tris)
    me.loops.add(nt*3); me.loops.foreach_set('vertex_index', np.asarray(tris, dtype=np.int32).ravel())
    me.polygons.add(nt); me.polygons.foreach_set('loop_start', np.arange(0, nt*3, 3, dtype=np.int32))
    me.update(calc_edges=True)
    if with_uv:
        uvl = me.uv_layers.new(name='UVMap')
        a = np.asarray(uvs, dtype=np.float64).reshape(-1, 2); a[:, 1] = 1.0-a[:, 1]
        uvl.data.foreach_set('uv', a.astype(np.float32).ravel())
    if with_mats:
        for n in mats_body+mats_head:
            m = bpy.data.materials.get('SPH_'+n) or bpy.data.materials.new('SPH_'+n)
            m.diffuse_color = (0.72, 0.62, 0.56, 1) if 'shader' in n and ('body' in n or 'head_shader' in n) else (0.35, 0.35, 0.4, 1)
            me.materials.append(m)
        me.polygons.foreach_set('material_index', np.asarray(matidx, dtype=np.int32))
    return me
def check_mesh(me):
    assert len(me.vertices) == NV and len(me.polygons) == len(tris), (len(me.vertices), len(me.polygons))
    lv = np.zeros(len(me.loops), dtype=np.int32); me.loops.foreach_get('vertex_index', lv)
    assert (lv == np.asarray(tris, dtype=np.int32).ravel()).all(), 'loop order changed'

B2 = P['accepted_b2']; BRN = P['br_neutral']
me = make_mesh('SPH_BR_ArtistSculpt_Mesh', B2); check_mesh(me)
ob = bpy.data.objects.new('SPH_BR_ArtistSculpt', me); C_SCULPT.objects.link(ob)

# ---------------- vertex groups: protection + regions first, then skin weights (bone names) ----------------
ORDER = ['FACE_LOCK', 'HEAD_IDENTITY_LOCK', 'SEAM_LOCK', 'NECK_COLLAR', 'SHOULDERS', 'CHEST_RIBCAGE', 'BREASTS', 'ABDOMEN',
         'UPPER_BACK', 'LOWER_BACK', 'PELVIS_HIPS', 'GLUTES', 'THIGHS', 'KNEES', 'CALVES_ANKLES', 'UPPER_ARMS',
         'ELBOWS_FOREARMS', 'HANDS_FEET']
for g in ORDER:
    vg = ob.vertex_groups.new(name=g)
    byw = {}
    for u, w in P['groups'][g].items(): byw.setdefault(float(w), []).append(int(u))
    for w, ids in byw.items(): vg.add(ids, w, 'REPLACE')
    vg.lock_weight = True
bones = {}
for u, wd in enumerate(P['weights']):
    for b, w in wd.items(): bones.setdefault(b, {}).setdefault(float(w), []).append(u)
for b in sorted(bones):
    vg = ob.vertex_groups.new(name=b)
    for w, ids in bones[b].items(): vg.add(ids, w, 'REPLACE')
    vg.lock_weight = True
ob.vertex_groups.active_index = 0

# ---------------- shape keys ----------------
ob.shape_key_add(name='ACCEPTED_B2', from_mix=False)
def add_key(name, coords, value, lock):
    k = ob.shape_key_add(name=name, from_mix=False); k.data.foreach_set('co', blv(coords).astype(np.float32).ravel())
    k.value = value; k.slider_min = 0.0; k.slider_max = 1.0; k.relative_key = me.shape_keys.key_blocks['ACCEPTED_B2']; k.lock_shape = lock
    return k
add_key('BR_NEUTRAL', BRN, 0.0, True)
add_key('SCULPT_BASE', BRN, 0.0, True)
add_key('ARTIST_SCULPT', BRN, 1.0, False)
me.shape_keys.key_blocks['ACCEPTED_B2'].lock_shape = True
me.shape_keys.use_relative = True
ob.active_shape_key_index = list(me.shape_keys.key_blocks.keys()).index('ARTIST_SCULPT')
ob.show_only_shape_key = False; ob.use_shape_key_edit_mode = False

# ---------------- sculpt mask, face sets, hidden locked head ----------------
mask = np.asarray(P['mask'], dtype=np.float32)
at = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); at.data.foreach_set('value', mask)
bk = me.attributes.new('sph_mask_backup', 'FLOAT', 'POINT'); bk.data.foreach_set('value', mask)  # used by Restore Protection
REG = ['NECK_COLLAR', 'SHOULDERS', 'CHEST_RIBCAGE', 'BREASTS', 'ABDOMEN', 'UPPER_BACK', 'LOWER_BACK', 'PELVIS_HIPS', 'GLUTES',
       'THIGHS', 'KNEES', 'CALVES_ANKLES', 'UPPER_ARMS', 'ELBOWS_FOREARMS', 'HANDS_FEET']
FS = {r: i+1 for i, r in enumerate(REG)}; FS['LOCKED_HEAD'] = 100
lab = P['region_label']; hid_v = set(int(u) for u in P['groups']['HEAD_IDENTITY_LOCK'])
fs = np.zeros(len(tris), dtype=np.int32); hide_p = np.zeros(len(tris), dtype=bool)
for t, tri in enumerate(tris):
    if all(v in hid_v for v in tri): fs[t] = FS['LOCKED_HEAD']; hide_p[t] = True; continue
    ls = [lab[v] for v in tri if lab[v]]
    fs[t] = FS[max(set(ls), key=ls.count)] if ls else FS['NECK_COLLAR']
fa = me.attributes.get('.sculpt_face_set') or me.attributes.new('.sculpt_face_set', 'INT', 'FACE'); fa.data.foreach_set('value', fs)
me.polygons.foreach_set('hide', hide_p)
vis = np.zeros(NV, dtype=bool)
for t, tri in enumerate(tris):
    if not hide_p[t]: vis[tri] = True
me.vertices.foreach_set('hide', ~vis)
ed = np.zeros(len(me.edges)*2, dtype=np.int32); me.edges.foreach_get('vertices', ed); ed = ed.reshape(-1, 2)
me.edges.foreach_set('hide', ~(vis[ed[:, 0]] & vis[ed[:, 1]]))
me.use_mirror_x = True; me.use_mirror_y = False; me.use_mirror_z = False; me.use_mirror_topology = False
me.update()

# locked-head display (exact BR geometry of the hidden identity region; not selectable, not part of the export)
hp = [t for t in range(len(tris)) if hide_p[t]]
used = sorted({v for t in hp for v in tris[t]}); remap = {v: i for i, v in enumerate(used)}
hme = bpy.data.meshes.new('SPH_LOCKED_HEAD_DISPLAY_Mesh')
hme.from_pydata([bl(BRN[v]) for v in used], [], [[remap[v] for v in tris[t]] for t in hp])
for n in mats_body+mats_head: hme.materials.append(bpy.data.materials['SPH_'+n])
hme.polygons.foreach_set('material_index', np.asarray([matidx[t] for t in hp], dtype=np.int32))
for p_ in hme.polygons: p_.use_smooth = True
hob = bpy.data.objects.new('SPH_LOCKED_HEAD_DISPLAY', hme); C_SCULPT.objects.link(hob); hob.hide_select = True
for p_ in me.polygons: p_.use_smooth = True

# ---------------- reference objects (read-only) ----------------
for name, co, dx in (('REF_ACCEPTED_B2', B2, -1.0), ('REF_BR_NEUTRAL', BRN, 1.0)):
    rm = make_mesh(name+'_Mesh', co, with_uv=False, with_mats=False)
    for p_ in rm.polygons: p_.use_smooth = True
    ro = bpy.data.objects.new(name, rm); C_REF.objects.link(ro); ro.location.x = dx; ro.hide_select = True
    ro['note'] = 'reference only; offset %+.1f m in X; exact copy of the %s state' % (dx, name[4:])

# ---------------- skeleton reference (mesh bind, from the neutral capture) ----------------
arm = bpy.data.armatures.new('SPH_Body_Bind_Skeleton'); aob = bpy.data.objects.new('SPH_SKELETON_BIND_REF', arm)
C_SKEL.objects.link(aob); bpy.context.view_layer.objects.active = aob
bpy.ops.object.mode_set(mode='EDIT')
bind = P['skeleton']['Body']['bind']; par = P['skeleton']['Body']['parents']; order = P['skeleton']['Body']['order']
kids = {}
for n in order: kids.setdefault(par.get(n), []).append(n)
for n in order:
    d = bind[n]; h = Vector(bl(d['translation'])); q = d['rotation']
    rq = Quaternion((q[3], q[0], q[1], q[2])); xa = rq @ Vector((1, 0, 0)); xa = Vector((xa.x, -xa.y, xa.z))
    ch = [c for c in kids.get(n, []) if (Vector(bl(bind[c]['translation']))-h).length > 0.004]
    L = min((Vector(bl(bind[c]['translation']))-h).length for c in ch) if ch else 0.02
    eb = arm.edit_bones.new(n); eb.head = h; eb.tail = h+xa.normalized()*max(0.005, L)
for n in order:
    if par.get(n) in arm.edit_bones and n in arm.edit_bones: arm.edit_bones[n].parent = arm.edit_bones[par[n]]
bpy.ops.object.mode_set(mode='OBJECT')
aob['bind_matrices_ue_component_cm'] = json.dumps(bind)
aob['note'] = 'Reference only. Joint positions = mesh bind (neutral capture). Rest matrices stored exactly in the custom property; bone rolls are display approximations. NO armature modifier on the sculpt object.'
arm.display_type = 'STICK'; aob.show_in_front = True; aob.hide_select = True; aob.hide_viewport = True

# ---------------- guides ----------------
def mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color = (*rgb, 1); return m
GCOL = {'CLAVICLE': (0.95, 0.85, 0.2), 'SCAPULA': (0.2, 0.8, 0.95), 'COSTAL': (0.95, 0.5, 0.2), 'RIBCAGE': (0.95, 0.5, 0.2),
        'STERNUM': (0.95, 0.95, 0.95), 'LINEA': (0.8, 0.8, 0.8), 'SPINE': (0.8, 0.8, 0.8), 'ILIAC': (0.3, 0.95, 0.4),
        'INGUINAL': (0.3, 0.95, 0.4), 'INFRAMAMMARY': (0.95, 0.4, 0.7), 'GLUTEAL': (0.95, 0.4, 0.7), 'PATELLA': (0.6, 0.5, 0.95),
        'ACHILLES': (0.6, 0.5, 0.95)}
from mathutils.bvhtree import BVHTree
_bv = BVHTree.FromPolygons([Vector(bl(p)) for p in BRN], tris)
def cast(r):
    o = Vector(bl(r['o'])); d = Vector((r['d'][0], -r['d'][1], r['d'][2])).normalized()
    hit, nrm, fi, dist = _bv.ray_cast(o, d, 1.0)
    return None if hit is None else tuple(hit+d*0.0022)
gstat = {}
for name, rays in list(P['guides']['curves'].items()):
    pts = [q for q in (cast(r) for r in rays) if q]
    if len(pts) > 4:  # light smoothing along the curve (display only)
        pts = [pts[0]]+[tuple((Vector(pts[i-1])+Vector(pts[i])*2+Vector(pts[i+1]))/4) for i in range(1, len(pts)-1)]+[pts[-1]]
    gstat[name] = [len(pts), len(rays)]
    if len(pts) < 2: continue
    cu = bpy.data.curves.new('G_'+name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.001
    sp = cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i, p in enumerate(pts): sp.points[i].co = (*p, 1)
    go = bpy.data.objects.new('GUIDE_'+name, cu); C_GUIDE.objects.link(go); go.hide_select = True; go.show_in_front = False
    cu.materials.append(mat('SPH_GUIDE_'+name.split('_')[0], GCOL.get(name.split('_')[0], (1, 1, 0))))
for name, r in P['guides']['points'].items():
    p = cast(r); gstat['LM_'+name] = 1 if p else 0
    if not p: continue
    e = bpy.data.objects.new('LM_'+name, None); e.empty_display_type = 'SPHERE'; e.empty_display_size = 0.008
    e.location = p; e.show_name = True; e.show_in_front = False; e.hide_select = True; C_GUIDE.objects.link(e)
gtxt = bpy.data.objects.new('GUIDES_ARE_APPROXIMATE__DO_NOT_SCULPT_TO_LINES', None); gtxt.location = (0, 0, 1.95)
gtxt.show_name = True; gtxt.hide_select = True; C_GUIDE.objects.link(gtxt)
C_GUIDE.hide_render = True; C_REF.hide_render = True; C_MEAS.hide_render = True; C_SKEL.hide_render = True

# ---------------- measurement rings (start state, for visual drift reference) ----------------
def hull2(pts):
    pts = sorted(set(pts))
    if len(pts) < 3: return pts
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
for k, m in P['measure'].items():
    if 'ids' not in m or len(m['ids']) < 3: continue
    ax = Vector(m['axis']).normalized(); a1 = ax.orthogonal().normalized(); a2 = ax.cross(a1)
    pts = [Vector(BRN[u]) for u in m['ids']]; c = sum(pts, Vector())/len(pts); c0 = c.dot(ax)
    h = hull2([(round((p-c).dot(a1), 5), round((p-c).dot(a2), 5)) for p in pts])
    cu = bpy.data.curves.new('R_'+k, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0008
    sp = cu.splines.new('POLY'); sp.points.add(len(h)-1); sp.use_cyclic_u = True
    for i, (x, y) in enumerate(h):
        w = c+a1*x+a2*y; sp.points[i].co = (*bl(w), 1)
    ro = bpy.data.objects.new('RING_'+k, cu); C_MEAS.objects.link(ro); ro.hide_select = True; ro.show_in_front = True
    cu.materials.append(mat('SPH_RING', (0.1, 0.9, 0.9)))
bpy.context.view_layer.layer_collection.children['SPH_MEASURE_RINGS'].hide_viewport = True
bpy.context.view_layer.layer_collection.children['SPH_SKELETON_REFERENCE'].hide_viewport = True
bpy.context.view_layer.layer_collection.children['SPH_REFERENCE_READONLY'].hide_viewport = True

# ---------------- cameras (character faces -Y, its left side is +X) ----------------
tgt = Vector((0, 0, 0.88)); D = 4.3
CAMS = {'CAM_1_FRONT': (0, -D), 'CAM_2_SIDE_LEFT': (D, 0), 'CAM_3_BACK': (0, D), 'CAM_4_FRONT_3Q_LEFT': (D*0.7071, -D*0.7071),
        'CAM_5_REAR_3Q_RIGHT': (-D*0.7071, D*0.7071)}
for n, (x, y) in CAMS.items():
    cd = bpy.data.cameras.new(n); cd.lens = 70; cd.sensor_width = 36; cd.clip_start = 0.05; cd.clip_end = 50
    co = bpy.data.objects.new(n, cd); co.location = (x, y, 0.95); C_CAM.objects.link(co)
    co.rotation_euler = (tgt-co.location).to_track_quat('-Z', 'Y').to_euler()
sc.camera = bpy.data.objects['CAM_1_FRONT']
sc.render.resolution_x = 1080; sc.render.resolution_y = 1920; sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'MATCAP'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.75, 0.66, 0.6)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'BOTH'
sc.display.shading.curvature_ridge_factor = 0.6; sc.display.shading.curvature_valley_factor = 0.8

# ---------------- sculpt settings ----------------
ts = sc.tool_settings
ts.sculpt.use_symmetry_feather = False
try:
    ups = ts.sculpt.unified_paint_settings
    ups.use_unified_size = True; ups.size = 70; ups.use_unified_strength = True; ups.strength = 0.25
except Exception as e: print('unified settings', e)
for scr in bpy.data.screens:
    for area in scr.areas:
        if area.type != 'VIEW_3D': continue
        for sp in area.spaces:
            if sp.type != 'VIEW_3D': continue
            sh = sp.shading; sh.type = 'SOLID'; sh.light = 'MATCAP'; sh.color_type = 'SINGLE'; sh.single_color = (0.75, 0.66, 0.6)
            sh.show_cavity = True; sh.cavity_type = 'BOTH'; sp.clip_start = 0.01; sp.clip_end = 100
            sp.overlay.show_sculpt_mask = True; sp.overlay.sculpt_mode_mask_opacity = 0.55
            sp.overlay.show_sculpt_face_sets = False; sp.overlay.show_wireframes = False
            r3 = sp.region_3d; r3.view_location = tgt; r3.view_distance = 2.6
            r3.view_rotation = Quaternion((0.7071, 0.7071, 0, 0)); r3.view_perspective = 'PERSP'

# ---------------- metadata + helper texts ----------------
ob['sph_package'] = P['version']; ob['sph_package_sha256'] = hashlib.sha256(json.dumps(P, separators=(',', ':')).encode()).hexdigest()
ob['sph_topology_sha256'] = topo_hash; ob['sph_vertex_count'] = NV; ob['sph_triangle_count'] = len(tris)
ob['sph_body_vertices'] = NB; ob['sph_head_vertices'] = NH
ob['sph_coords'] = P['coords']; ob['sph_validator'] = argv[4]; ob['sph_package_path'] = PKG; ob['sph_sculpt_key'] = 'ARTIST_SCULPT'
for fn, name in ((TOOLS, 'SPH_TOOLS.py'), (README, 'SPH_README_SCULPT_GUIDE.md')):
    t = bpy.data.texts.new(name); t.from_string(open(fn, encoding='utf-8').read())
bpy.data.texts['SPH_TOOLS.py'].use_module = True

# enter sculpt mode on the sculpt object so the file opens ready
for o in bpy.context.view_layer.objects: o.select_set(False)
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.mode_set(mode='SCULPT')
try:
    wm = bpy.data.window_managers[0]
    if wm.windows and 'Sculpting' in bpy.data.workspaces: wm.windows[0].workspace = bpy.data.workspaces['Sculpting']
except Exception as e: print('workspace', e)
check_mesh(me)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print('GUIDES', json.dumps(gstat)); print('BUILD_OK', OUT, 'verts', NV, 'tris', len(tris), 'vgroups', len(ob.vertex_groups), 'keys', list(me.shape_keys.key_blocks.keys()),
      'hidden_polys', int(hide_p.sum()), 'mode', ob.mode)
