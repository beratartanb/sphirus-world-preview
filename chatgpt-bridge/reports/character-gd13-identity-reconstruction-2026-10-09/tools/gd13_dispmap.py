"""GD13 deformation maps: HEAD = candidate npy, vertex colours = displacement vs a base npy. Two maps: 'signed' = component along the base
surface normal (red = outward / fuller, blue = inward, +-RANGE mm), 'mag' = full 3D displacement length (black 0 -> yellow RANGE mm).
Rendered with an emission material from the review cameras. usage: blender -b <scene.blend> --python gd13_dispmap.py -- <cand.npy> <base.npy> <out prefix> [range_mm=4]"""
import bpy, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import skin_normals, NS
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); B = np.load(a[1]); OUT = a[2]; RG = float(a[3]) if len(a) > 3 else 4.0
OB = bpy.data.objects; sc = bpy.context.scene; me = OB['HEAD'].data; n = len(me.vertices)
V = X[:n].copy(); V[:, 0] *= -1; me.vertices.foreach_set('co', (V*0.01).ravel()); me.update()
D = (X-B)[:n]*10.0; N = np.zeros((n, 3)); N[:NS] = skin_normals(B)
sd = (D*N).sum(1); mag = np.linalg.norm(D, axis=1)
def cm_signed(v):
    t = np.clip(v/RG, -1, 1); c = np.ones((len(v), 4), np.float32); c[:, :3] = 0.92
    p = t > 0; c[p, 0] = 0.92; c[p, 1] = 0.92*(1-t[p]); c[p, 2] = 0.92*(1-t[p])
    q = t < 0; c[q, 0] = 0.92*(1+t[q]); c[q, 1] = 0.92*(1+t[q]); c[q, 2] = 0.92
    return c
def cm_mag(v):
    t = np.clip(v/RG, 0, 1); c = np.ones((len(v), 4), np.float32); c[:, 0] = np.clip(t*2, 0, 1); c[:, 1] = np.clip(t*2-1, 0, 1)*0.95+0.05*t; c[:, 2] = 0.15*(1-t); return c
for nm, col in (('dsigned', cm_signed(sd)), ('dmag', cm_mag(mag))):
    at = me.color_attributes.get(nm) or me.color_attributes.new(nm, 'FLOAT_COLOR', 'POINT'); at.data.foreach_set('color', col.ravel())
def emat(attr):
    m = bpy.data.materials.new('M_'+attr); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = attr; bs = nt.nodes.new('ShaderNodeBsdfDiffuse'); em = nt.nodes.new('ShaderNodeEmission')
    ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(at.outputs['Color'], bs.inputs['Color']); nt.links.new(at.outputs['Color'], em.inputs['Color']); em.inputs['Strength'].default_value = 0.55
    nt.links.new(bs.outputs[0], ad.inputs[0]); nt.links.new(em.outputs[0], ad.inputs[1]); nt.links.new(ad.outputs[0], o.inputs['Surface']); return m
OB['Body_Context'].hide_render = True; bpy.data.collections['LIGHTS_A'].hide_render = False; bpy.data.collections['LIGHTS_B'].hide_render = True
mi0 = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('material_index', mi0)
for attr in ('dsigned', 'dmag'):
    m = emat(attr); me.materials.append(m); k = len(me.materials)-1; mi = np.where(mi0 == 2, 2, k).astype(np.int32); me.polygons.foreach_set('material_index', mi); me.update()
    for cam in ('CAM_front', 'CAM_q3R', 'CAM_q3L', 'CAM_profL'):
        c = OB[cam]; sc.camera = c; W, H = c['res']; sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.film_transparent = False
        sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'; sc.render.filepath = f'{OUT}_{attr}_{cam[4:]}.png'; bpy.ops.render.render(write_still=True); print('RENDERED', sc.render.filepath)
print('DISPMAP_OK', 'signed range +-%.1f mm' % RG, 'max |d| %.2f mm' % mag[:NS].max())
