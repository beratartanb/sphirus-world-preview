"""Workbench preview renders of the built outfit .blend (5 views + close-ups). blender -b <blend> --python this.py -- <out_dir>"""
import bpy, sys, os, math
from mathutils import Vector
out = sys.argv[sys.argv.index('--')+1]; os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
for o in bpy.data.objects:
    if o.type == 'MESH': o.hide_render = False
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = 900; sc.render.resolution_y = 1600; sc.render.image_settings.file_format = 'PNG'
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.show_shadows = True; sh.shadow_intensity = 0.4
sc.display.shading.curvature_ridge_factor = 0.5; sc.display.shading.curvature_valley_factor = 1.0
world = bpy.data.worlds.get('World') or bpy.data.worlds.new('World'); sc.world = world; world.color = (0.32, 0.32, 0.33)
def cam(name, loc, tgt, lens=70):
    cd = bpy.data.cameras.new(name); cd.lens = lens; co = bpy.data.objects.new(name, cd); sc.collection.objects.link(co)
    co.location = loc; co.rotation_euler = (Vector(tgt)-Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return co
D = 4.3; t = (0, 0, 0.88)
views = {'01_front': ((0, -D, 0.95), t, 70), '02_side': ((D, 0, 0.95), t, 70), '03_back': ((0, D, 0.95), t, 70), '04_front3q': ((D*0.7, -D*0.7, 0.95), t, 70), '05_rear3q': ((-D*0.7, D*0.7, 0.95), t, 70),
         '06_cu_neckline': ((0.2, -1.5, 1.36), (0, 0, 1.33), 120), '07_cu_chest': ((0.4, -1.6, 1.22), (0, 0, 1.2), 110), '08_cu_shoulder_armpit': ((1.1, -1.2, 1.32), (0.17, 0, 1.28), 110),
         '09_cu_waist_tuck': ((0.3, -1.6, 1.0), (0, 0, 0.99), 110), '10_cu_waistband_drawstring': ((0.0, -1.3, 1.02), (0, 0, 1.0), 130), '11_cu_crotch_hip': ((0.5, -1.8, 0.85), (0, 0, 0.84), 100),
         '12_cu_knee': ((0.6, -1.5, 0.5), (0.1, 0, 0.5), 110), '13_cu_hem': ((0.5, -1.4, 0.12), (0.1, 0, 0.1), 110), '14_cu_back_waist': ((0.3, 1.6, 1.0), (0, 0, 0.97), 110), '15_cu_sleeve_elbow': ((1.3, -1.2, 1.15), (0.33, 0, 1.15), 110)}
for name, (loc, tgt, lens) in views.items():
    c = cam('CAM_'+name, loc, tgt, lens); sc.camera = c; sc.render.filepath = os.path.join(out, name+'.png'); bpy.ops.render.render(write_still=True); print('rendered', name)
