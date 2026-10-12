"""GD43: render the SPHIRUS body (+ head) in Blender for silhouette / shape comparison with the body references.
State = accepted_b2 + BR_Neutral (package br_neutral) + LK_Neutral (CharacterFinalArt morph_lk_body_lod0.json) [+ optional extra body delta
json {'Body': {name: {idx: [dx,dy,dz]}}}]. Bind space, UE cm (x = left, y = front, z = up). Views: front (looking at the face, -y), back,
side (subject's left side, the face toward image left like the reference profile), front3q. MODE sil = flat white on black (silhouette),
clay = soft studio clay (grey) for visual comparison. Orthographic, figure height = FRAC of the image height.
usage: blender -b --factory-startup --python gd43_bodyrender.py -- <pkg.json.gz> <lk_lod0.json> <out_prefix> <mode sil|clay> [extra_delta.json] [W=900 H=1000]"""
import bpy, sys, json, gzip, math, os
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; PKG, LK, OUT, MODE = a[:4]; EXTRA = a[4] if len(a) > 4 and a[4] not in ('-', '') else None
W, H = (int(a[5]), int(a[6])) if len(a) > 6 else (900, 1000)
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; X = np.asarray(P['br_neutral'], np.float64).copy()
def add(path, key=None):
    d = json.load(open(path))['Body']
    for name, dd in d.items():
        if key and name != key: continue
        for k, v in dd.items(): X[int(k)] += v
add(LK, 'LK_Neutral')
if EXTRA: add(EXTRA)
TB = np.asarray(P['body']['triangles'], np.int64); TH = np.asarray(P['head']['triangles'], np.int64)+NB if 'triangles' in P['head'] else None
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
def mk(name, V, T):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in V], [], [tuple(t) for t in T]); me.update(); ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    return ob
# Blender frame: x = UE x, y = -UE y? keep UE coordinates but view along -Y/ +Y with a camera; z up
Vb = X[:NB]; ob = mk('body', Vb, TB)
if TH is not None:
    Vh = X[NB:]; th = TH-NB; hk = (Vh[:, 2] > 0); oh = mk('head', Vh, th[(th < len(Vh)).all(1)])
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = W, H; sc.render.film_transparent = False
if MODE == 'sil':
    sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'FLAT'; sh.color_type = 'SINGLE'; sh.single_color = (1, 1, 1); sh.background_type = 'VIEWPORT'; sh.background_color = (0, 0, 0)
    sc.view_settings.view_transform = 'Standard'
elif MODE == 'lit':   # directional sculpt light (like a sculpt presentation render): EEVEE, key sun from front-upper-left, weak fill, AO
    sc.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE_NEXT'
    mat = bpy.data.materials.new('clay'); mat.use_nodes = True; bs = mat.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value = (0.55, 0.53, 0.56, 1); bs.inputs['Roughness'].default_value = 0.55
    for o in bpy.data.objects:
        if o.type == 'MESH': o.data.materials.append(mat)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.03, 0.03, 0.04, 1); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.6
    for nm, rot, en in (('key', (math.radians(50), 0, math.radians(-150)), 3.2), ('fill', (math.radians(70), 0, math.radians(40)), 0.6), ('rim', (math.radians(110), 0, math.radians(0)), 1.4)):
        ld = bpy.data.lights.new(nm, 'SUN'); ld.energy = en; ld.angle = math.radians(8); lo = bpy.data.objects.new(nm, ld); lo.rotation_euler = rot; sc.collection.objects.link(lo)
    try: sc.eevee.use_gtao = True
    except Exception: pass
    sc.view_settings.view_transform = 'Standard'
else:
    sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.62, 0.6, 0.62); sh.background_type = 'VIEWPORT'
    sh.background_color = (0.09, 0.09, 0.11); sh.show_cavity = False; sh.studio_light = 'paint.sl' if 'paint.sl' in [l.name for l in bpy.context.preferences.studio_lights] else sh.studio_light
    sc.view_settings.view_transform = 'Standard'
zmin, zmax = float(X[:, 2].min()), float(X[:, 2].max()); hgt = zmax-zmin; FRAC = 0.94; cx = float(-0.23)
cam_d = bpy.data.cameras.new('cam'); cam_d.type = 'ORTHO'; cam_d.ortho_scale = hgt/FRAC*max(1.0, W/H); cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
zc = zmin+hgt/2
VIEWS = {'front': ((cx, 400.0, zc), (math.radians(90), 0, math.radians(180))), 'back': ((cx, -400.0, zc), (math.radians(90), 0, 0)),
         'side': ((400.0, 3.0, zc), (math.radians(90), 0, math.radians(90))), 'front3q': ((cx+283.0, 283.0, zc), (math.radians(90), 0, math.radians(135)))}
CROP = os.environ.get('CROP', '')
if CROP == 'chest':   # breast close-up framing: 44 cm ortho window centred on the bust (z 126), front / side / 3q / low 3q (camera 20 deg below, looking up)
    zc = 126.0; cam_d.ortho_scale = 44.0*max(1.0, W/H); e = math.radians(20)
    VIEWS = {'front': ((cx, 400.0, zc), (math.radians(90), 0, math.radians(180))), 'side': ((400.0, 3.0, zc), (math.radians(90), 0, math.radians(90))),
             'front3q': ((cx+283.0, 283.0, zc), (math.radians(90), 0, math.radians(135))), 'low3q': ((cx+283.0, 283.0, zc-400.0*math.tan(e)), (math.radians(90)+e, 0, math.radians(135)))}
for v, (loc, rot) in VIEWS.items():
    cam.location = loc; cam.rotation_euler = rot
    sc.render.filepath = f'{OUT}_{v}_{MODE}.png'
    if MODE == 'lit':
        for o in sc.objects:
            if o.type == 'LIGHT' and o.name == 'key': o.rotation_euler = (math.radians(50), 0, math.radians(-150)+cam.rotation_euler[2]-math.radians(180))
    bpy.ops.render.render(write_still=True); print('BODYRENDER', v, sc.render.filepath)
print('BODYRENDER_OK height_cm %.2f zmin %.2f zmax %.2f' % (hgt, zmin, zmax))
