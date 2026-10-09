"""GD13 render / comparison scene (Blender 5.2): one HEAD object (positions replaced per render job from any DNA-order head npy),
body neck/shoulder context, eye iris/pupil vertex colours, temporary diagnostic brow (vertex-colour band attached to the F1H skin material
points, so it follows the surface when the head is re-shaped; not a groom), clay / skin materials.
Cameras: CAM_REF_<view> = the solved per-panel head cameras of the user's 2026-10-09 6-view sheet (gd13_camsolve.py json; render = 2x panel),
CAM_front / CAM_q3R / CAM_q3L / CAM_profR / CAM_profL = review cameras (same as GD12). Mirrored in x like GD12 (UE is left-handed).
usage: blender -b --factory-startup --python gd13_scene.py -- <brow-reference head.npy (F1H)> <cams.json> <out.blend> [extra head name=npy ...]"""
import bpy, sys, os, math, json, numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
import gd_common as gc
a = sys.argv[sys.argv.index('--')+1:]; XB = np.load(a[0]); CAMS = json.load(open(a[1])); OUT = a[2]; EXTRA = [s.split('=', 1) for s in a[3:]]
S = 0.01; MM3 = np.diag([-1.0, 1, 1])
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
P = pkg(); TRI = np.asarray(P['head']['triangles'])
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
LASH = mat('M_Lash', (0.03, 0.02, 0.015), 0.6); CLAY = mat('M_Clay', (0.40, 0.385, 0.37), 0.62); SKIN = mat('M_Skin', (0.62, 0.42, 0.33), 0.5, sss=0.2, vcol='brow')
def eye_mat():
    """per-pixel iris / pupil / limbus from the interpolated angle-from-gaze attribute 'eyeang' (degrees / 90)"""
    m = bpy.data.materials.new('M_Eye'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.38; b.inputs['Specular IOR Level'].default_value = 0.22
    at = nt.nodes.new('ShaderNodeAttribute'); at.attribute_name = 'eyeang'; cr = nt.nodes.new('ShaderNodeValToRGB'); r = cr.color_ramp; r.interpolation = 'LINEAR'
    stops = [(0.0, (0.012, 0.010, 0.007)), (9.0/90, (0.015, 0.012, 0.008)), (10.0/90, (0.10, 0.065, 0.03)), (20.0/90, (0.17, 0.115, 0.05)), (26.0/90, (0.11, 0.075, 0.035)),
             (28.0/90, (0.045, 0.032, 0.02)), (29.5/90, (0.36, 0.31, 0.29)), (45.0/90, (0.42, 0.37, 0.34)), (1.0, (0.36, 0.30, 0.28))]
    r.elements[0].position, r.elements[0].color = stops[0][0], (*stops[0][1], 1); r.elements[1].position, r.elements[1].color = stops[-1][0], (*stops[-1][1], 1)
    for pos, col in stops[1:-1]: e = r.elements.new(pos); e.color = (*col, 1)
    nt.links.new(at.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color']); return m
EYE = eye_mat()
seg_skin = (TRI < SEG['skin'][1]).all(1) | ((TRI >= SEG['cartilage'][0]) & (TRI < SEG['cartilage'][1])).all(1)
seg_eye = ((TRI >= SEG['eyeL'][0]) & (TRI < SEG['eyeR'][1])).all(1); seg_lash = ((TRI >= SEG['lashes'][0]) & (TRI < SEG['lashes'][1])).all(1)
seg_lash[:] = False   # solid lash cards read as a cartoon band without their alpha: replaced by the lash-line tint
TK = TRI[seg_skin | seg_eye | seg_lash]; IS_EYE = seg_eye[seg_skin | seg_eye | seg_lash]; IS_LASH = seg_lash[seg_skin | seg_eye | seg_lash]
# brow band weights computed ONCE on the brow-reference head (F1H, same formula as GD12), stored per vertex -> material-attached
H = XB[:NS]; ax = np.abs(H[:, 0]-MX)
# diagnostic brow (GD13): straight, lower-arched, thinner band placed like the reference brow centre line (~2.0 cm above the eye centre at
# mid-brow, medial head ~1.8, tail ~1.7); a stand-in for the groom, NOT anatomy
zc = 163.85+0.15*np.exp(-((ax-3.0)/1.6)**2)-0.22*np.clip((ax-4.2)/1.0, 0, 1)-0.12*(1-np.clip((ax-1.2)/1.2, 0, 1)); th = 0.22*(1-np.clip((ax-1.3)/4.0, 0, 1))+0.08
def _ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
WB = (1-_ss((np.abs(H[:, 2]-zc)-th)/0.12))*_ss((ax-1.1)/0.3)*(1-_ss((ax-5.1)/0.35))*_ss((H[:, 1]-8.5)/0.5)
# lip vermilion tint: vertices inside the frontal (x, z) outline of the mesh-bound outer lip curves, front surface only
MMv = mirror_map(XB); BF = bindings('front', MMv); poly = np.vstack([bind_pts(BF['crv_lip_upper_outer_l'], XB), bind_pts(BF['crv_lip_upper_outer_r'], XB)[::-1], bind_pts(BF['crv_lip_lower_outer_r'], XB), bind_pts(BF['crv_lip_lower_outer_l'], XB)[::-1]])
poly = poly[~np.isnan(poly[:, 0])][:, [0, 2]]; cen = poly.mean(0); ang = np.arctan2(poly[:, 1]-cen[1], poly[:, 0]-cen[0]); poly = poly[np.argsort(ang)]
def _inside(P, Q):
    x, y = P[:, 0], P[:, 1]; ins = np.zeros(len(P), bool); j = len(Q)-1
    for i in range(len(Q)):
        xi, yi = Q[i]; xj, yj = Q[j]; c = ((yi > y) != (yj > y)) & (x < (xj-xi)*(y-yi)/(yj-yi+1e-12)+xi); ins ^= c; j = i
    return ins
ymouth = np.nanmax(bind_pts(BF['crv_lip_upper_outer_l'], XB)[:, 1]); WL = (_inside(H[:, [0, 2]], poly) & (H[:, 1] > ymouth-0.9)).astype(float)
# temporary lash line (diagnostic stand-in for the lash cards): dark tint on the skin just above the mesh-bound upper-lid margin, lighter below
# the lower margin; material-attached (computed on the brow-reference head)
WLL = np.zeros(NS)
for s_ in 'lr':
    for nm, top, amt in (('crv_eyelid_upper_'+s_, True, 0.78), ('crv_eyelid_lower_'+s_, False, 0.35)):
        Pm = bind_pts(BF[nm], XB); Pm = Pm[~np.isnan(Pm[:, 0])]
        pass
for k_ in ('eyeL', 'eyeR'):   # lid rim = skin within ~1.2 mm of the eyeball surface (upper rim dark, lower rim light)
    E_ = XB[SEG[k_][0]:SEG[k_][1]]; ce_ = E_.mean(0); rad_ = np.linalg.norm(E_-ce_, axis=1); r_ = np.percentile(rad_, 60)
    dist = np.linalg.norm(H-ce_, axis=1)-r_; front = H[:, 1] > ce_[1]+0.2; near = (dist < 0.22)*(np.linalg.norm(H-ce_, axis=1) < 2.2)*front
    WLL = np.maximum(WLL, near*np.where(H[:, 2] > ce_[2]-0.05, 0.9, 0.45)*(1-_ss((dist-0.10)/0.12)))
print('LASHLINE verts', int((WLL > 0.2).sum()), 'LIP verts', int((WL > 0.5).sum()) if 'WL' in dir() else -1)
for _ in range(3):
    T2 = TRI[(TRI < NS).all(1)]; acc = np.zeros(NS); cnt = np.zeros(NS); np.add.at(acc, T2.ravel(), np.repeat(WL[T2].mean(1), 3)); np.add.at(cnt, T2.ravel(), 1); WL = 0.5*WL+0.5*acc/np.maximum(cnt, 1)
def head_object(name, X, collection):
    me = bpy.data.meshes.new(name); me.from_pydata(mirror(X).tolist(), [], TK[:, ::-1].tolist()); me.update(); ob = bpy.data.objects.new(name, me); collection.objects.link(ob)
    for m in (CLAY, SKIN, EYE, LASH): ob.data.materials.append(m)
    me.polygons.foreach_set('material_index', np.where(IS_LASH, 3, np.where(IS_EYE, 2, 0)).astype(np.int32))
    for p in me.polygons: p.use_smooth = True
    ec = np.ones((len(X), 4), np.float32); EA = np.ones(len(X), np.float32)
    for k in ('eyeL', 'eyeR'):
        idx = np.arange(*SEG[k]); E = X[idx]; c = E.mean(0); d = E-c; d /= np.linalg.norm(d, axis=1)[:, None]
        fw = d[np.argmax(E[:, 1])]; ang = np.degrees(np.arccos(np.clip(d@fw, -1, 1)))
        # anatomical iris: ~11.7 mm diameter on the ~13 mm-radius eyeball (half-angle 27.5 deg) with a darker limbal ring; pupil ~4 mm
        ec[idx, :3] = np.where((ang < 10.5)[:, None], [0.02, 0.015, 0.01], np.where((ang < 29.5)[:, None], [0.28, 0.18, 0.08], np.where((ang < 31.5)[:, None], [0.11, 0.07, 0.04], [0.90, 0.86, 0.82])))
        EA[idx] = np.clip(ang/90.0, 0, 1)
    br = np.ones((len(X), 4), np.float32); br[:NS, :3] = (1-WB[:, None]*(1-np.array([0.22, 0.13, 0.09])))*(1-WL[:, None]*(1-np.array([0.86, 0.62, 0.62])))*(1-WLL[:, None]*(1-np.array([0.10, 0.07, 0.05])))
    for nm, arr in (('eyecol', ec), ('brow', br)):
        at = me.color_attributes.new(nm, 'FLOAT_COLOR', 'POINT'); at.data.foreach_set('color', arr.ravel())
    ea = me.attributes.new('eyeang', 'FLOAT', 'POINT'); ea.data.foreach_set('value', EA)
    return ob
HC = col('HEAD'); head_object('HEAD', XB, HC)
if EXTRA:
    CC = col('COMPARE_READONLY')
    for nm, p in EXTRA: o = head_object(nm, np.load(p), CC); o.hide_select = True; o.hide_render = True
    CC.hide_render = True
BODYC = col('BODY_CONTEXT'); NB = P['NB']; BX = np.asarray(P['br_neutral'])[:NB]; BT = np.asarray(P['body']['triangles']); keep = BX[:, 2] > 115.0; km = keep[BT].all(1)
remap = -np.ones(NB, int); remap[keep] = np.arange(keep.sum()); me = bpy.data.meshes.new('Body'); me.from_pydata(mirror(BX[keep]).tolist(), [], remap[BT[km]][:, ::-1].tolist()); me.update()
bo = bpy.data.objects.new('Body_Context', me); BODYC.objects.link(bo); bo.data.materials.append(CLAY); bo.data.materials.append(SKIN)
for p in me.polygons: p.use_smooth = True
CAMC = col('CAMERAS')
def ref_cam(v, c, W, Hh):
    R = cam_R(c); Rb = R@MM3; cb = bpy.data.cameras.new('CAM_REF_'+v); ob = bpy.data.objects.new('CAM_REF_'+v, cb); CAMC.objects.link(ob)
    M = Matrix([list(Rb[0]), list(-Rb[1]), list(-Rb[2])]).transposed(); loc = (MM3@CH)*S-c['D']*S*Rb[2]
    ob.matrix_world = Matrix.Translation(Vector(loc))@M.to_4x4(); cb.sensor_fit = 'VERTICAL'; cb.angle = 2*math.atan(Hh/2/c['f'])
    cb.shift_x = (W/2-c['cx'])/Hh; cb.shift_y = (c['cy']-Hh/2)/Hh; cb.clip_start = 0.05; cb.clip_end = 20; ob['res'] = [W*2, Hh*2]
PANEL = {'front': (483, 541), 'q3_faceR': (483, 541), 'q3_faceL': (482, 541), 'prof_faceL': (483, 545)}
for v, c in CAMS.items(): ref_cam(v, c, *PANEL[v])
def make_cam(name, cam, fov, W, Hh, rect):
    o, f, r, u = gc.basis(cam); Mx = np.diag([-1.0, 1, 1])
    R = Matrix([list(Mx@r), list(Mx@u), list(-(Mx@f))]).transposed(); cc = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cc); CAMC.objects.link(ob)
    ob.matrix_world = Matrix.Translation(Vector(mirror(o)))@R.to_4x4(); t = math.tan(math.radians(fov)/2); x0, y0, x1, y1 = rect
    ty = (y1-y0)*2*t; cc.sensor_fit = 'VERTICAL'; cc.angle = 2*math.atan(ty/2); cc.shift_x = ((x0+x1)/2-0.5)*2*t/ty; cc.shift_y = -((y0+y1)/2-0.5)*2*t/ty
    cc.clip_start = 0.05; cc.clip_end = 20; ob['res'] = [W, Hh]
REV = {'front': ([0, 125, 159, -90, 0], 15), 'q3R': ([-64.468, 113.297, 160.141, -58.0, 1.0], 15), 'q3L': ([64.468, 113.297, 160.141, -122.0, 1.0], 15),
       'profR': ([-125, 3, 160, 0, 0], 15), 'profL': ([125, 3, 160, 180, 0], 15)}
HX = XB[:NS]; HX = HX[(HX[:, 2] > 147.5) & (HX[:, 2] < 176.0)]
for k, (cm, fv) in REV.items():
    o, f, r, u = gc.basis(cm); t = math.tan(math.radians(fv)/2); d = HX-np.array(o); dd = d@f; qx = 0.5+0.5*(d@r)/dd/t; qy = 0.5-0.5*(d@u)/dd/t
    cx, cy = (qx.min()+qx.max())/2, (qy.min()+qy.max())/2; hh = (qy.max()-qy.min())*1.10; ww = hh*1100/1250; ww = max(ww, (qx.max()-qx.min())*1.08); hh = ww*1250/1100
    make_cam('CAM_'+k, cm, fv, 1100, 1250, (cx-ww/2, cy-hh/2, cx+ww/2, cy+hh/2))
def area(name, loc, target, power, size, colc):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = power; l.size = size; ob = bpy.data.objects.new(name, l); colc.objects.link(ob); ob.location = loc
    d = Vector(target)-Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); return ob
LA = col('LIGHTS_A'); LB = col('LIGHTS_B'); tgt = Vector(mirror([MX, 6.0, 159.0]))
area('A_key', tgt+Vector((0.55, 1.1, 0.55)), tgt, 60, 0.9, LA); area('A_fill', tgt+Vector((-0.8, 0.9, 0.1)), tgt, 22, 1.2, LA); area('A_top', tgt+Vector((0, 0.2, 1.2)), tgt, 14, 1.0, LA)
area('B_side', tgt+Vector((0.75, 0.45, 1.05)), tgt, 85, 0.45, LB); area('B_fill', tgt+Vector((-0.9, 0.8, -0.2)), tgt, 10, 1.6, LB); LB.hide_render = True
w = bpy.data.worlds.new('W'); w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.36, 0.36, 0.37, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.25; bpy.context.scene.world = w
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -1.3; sc.render.film_transparent = False
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(OUT)); print('GD13_SCENE_OK', OUT)
