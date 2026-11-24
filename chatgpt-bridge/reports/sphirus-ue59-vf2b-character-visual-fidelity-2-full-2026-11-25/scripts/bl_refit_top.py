# Blender 5.3: refit the cropped top on the body. Cloth-sim drape of the free lower part (pinned at shoulders/bust), poke repair,
# thin solidify for fabric thickness at hems, skin weights kept. Renders BEFORE/AFTER from the same cameras, exports FBX with the armature.
import bpy, sys, os, math, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; D, OUT = a[0], a[1]; FRAMES = int(a[2]) if len(a) > 2 else 45; PIN_Z = float(a[3]) if len(a) > 3 else 1.31; THICK = float(a[4]) if len(a) > 4 else 0.0022
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(k):
    before = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=os.path.join(D, k + '.fbx'), automatic_bone_orientation=False)
    new = [o for o in bpy.data.objects if o not in before]; return [o for o in new if o.type == 'MESH'][0], [o for o in new if o.type == 'ARMATURE'][0]
body, barm = imp('body'); top, tarm = imp('top')
sc = bpy.context.scene
def render(tag):
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = 700; sc.render.resolution_y = 800
    sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'OBJECT'; sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'BOTH'
    body.color = (0.8, 0.62, 0.52, 1); top.color = (0.55, 0.7, 0.8, 1)
    cam = bpy.data.objects.get('cam')
    if not cam:
        cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); cam.data.type = 'ORTHO'; cam.data.ortho_scale = 0.75
    sc.camera = cam
    for nm, ang in (('front', 0), ('side', 90), ('back', 180), ('q34b', 140)):
        r = math.radians(ang); cam.location = (3 * math.sin(r), -3 * math.cos(r), 1.24); cam.rotation_euler = (math.radians(90), 0, r)
        sc.render.filepath = os.path.join(OUT, 'top_%s_%s.png' % (tag, nm)); bpy.ops.render.render(write_still=True)
def stats(tag):
    bm = bmesh.new(); bm.from_mesh(body.data); bm.transform(body.matrix_world); bm.normal_update(); bvh = BVHTree.FromBMesh(bm)
    rows = {}; poke = 0
    for v in top.data.vertices:
        p = top.matrix_world @ v.co; loc, nrm, _, _ = bvh.find_nearest(p); d = (p - loc).length; ins = (p - loc).dot(nrm) < 0
        poke += 1 if ins else 0; b = round(p.z * 20) / 20; r = rows.setdefault(b, [0, 0.0, 0.0]); r[0] += 1; r[1] += d; r[2] = max(r[2], d)
    print('RF', tag, 'verts', len(top.data.vertices), 'inside_body', poke, ' | '.join('%.2f:%.1f/%.1f' % (b, 100 * rows[b][1] / rows[b][0], 100 * rows[b][2]) for b in sorted(rows, reverse=True)))
    bm.free()
render('before'); stats('before')
# ---- pin group: 1 above PIN_Z, smooth falloff over 6 cm, 0 below
mw = top.matrix_world; pin = top.vertex_groups.new(name='VF2_pin')
zmin = min((mw @ v.co).z for v in top.data.vertices)
for v in top.data.vertices:
    z = (mw @ v.co).z; w = min(1.0, max(0.0, (z - (PIN_Z - 0.06)) / 0.06)); w = w * w * (3 - 2 * w)
    if w > 0: pin.add([v.index], w, 'REPLACE')
# ---- take in the side/back seams: the vendor cut flares outward below the bust; pull the free part toward the body (front least)
TAKE = float(a[5]) if len(a) > 5 else 0.45; TAKE_Z = float(a[6]) if len(a) > 6 else 1.31
bb0 = bmesh.new(); bb0.from_mesh(body.data); bb0.transform(body.matrix_world); bb0.normal_update(); bvh0 = BVHTree.FromBMesh(bb0); inv0 = mw.inverted(); moved = 0
for v in top.data.vertices:
    p = mw @ v.co
    if p.z >= TAKE_Z: continue
    loc, nrm, _, _ = bvh0.find_nearest(p); dv = p - loc; d = dv.length
    if d < 0.014: continue
    t = min(1.0, (TAKE_Z - p.z) / max(1e-4, TAKE_Z - zmin)); t = t * t * (3 - 2 * t); dirn = dv / d
    w = 0.30 + 0.70 * min(1.0, max(0.0, (dirn.y + 0.45) / 1.0))
    nd = max(0.014, d * (1.0 - TAKE * t * w)); v.co = inv0 @ (loc + dirn * nd); moved += 1
