"""GD31 textured soft-light proxy renders (fast stand-in for UE captures when judging nostril openings / crease darkness against the photo).
The GD13 scene is opened read-only (never saved). Per-loop UVs are transferred to the scene HEAD mesh from the head package (triangle match by
vertex set), the skin polygons get a Principled material driven by the baked base-colour texture (black-painted nostrils included), the
GD13 light rigs are hidden and replaced by a large soft area light near each camera plus an even grey world (photo-like soft lighting).
Cameras are re-posed from the solved panel cameras exactly as gd13_render.py does.
usage: blender -b GD13_scene.blend --python gd31_texrender.py -- <texture.png> <cams.json> <jobs json [{head, view, out, scale}]> [light_strength=60] [world=0.35] [engine=CYCLES]"""
import bpy, sys, os, json, math, numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import cam_R, CH
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; TEX, CAMS = a[0], a[1]; JOBS = json.loads(open(a[2]).read()); LS = float(a[3]) if len(a) > 3 else 60.0; WORLD = float(a[4]) if len(a) > 4 else 0.35; ENG = a[5] if len(a) > 5 else 'CYCLES'
sc = bpy.context.scene; OB = bpy.data.objects; COL = bpy.data.collections
PANEL = {'front': (483, 541), 'q3_faceR': (483, 541), 'q3_faceL': (482, 541), 'prof_faceL': (483, 545)}; MM3 = np.diag([-1.0, 1, 1]); S = 0.01
C = json.load(open(CAMS))
def pose(v):
    c = C[v]; ob = OB['CAM_REF_'+v]; W, Hh = PANEL[v]; R = cam_R(c); Rb = R@MM3; M = Matrix([list(Rb[0]), list(-Rb[1]), list(-Rb[2])]).transposed(); loc = (MM3@CH)*S-c['D']*S*Rb[2]
    ob.matrix_world = Matrix.Translation(Vector(loc))@M.to_4x4(); cb = ob.data; cb.angle = 2*math.atan(Hh/2/c['f']); cb.shift_x = (W/2-c['cx'])/Hh; cb.shift_y = (c['cy']-Hh/2)/Hh; return ob
# ---- UV transfer
me = OB['HEAD'].data; P = pkg()['head']; T = np.asarray(P['triangles'], int); UVc = np.asarray(P['uv'], float)
key = {}
for i, t in enumerate(T): key[tuple(sorted(t))] = i
uvl = me.uv_layers.new(name='UV_pkg'); lv = np.zeros(len(me.loops), int); me.loops.foreach_get('vertex_index', lv); out = np.zeros((len(me.loops), 2)); miss = 0
for poly in me.polygons:
    vs = [lv[li] for li in poly.loop_indices]; ti = key.get(tuple(sorted(vs)))
    if ti is None: miss += 1; continue
    for li in poly.loop_indices:
        k = list(T[ti]).index(lv[li]); out[li] = UVc[ti, k]
uvl.data.foreach_set('uv', out.ravel()); me.uv_layers.active = uvl; print('TEXRENDER uv transfer, unmatched polys', miss)
# ---- textured skin material on slots 0/1 (clay / skin)
mat = bpy.data.materials.new('M_GD31_TexSkin'); mat.use_nodes = True; nt = mat.node_tree; bs = nt.nodes['Principled BSDF']
im = nt.nodes.new('ShaderNodeTexImage'); im.image = bpy.data.images.load(TEX); nt.links.new(im.outputs['Color'], bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value = 0.55
for nm, val in (('Subsurface Weight', 0.12), ('Specular IOR Level', 0.35)):
    if nm in bs.inputs: bs.inputs[nm].default_value = val
if 'Subsurface Radius' in bs.inputs: bs.inputs['Subsurface Radius'].default_value = (0.36, 0.14, 0.08)
for o in [OB['HEAD']]:
    m = o.data; m.materials[0] = mat; m.materials[1] = mat
    mi = np.zeros(len(m.polygons), np.int32); m.polygons.foreach_get('material_index', mi); mi[mi < 2] = 1; m.polygons.foreach_set('material_index', mi); m.update()
OB['Body_Context'].hide_render = True
for cn in ('LIGHTS_A', 'LIGHTS_B'):
    if cn in COL: COL[cn].hide_render = True
w = sc.world or bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes.get('Background'); bg.inputs['Color'].default_value = (WORLD, WORLD, WORLD, 1); bg.inputs['Strength'].default_value = 1.0
ld = bpy.data.lights.new('GD31_Soft', 'AREA'); ld.size = 0.9; ld.energy = LS; lo = bpy.data.objects.new('GD31_Soft', ld); sc.collection.objects.link(lo)
sc.render.engine = ENG
if ENG == 'CYCLES': sc.cycles.samples = 48; sc.cycles.use_denoising = True; sc.cycles.device = 'CPU'
cur = None; n = len(me.vertices)
for j in JOBS:
    if j['head'] != cur:
        X = np.load(j['head']); V = X[:n].copy(); V[:, 0] *= -1; me.vertices.foreach_set('co', (V*0.01).ravel()); me.update(); cur = j['head']
    cam = pose(j['view']); sc.camera = cam
    # soft key light: 0.6 m from the head along the camera direction, raised 0.25 m, aimed at the head centre
    cpos = cam.matrix_world.translation; hc = Vector(((MM3@CH)*S).tolist()); dvec = (cpos-hc).normalized(); lpos = hc+dvec*0.6+Vector((0, 0, 0.25))
    lo.location = lpos; lo.rotation_euler = (hc-lpos).to_track_quat('-Z', 'Y').to_euler()
    W, H = cam['res']; s = j.get('scale', 2.0); sc.render.resolution_x = int(W*s); sc.render.resolution_y = int(H*s); sc.render.resolution_percentage = 100
    sc.render.film_transparent = False; sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGB'
    sc.render.filepath = j['out']; bpy.ops.render.render(write_still=True); print('TEXRENDERED', j['out'])
