"""GD11 head refinement C: whole-head clay renders (no crop, no clipping) of DNA-order head npys for A/B judgement.
Views (UE cm cameras [x, y, z, yaw, pitch], fov 15, 125 cm): front, q3R / q3L (32 deg yaw, pitch 1 = refinement-B matched 3/4), profR (camera
at -x, face points right in the image), profL (camera at +x, mirrored so the face also points right), top3q (looking down at the brow/forehead),
low3q (from below: nostrils / lips). Light: studio + cavity, and a 'graze' pass (side key, flat) for planes.
usage: blender -b --factory-startup --python blender_g11rc_clay.py -- <out_dir> <head1.npy> [<head2.npy> ...]   env VIEWS=front,q3R,...  RES=1100"""
import bpy, sys, os, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology, basis
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEADS = a[0], a[1:]; os.makedirs(OUT, exist_ok=True)
RS = int(os.environ.get('RES', '1100'))
CAMS = {'front': [0, 125, 160, -90, 0], 'q3R': [-66.2, 106.0, 161.5, -58.0, 1.0], 'q3L': [66.2, 106.0, 161.5, -122.0, 1.0],
        'profR': [-125, 3, 160, 0, 0], 'profL': [125, 3, 160, 180, 0], 'top3q': [-16.6, 57.6, 188.8, -70, -28], 'low3q': [-17.6, 50.3, 140.1, -65, 22],
        'nose': [-20.0, 48.1, 163.1, -60, -3], 'lips': [-24, 60, 154.5, -68, 3], 'chinF': [0, 52, 153.0, -90, 0], 'chinQ': [-20.0, 46.6, 153.0, -60, 0], 'cheekQ': [-30.0, 42.0, 159.5, -50, 0]}
FOV = {'nose': 15, 'lips': 15, 'chinF': 14, 'chinQ': 14, 'cheekQ': 16}
VW = [v for v in os.environ.get('VIEWS', 'front,q3R,q3L,profR,profL').split(',') if v]
T, MI = head_topology(); TT = T[np.isin(MI, [0, 3, 4, 8])]
sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.78, 0.76, 0.74)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'WORLD'; sc.render.film_transparent = False; sc.render.resolution_x = sc.render.resolution_y = RS
sc.display.shading.studiolight_rotate_z = __import__('math').radians(float(os.environ.get('ROTZ', '0'))); sc.view_settings.view_transform = 'Standard'; sc.world = sc.world or bpy.data.worlds.new('w'); sc.display.shading.background_type = 'VIEWPORT' if hasattr(sc.display.shading, 'background_type') else None
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.sensor_fit = 'HORIZONTAL'
from mathutils import Matrix
def set_cam(c, fov):
    o, f, r, u = basis(c); X = -r; Y = u; Z = -f
    cam.matrix_world = Matrix(((X[0], Y[0], Z[0], o[0]), (X[1], Y[1], Z[1], o[1]), (X[2], Y[2], Z[2], o[2]), (0, 0, 0, 1))); cam.data.angle = math.radians(fov)
def light(mode):
    s = sc.display.shading
    if mode == 'studio': s.light = 'STUDIO'
    else:
        s.light = 'FLAT' if False else 'STUDIO'
        try: s.studio_light = 'rim.sl' if mode == 'graze' else s.studio_light
        except Exception: pass
for hp in HEADS:
    X = np.load(hp); me = bpy.data.meshes.new('h'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.validate(); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob); tag = os.path.basename(hp).replace('.npy', '')
    for v in VW:
        set_cam(CAMS[v], FOV.get(v, 15.0)); p = os.path.abspath(os.path.join(OUT, f'{tag}_{v}.png')); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        # mirror back (UE left-handed basis renders mirrored); profL is additionally mirrored so its face points right like profR
        im = bpy.data.images.load(p); w, h = im.size; px = np.asarray(im.pixels[:], np.float32).reshape(h, w, 4)
        px = px[:, ::-1] if v != 'profL' else px
        im.pixels.foreach_set(np.ascontiguousarray(px).ravel()); im.save(); bpy.data.images.remove(im)
    bpy.data.objects.remove(ob, do_unlink=True)
print('CLAY_OK', len(HEADS), VW)
