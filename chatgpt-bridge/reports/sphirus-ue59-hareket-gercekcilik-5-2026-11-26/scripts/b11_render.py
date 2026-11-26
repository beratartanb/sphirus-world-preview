# b11_render.py (Blender -b): clay renders of B10 (open, hidden-face holes) vs B11 (template topology, closed) - full body + pelvis close-ups
import bpy, sys, json, os, numpy as np
from mathutils import Vector
D = sys.argv[sys.argv.index('--') + 1]; OUT = D + 'r/'; os.makedirs(OUT, exist_ok=True)
T = json.load(open(D + 'tmpl.json')); B = json.load(open(D + 'b10.json')); P = json.load(open(D + 'b11_pos.json'))
FC = json.load(open(D + '../b4/dump_face.json'))['lods']['0']
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.world = bpy.data.worlds.new('w'); sc.world.color = (0.32, 0.30, 0.31)
def build(name, V, Tr):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in V], [], [tuple(t) for t in Tr]); me.update()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return o
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.72, 0.68, 0.64)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'BOTH'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'
f = np.array([0, 1.0, 0]); lv = np.array([1.0, 0, 0])
views = (('front', f), ('side', -lv), ('back', -f), ('front34', (f - lv) / np.linalg.norm(f - lv)), ('back34', (-f + lv) / np.linalg.norm(f - lv)), ('low', np.array([0, 0.55, -0.83])))
for tag, V, Tr in (('b10', B['v'], B['t']), ('b11', P['pos'], T['t'])):
    for o in [o for o in sc.collection.objects if o.type == 'MESH']: bpy.data.objects.remove(o)
    build('body', V, Tr); build('head', FC['v'], FC['t'])
    for full in (1, 0):
        if full: sc.render.resolution_x, sc.render.resolution_y = 600, 1200; cam.data.ortho_scale = 200.0; c = np.array([0, 0, 87.0])
        else: sc.render.resolution_x, sc.render.resolution_y = 900, 900; cam.data.ortho_scale = 52.0; c = np.array([0, 0, 92.0])
        for view, d in views:
            if full and view in ('back34', 'low'): continue
            cam.location = Vector((c + d * 600).tolist()); cam.rotation_euler = Vector((-d).tolist()).to_track_quat('-Z', 'Y').to_euler()
            sc.render.filepath = OUT + '%s_%s_%s.png' % (tag, 'full' if full else 'pelvis', view); bpy.ops.render.render(write_still=True)
open(OUT + 'done.txt', 'w').write('ok')
