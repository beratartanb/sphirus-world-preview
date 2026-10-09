"""GD12 deformation map: colours GD12_Head by the signed displacement F1H -> GD12 along the F1H normal (red = out / fuller, blue = in, white = 0,
+-RANGE mm) and renders the given cameras. usage: blender -b master.blend --python blender_gd12_dispmap.py -- <F1H.npy> <GD12.npy> <out prefix> <RANGE_mm> <cam>..."""
import bpy, sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; A = np.load(a[0]); X = np.load(a[1]); OUT = a[2]; RG = float(a[3]); NH = 24049
T = np.asarray(pkg()['head']['triangles']); T3 = T[(T < NH).all(1)]; H = A[:NH]; N = np.zeros_like(H); fn = -np.cross(H[T3[:, 1]]-H[T3[:, 0]], H[T3[:, 2]]-H[T3[:, 0]])
for k in range(3): np.add.at(N, T3[:, k], fn)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
if (N[H[:, 1] > 12, 1]).mean() < 0: N = -N
dn = np.zeros(len(A)); dn[:NH] = ((X[:NH]-H)*N).sum(1)*10; t = np.clip(dn/RG, -1, 1)
col = np.ones((len(A), 4), np.float32); col[:, 0] = np.where(t < 0, 1+t, 1); col[:, 1] = 1-np.abs(t)*0.85; col[:, 2] = np.where(t > 0, 1-t, 1)
ob = bpy.data.objects['GD12_Head']; me = ob.data; V = X[:len(me.vertices)].copy(); V[:, 0] *= -1; me.vertices.foreach_set('co', (V*0.01).ravel())
at = me.color_attributes.get('disp') or me.color_attributes.new('disp', 'FLOAT_COLOR', 'POINT'); at.data.foreach_set('color', col.ravel()); me.update()
m = bpy.data.materials.new('M_Disp'); m.use_nodes = True; nt = m.node_tree; bs = nt.nodes['Principled BSDF']; an = nt.nodes.new('ShaderNodeAttribute'); an.attribute_name = 'disp'
nt.links.new(an.outputs['Color'], bs.inputs['Base Color']); bs.inputs['Roughness'].default_value = 0.7
me.materials.append(m); idx = len(me.materials)-1; mi = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', mi); mi[mi != 2] = idx; me.polygons.foreach_set('material_index', mi)
sc = bpy.context.scene; bpy.data.collections['COMPARE_READONLY'].hide_render = True; bpy.data.collections['LIGHTS_A'].hide_render = False; bpy.data.collections['LIGHTS_B'].hide_render = True
for c in a[4:]:
    cam = bpy.data.objects[c]; sc.camera = cam; sc.render.resolution_x, sc.render.resolution_y = cam['res']; sc.render.filepath = '%s_%s.png' % (OUT, c); bpy.ops.render.render(write_still=True); print('DISP', c)
