"""GD11 head refinement: Blender clay preview of package-topology heads (skin only) under fixed cameras and raking light.
usage: blender -b --factory-startup --python gd11r_preview.py -- <out_prefix> <head1.npy> [head2.npy ...]
writes <out_prefix>_<i>_<view>.png ; views: front, q3R, q3L, profR, profL, cheekR, cheekL, nose3qR, nose3qL, noseBelow, mouth"""
import bpy, sys, os, math, numpy as np
from mathutils import Vector
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; HEADS = a[1:]; VIEWS = os.environ.get('G11R_VIEWS', 'front,q3R,q3L,profR,profL,cheekR,cheekL,nose3qR,nose3qL,noseBelow,mouth').split(',')
NH = 24049; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
for eng in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
    try: sc.render.engine = eng; break
    except Exception: pass
sc.render.resolution_x = sc.render.resolution_y = 900; sc.view_settings.view_transform = 'AgX'
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.18, 0.18, 0.18, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
m = bpy.data.materials.new('clay'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.32, 0.32, 0.32, 1); b.inputs['Roughness'].default_value = 0.55
S = 0.01; C0 = np.array([-0.23, 10.0, 158.5])            # UE cm (x, y forward, z up) -> Blender m with face toward -Y
def tob(p): p = np.asarray(p, float); return np.stack([p[..., 0]-C0[0], -(p[..., 1]-C0[1]), p[..., 2]-C0[2]], -1)*S
def light(name, loc, energy, size):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.size = size; ob = bpy.data.objects.new(name, ld); sc.collection.objects.link(ob)
    ob.location = Vector(loc); ob.rotation_euler = (Vector((0, 0, 0))-Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
light('key', (-0.8, -1.0, 0.7), 60, 1.2); light('fill', (1.0, -0.8, 0.0), 14, 1.6); light('rake', (0.9, 0.15, 0.25), 28, 0.4)
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam; cd.lens = 100; cd.clip_start = 0.05
# view: (yaw deg, pitch deg, target UE cm (x, y, z), half frame width m)
CAMS = {'front': (0, 0, (-0.23, 10.0, 159.5), 0.13), 'q3R': (-40, 0, (-0.23, 10.0, 159.5), 0.13), 'q3L': (40, 0, (-0.23, 10.0, 159.5), 0.13), 'profR': (-90, 0, (-0.23, 8.0, 159.5), 0.13), 'profL': (90, 0, (-0.23, 8.0, 159.5), 0.13),
        'cheekR': (-55, 0, (-4.0, 9.0, 157.5), 0.055), 'cheekL': (55, 0, (3.6, 9.0, 157.5), 0.055), 'nose3qR': (-45, 0, (-0.6, 12.5, 158.6), 0.03), 'nose3qL': (45, 0, (0.2, 12.5, 158.6), 0.03),
        'noseBelow': (0, -28, (-0.23, 12.5, 158.2), 0.03), 'mouth': (0, 0, (-0.23, 11.5, 155.4), 0.035), 'eyes': (0, 0, (-0.23, 10.5, 162.3), 0.05)}
for hi, hp in enumerate(HEADS):
    V = np.load(hp)[:NH]; me = bpy.data.meshes.new('h%d' % hi); me.from_pydata(tob(V).tolist(), [], TT.tolist()); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new('h%d' % hi, me); sc.collection.objects.link(ob); me.materials.append(m)
    for o in sc.objects:
        if o.type == 'MESH': o.hide_render = (o != ob)
    for v in VIEWS:
        yaw, pitch, tg, half = CAMS[v]; D = half*2/(36/100.0); r, pr = math.radians(yaw), math.radians(pitch)
        tgt = Vector(tob(np.array(tg)).tolist()); loc = tgt+Vector((D*math.sin(r)*math.cos(pr), -D*math.cos(r)*math.cos(pr), D*math.sin(pr)))
        cam.location = loc; cam.rotation_euler = (tgt-loc).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = '%s_%d_%s.png' % (OUT, hi, v); bpy.ops.render.render(write_still=True)
print('PREVIEW_OK', len(HEADS), VIEWS)
