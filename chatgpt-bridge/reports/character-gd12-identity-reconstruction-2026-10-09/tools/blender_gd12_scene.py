"""GD12 Identity Master scene (Blender 5.2). Builds an editable .blend from head npys (DNA order, UE cm):
  GD12_Head (editable master, clay/skin materials), F1H_Head (read-only comparison, hidden from render by default), eyes with iris/pupil
  vertex colours, a temporary diagnostic brow (vertex-colour band, not a groom), body neck/shoulders (clay).
  Cameras: CAM_REF_front / CAM_REF_close = the solved cameras of the two Tier A reference crops (gd_common VIEWS + camfit, render size =
  reference crop size, shift/angle = crop rect), CAM_front / CAM_q3R / CAM_q3L / CAM_profR / CAM_profL = the UE review cameras.
  UE is left-handed: everything is mirrored in x (p' = diag(-1,1,1) p) so the camera basis is a proper rotation and images match UE / topix.
  Lights: LIGHTS_A (soft frontal key + fill), LIGHTS_B (raking side key from screen right).
usage: blender -b --factory-startup --python blender_gd12_scene.py -- <master head.npy> <compare head.npy> <out.blend>"""
import bpy, sys, os, math, json, numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
import gd_common as gc
a = sys.argv[sys.argv.index('--')+1:]; MASTER, COMPARE, OUT = a[0], a[1], a[2]
S = 0.01; MX = -0.23
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
P = pkg(); TRI = np.asarray(P['head']['triangles']); MID = np.asarray(P['head']['material_ids'])
def mirror(p): p = np.asarray(p, float).copy(); p[..., 0] *= -1; return p*S
def col(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children: bpy.context.scene.collection.children.link(c)
    return c
def mat(name, rgb, rough=0.55, sss=0.0, vcol=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough
    if sss: b.inputs['Subsurface Weight'].default_value = sss; b.inputs['Subsurface Radius'].default_value = (1.0, 0.45, 0.25); b.inputs['Subsurface Scale'].default_value = 0.004
    if vcol:
        at = m.node_tree.nodes.new('ShaderNodeAttribute'); at.attribute_name = vcol; mx = m.node_tree.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
        mx.inputs[0].default_value = 1.0; mx.inputs[6].default_value = (*rgb, 1); m.node_tree.links.new(at.outputs['Color'], mx.inputs[7]); m.node_tree.links.new(mx.outputs[2], b.inputs['Base Color'])
    return m
CLAY = mat('M_Clay', (0.40, 0.385, 0.37), 0.62)
SKIN = mat('M_Skin', (0.62, 0.42, 0.33), 0.5, sss=0.2, vcol='brow')
EYE = mat('M_Eye', (1, 1, 1), 0.2, vcol='eyecol')
def head_object(name, X, collection, master=True):
    keep_tri = np.isin(MID, [0]) if True else None
    seg_skin = (TRI < SEG['skin'][1]).all(1) | ((TRI >= SEG['cartilage'][0]) & (TRI < SEG['cartilage'][1])).all(1)
    seg_eye = ((TRI >= SEG['eyeL'][0]) & (TRI < SEG['eyeR'][1])).all(1)
    T = TRI[seg_skin | seg_eye]; is_eye = seg_eye[seg_skin | seg_eye]
    me = bpy.data.meshes.new(name); V = mirror(X); me.from_pydata(V.tolist(), [], T[:, ::-1].tolist())   # winding reversed (mirrored)
    me.update(); ob = bpy.data.objects.new(name, me); collection.objects.link(ob)
    ob.data.materials.append(CLAY); ob.data.materials.append(SKIN); ob.data.materials.append(EYE)
    mi = np.where(is_eye, 2, 0).astype(np.int32); me.polygons.foreach_set('material_index', mi)
    for p in me.polygons: p.use_smooth = True
    # eye colours: iris / pupil by angle from each eyeball's forward axis
    ec = np.ones((len(X), 4), np.float32)
    for k in ('eyeL', 'eyeR'):
        idx = np.arange(*SEG[k]); E = X[idx]; c = E.mean(0); d = E-c; d /= np.linalg.norm(d, axis=1)[:, None]
        fw = d[np.argmax(E[:, 1])]; ang = np.degrees(np.arccos(np.clip(d@fw, -1, 1)))
        ec[idx, :3] = np.where((ang < 9)[:, None], [0.02, 0.015, 0.01], np.where((ang < 21)[:, None], [0.30, 0.17, 0.07], [0.92, 0.88, 0.84]))
    # temporary diagnostic brow (vertex colour band on skin; arch from the eye centre)
    br = np.ones((len(X), 4), np.float32); H = X[:SEG['skin'][1]]; ax = np.abs(H[:, 0]-MX)
    zc = 164.05+0.35*np.exp(-((ax-3.3)/1.5)**2)-0.35*np.clip((ax-4.5)/1.0, 0, 1)**1.5; th = 0.26*(1-np.clip((ax-1.4)/4.0, 0, 1))+0.10
    def _ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
    wb = (1-_ss((np.abs(H[:, 2]-zc)-th)/0.14))*_ss((ax-1.0)/0.3)*(1-_ss((ax-5.2)/0.35))*_ss((H[:, 1]-8.5)/0.5)
    br[:SEG['skin'][1], :3] = 1-wb[:, None]*(1-np.array([0.22, 0.13, 0.09]))
    for nm, arr in (('eyecol', ec), ('brow', br)):
        at = me.color_attributes.new(nm, 'FLOAT_COLOR', 'POINT'); at.data.foreach_set('color', arr.ravel())
    if not master: ob.hide_select = True
    return ob
M = col('GD12_MASTER'); CMP = col('COMPARE_READONLY'); CAMS = col('CAMERAS'); LA = col('LIGHTS_A'); LB = col('LIGHTS_B'); BODYC = col('BODY_CONTEXT')
head_object('GD12_Head', np.load(MASTER), M, True)
cmp = head_object('F1H_Head', np.load(COMPARE), CMP, False); CMP.hide_render = True
# body (neck / shoulders) clay context
NB = P['NB']; BX = np.asarray(P['br_neutral'])[:NB]; BT = np.asarray(P['body']['triangles']); keep = BX[:, 2] > 115.0; km = keep[BT].all(1)
remap = -np.ones(NB, int); remap[keep] = np.arange(keep.sum()); me = bpy.data.meshes.new('Body'); me.from_pydata(mirror(BX[keep]).tolist(), [], remap[BT[km]][:, ::-1].tolist()); me.update()
bo = bpy.data.objects.new('Body_Context', me); BODYC.objects.link(bo); bo.data.materials.append(CLAY); bo.data.materials.append(SKIN)
for p in me.polygons: p.use_smooth = True
# cameras
def make_cam(name, cam, fov, W, H, rect=None):
    o, f, r, u = gc.basis(cam); Mx = np.diag([-1.0, 1, 1])
    R = Matrix([list(Mx@r), list(Mx@u), list(-(Mx@f))]).transposed(); c = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, c); CAMS.objects.link(ob)
    ob.matrix_world = Matrix.Translation(Vector(mirror(o))) @ R.to_4x4()
    t = math.tan(math.radians(fov)/2); x0, y0, x1, y1 = rect if rect else (0, 0, 1, 1)
    tx, ty = (x1-x0)*2*t, (y1-y0)*2*t; big = max(tx*W/W, ty) if H >= W else tx
    c.sensor_fit = 'VERTICAL' if H >= W else 'HORIZONTAL'; span = ty if H >= W else tx; c.angle = 2*math.atan(span/2)
    c.shift_x = ((x0+x1)/2-0.5)*2*t/span; c.shift_y = -((y0+y1)/2-0.5)*2*t/span; c.clip_start = 0.05; c.clip_end = 20
    ob['res'] = [W, H]; return ob
for v in ('front', 'close'):
    V_ = gc.VIEWS[v]; make_cam('CAM_REF_'+v, V_['cam'], V_['fov'], V_['W'], V_['H'], gc.crop_rect(v))
REV = {'front': ([0, 125, 159, -90, 0], 15), 'q3R': ([-64.468, 113.297, 160.141, -58.0, 1.0], 15), 'q3L': ([64.468, 113.297, 160.141, -122.0, 1.0], 15),
       'profR': ([-125, 3, 160, 0, 0], 15), 'profL': ([125, 3, 160, 180, 0], 15)}
CROP = (0.27, 0.12, 0.73, 0.64)   # head framing inside the 15 deg review frame
HX = np.load(MASTER)[:SEG['skin'][1]]; HX = HX[(HX[:, 2] > 147.5) & (HX[:, 2] < 176.0)]
for k, (cm, fv) in REV.items():   # framing from the projected head (face + cranium) bbox, 1100 x 1250
    o, f, r, u = gc.basis(cm); t = math.tan(math.radians(fv)/2); d = HX-np.array(o); dd = d@f; qx = 0.5+0.5*(d@r)/dd/t; qy = 0.5-0.5*(d@u)/dd/t
    cx, cy = (qx.min()+qx.max())/2, (qy.min()+qy.max())/2; hh = (qy.max()-qy.min())*1.10; ww = hh*1100/1250; ww = max(ww, (qx.max()-qx.min())*1.08); hh = ww*1250/1100
    make_cam('CAM_'+k, cm, fv, 1100, 1250, (cx-ww/2, cy-hh/2, cx+ww/2, cy+hh/2))
# lights
def area(name, loc, target, power, size, colc):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = power; l.size = size; ob = bpy.data.objects.new(name, l); colc.objects.link(ob); ob.location = loc
    d = Vector(target)-Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return ob
tgt = Vector(mirror([MX, 6.0, 159.0]))
area('A_key', tgt+Vector((0.55, 1.1, 0.55)), tgt, 60, 0.9, LA); area('A_fill', tgt+Vector((-0.8, 0.9, 0.1)), tgt, 22, 1.2, LA); area('A_top', tgt+Vector((0, 0.2, 1.2)), tgt, 14, 1.0, LA)
area('B_side', tgt+Vector((0.75, 0.45, 1.05)), tgt, 85, 0.45, LB); area('B_fill', tgt+Vector((-0.9, 0.8, -0.2)), tgt, 10, 1.6, LB)
LB.hide_render = True
w = bpy.data.worlds.new('W'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.36, 0.36, 0.37, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.25; bpy.context.scene.world = w
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -1.3; sc.render.film_transparent = False
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT)); print('GD12_SCENE_OK', OUT)
