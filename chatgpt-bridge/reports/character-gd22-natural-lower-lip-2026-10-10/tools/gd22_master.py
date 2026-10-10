"""GD22 Identity Master deliverable (Blender; from the GD14/GD15 version): opens the GD13 render scene (read-only source), sets the editable HEAD to the final
GD22 sculpt geometry (renamed GD22_Head, collection GD22_MASTER), adds hidden read-only comparison heads (GD14 W9, GD22 post-rig, ...) in COMPARE_READONLY, poses the solved
reference cameras with their reference panels as camera backgrounds, stores the brush / landmark programs and the build log as text blocks,
saves the .blend and exports GD22_Head (skin + eyes) as GLB and OBJ.
usage: blender -b <GD13_scene.blend> --python gd22_master.py -- <final.npy> <cams.json> <out.blend> <out.glb> <out.obj> <ref panel dir>
       <compare spec json {name: npy}> <text files json [paths]>"""
import bpy, sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools'))
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); CAMS = a[1]; OUTB, OUTG, OUTO, RD = a[2], a[3], a[4], a[5]; CMP = json.loads(open(a[6]).read()); TXT = json.loads(open(a[7]).read())
OB = bpy.data.objects
_ej = os.path.join(os.path.dirname(os.path.abspath(OUTB)), '_empty_jobs.json'); open(_ej, 'w').write('[]'); sys.argv = [sys.argv[0], '--', _ej]; import gd13_render; os.remove(_ej)
gd13_render.pose_cams(CAMS)
ob = OB['HEAD']; me = ob.data; n = len(me.vertices)
def setco(m, Y): V = Y[:n].copy(); V[:, 0] *= -1; m.vertices.foreach_set('co', (V*0.01).ravel()); m.update()
setco(me, X); ob.name = 'GD22_Head'; me.name = 'GD22_Head'; bpy.data.collections['HEAD'].name = 'GD22_MASTER'
col = bpy.data.collections.new('COMPARE_READONLY'); bpy.context.scene.collection.children.link(col)
for nm, p in CMP.items():
    m2 = me.copy(); m2.name = 'CMP_'+nm; setco(m2, np.load(p)); o2 = bpy.data.objects.new('CMP_'+nm, m2); col.objects.link(o2); o2.hide_viewport = True; o2.hide_render = True; o2['readonly_note'] = 'comparison only - not editable source'
for v in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceL'):
    c = OB.get('CAM_REF_'+v)
    if c is None: continue
    img = bpy.data.images.load(os.path.join(RD, f'GD13_REF_panel_{v}.png')); cd = c.data; cd.show_background_images = True; bg = cd.background_images.new(); bg.image = img; bg.alpha = 0.6; bg.frame_method = 'FIT'
for p in TXT:
    t = bpy.data.texts.new(os.path.basename(p)); t.write(open(p, encoding='utf-8').read())
ob['gd22_note'] = ('GD22 Identity Master 2026-10-10: start GD19 G19 (natural lower lip). User: the lower lip of GD21 was deformed (beak + notch + double-lip crease). GD22 = one full-thickness profile field that moves the lower lip RIGIDLY +1.5 mm (shape kept) and fills the lower-lip body / sulcus +3..+6 mm, upper vermilion +2 mm, infratip +1.3 mm, then a targeted positional rounding of the lip-underside crease. Nose, chin length and width as GD19/GD20. 0 flipped triangles. Final = G22S -> MHC_GD22_G22.')
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUTB)); print('MASTER_SAVED', OUTB)
for o in bpy.context.scene.objects: o.select_set(False)
ob.hide_set(False); ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.export_scene.gltf(filepath=os.path.abspath(OUTG), use_selection=True, export_format='GLB', export_apply=False)
bpy.ops.wm.obj_export(filepath=os.path.abspath(OUTO), export_selected_objects=True, export_materials=False)
print('EXPORT_OK', OUTG, OUTO)
