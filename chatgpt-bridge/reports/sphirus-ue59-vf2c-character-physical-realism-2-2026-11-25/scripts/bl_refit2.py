# Blender 5.3 (background): take in the SIDE ease of a garment where the swinging forearm / hand passes (pose matrix finding).
# For every vertex whose nearest-body direction is mostly lateral (|dir.x| large) inside a height band, the gap to the body is scaled
# (never below a minimum); a light relax follows and anything closer than 4 mm to the skin is pushed out. Skin weights are kept.
# args: body.fbx garment.fbx out.fbx zmin zmax scale min_gap_m [lat]
import bpy, sys, os, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; BODY, SRC, OUT = a[0], a[1], a[2]; ZMIN, ZMAX, SC, MING = float(a[3]), float(a[4]), float(a[5]), float(a[6]); LAT = float(a[7]) if len(a) > 7 else 0.55
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(p):
    before = set(bpy.data.objects); bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=False, primary_bone_axis='Y', secondary_bone_axis='X')
    new = [o for o in bpy.data.objects if o not in before]; return [o for o in new if o.type == 'MESH'][0], [o for o in new if o.type == 'ARMATURE'][0]
body, barm = imp(BODY); g, garm = imp(SRC)
bb = bmesh.new(); bb.from_mesh(body.data); bb.transform(body.matrix_world); bb.normal_update(); bvh = BVHTree.FromBMesh(bb)
mw = g.matrix_world; inv = mw.inverted(); moved = 0; before = []; after = []
bm = bmesh.new(); bm.from_mesh(g.data); sel = []
for v in bm.verts:
    p = mw @ v.co
    if not (ZMIN <= p.z <= ZMAX): continue
    loc, nrm, _, _ = bvh.find_nearest(p); dv = p - loc; d = dv.length
    if d < MING: continue
    dirn = dv / d; w = min(1.0, max(0.0, (abs(dirn.x) - LAT) / (1.0 - LAT)))
    if w <= 0: continue
    edge = min(1.0, (p.z - ZMIN) / 0.04, (ZMAX - p.z) / 0.04); w *= max(0.0, edge)           # fade at the band ends
    nd = max(MING, d * (1.0 - (1.0 - SC) * w)); before.append(d); after.append(nd); v.co = inv @ (loc + dirn * nd); moved += 1; sel.append(v)
if sel: bmesh.ops.smooth_vert(bm, verts=sel, factor=0.3, use_axis_x=True, use_axis_y=True, use_axis_z=True)
fixed = 0
for v in bm.verts:
    p = mw @ v.co; loc, nrm, _, _ = bvh.find_nearest(p); s = (p - loc).dot(nrm)
    if s < 0.004 and (p - loc).length < 0.03: v.co = inv @ (loc + nrm * 0.004 + (p - loc - nrm * s)); fixed += 1
bm.to_mesh(g.data); bm.free(); bb.free()
print('RF2', os.path.basename(SRC), 'moved', moved, 'mean side gap cm %.1f -> %.1f' % (100 * sum(before) / max(1, len(before)), 100 * sum(after) / max(1, len(after))), 'pushed out', fixed, 'verts', len(g.data.vertices))
if 'custom_normal' in g.data.attributes: g.data.attributes.remove(g.data.attributes['custom_normal'])
for i, mt in enumerate(g.data.materials):
    if mt: mt.name = 'Slot%d' % i
bpy.ops.object.select_all(action='DESELECT'); g.select_set(True); garm.select_set(True); bpy.context.view_layer.objects.active = garm
bpy.ops.export_scene.fbx(filepath=OUT, use_selection=True, object_types={'ARMATURE', 'MESH'}, add_leaf_bones=False, bake_anim=False, primary_bone_axis='Y', secondary_bone_axis='X', mesh_smooth_type='OFF',
                         use_armature_deform_only=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y')
print('RF2 exported', OUT, os.path.getsize(OUT))
