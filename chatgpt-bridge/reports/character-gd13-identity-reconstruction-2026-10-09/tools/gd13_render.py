"""GD13 renders from the GD13 scene .blend: per job the HEAD positions come from a DNA-order head npy (no save).
jobs json: [{"head": npy, "cam": "CAM_REF_front", "variant": "clay"|"skin", "lights": "A"|"B", "out": png, "scale": 1.0, "alpha": false,
             "cams": optional solved-camera json (re-poses the CAM_REF_* cameras first), "body": true}]
usage: blender -b <scene.blend> --python gd13_render.py -- jobs.json"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import cam_R, CH
a = sys.argv[sys.argv.index('--')+1:]; JOBS = json.load(open(a[0])); sc = bpy.context.scene; OB = bpy.data.objects; COL = bpy.data.collections
PANEL = {'front': (483, 541), 'q3_faceR': (483, 541), 'q3_faceL': (482, 541), 'prof_faceL': (483, 545)}; MM3 = np.diag([-1.0, 1, 1]); S = 0.01
def pose_cams(path):
    for v, c in json.load(open(path)).items():
        ob = OB.get('CAM_REF_'+v)
        if ob is None: continue
        W, Hh = PANEL[v]; R = cam_R(c); Rb = R@MM3; M = Matrix([list(Rb[0]), list(-Rb[1]), list(-Rb[2])]).transposed(); loc = (MM3@CH)*S-c['D']*S*Rb[2]
        ob.matrix_world = Matrix.Translation(Vector(loc))@M.to_4x4(); cb = ob.data; cb.angle = 2*math.atan(Hh/2/c['f']); cb.shift_x = (W/2-c['cx'])/Hh; cb.shift_y = (c['cy']-Hh/2)/Hh
cur = None; curc = None; me = OB['HEAD'].data; n = len(me.vertices)
for j in JOBS:
    if j.get('cams') and j['cams'] != curc: pose_cams(j['cams']); curc = j['cams']
    if j['head'] != cur:
        X = np.load(j['head']); V = X[:n].copy(); V[:, 0] *= -1; me.vertices.foreach_set('co', (V*0.01).ravel()); me.update(); cur = j['head']
    skin = j.get('variant', 'clay') == 'skin'
    for o in [OB['HEAD'], OB['Body_Context']]:
        m = o.data; mi = np.zeros(len(m.polygons), np.int32); m.polygons.foreach_get('material_index', mi); mi[mi < 2] = 1 if skin else 0; m.polygons.foreach_set('material_index', mi); m.update()
    COL['LIGHTS_A'].hide_render = j.get('lights', 'A') != 'A'; COL['LIGHTS_B'].hide_render = j.get('lights', 'A') != 'B'
    OB['Body_Context'].hide_render = not j.get('body', True)
    hm = OB['HEAD'].data; mi = np.zeros(len(hm.polygons), np.int32); hm.polygons.foreach_get('material_index', mi)
    if j.get('alpha') or not j.get('lashes', True): mi[mi == 3] = 3   # lashes stay (thin); alpha silhouette ignores them by threshold
    cam = OB[j['cam']]; sc.camera = cam; W, H = cam['res']; s = j.get('scale', 1.0); sc.render.resolution_x = int(W*s); sc.render.resolution_y = int(H*s); sc.render.resolution_percentage = 100
    sc.render.film_transparent = bool(j.get('alpha', False)); sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA' if j.get('alpha') else 'RGB'
    sc.render.filepath = j['out']; bpy.ops.render.render(write_still=True); print('RENDERED', j['out'])
