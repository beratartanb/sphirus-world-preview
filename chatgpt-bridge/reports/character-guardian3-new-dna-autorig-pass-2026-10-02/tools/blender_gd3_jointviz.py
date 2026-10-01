"""GUARDIAN-3 board 13: orthographic clay (front / side) of P and NEW with their face joints drawn (P archetype-placed joints vs NEW auto-rig joints).
usage: blender -b -P blender_gd3_jointviz.py -- <P head npy> <NEW head npy> <joints_dump.json> <out png>"""
import bpy, sys, os, json, numpy as np
from mathutils import Matrix
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HP, HN, JD, OUT = a; J = json.load(open(JD)); T, MI = head_topology(); TT = T[np.isin(MI, [0, 3, 4, 8])]
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.78, 0.76, 0.74)
sc.render.film_transparent = False; sc.render.resolution_x = sc.render.resolution_y = 700; sc.view_settings.view_transform = 'Standard'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 26
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1][..., :3].copy(); bpy.data.images.remove(im); return x
panels = []
for lab, hp, col in (('P', HP, (1, 0.15, 0.15)), ('NEW', HN, (0.1, 0.9, 0.2))):
    X = np.load(hp)
    for o in list(bpy.data.objects):
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new('h'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.update(); ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
    for view, f, r in (('front', np.array([0, -1.0, 0]), np.array([1.0, 0, 0])), ('side', np.array([1.0, 0, 0]), np.array([0, 1.0, 0]))):
        c = np.array([-0.23, 5.0, 157.0]); o = c-300*f; Xa = -r; Za = -f; u = np.array([0, 0, 1.0])
        cam.matrix_world = Matrix(((Xa[0], u[0], Za[0], o[0]), (Xa[1], u[1], Za[1], o[1]), (Xa[2], u[2], Za[2], o[2]), (0, 0, 0, 1)))
        tmp = os.path.abspath(OUT+'_tmp.png'); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True); img = load(tmp)[:, ::-1].copy()
        s = 700/26.0
        for n, p in J[lab].items():
            if not (n.startswith('FACIAL') or n in ('head', 'neck_02')): continue
            p = np.asarray(p); xi = int(350+s*((p-c)@r)); yi = int(350-s*(p[2]-c[2]))
            big = n in ('FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_C_Jaw', 'head', 'FACIAL_C_NoseTip', 'FACIAL_L_LipCorner', 'FACIAL_R_LipCorner'); rr = 4 if big else 1
            if 0 <= xi < 700 and 0 <= yi < 700: img[max(yi-rr, 0):yi+rr+1, max(xi-rr, 0):xi+rr+1] = col
        panels.append(img)
c = np.concatenate([np.concatenate(panels[:2], 1), np.concatenate(panels[2:], 1)], 0); h, w = c.shape[:2]
rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = c; im = bpy.data.images.new('o', w, h); im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(OUT); im.file_format = 'PNG'; im.save(); print('JOINTVIZ', OUT)