bb0.free(); print('RF take-in moved', moved, 'TAKE', TAKE)
orig = [v.co.copy() for v in top.data.vertices]
# ---- cloth sim: body collides, top settles under gravity
bpy.context.view_layer.objects.active = body; col = body.modifiers.new('col', 'COLLISION'); body.collision.thickness_outer = 0.004; body.collision.thickness_inner = 0.01; body.collision.cloth_friction = 12
bpy.context.view_layer.objects.active = top; cm = top.modifiers.new('cloth', 'CLOTH'); cs = cm.settings; cc = cm.collision_settings
cs.quality = 12; cs.mass = 0.18; cs.tension_stiffness = 18; cs.compression_stiffness = 18; cs.shear_stiffness = 6; cs.bending_stiffness = 0.8
cs.tension_damping = 8; cs.compression_damping = 8; cs.shear_damping = 6; cs.bending_damping = 0.6; cs.air_damping = 2.0
cs.vertex_group_mass = 'VF2_pin'; cs.pin_stiffness = 1.0
cc.use_collision = True; cc.collision_quality = 4; cc.distance_min = 0.006; cc.use_self_collision = False
# move the cloth modifier above the armature so it simulates in rest space
while top.modifiers[0].name != 'cloth': bpy.ops.object.modifier_move_up(modifier='cloth')
for m in top.modifiers:
    if m.type == 'ARMATURE': m.show_viewport = False
for m in body.modifiers:
    if m.type == 'ARMATURE': m.show_viewport = False
sc.frame_start = 1; sc.frame_end = FRAMES; cm.point_cache.frame_start = 1; cm.point_cache.frame_end = FRAMES
for f in range(1, FRAMES + 1): sc.frame_set(f)
dg = bpy.context.evaluated_depsgraph_get(); ev = top.evaluated_get(dg); sim = [v.co.copy() for v in ev.data.vertices]
assert len(sim) == len(orig)
top.modifiers.remove(cm); body.modifiers.remove(col)
for i, v in enumerate(top.data.vertices): v.co = sim[i]
# ---- light relax of the simulated region (kills sim jitter, keeps folds), then poke repair to >= 5 mm
bm = bmesh.new(); bm.from_mesh(top.data)
dl = bm.verts.layers.deform.active; gi = pin.index
free = [v for v in bm.verts if v[dl].get(gi, 0.0) < 0.999]
bmesh.ops.smooth_vert(bm, verts=free, factor=0.35, use_axis_x=True, use_axis_y=True, use_axis_z=True)
bm.to_mesh(top.data); bm.free()
bb = bmesh.new(); bb.from_mesh(body.data); bb.transform(body.matrix_world); bb.normal_update(); bvh = BVHTree.FromBMesh(bb); inv = mw.inverted(); fixed = 0
for v in top.data.vertices:
    p = mw @ v.co; loc, nrm, _, _ = bvh.find_nearest(p); s = (p - loc).dot(nrm)
    if s < 0.005: v.co = inv @ (loc + nrm * 0.005 + (p - loc - nrm * s)); fixed += 1
print('RF poke repaired', fixed); bb.free()
stats('draped')
# ---- fabric thickness: solidify inward, even thickness, rim
so = top.modifiers.new('solid', 'SOLIDIFY'); so.thickness = THICK; so.offset = -1.0; so.use_even_offset = True; so.use_rim = True; so.use_quality_normals = True
while top.modifiers[0].name != 'solid': bpy.ops.object.modifier_move_up(modifier='solid')
bpy.ops.object.modifier_apply(modifier='solid')
top.vertex_groups.remove(top.vertex_groups['VF2_pin'])
for p in top.data.polygons: p.use_smooth = True
for m in top.modifiers: m.show_viewport = True
for m in body.modifiers: m.show_viewport = True
# weights sanity
mx = 0; un = 0
for v in top.data.vertices:
    n = len([g for g in v.groups if g.weight > 0.0]); mx = max(mx, n); un += 1 if n == 0 else 0
print('RF weights max influences', mx, 'unweighted', un, 'verts', len(top.data.vertices), 'polys', len(top.data.polygons))
render('after'); stats('after')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'top_refit.blend'))
# ---- export: garment mesh + its armature only
bpy.ops.object.select_all(action='DESELECT'); top.select_set(True); tarm.select_set(True); bpy.context.view_layer.objects.active = tarm
print('RF arm name', tarm.name, 'scale', tuple(round(s, 4) for s in tarm.scale), 'bones', len(tarm.data.bones))
if 'custom_normal' in top.data.attributes: top.data.attributes.remove(top.data.attributes['custom_normal'])
for i, mt in enumerate(top.data.materials):
    if mt: mt.name = 'Slot%d' % i
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, 'retro_top_vf2.fbx'), use_selection=True, object_types={'ARMATURE', 'MESH'}, add_leaf_bones=False, bake_anim=False,
                         primary_bone_axis='Y', secondary_bone_axis='X', mesh_smooth_type='OFF', use_armature_deform_only=False, global_scale=1.0, apply_unit_scale=True,
                         apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y')
print('RF exported', os.path.getsize(os.path.join(OUT, 'retro_top_vf2.fbx')))
