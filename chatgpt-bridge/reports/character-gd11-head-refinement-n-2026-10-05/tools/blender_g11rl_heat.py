"""GD11 refinement L: displacement HEAT render (op mask / affected area) of a candidate head vs its base: vertex colour = |delta| on a 0..MAXMM mm
ramp (grey 0 -> yellow -> red at MAXMM); views front, q3R, q3L, profR, profL (same cameras as blender_g11rc_clay.py); Workbench vertex-colour shading.
Prints per-region max / mean (mm) for the protected regions. usage: blender -b --factory-startup --python blender_g11rl_heat.py -- <out prefix> <base.npy> <cand.npy> [MAXMM=2.0]"""
import bpy, sys, os, math, numpy as np
from mathutils import Matrix
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology, basis
a = sys.argv[sys.argv.index('--')+1:]; OUT, BASE, CAND = a[0], a[1], a[2]; MAXMM = float(a[3]) if len(a) > 3 else 2.0
A = np.load(BASE)[:24049]; B = np.load(CAND)[:24049]; d = np.linalg.norm(B-A, axis=1)*10; MX = -0.23; x, y, z = A[:, 0]-MX, A[:, 1], A[:, 2]
REG = {'lips/mouth': (np.abs(x) < 2.8) & (z > 152.6) & (z < 157.2) & (y > 12.0), 'nose base/nostrils z<160': (np.abs(x) < 2.6) & (z > 154.6) & (z < 160.0) & (y > 11.8),
       'eyes/lids': (z > 160.6) & (z < 164.6) & (np.abs(x) > 1.2) & (np.abs(x) < 5.4) & (y > 8.0), 'chin/mandible z<154.5': (z < 154.5) & (y > 2.0),
       'cheeks': (z > 151) & (z < 162) & (np.abs(x) > 2.8) & (y > 3) & ~((z > 160.6) & (np.abs(x) < 5.4)), 'ears': (np.abs(A[:, 0]) > 6.9) & (y < 4.6) & (z > 154) & (z < 168), 'skull z>170': z > 170,
       'radix band (edited)': (np.abs(x) < 1.6) & (z > 161.8) & (z < 165.2) & (y > 11.5)}
for k, m in REG.items(): print('HEAT_REGION %-28s n=%5d mean %.3f mm max %.2f mm' % (k, int(m.sum()), float(d[m].mean()) if m.any() else 0, float(d[m].max()) if m.any() else 0))
i = int(np.argmax(d)); print('HEAT_MAX %.2f mm at x=%.2f y=%.2f z=%.2f' % (d[i], A[i, 0], A[i, 1], A[i, 2]))
t = np.clip(d/MAXMM, 0, 1); col = np.stack([0.55+0.45*np.clip(t*2, 0, 1), 0.55+0.45*np.clip(t*2, 0, 1)-0.55*np.clip(t*2-1, 0, 1)*1.0, 0.55-0.55*np.clip(t*2, 0, 1)], 1); col = np.clip(col, 0, 1)
T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('h'); me.from_pydata([tuple(map(float, p)) for p in B], [], [tuple(int(i) for i in tri) for tri in TT]); me.update()
ca = me.color_attributes.new('heat', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.concatenate([col, np.ones((len(col), 1))], 1).ravel().tolist())
ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
cam = bpy.data.cameras.new('c'); cam.type = 'PERSP'; cam.sensor_fit = 'HORIZONTAL'; cam.angle = math.radians(15.0); cam.clip_end = 1000; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = sc.render.resolution_y = 1100; sc.render.resolution_percentage = 100; sc.render.film_transparent = False
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'VERTEX'; sc.display.shading.show_cavity = True; sc.render.image_settings.file_format = 'PNG'
VIEWS = {'front': [0, 125, 159, -90, 0], 'q3R': [-64.468, 113.297, 160.141, -58.0, 1.0], 'q3L': [64.468, 113.297, 160.141, -122.0, 1.0], 'profR': [-125, 3, 160, 0, 0], 'profL': [125, 3, 160, 180, 0]}
for v, c in VIEWS.items():
    o, f, r, u = basis(c); co.matrix_world = Matrix(((r[0], u[0], -f[0], o[0]), (r[1], u[1], -f[1], o[1]), (r[2], u[2], -f[2], o[2]), (0, 0, 0, 1)))
    sc.render.filepath = os.path.abspath(OUT+'_'+v+'.png'); bpy.ops.render.render(write_still=True)
print('HEAT_OK', OUT, 'ramp grey=0 .. yellow=%.1f .. red=%.1f mm' % (MAXMM/2, MAXMM))
