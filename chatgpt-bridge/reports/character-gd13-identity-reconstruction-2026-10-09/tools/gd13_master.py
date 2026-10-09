"""GD13 Identity Master deliverable: opens the GD13 comparison scene (built by gd13_scene.py with GD12 / F1H as extra read-only heads), sets the
editable HEAD to the GD13 geometry and renames it GD13_Head, poses the solved reference cameras (final cameras) and gives each one its reference
panel as a camera background image, saves the .blend, then exports GD13_Head (skin + eyes) as GLB and OBJ.
usage: blender -b <scene_with_extras.blend> --python gd13_master.py -- <GD13.npy> <cams.json> <out.blend> <out.glb> <out.obj> <ref panel dir>"""
import bpy, sys, os, json, math, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import importlib
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); CAMS = a[1]; OUTB, OUTG, OUTO, RD = a[2], a[3], a[4], a[5]
OB = bpy.data.objects
_ej = os.path.join(os.path.dirname(os.path.abspath(OUTB)), '_empty_jobs.json'); open(_ej, 'w').write('[]'); sys.argv = [sys.argv[0], '--', _ej]; import gd13_render; os.remove(_ej)   # pose helper only (empty job list)
gd13_render.pose_cams(CAMS)
ob = OB['HEAD']; me = ob.data; n = len(me.vertices); V = X[:n].copy(); V[:, 0] *= -1; me.vertices.foreach_set('co', (V*0.01).ravel()); me.update()
ob.name = 'GD13_Head'; me.name = 'GD13_Head'; bpy.data.collections['HEAD'].name = 'GD13_MASTER'
for o in bpy.data.collections['COMPARE_READONLY'].objects: o.hide_viewport = True
# pose solved reference cameras (same code as gd13_render.pose_cams) + reference panel backgrounds
for v in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceL'):
    c = OB.get('CAM_REF_'+v)
    if c is None: continue
    img = bpy.data.images.load(os.path.join(RD, f'GD13_REF_panel_{v}.png')); cd = c.data; cd.show_background_images = True; bg = cd.background_images.new(); bg.image = img; bg.alpha = 0.6; bg.frame_method = 'FIT'
ob['gd13_note'] = 'GD13 Identity Master 2026-10-09: F1H + MetaHuman-PCA/multi-view-measured large-form re-proportioning + scripted regional sculpt operators; DNA vertex order kept (33845). Not baked into UE.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUTB)); print('MASTER_SAVED', OUTB)
# export: GD13_Head only (skin + eyes, Blender axes, metres)
for o in bpy.context.scene.objects: o.select_set(False)
ob.hide_set(False); ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.export_scene.gltf(filepath=os.path.abspath(OUTG), use_selection=True, export_format='GLB', export_apply=False)
bpy.ops.wm.obj_export(filepath=os.path.abspath(OUTO), export_selected_objects=True, export_materials=False)
print('EXPORT_OK', OUTG, OUTO)
