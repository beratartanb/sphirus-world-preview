"""GUARDIAN-13 clay close-up renders of the nose base / mouth region (workbench, studio matcap-free flat lighting + cavity) for one or more
DNA-order head npys. Views (UE cm, camera looks at target): nostril (front-low), nose_front, nose_3q (33 deg), nose_side, mouth_front, mouth_3q, mouth_side.
usage: blender -b --factory-startup --python blender_gd13_closeup.py -- <out_prefix> <a.npy> [<b.npy> ...]   -> <out_prefix>_<view>_<i>.png"""
import bpy, sys, os, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
from mathutils import Vector
a = sys.argv[sys.argv.index('--')+1:]; OUT = os.path.abspath(a[0]); HS = a[1:]; T, MI = head_topology(); TT = T[MI == 0]; MX = -0.25
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'
sc.display.shading.single_color = (0.75, 0.74, 0.72); sc.display.shading.show_cavity = False; sc.render.resolution_x = 700; sc.render.resolution_y = 560
sc.display.shading.studio_light = 'Default'
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 85
VIEWS = {  # name: target (UE), azimuth deg (0 = front, + = toward +x side), elevation deg, distance cm, ortho scale
    'nostril': ((MX, 13.6, 158.4), 0, -28, 40, 5.0), 'nose_front': ((MX, 13.5, 159.6), 0, 0, 40, 6.0), 'nose_3q': ((MX, 13.0, 159.2), 33, -4, 40, 6.5),
    'nose_side': ((MX, 13.0, 159.5), 90, 0, 40, 7.0), 'mouth_front': ((MX, 12.8, 155.6), 0, 0, 40, 6.5), 'mouth_3q': ((MX, 12.3, 155.6), 33, -4, 40, 7.0),
    'mouth_side': ((MX, 12.0, 155.6), 90, 0, 40, 7.5)}
def ue2b(p): return Vector((-p[0], p[1], p[2]))   # UE (left-handed) -> Blender
for i, h in enumerate(HS):
    X = np.load(h); me = bpy.data.meshes.new('h%d' % i); me.from_pydata([tuple(ue2b(v)) for v in X[:24049]], [], [tuple(t[::-1]) for t in TT if t.max() < 24049]); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new('h%d' % i, me); sc.collection.objects.link(ob)
    for o in sc.objects:
        if o.type == 'MESH': o.hide_render = (o != ob)
    for v, (tg, az, el, d, osc) in VIEWS.items():
        t = ue2b(tg); azr, elr = math.radians(az), math.radians(el)
        dirv = Vector((-math.sin(azr)*math.cos(elr), math.cos(azr)*math.cos(elr), math.sin(elr)))   # from target toward camera (Blender x = -UE x)
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = osc; cam.location = t+dirv*d
        cam.rotation_euler = (t-cam.location).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = f'{OUT}_{v}_{i}.png'; bpy.ops.render.render(write_still=True)
print('CLOSEUP_OK', len(HS))
