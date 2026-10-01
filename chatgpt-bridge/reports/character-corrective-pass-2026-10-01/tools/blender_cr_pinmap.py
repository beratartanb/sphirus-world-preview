"""CORRECTIVE pass: render the Chaos Cloth MaxDistance pin maps (same weight functions as ue_cr_cloth_build.py) on the garment rest meshes.
blue = pinned (0 cm, follows skinning), red = free (High cm). usage: blender -b --factory-startup --python blender_cr_pinmap.py -- <geometry.json.gz> <out_dir>"""
import bpy, sys, json, gzip, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; GEO, OUT = a
G = json.loads(gzip.open(GEO, 'rb').read())
def ss(x): x = max(0.0, min(1.0, x)); return x*x*(3-2*x)
def w_shorts(x, y, z):
    if z >= 97.5: return 0.0
    t = ss((96.5-z)/18.0)**1.4; core = 1.0-math.exp(-((x/5.5)**2+((z-77.0)/6.0)**2)); rise = ss((abs(x)-1.5)/4.0) if z > 80 else 1.0; side = 1.0+0.35*ss((abs(x)-11.0)/4.0)
    return max(0.0, min(1.0, t*core*rise*side))
def w_hl(x, y, z): return max(0.0, min(1.0, ss((109.0-1.5-z)/10.0)**1.3))
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
def mk(name, part, wf, keep=None, grey=False):
    X = np.asarray(G[part]['positions']); F = np.asarray(G[part]['triangles'])
    if keep: c = X[F].mean(1); F = F[(c[:, 2] < keep[0]) & (np.abs(c[:, 0]) < keep[1])]
    me = bpy.data.meshes.new(name); me.from_pydata([(p[0]*0.01, -p[1]*0.01, p[2]*0.01) for p in X], [], [tuple(f) for f in F]); me.update()
    col = me.color_attributes.new('W', 'FLOAT_COLOR', 'POINT')
    for i, p in enumerate(X):
        w = wf(*p) if wf else 0.0
        col.data[i].color = (0.55, 0.55, 0.55, 1) if grey else (w, 0.15*(1-abs(2*w-1)), 1-w, 1)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'VERTEX'
sc.render.resolution_x, sc.render.resolution_y = 700, 900; sc.render.film_transparent = False; sc.world = bpy.data.worlds.new('w'); sc.world.color = (0.18, 0.18, 0.18)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'
def shot(fn, loc, rot, scale, zc):
    cam.location = (loc[0], loc[1], zc); cam.rotation_euler = rot; cam.data.ortho_scale = scale; sc.render.filepath = OUT+'/'+fn; bpy.ops.render.render(write_still=True)
VIEWS = {'front': ((0, -3, 0), (math.radians(90), 0, 0)), 'side': ((3, 0, 0), (math.radians(90), 0, math.radians(90))), 'back': ((0, 3, 0), (math.radians(90), 0, math.radians(180))), '3q': ((2.1, -2.1, 0), (math.radians(90), 0, math.radians(45)))}
s = mk('shorts', 'trousers', w_shorts)
for v, (l, r) in VIEWS.items(): shot(f'pin_shorts_{v}.png', l, r, 0.62, 0.89)
bpy.data.objects.remove(s, do_unlink=True)
up = mk('henley_up', 'henley', None, grey=True); lo = mk('henley_lo', 'henley', w_hl, keep=(110.8, 21.0))
lo.location = (0, 0, 0)
up.data.polygons.foreach_set('hide', [False]*len(up.data.polygons))
# show the upper (skinned) part only above the cut so the simulated piece is readable
X = np.asarray(G['henley']['positions']); F = np.asarray(G['henley']['triangles']); c = X[F].mean(1); keepu = ~((c[:, 2] < 109.0) & (np.abs(c[:, 0]) < 21.0))
import bmesh; bm = bmesh.new(); bm.from_mesh(up.data); bm.faces.ensure_lookup_table(); bmesh.ops.delete(bm, geom=[f for f, k in zip(bm.faces, keepu) if not k], context='FACES'); bm.to_mesh(up.data); bm.free()
for v, (l, r) in VIEWS.items(): shot(f'pin_henley_{v}.png', l, r, 0.75, 1.12)
print('PINMAP_OK')
