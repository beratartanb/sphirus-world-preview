"""pass XX: signed RELIEF map render: per skin vertex the offset from the Gaussian average of the surface around it along the normal (sigma
cm), large-scale curvature removed (minus a surface-diffused copy) -> red = local ridge / bump, blue = local groove / hollow, grey = smooth;
+-RANGE mm. Close front + close 3/4 cameras (same as the nohair UE captures). usage: blender -b --factory-startup --python
blender_g11xx_reliefmap.py -- <out prefix> <head.npy> [sigma=0.8] [RANGE=2.5]"""
import bpy, sys, os, math, numpy as np
from mathutils import Matrix
from mathutils.kdtree import KDTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology, basis
from id_common import SEG
a = sys.argv[sys.argv.index('--')+1:]; OUT, HP = a[0], a[1]; sig = float(a[2]) if len(a) > 2 else 0.8; RG = float(a[3]) if len(a) > 3 else 2.5
X = np.load(HP)[:24049]; NH = 24049
T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
N = np.zeros_like(X); fn = -np.cross(X[TT[:, 1]]-X[TT[:, 0]], X[TT[:, 2]]-X[TT[:, 0]])
for k in range(3): np.add.at(N, TT[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
if (N[:, 1][X[:, 1] > 12]).mean() < 0: N = -N   # outward
idx = np.where(X[:, 1] > -3)[0]; kd = KDTree(len(idx))
for j, i in enumerate(idx): kd.insert(X[i], j)
kd.balance(); D = np.zeros(NH); val = np.zeros(NH)
for i in idx:
    if X[i, 2] < 147 or X[i, 2] > 168: continue
    hits = kd.find_range(X[i], 3*sig)
    if len(hits) < 8: continue
    P = np.array([h[0] for h in hits]); w = np.exp(-0.5*(np.array([h[2] for h in hits])/sig)**2); avg = (P*w[:, None]).sum(0)/w.sum(); D[i] = float((X[i]-avg)@N[i]); val[i] = 1
E = np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
fw, ww = D*val, val.copy()
for _ in range(120):
    a1 = np.zeros(NH); np.add.at(a1, E[:, 0], fw[E[:, 1]]); a2 = np.zeros(NH); np.add.at(a2, E[:, 0], ww[E[:, 1]]); fw += 0.5*(a1/np.maximum(DEG, 1)-fw); ww += 0.5*(a2/np.maximum(DEG, 1)-ww)
Db = (D-fw/np.maximum(ww, 1e-6))*val*10   # mm
t = np.clip(Db/RG, -1, 1); g = 0.62
col = np.stack([g+(1-g)*np.clip(t, 0, 1)-g*np.clip(-t, 0, 1)*0.8, g-g*np.abs(t)*0.7, g+(1-g)*np.clip(-t, 0, 1)-g*np.clip(t, 0, 1)*0.8], 1); col = np.clip(col, 0, 1)
np.save(OUT+'_relief.npy', Db.astype(np.float32))
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('h'); me.from_pydata([tuple(map(float, p)) for p in X], [], [tuple(int(i) for i in tri) for tri in TT]); me.update()
for p in me.polygons: p.use_smooth = True
ca = me.color_attributes.new('rel', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.concatenate([col, np.ones((len(col), 1))], 1).ravel().tolist())
ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
cam = bpy.data.cameras.new('c'); cam.type = 'PERSP'; cam.sensor_fit = 'HORIZONTAL'; cam.clip_end = 1000; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.resolution_x = sc.render.resolution_y = 900; sc.render.film_transparent = False
sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'VERTEX'; sc.render.image_settings.file_format = 'PNG'
for v, c, fv in (('front', [0, 62, 160.0, -90, 0], 22.0), ('q3', [-42, 42, 158, -45, 0], 24.0)):
    cam.angle = math.radians(fv); o, f, r, u = basis(c); co.matrix_world = Matrix(((r[0], u[0], -f[0], o[0]), (r[1], u[1], -f[1], o[1]), (r[2], u[2], -f[2], o[2]), (0, 0, 0, 1)))
    sc.render.filepath = os.path.abspath(OUT+'_'+v+'.png'); bpy.ops.render.render(write_still=True)
print('RELIEF_OK', OUT, 'p05 %.2f p95 %.2f mm' % (np.percentile(Db[val > 0], 5), np.percentile(Db[val > 0], 95)))
