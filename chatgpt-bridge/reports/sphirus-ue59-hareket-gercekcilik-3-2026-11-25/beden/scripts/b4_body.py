# b4_body.py (Blender 5.3, background) - body form pass B4 (movement realism pass 3 follow-up, 2026-11-25).
# args after '--': <params json path>
#  params: {'body': dump json (b4_dump.py, LOD0 + weights + bones), 'face': dump json, 'out': dir, 'mode': 'measure'|'shape',
#           'shape': {...field params...}, 'garments': [dump json, ...], 'render': true}
# measure: real height (body sole -> face skull top, hair excluded), head height, widths / depths / hull circumferences on the neutral
#          bind pose, limb circumferences perpendicular to the bone axes, arm span from the bone chain. -> <out>/measure_<tag>.json
# shape:   delta field = sum over the vertex's skin weights of region deltas (torso width / depth profile about the section centre,
#          limb radial profiles about the bone axis, local pushes); graph-diffused; neck seam (face weld) guarded; flips / stretch checked;
#          transferred to LOD1..N and to garments by nearest-surface barycentric delta. -> <out>/delta.json + measure_after.json
# render:  clay front / side / back orthographic boards of body+head, same camera for before and after -> <out>/clay_<tag>_<view>.png
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
A = json.load(open(sys.argv[sys.argv.index('--') + 1])); OUT = A['out']; os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, 'log_%s.txt' % A.get('tag', 'x')), 'w')
def log(*a):
    s = ' '.join(str(x) for x in a); LOG.write(s + '\n'); LOG.flush()
B = json.load(open(A['body'])); FC = json.load(open(A['face']))
bones = {k: np.array(v) for k, v in B['bones'].items()}; bn = B['bone_index_names']
L0 = B['lods']['0']; V0 = np.array(L0['v'], dtype=np.float64); T0 = np.array(L0['t'], dtype=np.int64); W0 = L0['w']
FV = np.array(FC['lods']['0']['v'], dtype=np.float64); FT = np.array(FC['lods']['0']['t'], dtype=np.int64)
FVa = FV
log('body verts', len(V0), 'tris', len(T0), 'face verts', len(FV), 'weights', len(W0))
# ---------------------------------------------------------------- frame: up z, forward f, left l (towards *_l bones)
up = np.array([0, 0, 1.0])
f = np.array([0, 1.0, 0]); lv = np.array([1.0, 0, 0])   # MetaHuman bind: forward +Y, left +X
mid = (bones['thigh_l'] + bones['thigh_r']) / 2; mid[2] = 0
def fw(P): return (P - mid) @ f
def lt(P): return (P - mid) @ lv
log('forward', f.round(3), 'left', lv.round(3))
# ---------------------------------------------------------------- vertex regions from dominant bone
def bname(i): return bn[i] if 0 <= i < len(bn) else '?'
def region_of(name):
    n = name.lower()
    for key, reg in (('toe', 'foot'), ('hand', 'hand'), ('thumb', 'hand'), ('index', 'hand'), ('middle_', 'hand'), ('ring', 'hand'), ('pinky', 'hand'), ('lowerarm', 'forearm'), ('upperarm', 'uarm'),
                     ('ball', 'foot'), ('foot', 'foot'), ('calf', 'calf'), ('thigh', 'thigh'), ('clavicle', 'torso'), ('spine', 'torso'), ('pelvis', 'torso'), ('neck', 'neck'), ('head', 'neck')):
        if key in n: return reg + ('_l' if n.endswith('_l') or '_l_' in n else '_r' if n.endswith('_r') or '_r_' in n else '')
    return 'other'
DOM = [region_of(bname(w[0][0])) if w else 'other' for w in W0]
RW = {}  # per vertex: region -> weight (summed over bones of that region)
for i, w in enumerate(W0):
    d = {}
    for bi, ww in w:
        r = region_of(bname(bi)); d[r] = d.get(r, 0.0) + ww
    s = sum(d.values()) or 1.0; RW[i] = {k: v / s for k, v in d.items()}
def rw(region):
    return np.array([RW[i].get(region, 0.0) for i in range(len(V0))])
