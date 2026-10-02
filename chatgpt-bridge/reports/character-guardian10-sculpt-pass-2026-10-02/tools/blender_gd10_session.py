"""GUARDIAN-10: build a hands-on Blender sculpt session (.blend) for the face neutral.
  - object 'FACE_SCULPT' = DNA-order head skin + cartilage mesh (vertex order preserved -> exportable back to the pipeline); eyes / teeth as
    separate non-sculpt reference objects; mirror sculpting on X about the facial midline (object origin on the midline). The session is in Blender (right-handed) space = UE x mirrored; the export mirrors back
  - vertex group 'LOCK' (weight 1 = do not sculpt): cranium above the brow ridge, ears, jaw contour / chin sides, collar -> use as a sculpt mask
  - cameras 'TierA_Front' / 'TierA_3Q' reproduce the reference-solved capture cameras CROPPED to the Tier A photo frames (identical framing
    to the review boards), with the Tier A photo as a camera background image (alpha 0.5); 'TierB_Profile_aid' orthographic side camera with
    the Tier B profile panel (low-weight aid only)
  - text block 'EXPORT_TO_PIPELINE' : run it to write <project>/Saved/Codex/CharacterGuardian10_20261002/head_handsculpt.npy (full DNA-order head,
    sculpted skin + untouched eyes / teeth / lashes), ready for gd10_review.sh and gd10_cycle.sh
usage: blender -b --factory-startup --python blender_gd10_session.py -- <head.npy> <out.blend>"""
import bpy, sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import VIEWS, basis, crop_rect, head_topology
from id_common import SEG
from mathutils import Matrix
a = sys.argv[sys.argv.index('--')+1:]; HP, OUT = os.path.abspath(a[0]), os.path.abspath(a[1]); X = np.load(HP); MX = -0.25
M = np.array([-1.0, 1, 1])   # UE (left-handed) -> Blender (right-handed): mirror x; the export mirrors back
XB = X*M; MXB = -MX
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene; T, MI = head_topology()
def mk(name, mat_ids, col):
    TT = T[np.isin(MI, mat_ids)]; me = bpy.data.meshes.new(name); me.from_pydata([tuple(v-np.array([MXB, 0, 0])) for v in XB], [], [tuple(t[::-1]) for t in TT]); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.location = (MXB, 0, 0)
    m = bpy.data.materials.new(name+'_mat'); m.diffuse_color = col; ob.data.materials.append(m); return ob
face = mk('FACE_SCULPT', [0], (0.78, 0.76, 0.74, 1)); eyes = mk('EYES_ref', [3, 4], (0.95, 0.95, 0.95, 1)); eyes.hide_select = True
face.data.use_mirror_x = True; face.data.use_mirror_topology = False
S = X[:24049]; lock = (S[:, 2] > 165.2) | (np.abs(S[:, 0]-MX) > 6.3) | (S[:, 2] < 148.5) | ((S[:, 1] < 4.0) & (S[:, 2] < 156.0))
vg = face.vertex_groups.new(name='LOCK'); vg.add([int(i) for i in np.nonzero(lock)[0]], 1.0, 'REPLACE')
sc.render.resolution_percentage = 100
def cam_for(view, img):
    v = VIEWS[view]; o, f, r, u = basis(v['cam']); o, f, r, u = o*M, f*M, r*M, u*M; x0, y0, x1, y1 = crop_rect(view); cw, ch = x1-x0, y1-y0
    c = bpy.data.cameras.new('TierA_'+view); ob = bpy.data.objects.new('TierA_Front' if view == 'front' else 'TierA_3Q', c); sc.collection.objects.link(ob)
    Xa, Ya, Za = r, u, -f; ob.matrix_world = Matrix(((Xa[0], Ya[0], Za[0], o[0]), (Xa[1], Ya[1], Za[1], o[1]), (Xa[2], Ya[2], Za[2], o[2]), (0, 0, 0, 1)))
    c.sensor_fit = 'VERTICAL' if ch > cw else 'HORIZONTAL'; t = math.tan(math.radians(v['fov'])/2); big = max(cw, ch)
    c.angle = 2*math.atan(t*big); c.shift_x = ((x0+x1)/2-0.5)/big; c.shift_y = -((y0+y1)/2-0.5)/big
    im = bpy.data.images.load(os.path.abspath(img)); c.show_background_images = True; bg = c.background_images.new(); bg.image = im; bg.alpha = 0.5; bg.display_depth = 'FRONT'
    ob['res'] = [v['W'], v['H']]; return ob
cf = cam_for('front', VIEWS['front']['ref']); cc = cam_for('close', VIEWS['close']['ref'])
cp = bpy.data.cameras.new('TierB_Profile_aid'); po = bpy.data.objects.new('TierB_Profile_aid', cp); sc.collection.objects.link(po); cp.type = 'ORTHO'; cp.ortho_scale = 36.0
po.location = (125, 3, 157); po.rotation_euler = (math.radians(90), 0, math.radians(90))
im = bpy.data.images.load(os.path.abspath('Saved/Codex/CharacterGuardian2_20261001/refB/turnaround_p5.png')); cp.show_background_images = True; bg = cp.background_images.new(); bg.image = im; bg.alpha = 0.35
sc.camera = cf; sc.render.resolution_x, sc.render.resolution_y = 800, 960
txt = bpy.data.texts.new('EXPORT_TO_PIPELINE'); txt.write('''import bpy, numpy as np, os
# writes the sculpted neutral back in DNA vertex order (skin from FACE_SCULPT, everything else from the source head)
src = r"%s"; out = os.path.join(os.path.dirname(src), 'head_handsculpt.npy')
X = np.load(src); ob = bpy.data.objects['FACE_SCULPT']; me = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
P = np.array([(ob.matrix_world @ v.co)[:] for v in me.vertices])*np.array([-1.0, 1, 1]); X[:24049] = P[:24049]; np.save(out, X); print('EXPORTED', out)
''' % HP)
note = bpy.data.texts.new('README_SCULPT'); note.write('''GUARDIAN-10 hands-on sculpt session
- Sculpt FACE_SCULPT in Sculpt Mode; X-mirror is on (facial midline). Mask from vertex group LOCK (Mask > Mask from Vertex Group / or paint) to keep
  cranium, ears, jaw contour, chin sides and collar unchanged.
- Judge in cameras TierA_Front (render 800x960) and TierA_3Q (render 794x940): Tier A photos are the camera backgrounds (identity authority).
  TierB_Profile_aid = low-weight aid only (the generated profile sheets disagree with each other).
- Goals: fuller nose / tip / alae with continuous forehead-radix-bridge; more midface and lower-face soft tissue (no hollows, no grooves); fuller lips
  (keep width); adult tissue distribution (no wrinkles / bags); keep jaw/chin balance; do not touch the eyelid margins.
- When done: Text Editor > EXPORT_TO_PIPELINE > Run Script, save the .blend, and tell Claude -> review + one auto-rig + rig/LOD/restart checks.
''')
bpy.ops.wm.save_as_mainfile(filepath=OUT); print('SESSION_OK', OUT)