RA = {r: rw(r) for r in ('uarm_l', 'uarm_r', 'forearm_l', 'forearm_r', 'hand_l', 'hand_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'torso', 'torso_l', 'torso_r', 'neck', 'other')}
ARMW = sum(RA[r] for r in ('uarm_l', 'uarm_r', 'forearm_l', 'forearm_r', 'hand_l', 'hand_r'))
# ---------------------------------------------------------------- geometry helpers
def section(V, T, z, mask=None):
    """edge-plane intersection points of triangles (all 3 verts in mask) with plane z"""
    tri = T if mask is None else T[mask[T].all(axis=1)]
    a = V[tri]; dz = a[:, :, 2] - z; pts = []
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        s = dz[:, i] * dz[:, j] < 0; t = dz[s, i] / (dz[s, i] - dz[s, j]); p = a[s, i] + (a[s, j] - a[s, i]) * t[:, None]; pts.append(p)
    return np.concatenate(pts) if pts else np.zeros((0, 3))
def section_axis(V, T, c, n, mask=None):
    """intersection with plane through c normal n"""
    tri = T if mask is None else T[mask[T].all(axis=1)]
    a = V[tri]; dz = (a - c) @ n; pts = []
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        s = dz[:, i] * dz[:, j] < 0; t = dz[s, i] / (dz[s, i] - dz[s, j]); p = a[s, i] + (a[s, j] - a[s, i]) * t[:, None]; pts.append(p)
    return np.concatenate(pts) if pts else np.zeros((0, 3))
def hull_perim(P2):
    if len(P2) < 3: return 0.0
    P2 = np.unique(np.round(P2, 4), axis=0); P2 = P2[np.lexsort((P2[:, 1], P2[:, 0]))]
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []; hi = []
    for p in P2:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in P2[::-1]:
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    h = np.array(lo[:-1] + hi[:-1]); return float(np.sum(np.linalg.norm(h - np.roll(h, 1, axis=0), axis=1)))
def plane2(P, n):
    e1 = np.cross(n, [0, 0, 1.0]) if abs(n[2]) < 0.9 else np.cross(n, [1.0, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1); return np.stack([P @ e1, P @ e2], axis=1)
# ---------------------------------------------------------------- measure
def measure(V, tag):
    M = {}
    sole = float(V[:, 2].min()); top = float((FV if tag == 'before' else FVa)[:, 2].max())
    H = top - sole; M['height_cm'] = round(H, 1); M['sole_z'] = round(sole, 1); M['skull_top_z'] = round(top, 1)
    # menton: midline profile (front-most y per 0.5 cm, |x| < 0.8); the chin underside is the largest upward jump of the profile in z 145..160
    F = FV if tag == 'before' else FVa; Fm = F[np.abs(F[:, 0]) < 1.0]; band = Fm[(Fm[:, 2] > 144) & (Fm[:, 2] < 152)]
    neck_front = float(np.percentile(band[:, 1], 98)) if len(band) else 4.0          # throat front (midline), below the chin
    chin = Fm[(Fm[:, 1] > neck_front + 3.5) & (Fm[:, 2] > 144) & (Fm[:, 2] < 162)]
    menton = float(chin[:, 2].min()) if len(chin) else float('nan'); M['neck_front_y'] = round(neck_front, 1); M['menton_z'] = round(menton, 1); M['head_height_cm'] = round(top - menton, 1); M['heads_tall'] = round(H / (top - menton), 2)
    armless = ARMW < 0.15
    crotch = float(V[(np.abs(lt(V)) < 1.5) & armless, 2].min()); M['crotch_z'] = round(crotch, 1); M['crotch_ratio'] = round((crotch - sole) / H, 3)
    def tsec(z, mask=armless):
        P = section(V, T0, z, mask)
        if len(P) < 5: return None
        x = lt(P); y = fw(P); return {'z': round(z, 1), 'w': round(float(x.max() - x.min()), 1), 'd': round(float(y.max() - y.min()), 1), 'circ': round(hull_perim(np.stack([x, y], 1)), 1), 'front': round(float(y.max()), 1), 'back': round(float(y.min()), 1)}
    zs = np.arange(crotch + 4, bones['neck_01'][2] - 4, 1.0); S = [tsec(z) for z in zs]; S = [s for s in S if s]
    M['torso_profile'] = S
    # waist = min circumference between z(spine_01)+2 and z(spine_04); hip = max circumference crotch+5 .. pelvis+6 ; chest = max depth z spine_04..spine_05
    def pick(lo, hi, key, fn):
        c = [s for s in S if lo <= s['z'] <= hi and s['front'] > 4 and s['back'] < -4 and 14 < s['w'] < 45]; return fn(c, key=lambda s: s[key]) if c else None
    M['waist'] = pick(100, 120, 'circ', min)            # natural waist = narrowest complete torso section
    M['hip'] = pick(crotch + 5, bones['pelvis'][2] + 8, 'circ', max)
    M['chest_bust'] = pick(bones['spine_04'][2], bones['spine_05'][2] + 4, 'd', max)
    bz = M['chest_bust']['z'] if M['chest_bust'] else bones['spine_04'][2]
    M['underbust'] = pick(bz - 13, bz - 5, 'circ', min)
    M['chest_axilla'] = pick(bz + 4, bz + 9, 'circ', max)
    # shoulder breadth: lateral extent of verts within 12 cm of the shoulder joint, z band joint-10..joint+3
    # bideltoid breadth with the arms hanging: joint distance + 2 x lateral deltoid thickness (perpendicular to the humerus, t 0.1..0.35)
    rl = []
    for s, sg in (('l', 1), ('r', -1)):
        A_, B_ = bones['upperarm_' + s], bones['lowerarm_' + s]; n = (B_ - A_) / np.linalg.norm(B_ - A_); e = np.array([sg, 0, 0.0]); e -= n * e.dot(n); e /= np.linalg.norm(e)
        msk = (RA['uarm_' + s] + RA['torso_' + s] * 0) > 0.4; best = 0
        for t in np.arange(0.08, 0.36, 0.04):
            c = A_ + (B_ - A_) * t; P = section_axis(V, T0, c, n, msk)
            if len(P):
                rr = np.linalg.norm((P - c) - np.outer((P - c) @ n, n), axis=1); P = P[rr < 9.0]
                if len(P): best = max(best, float(((P - c) @ e).max()))
        rl.append(best)
    M['deltoid_lat_thickness'] = [round(x, 1) for x in rl]
    M['shoulder_joint_dist'] = round(float(np.linalg.norm(bones['upperarm_l'] - bones['upperarm_r'])), 1); M['bideltoid_breadth'] = round(M['shoulder_joint_dist'] + rl[0] + rl[1], 1)
    # limbs: perpendicular sections, max / at t
    def limb(a, b, reg, ts, fn):
        A_, B_ = bones[a], bones[b]; n = (B_ - A_) / np.linalg.norm(B_ - A_); msk = RA[reg] > 0.35; best = None
        for t in ts:
            P = section_axis(V, T0, A_ + (B_ - A_) * t, n, msk)
            if len(P) < 5: continue
            P2 = plane2(P - (A_ + (B_ - A_) * t), n); r = np.linalg.norm(P2, axis=1)
            P2 = P2[r < np.median(r) * 1.8]; c = hull_perim(P2)
            if best is None or fn(c, best[0]) == c: best = (round(c, 1), round(t, 2))
        return best
    for s in ('l', 'r'):
        M['upperarm_relaxed_' + s] = limb('upperarm_' + s, 'lowerarm_' + s, 'uarm_' + s, [0.5], max)
        M['upperarm_max_' + s] = limb('upperarm_' + s, 'lowerarm_' + s, 'uarm_' + s, np.arange(0.3, 0.8, 0.05), max)
        M['forearm_max_' + s] = limb('lowerarm_' + s, 'hand_' + s, 'forearm_' + s, np.arange(0.08, 0.45, 0.04), max)
        M['wrist_' + s] = limb('lowerarm_' + s, 'hand_' + s, 'forearm_' + s, [0.92], max)
        M['thigh_upper_' + s] = limb('thigh_' + s, 'calf_' + s, 'thigh_' + s, np.arange(0.12, 0.3, 0.03), max)
        M['thigh_mid_' + s] = limb('thigh_' + s, 'calf_' + s, 'thigh_' + s, [0.5], max)
        M['knee_' + s] = limb('thigh_' + s, 'calf_' + s, 'thigh_' + s, [0.95], max)
        M['calf_max_' + s] = limb('calf_' + s, 'foot_' + s, 'calf_' + s, np.arange(0.1, 0.5, 0.04), max)
        M['ankle_' + s] = limb('calf_' + s, 'foot_' + s, 'calf_' + s, [0.9], min)
    # arm span from the bone chain (joint to joint + hand to middle finger tip + 1 cm pad)
    def chain(s):
        names = ['upperarm_', 'lowerarm_', 'hand_', 'middle_metacarpal_', 'middle_01_', 'middle_02_', 'middle_03_']
        P = [bones[n + s] for n in names if n + s in bones]; L = sum(float(np.linalg.norm(P[i + 1] - P[i])) for i in range(len(P) - 1))
        tip = V[np.array([d == 'hand_' + s for d in DOM])]; far = float(np.linalg.norm(tip - bones['hand_' + s], axis=1).max())
        return L, far
    cl, fl = chain('l'); cr, fr_ = chain('r')
    hc = ['hand_l', 'middle_metacarpal_l', 'middle_01_l', 'middle_02_l', 'middle_03_l']; hl = sum(float(np.linalg.norm(bones[hc[i + 1]] - bones[hc[i]])) for i in range(4)) + 2.2
    M['hand_length_chain'] = round(hl, 1); M['hand_len_ratio'] = round(hl / H, 3)
    M['arm_len_joint_to_fingertip_l'] = round(float(np.linalg.norm(bones['lowerarm_l'] - bones['upperarm_l']) + np.linalg.norm(bones['hand_l'] - bones['lowerarm_l'])) + hl, 1)
    M['arm_span'] = round(M['shoulder_joint_dist'] + 2 * M['arm_len_joint_to_fingertip_l'], 1); M['arm_span_ratio'] = round(M['arm_span'] / H, 3)
    M['upperarm_bone'] = round(float(np.linalg.norm(bones['lowerarm_l'] - bones['upperarm_l'])), 1); M['forearm_bone'] = round(float(np.linalg.norm(bones['hand_l'] - bones['lowerarm_l'])), 1)

    foot = V[np.array([d.startswith('foot_l') for d in DOM])]; fl2 = fw(foot); M['foot_length'] = round(float(fl2.max() - fl2.min()), 1); M['foot_len_ratio'] = round(M['foot_length'] / H, 3)
    M['scale_168'] = round(H / 168.0, 4)
    return M
# ---------------------------------------------------------------- render (workbench clay, orthographic)
def build(name, V, T):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in V], [], [tuple(t) for t in T]); me.update()
    for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); return o
def render(tag, V, FVx):
    sc = bpy.context.scene
    for o in list(sc.collection.objects): bpy.data.objects.remove(o)
    build('body', V, T0); build('head', FVx, FT)
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.72, 0.68, 0.64)
    sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'BOTH'; sc.render.resolution_x = 700; sc.render.resolution_y = 1400; sc.render.film_transparent = False
    try: sc.world.color = (0.32, 0.30, 0.31)
    except Exception: pass
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.ortho_scale = 200.0
    cz = (V[:, 2].min() + FVx[:, 2].max()) / 2; c = np.array([mid[0], mid[1], cz])
    for view, d in (('front', f), ('side', -lv), ('back', -f), ('front34', (f - lv) / np.linalg.norm(f - lv))):
        pos = c + d * 600; cam.location = Vector(pos.tolist()); dirv = Vector((-d).tolist()); cam.rotation_euler = dirv.to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(OUT, 'clay_%s_%s.png' % (tag, view)); bpy.ops.render.render(write_still=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
if bpy.context.scene.world is None: bpy.context.scene.world = bpy.data.worlds.new('w')
Mb = measure(V0, 'before'); json.dump(Mb, open(os.path.join(OUT, 'measure_before.json'), 'w'), indent=1)
log('MEASURE before', json.dumps({k: v for k, v in Mb.items() if k != 'torso_profile'}))
if A.get('render'): render('before', V0, FV)
if A.get('mode') == 'shape':
    exec(open(A['shape_script']).read())
log('B4_DONE'); LOG.close()
open(os.path.join(OUT, 'done_%s.txt' % A.get('tag', 'x')), 'w').write('ok')
