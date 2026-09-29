"""SPHIRUS first production outfit (home / everyday): ivory long-sleeve Henley + charcoal drawstring trousers.
Blender 5.2 background:  blender -b --factory-startup --python blender_outfit_build.py -- <sculpt_package.json.gz> <out_dir>

Garment construction (pattern logic, not body inflation):
  Henley  = front/back body panels joined at shoulder + side seams (one closed shell with armholes + neck opening),
            set-in sleeve tubes, centre-front placket slit; ease: chest +10, waist +14, hem +12, sleeve +8 cm.
  Trousers= hip shell (waistband row -> crotch ring) + two leg tubes joined along a sagittal crotch seam;
            ease: waistband +4 (gathered), hip +12, thigh +13, hem straight 47 cm.
Both are draped with Blender cloth simulation against the exact current BR body (collision), then the construction
details (neck binding, placket, buttons, cuffs, hem, waistband layer, eyelets, drawstring, pocket welts) are built on the
settled cloth. Output: JSON (UE cm) with positions / triangles / per-vertex UVs / material ids per garment, a QA json
(clearance, penetrations), the .blend, and preview renders. The body is never modified."""
import bpy, bmesh, sys, os, json, gzip, math, time
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index('--')+1:]; PKG, OUT = argv[0], argv[1]; os.makedirs(OUT, exist_ok=True)
T0 = time.time()
def log(*a): print('[outfit %6.1fs]' % (time.time()-T0), *a, flush=True)
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)     # factory scene: cube / light / camera
RES = float(os.environ.get('SPH_RES', '1.5'))                                       # column/row density multiplier
HEN_SELFCOL = os.environ.get('SPH_HEN_SELFCOL', '1') == '1'
SLEEVE_EASE = float(os.environ.get('SPH_SLEEVE_EASE', '1.0'))                        # multiplier on the sleeve ease profile
ARMPIT_EASE = float(os.environ.get('SPH_ARMPIT_EASE', '5.0'))                      # fitted armhole: underarm fabric follows the arm/armpit skin blend
CAP_PIN = float(os.environ.get('SPH_CAP_PIN', '0.0'))                                # pin weight for the first sleeve rings
P = json.loads(gzip.open(PKG, 'rb').read()); NB, NH = P['NB'], P['NH']
BODY = np.asarray(P['br_neutral'], np.float64)                       # UE cm, x = character left, y = front, z = up
TRI = np.asarray([list(t) for t in P['body']['triangles']]+[[a+NB, b+NB, c+NB] for a, b, c in P['head']['triangles']], np.int64)
W = P['weights']
def chain(u, pre): return sum(x for b, x in W[u].items() if b.startswith(pre))
ARM = ('upperarm', 'lowerarm', 'hand', 'wrist', 'thumb', 'index', 'middle', 'ring', 'pinky')
LEG = ('thigh', 'calf', 'foot', 'ball', 'ankle', 'bigtoe', 'indextoe', 'middletoe', 'ringtoe', 'littletoe')
armw = np.asarray([chain(u, ARM) for u in range(NB+NH)]); legw = np.asarray([chain(u, LEG) for u in range(NB+NH)])
BIND = P['skeleton']['Body']['bind']; J = lambda n: np.asarray(BIND[n]['translation'])
S = 0.01
def bl(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]*S, -p[..., 1]*S, p[..., 2]*S], -1)
def ue(p): p = np.asarray(p, np.float64); return np.stack([p[..., 0]/S, -p[..., 1]/S, p[..., 2]/S], -1)

# ============================================================ body helpers ============================================
def hull2d(pts):
    pts = sorted(set(map(tuple, np.round(pts, 4))))
    if len(pts) < 3: return np.asarray(pts)
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return np.asarray(lo[:-1]+up[:-1])
def circ(h): return float(np.sum(np.linalg.norm(np.roll(h, -1, 0)-h, axis=1))) if len(h) > 2 else 0.0
HEADC = np.arange(NB+NH) >= NB
TORSO = (armw < 0.3) & (legw < 0.5) & (np.arange(NB+NH) < NB)
lowarm = np.asarray([chain(u, ('lowerarm', 'hand', 'wrist', 'thumb', 'index', 'middle', 'ring', 'pinky')) for u in range(NB+NH)])
SHOULDER = (lowarm < 0.2) & (np.arange(NB+NH) < NB) & (BODY[:, 2] > 112)     # torso + deltoid/upper arm: used for the strip/shoulder surface sampling
HEADC = np.arange(NB+NH) >= NB
def section(z, mask, half=0.6):
    sel = mask & (np.abs(BODY[:, 2]-z) < half); return BODY[sel][:, :2]
def radial_fn(pts2, centre):
    """convex hull of a section as a radial function r(theta), theta from +y (front) toward +x (left)"""
    h = hull2d(pts2); d = h-centre; th = np.arctan2(d[:, 0], d[:, 1]) % (2*np.pi); r = np.linalg.norm(d, axis=1)
    o = np.argsort(th); th, r = th[o], r[o]
    th = np.concatenate([th-2*np.pi, th, th+2*np.pi]); r = np.concatenate([r, r, r])
    return lambda t: np.interp(np.asarray(t) % (2*np.pi), th, r)
def torso_ring(z, ease_cm, mask=TORSO, centre=None):
    pts = section(z, mask); c = centre if centre is not None else pts.mean(0); f = radial_fn(pts, c)
    return c, f, ease_cm/(2*np.pi)
bvh = BVHTree.FromPolygons([Vector(bl(p)) for p in BODY], [list(t) for t in TRI])
def surf_y(x, z, face, mask=TORSO, r=0.8):
    """front / back body surface y at (x, z): samples only the matching half-space about the section centre, so a
    front sample can never land on the back surface (e.g. above the clavicle where there is no front surface)"""
    sel = mask & (np.abs(BODY[:, 0]-x) < r) & (np.abs(BODY[:, 2]-z) < r)
    if not sel.any(): return None
    pts = section(z, mask, half=1.5); cy = float(pts[:, 1].mean()) if len(pts) else 0.0
    ys = BODY[sel][:, 1]; ys = ys[ys > cy] if face == 'front' else ys[ys < cy]
    if len(ys) == 0: return None
    return float(ys.max() if face == 'front' else ys.min())

# key body facts
z_crotch = float(BODY[(np.abs(BODY[:, 0]) < 1.0) & (BODY[:, 2] > 55) & (BODY[:, 2] < 92)][:, 2].min())
ap = BODY[(armw > 0.25) & (armw < 0.75) & (np.abs(BODY[:, 0]) < 22) & (BODY[:, 2] > 115)]
z_armpit = float(np.percentile(ap[:, 2], 3))
sh_l = J('upperarm_l'); el_l = J('lowerarm_l'); wr_l = J('hand_l')
hip_l = J('thigh_l'); kn_l = J('calf_l'); an_l = J('foot_l')
def ridge(x):  # top of the shoulder / trapezius at |x|: (y, z) of the highest body point in a thin x slab (neck excluded)
    sel = (np.abs(BODY[:, 0]-x) < 0.6) & (BODY[:, 2] > 125) & (BODY[:, 2] < (145.5 if abs(x) < 9 else 150)) & (((np.arange(NB+NH) < NB) & (armw < 0.85)) | HEADC) & (BODY[:, 1] > -5.0)   # the trapezius top near the neck is head-owned (collar)
    p = BODY[sel]; i = np.argmax(p[:, 2]); return float(p[i, 1]), float(p[i, 2])
facts = {'z_crotch': z_crotch, 'z_armpit': z_armpit, 'shoulder_joint_l': sh_l.tolist(), 'elbow_l': el_l.tolist(), 'wrist_l': wr_l.tolist(),
         'hip_l': hip_l.tolist(), 'knee_l': kn_l.tolist(), 'ankle_l': an_l.tolist(),
         'circ': {f'torso_z{z}': round(circ(hull2d(section(z, TORSO))), 2) for z in (86, 92, 97, 102, 109, 119, 128, 134)},
         'ridge': {x: ridge(x) for x in (0, 4, 7, 10, 13, 16)}}
log('facts', json.dumps(facts))

# ============================================================ mesh builder =============================================
class MeshBuilder:
    def __init__(s): s.v = []; s.f = []; s.uv = []; s.mat = []; s.groups = {}; s.pin = {}
    def add(s, p): s.v.append([float(p[0]), float(p[1]), float(p[2])]); return len(s.v)-1
    def quad(s, a, b, c, d, uvs, m=0):
        if len({a, b, c, d}) < 4:
            ids = [a, b, c, d]; uu = list(uvs); keep = []
            for i in range(4):
                if ids[i] not in [ids[j] for j in keep]: keep.append(i)
            if len(keep) < 3: return
            s.f.append([ids[i] for i in keep]); s.uv.append([uu[i] for i in keep]); s.mat.append(m); return
        s.f.append([a, b, c, d]); s.uv.append(list(uvs)); s.mat.append(m)
    def group(s, name, ids, w=1.0):
        g = s.groups.setdefault(name, {})
        for i in ids: g[int(i)] = max(g.get(int(i), 0.0), float(w))
    def to_object(s, name, mats):
        me = bpy.data.meshes.new(name+'_Mesh')
        me.from_pydata([tuple(bl(p)) for p in s.v], [], s.f)
        for m in mats: me.materials.append(m)
        me.polygons.foreach_set('material_index', np.asarray(s.mat, np.int32))
        uvl = me.uv_layers.new(name='UVMap'); k = 0
        for poly, uvs in zip(me.polygons, s.uv):
            for li, uvc in zip(poly.loop_indices, uvs): uvl.data[li].uv = (uvc[0], uvc[1])
        for p_ in me.polygons: p_.use_smooth = True
        me.validate(); me.update()
        # consistent face orientation (angular bending needs coherent windings), normals pointing away from the garment axis
        bm = bmesh.new(); bm.from_mesh(me)
        # close small construction gaps (armhole/strip junctions): boundary loops shorter than 20 edges
        bd = [e for e in bm.edges if e.is_boundary]; adj = {}
        for e in bd:
            for v in e.verts: adj.setdefault(v, []).append(e)
        seen = set(); small = []
        for e0 in bd:
            if e0 in seen: continue
            comp = []; st = [e0]
            while st:
                e = st.pop()
                if e in seen: continue
                seen.add(e); comp.append(e)
                for v in e.verts: st.extend(x for x in adj[v] if x not in seen)
            if len(comp) < 20: small.append(comp)
        for comp in (small if name in ('SPH_Henley', 'SPH_Trousers') else []):
            try: bmesh.ops.holes_fill(bm, edges=comp, sides=len(comp))
            except Exception as ex: log('hole fill failed', len(comp), ex)
        if small and name in ('SPH_Henley', 'SPH_Trousers'): log(name, 'closed', len(small), 'small gaps', [len(c) for c in small])
        elif small: small = []
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
        cen = np.asarray([tuple(v.co) for v in me.vertices]).mean(0); score = 0.0
        for p_ in me.polygons:
            c = np.asarray(p_.center); d = c-cen; d[2] = 0; score += float(np.dot(np.asarray(p_.normal), d))
        if score < 0:
            bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.reverse_faces(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); me.update()
        log(name, 'faces oriented, outward score', round(score, 3), 'flipped' if score < 0 else '')
        ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
        for gname, d in s.groups.items():
            vg = ob.vertex_groups.new(name=gname)
            byw = {}
            for i, w in d.items(): byw.setdefault(w, []).append(i)
            for w, ids in byw.items(): vg.add(ids, w, 'REPLACE')
        return ob
def mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name); m.diffuse_color = (*rgb, 1); m.roughness = 0.9; return m
M_HEN = mat('M_Henley', (0.80, 0.74, 0.64)); M_HEN_TRIM = mat('M_Henley_Trim', (0.78, 0.72, 0.62)); M_BTN = mat('M_Buttons', (0.55, 0.45, 0.35))
M_TRS = mat('M_Trousers', (0.16, 0.16, 0.17)); M_TRS_TRIM = mat('M_Trousers_Trim', (0.15, 0.15, 0.16)); M_CORD = mat('M_Drawstring', (0.42, 0.36, 0.30))

# UV layout (0..1). Each island is a rectangle: (u0, v0, u1, v1). Texel density: 2048 px over ~1.45 m of fabric => 0.7 mm/px.
UV = {'henley': {'front': (0.02, 0.02, 0.40, 0.62), 'back': (0.42, 0.02, 0.80, 0.62), 'sleeve_l': (0.02, 0.64, 0.30, 0.98), 'sleeve_r': (0.32, 0.64, 0.60, 0.98),
                 'binding': (0.62, 0.64, 0.98, 0.70), 'placket': (0.62, 0.72, 0.98, 0.80), 'cuffs': (0.62, 0.82, 0.98, 0.88), 'hem': (0.62, 0.90, 0.98, 0.96), 'buttons': (0.82, 0.02, 0.98, 0.18)},
      'trousers': {'hip_front': (0.02, 0.70, 0.40, 0.98), 'hip_back': (0.42, 0.70, 0.80, 0.98), 'leg_l': (0.02, 0.02, 0.40, 0.68), 'leg_r': (0.42, 0.02, 0.80, 0.68),
                   'band': (0.82, 0.70, 0.98, 0.80), 'welts': (0.82, 0.82, 0.98, 0.88), 'hems': (0.82, 0.90, 0.98, 0.96), 'cord': (0.82, 0.02, 0.98, 0.30), 'crotch': (0.82, 0.32, 0.98, 0.68)}}
def uvmap(rect, u, v):  # u, v in 0..1 inside the island
    u0, v0, u1, v1 = rect; return (u0+(u1-u0)*u, v0+(v1-v0)*v)

# ============================================================ HENLEY ==================================================
N = int(64*RES)//2*2                     # columns around the torso (theta = 2*pi*i/N, 0 = centre front, pi/2 = left side)
EASE = {'hem': 20.0, 'hip': 19.0, 'waist': 14.0, 'chest': 10.0, 'armpit': ARMPIT_EASE}   # hem/hip: the shirt hangs OUTSIDE the trouser shell
z_hem_side, z_hem_back = 93.5, 94.0
z_tuck = 102.5                            # centre-front hem caught inside the trouser waistband
z_ap_g = z_armpit-1.2                     # garment armhole bottom (close to the body armpit)
ROWS_LOW = int(22*RES); ROWS_UP = int(8*RES)
def ease_at(z):
    zs = [90, 101, 106, 112, 119, 128, z_ap_g]; es = [EASE['hem'], EASE['hip'], EASE['waist']+1, EASE['waist'], EASE['waist']-1, EASE['chest'], EASE['armpit']]
    return float(np.interp(z, zs, es))
hen = MeshBuilder(); front_uv = UV['henley']['front']; back_uv = UV['henley']['back']
th = 2*np.pi*np.arange(N)/N
def tuck_w(t):  # 1 at centre front -> 0 beyond +-48 deg (smoothstep)
    a = np.abs(((t+np.pi) % (2*np.pi))-np.pi); x = np.clip(1-a/np.radians(58), 0, 1); return float(x*x*(3-2*x))
def hem_z(t):  # partial tuck: centre front rises into the waistband, sides/back relaxed
    a = np.abs(((t+np.pi) % (2*np.pi))-np.pi)          # 0 at centre front .. pi at centre back
    base = z_hem_side+(z_hem_back-z_hem_side)*np.clip((a-np.pi/2)/(np.pi/2), 0, 1); return float(base+(z_tuck-base)*tuck_w(t))
def torso_point(t, z, rad_shrink=0.0):
    c, f, g = torso_ring(z, ease_at(z)); r = f(t)+g-rad_shrink
    return np.array([c[0]+r*np.sin(t), c[1]+r*np.cos(t), z])
lower = np.zeros((ROWS_LOW+1, N), np.int64)
for j in range(ROWS_LOW+1):
    s = j/ROWS_LOW
    for i, t in enumerate(th):
        z_row = z_hem_side+(z_ap_g-z_hem_side)*s          # horizontal rows (columns never cross)
        tuck = tuck_w(t)*max(0.0, 1-s*3.0)**2
        p = torso_point(t, z_row, rad_shrink=0.7*tuck)  # tucked part sits closer to the body (under the band)
        p[2] += (hem_z(t)-z_hem_side)*(1-s)**1.5         # partial tuck / back drop as a smooth vertical shift
        lower[j, i] = hen.add(p)
def uv_torso(i, s):  # split at the sides into front / back islands
    t = th[i % N]; a = ((t+np.pi/2) % (2*np.pi))       # 0 .. 2pi starting at the right side going through front
    if a <= np.pi+1e-9: return uvmap(front_uv, a/np.pi, s*0.72)
    return uvmap(back_uv, (a-np.pi)/np.pi, s*0.72)
for j in range(ROWS_LOW):
    for i in range(N):
        i2 = (i+1) % N
        uvs = [uv_torso(i, j/ROWS_LOW), uv_torso(i+1 if i2 else N, j/ROWS_LOW), uv_torso(i+1 if i2 else N, (j+1)/ROWS_LOW), uv_torso(i, (j+1)/ROWS_LOW)]
        hen.quad(lower[j, i], lower[j, i2], lower[j+1, i2], lower[j+1, i], uvs, 0)
# strips above the armpit: columns whose armpit-ring x lies inside the armhole width
c_ap, f_ap, g_ap = torso_ring(z_ap_g, ease_at(z_ap_g)); x_ap = c_ap[0]+(f_ap(th)+g_ap)*np.sin(th); y_ap = c_ap[1]+(f_ap(th)+g_ap)*np.cos(th)
X_SH = 16.8                      # shoulder point (dropped 1.3 cm past the acromion)
X_NECK = 6.6
strip_front = [i for i in range(N) if (th[i] <= np.pi/2 or th[i] >= 3*np.pi/2) and abs(x_ap[i]) <= X_SH*0.93]
strip_back = [i for i in range(N) if (np.pi/2 < th[i] < 3*np.pi/2) and abs(x_ap[i]) <= X_SH*0.93]
def shoulder_line(x):  # (y, z) on the garment shoulder seam at |x|
    y, z = ridge(min(abs(x), 16.0)); return y-0.3, z+0.15
NECKM = ((np.arange(NB+NH) < NB) | HEADC) & (armw < 0.05) & (legw < 0.05) & (BODY[:, 2] > 134) & (BODY[:, 2] < 152) & (np.abs(BODY[:, 0]) < 9.5)
def neck_rim(xt, z, side, gap=1.8):
    """point of the neckline at height z with x = xt: on the neck section (hull) + gap, front or back half"""
    pts = section(z, NECKM, half=0.8)
    if len(pts) < 6: pts = section(z, NECKM, half=1.6)
    c = pts.mean(0); f = radial_fn(pts, c); ang = np.linspace(0, np.pi/2, 91) if side == 'front' else np.linspace(np.pi/2, np.pi, 91)
    sg = 1 if xt >= 0 else -1; xs = c[0]+(f(ang)+gap)*np.sin(ang)*sg; k = int(np.argmin(np.abs(xs-xt)))
    return float(c[1]+(f(ang[k])+gap)*np.cos(ang[k]))
def neck_front(x): return 137.2+(shoulder_line(X_NECK)[1]-137.2)*(abs(x)/X_NECK)**2
def neck_back(x): return 141.6+(shoulder_line(X_NECK)[1]-141.6)*(abs(x)/X_NECK)**2
top_index = {}                   # merged shoulder vertices keyed by rounded x
upper = {}                       # (i) -> list of ROWS_UP vertex ids (row 1..ROWS_UP above the armpit)
for side, cols in (('front', strip_front), ('back', strip_back)):
    xs_ap = np.asarray([x_ap[i] for i in cols]); xmax = np.abs(xs_ap).max()
    for i in cols:
        xt = x_ap[i]/xmax*X_SH                         # top x of this column (maps strip edge -> shoulder point)
        neck = abs(xt) < X_NECK
        if neck: z_top = neck_front(xt) if side == 'front' else neck_back(xt); y_top = None
        else: y_top, z_top = shoulder_line(xt)
        rows = []
        for j in range(1, ROWS_UP+1):
            s = j/ROWS_UP; x = x_ap[i]+(xt-x_ap[i])*s; z = z_ap_g+(z_top-z_ap_g)*s
            gap = 1.6*(1-s)+(1.7 if neck else 0.9)*s
            yb = surf_y(x, min(z, z_top-0.5) if not neck else z, side, mask=SHOULDER | HEADC, r=1.0)
            rows.append([x, (yb+gap if side == 'front' else yb-gap) if yb is not None else None, z])
        if neck:  # neckline: the neck rim (section + gap); rows near the top blend from the chest/back sample to the rim
            yr = neck_rim(xt, z_top, side); rows[-1][1] = yr
            for j in range(len(rows)-1):
                sj = (j+1)/ROWS_UP; w = max(0.0, (sj-0.55)/0.45)**1.5
                if rows[j][1] is not None: rows[j][1] = rows[j][1]*(1-w)+yr*w
        else: rows[-1] = [xt, y_top, z_top]
        # fill missing samples by interpolation between the armpit ring point and the nearest sampled rows (smooth columns)
        ys = [y_ap[i]]+[r_[1] for r_ in rows]; idx = [k for k, y in enumerate(ys) if y is not None]
        assert ys[-1] is not None, ('column top unresolved', side, i)
        for k in range(len(ys)):
            if ys[k] is None:
                lo = max(q for q in idx if q < k); hi = min(q for q in idx if q > k); ys[k] = ys[lo]+(ys[hi]-ys[lo])*(k-lo)/(hi-lo)
        ys = [y_ap[i]]+list(np.convolve(ys[1:], [0.25, 0.5, 0.25], 'same')[:-1])+[ys[-1]]  # light smoothing along the column
        ids = []
        for j, (x, _, z) in enumerate(rows):
            if not neck and j == ROWS_UP-1:
                # shared shoulder seam: reuse the nearest existing top vertex on this side of the seam (|dx| < 1.2 cm)
                sg = 1 if xt > 0 else -1; cands = [(abs(k[0]-abs(xt)), k) for k in top_index if k[1] == sg and abs(k[0]-abs(xt)) < 1.2]
                if cands: key = min(cands)[1]
                else: key = (abs(xt), sg); top_index[key] = hen.add([xt, y_top, z_top])
                ids.append(top_index[key]); continue
            ids.append(hen.add([x, ys[j+1], z]))
        upper[i] = ids
    # faces between adjacent strip columns
    cols_s = sorted(cols, key=lambda i: th[i] if side == 'back' else ((th[i]+np.pi) % (2*np.pi)))
    for a, b in zip(cols_s, cols_s[1:]):
        col_a = [lower[ROWS_LOW, a]]+upper[a]; col_b = [lower[ROWS_LOW, b]]+upper[b]
        for j in range(ROWS_UP):
            sa, sb = 0.72+0.28*j/ROWS_UP, 0.72+0.28*(j+1)/ROWS_UP
            ua = ((th[a]+np.pi/2) % (2*np.pi)); ub = ((th[b]+np.pi/2) % (2*np.pi))
            if side == 'front': uva, uvb = ua/np.pi, ub/np.pi; rect = front_uv
            else: uva, uvb = (ua-np.pi)/np.pi, (ub-np.pi)/np.pi; rect = back_uv
            hen.quad(col_a[j], col_b[j], col_b[j+1], col_a[j+1], [uvmap(rect, uva, sa), uvmap(rect, uvb, sa), uvmap(rect, uvb, sb), uvmap(rect, uva, sb)], 0)
# centre-front placket slit: split column 0 from the neckline down to z_slit
z_slit = 124.0
col0 = [lower[ROWS_LOW, 0]]+upper[0]
slit_pairs = []
vpos = np.asarray(hen.v)
for k, vid in enumerate(col0):
    if vpos[vid, 2] < z_slit: continue
    dup = hen.add(vpos[vid]); slit_pairs.append((vid, dup))
    # faces on the wearer's right (theta just below 2pi) use the duplicate
    for fi, face in enumerate(hen.f):
        if vid in face:
            others = [hen.v[x] for x in face if x != vid]; mx = np.mean([o[0] for o in others])
            if mx < 0: hen.f[fi] = [dup if x == vid else x for x in face]
# opened top: the two edges of the slit part above the 3rd button (V opening)
for vid, dup in slit_pairs:
    z = hen.v[vid][2]; o = 1.9*np.clip((z-129.5)/(neck_front(0)-129.5), 0, 1)
    hen.v[vid][0] += o; hen.v[dup][0] -= o
# sleeves: armhole loop -> tube along the arm
def armhole_loop(sign):
    """ordered boundary loop of the armhole: front strip edge (bottom->top), shoulder point, back strip edge (top->bottom), armpit arc"""
    fcols = [i for i in strip_front if np.sign(x_ap[i]) == sign]; bcols = [i for i in strip_back if np.sign(x_ap[i]) == sign]
    fe = max(fcols, key=lambda i: abs(x_ap[i])); be = max(bcols, key=lambda i: abs(x_ap[i]))
    loop = [lower[ROWS_LOW, fe]]+upper[fe]                      # up the front edge to the shoulder point (merged vertex)
    loop += list(reversed(upper[be]))[1:]+[lower[ROWS_LOW, be]]  # down the back edge
    arc = [i for i in range(N) if i not in strip_front and i not in strip_back and np.sign(x_ap[i]) == sign]
    arc = sorted(arc, key=lambda i: th[i] if sign > 0 else -((th[i]+np.pi) % (2*np.pi)))
    arc = arc if sign > 0 else arc
    # order arc from the back edge towards the front edge along the armpit ring
    if sign > 0: arc = sorted(arc, key=lambda i: -th[i])
    else: arc = sorted(arc, key=lambda i: -((th[i]+np.pi) % (2*np.pi)))
    loop += [lower[ROWS_LOW, i] for i in arc]
    return loop
def sleeve(sign):
    loop = armhole_loop(sign)
    sh, el, wr = (sh_l, el_l, wr_l) if sign > 0 else (sh_l*[-1, 1, 1], el_l*[-1, 1, 1], wr_l*[-1, 1, 1])
    axis1 = (el-sh)/np.linalg.norm(el-sh); axis2 = (wr-el)/np.linalg.norm(wr-el)
    def basis(ax):
        u = np.cross(ax, [0, 0, 1.0]); u /= np.linalg.norm(u); v = np.cross(ax, u); return u, v
    u1, v1 = basis(axis1)
    lp = vpos_now()[loop]; rel = lp-sh; phi = np.arctan2(rel @ v1, rel @ u1)
    order = np.argsort(phi); loop = [loop[i] for i in order]; lp = lp[order]; phi = phi[order]   # monotonic cycle about the arm axis
    L = len(loop); loop_c = lp.mean(0); d0 = max(0.0, float((loop_c-sh) @ axis1))
    if os.environ.get('SPH_DEBUG_LOOP'):
        for j in range(L): log('LOOP', sign, j, loop[j], np.round(lp[j], 1).tolist(), round(float(np.degrees(phi[j])), 1), 'edge %.1f' % np.linalg.norm(lp[j]-lp[(j+1) % L]))
    L1 = np.linalg.norm(el-sh); L2 = np.linalg.norm(wr-el)-0.5      # cuff ends at the wrist joint (the hand base is wider)
    K = int(20*RES); rings = [loop]; CAP = 7
    handw = np.asarray([chain(u, ('hand', 'thumb', 'index', 'middle', 'ring', 'pinky', 'wrist')) for u in range(NB+NH)])
    def arm_circ(c, ax, wrist=False):  # body circumference of the arm section at c (wrist: forearm-only sample, no hand/thumb)
        d = (BODY-c) @ ax; sel = (np.abs(d) < 0.7) & (armw > (0.2 if np.linalg.norm(c-sh) < 12 else 0.5)) & (np.sign(BODY[:, 0]) == sign) & (BODY[:, 2] < 146)
        if wrist: sel &= handw < 0.35
        p = BODY[sel]; b = np.stack(basis(ax), 1); q = (p-c) @ b; return circ(hull2d(q)) if len(q) > 5 else 30.0
    wrist_c = max(arm_circ(el+axis2*(L2-k), axis2, wrist=True) for k in (0.0, 1.0, 2.0))   # widest section at the cuff position
    uvr = UV['henley']['sleeve_l' if sign > 0 else 'sleeve_r']
    for k in range(1, K+1):
        s = k/K; d = d0+s*(L1+L2-d0)
        if d <= L1: c = sh+axis1*d
        else: c = el+axis2*(d-L1)
        w = np.clip((d-L1+6)/12, 0, 1); ax = axis1*(1-w)+axis2*w; ax /= np.linalg.norm(ax); u, v = basis(ax)
        ease = SLEEVE_EASE*np.interp(s, [0, 0.25, 0.55, 0.8, 0.93, 1.0], [7.0, 8.5, 10.0, 9.5, 7.0, 5.0])   # fitted cap, relaxed forearm
        base_c = arm_circ(c, ax) if s < 0.85 else min(arm_circ(c, ax), wrist_c+2.0*(1-s)/0.15)
        r = (base_c+ease)/(2*np.pi)   # snug knit cuff at the wrist
        mix = min(1.0, k/CAP)
        ring = []
        for j in range(L):
            phi_u = phi[0]+2*np.pi*j/L; ph = phi[j]*(1-mix)+phi_u*mix
            circle = c+u*r*np.cos(ph)+v*r*np.sin(ph)
            extr = lp[j]+axis1*(d-d0)                       # armhole shape carried along the arm (sleeve cap)
            ring.append(hen.add(extr*(1-mix)+circle*mix))
        rings.append(ring)
    for k in range(K):
        for j in range(L):
            j2 = (j+1) % L
            uvs = [uvmap(uvr, j/L, k/K), uvmap(uvr, (j+1)/L, k/K), uvmap(uvr, (j+1)/L, (k+1)/K), uvmap(uvr, j/L, (k+1)/K)]
            hen.quad(rings[k][j], rings[k][j2], rings[k+1][j2], rings[k+1][j], uvs, 0)
    return rings
def vpos_now(): return np.asarray(hen.v)
sl_l = sleeve(+1); sl_r = sleeve(-1)
# groups: pins and detail anchors
hen.group('PIN', list(top_index.values()), 0.3)   # shoulder seam half-pinned: settles onto the trapezius without a ridge
neck_ids = [upper[i][-1] for i in strip_front+strip_back if abs(x_ap[i]/max(abs(x_ap[k]) for k in (strip_front if i in strip_front else strip_back))*X_SH) < X_NECK]
hen.group('PIN', neck_ids, 1.0); hen.group('NECK', neck_ids+[d for _, d in slit_pairs if hen.v[d][2] > neck_front(0)-0.5])
# the neckline ring closes over the innermost shoulder-seam vertex on each side (not the whole seam)
for sg in (1, -1):
    ks = [k for k in top_index if k[1] == sg]
    if ks: hen.group('NECK', [top_index[min(ks)]])
tuck_ids = [lower[j, i] for j in range(0, 3) for i in range(N) if hem_z(th[i]) > z_hem_side+2]
hen.group('PIN', tuck_ids, 1.0); hen.group('TUCK', tuck_ids)
hen.group('PIN', [v for pr in slit_pairs for v in pr], 0.6); hen.group('SLIT_L', [a for a, _ in slit_pairs]); hen.group('SLIT_R', [b for _, b in slit_pairs])
hen.group('HEM', [lower[0, i] for i in range(N)]); hen.group('CUFF_L', sl_l[-1]); hen.group('CUFF_R', sl_r[-1])
# knit cuffs stay at the wrist (the solver's friction cannot hold a tube on the downward A-pose arm): pin the last two rings
hen.group('PIN', sl_l[-1]+sl_r[-1], 1.0); hen.group('PIN', sl_l[-2]+sl_r[-2], 0.5)
hen.group('SLEEVE_L', [v for r in sl_l[1:] for v in r]); hen.group('SLEEVE_R', [v for r in sl_r[1:] for v in r])
if CAP_PIN > 0: hen.group('PIN', [v for rings in (sl_l, sl_r) for r in rings[1:3] for v in r], CAP_PIN)
hen_ob = hen.to_object('SPH_Henley', [M_HEN]); log('henley built', len(hen.v), 'verts', len(hen.f), 'faces')

# ============================================================ TROUSERS ================================================
trs = MeshBuilder(); NT = int(64*RES)//4*4; tht = 2*np.pi*np.arange(NT)/NT
z_band_top, z_band_bot = 103.5, 100.0; z_cr_ring = 80.0; z_hem_t = 6.0
crotch_g = z_crotch-4.5
def t_ease(z): return float(np.interp(z, [z_cr_ring, 86, 94, 99, z_band_bot, z_band_top], [14.0, 12.0, 11.0, 9.0, 7.0, 7.0]))   # soft band: 7 cm ease, cinched by the drawstring
def hip_point(t, z, ease=None):
    c, f, g = torso_ring(z, t_ease(z) if ease is None else ease, mask=(legw < 0.9) & (armw < 0.3) & (np.arange(NB+NH) < NB)); r = f(t)+g
    return np.array([c[0]+r*np.sin(t), c[1]+r*np.cos(t), z])
ROWS_BAND = 3; ROWS_HIP = int(12*RES)+ROWS_BAND          # rows 0..ROWS_BAND = waistband (pinned), then the hip shell
hip = np.zeros((ROWS_HIP+1, NT), np.int64)
for j in range(ROWS_HIP+1):
    z = z_band_top+(z_band_bot-z_band_top)*j/ROWS_BAND if j <= ROWS_BAND else z_band_bot+(z_cr_ring-z_band_bot)*(j-ROWS_BAND)/(ROWS_HIP-ROWS_BAND)
    for i, t in enumerate(tht): hip[j, i] = trs.add(hip_point(t, z))
hf, hb = UV['trousers']['hip_front'], UV['trousers']['hip_back']
def uv_hip(i, s):
    a = ((tht[i % NT]+np.pi/2) % (2*np.pi))
    if a <= np.pi+1e-9: return uvmap(hf, a/np.pi, 1-s)
    return uvmap(hb, (a-np.pi)/np.pi, 1-s)
for j in range(ROWS_HIP):
    for i in range(NT):
        i2 = (i+1) % NT; iu = i+1 if i2 else NT
        trs.quad(hip[j, i], hip[j, i2], hip[j+1, i2], hip[j+1, i], [uv_hip(i, j/ROWS_HIP), uv_hip(iu, j/ROWS_HIP), uv_hip(iu, (j+1)/ROWS_HIP), uv_hip(i, (j+1)/ROWS_HIP)], 0)
# crotch seam curve (sagittal, shared by both legs at the crotch row): front ring point -> under the body -> back ring point
NI = int(9*RES)
pf = np.asarray(trs.v[hip[ROWS_HIP, 0]]); pb = np.asarray(trs.v[hip[ROWS_HIP, NT//2]])
def body_sag(z, face):  # sagittal body outline at |x|<1 (crotch region)
    sel = (np.abs(BODY[:, 0]) < 1.2) & (np.abs(BODY[:, 2]-z) < 0.8) & (np.arange(NB+NH) < NB)
    if not sel.any(): return None
    ys = BODY[sel][:, 1]; return float(ys.max() if face == 'front' else ys.min())
crotch_pts = []
for k in range(1, NI+1):
    s = k/(NI+1); ang = np.pi*s      # 0 = front, pi = back
    z = z_cr_ring-(z_cr_ring-crotch_g)*np.sin(ang)
    if s < 0.5: yb = body_sag(max(z, z_crotch+0.3), 'front'); y = (yb+2.0*(1-np.sin(ang))+1.0) if yb is not None else pf[1]
    else: yb = body_sag(max(z, z_crotch+0.3), 'back'); y = (yb-2.0*(1-np.sin(ang))-1.0) if yb is not None else pb[1]
    if abs(s-0.5) < 0.12: y = float(np.interp(s, [0.38, 0.5, 0.62], [y if s < 0.5 else 3.0, 1.5, y if s > 0.5 else 0.0]))
    crotch_pts.append([0.0, y, z])
crotch_ids = [trs.add(p) for p in crotch_pts]
trs.group('CROTCH', crotch_ids)
ROWS_LEG = int(34*RES)
def leg(sign):
    hp, kn, an = (hip_l, kn_l, an_l) if sign > 0 else (hip_l*[-1, 1, 1], kn_l*[-1, 1, 1], an_l*[-1, 1, 1])
    outer = list(range(0, NT//2+1)) if sign > 0 else [0]+list(range(NT-1, NT//2-1, -1))   # front -> outer side -> back
    Lr = len(outer)+NI
    # ring 0 = crotch row: outer columns from the hip ring, inner = crotch seam (back -> front)
    ring0 = [hip[ROWS_HIP, i] for i in outer]+list(reversed(crotch_ids))
    rings = [ring0]
    # leg axis: hang vertically from the hip joint, slight lateral follow of the leg
    def axis_pt(s):
        z = z_cr_ring+(z_hem_t-z_cr_ring)*s
        xk = np.interp(z, [an[2], kn[2], hp[2]], [an[0], kn[0], hp[0]]); yk = np.interp(z, [an[2], kn[2], hp[2]], [an[1], kn[1], hp[1]])
        return np.array([xk*0.6+hp[0]*0.4, yk*0.7+hp[1]*0.3, z])
    def leg_circ(z):
        sel = (legw > 0.5) & (np.sign(BODY[:, 0]) == sign) & (np.abs(BODY[:, 2]-z) < 0.6)
        return circ(hull2d(BODY[sel][:, :2])) if sel.sum() > 5 else 30.0
    uvr = UV['trousers']['leg_l' if sign > 0 else 'leg_r']
    for k in range(1, ROWS_LEG+1):
        s = k/ROWS_LEG; c = axis_pt(s); z = c[2]
        target = leg_circ(z)+float(np.interp(z, [z_hem_t, 30, 48, 70, z_cr_ring], [12, 12, 13, 13, 13]))
        target = max(target, 47.0) if z < 48 else target
        r = target/(2*np.pi); mix = min(1.0, s*ROWS_LEG/4.0)
        ring = []
        for j in range(Lr):
            phi = 2*np.pi*j/Lr        # 0 = front, pi/2 = outer side (sign), pi = back, 3pi/2 = inner
            q = c+np.array([sign*r*np.sin(phi), r*np.cos(phi), 0])
            p0 = np.asarray(trs.v[ring0[j]]); p0 = np.array([p0[0], p0[1], z])
            ring.append(trs.add(p0*(1-mix)+q*mix))
        rings.append(ring)
    for k in range(ROWS_LEG):
        for j in range(Lr):
            j2 = (j+1) % Lr
            uvs = [uvmap(uvr, j/Lr, 1-k/ROWS_LEG), uvmap(uvr, (j+1)/Lr, 1-k/ROWS_LEG), uvmap(uvr, (j+1)/Lr, 1-(k+1)/ROWS_LEG), uvmap(uvr, j/Lr, 1-(k+1)/ROWS_LEG)]
            if sign > 0: trs.quad(rings[k][j], rings[k][j2], rings[k+1][j2], rings[k+1][j], uvs, 0)
            else: trs.quad(rings[k][j2], rings[k][j], rings[k+1][j], rings[k+1][j2], uvs, 0)
    return rings
lg_l = leg(+1); lg_r = leg(-1)
for j in range(ROWS_BAND+1): trs.group('PIN', [hip[j, i] for i in range(NT)], 1.0)
trs.group('PIN', [hip[ROWS_BAND+1, i] for i in range(NT)], 0.35)
trs.group('BAND_TOP', [hip[0, i] for i in range(NT)]); trs.group('BAND_BOT', [hip[ROWS_BAND, i] for i in range(NT)]); trs.group('HEM_L', lg_l[-1]); trs.group('HEM_R', lg_r[-1])
trs.group('LEG_L', [v for r in lg_l[1:] for v in r]); trs.group('LEG_R', [v for r in lg_r[1:] for v in r])
side_l = [hip[j, NT//4] for j in range(ROWS_HIP+1)]; side_r = [hip[j, 3*NT//4] for j in range(ROWS_HIP+1)]
trs.group('OUTSEAM_L', side_l); trs.group('OUTSEAM_R', side_r)
trs_ob = trs.to_object('SPH_Trousers', [M_TRS]); log('trousers built', len(trs.v), 'verts', len(trs.f), 'faces')

# ============================================================ body collider ===========================================
body_me = bpy.data.meshes.new('SPH_Body_Mesh'); body_me.from_pydata([tuple(p) for p in bl(BODY)], [], [list(t) for t in TRI])
body_me.validate(); body_me.update()
for p_ in body_me.polygons: p_.use_smooth = True
body_ob = bpy.data.objects.new('SPH_Body_BR_Neutral_REF', body_me); bpy.context.scene.collection.objects.link(body_ob)
body_ob.data.materials.append(mat('M_Skin', (0.72, 0.60, 0.52)))
cm = body_ob.modifiers.new('Collision', 'COLLISION'); body_ob.collision.thickness_outer = 0.002; body_ob.collision.thickness_inner = 0.005; body_ob.collision.cloth_friction = 8.0

# ============================================================ cloth simulation ========================================
def ob_pos(ob): co = np.zeros(len(ob.data.vertices)*3); ob.data.vertices.foreach_get('co', co); return ue(co.reshape(-1, 3))
def group_ids(ob, name):
    gi = ob.vertex_groups[name].index; ids = []
    for v in ob.data.vertices:
        for g in v.groups:
            if g.group == gi and g.weight > 0: ids.append(v.index)
    return ids
sc = bpy.context.scene; sc.frame_start = 1
def simulate(ob, frames, mass, tension, bending, shear, air, self_col=True, extra_colliders=()):
    for o in extra_colliders:
        if not o.modifiers.get('Collision'): o.modifiers.new('Collision', 'COLLISION'); o.collision.thickness_outer = 0.002; o.collision.cloth_friction = 6
    cl = ob.modifiers.new('Cloth', 'CLOTH'); st = cl.settings; cs = cl.collision_settings
    st.quality = 12; st.mass = mass; st.tension_stiffness = tension; st.compression_stiffness = tension*0.5; st.shear_stiffness = shear
    st.bending_stiffness = bending; st.tension_damping = 5; st.compression_damping = 5; st.shear_damping = 5; st.bending_damping = 0.5
    st.air_damping = air; st.vertex_group_mass = 'PIN'; st.pin_stiffness = 1.0; st.bending_model = 'ANGULAR'
    cs.use_collision = True; cs.distance_min = 0.005; cs.collision_quality = 4; cs.use_self_collision = self_col; cs.self_distance_min = 0.003; cs.self_friction = 5
    cl.point_cache.frame_start = 1; cl.point_cache.frame_end = frames; sc.frame_end = frames
    dg = bpy.context.evaluated_depsgraph_get()
    for f in range(1, frames+1):
        sc.frame_set(f)
        if f % 20 == 0:
            ev = ob.evaluated_get(dg); co = np.zeros(len(ev.data.vertices)*3); ev.data.vertices.foreach_get('co', co)
            log(ob.name, 'frame', f, 'z-range', round(co.reshape(-1, 3)[:, 2].min(), 3), round(co.reshape(-1, 3)[:, 2].max(), 3))
    dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
    co = np.zeros(len(ev.data.vertices)*3, np.float32); ev.data.vertices.foreach_get('co', co)
    ob.modifiers.remove(cl); ob.data.vertices.foreach_set('co', co); ob.data.update(); sc.frame_set(1)
    for o in extra_colliders:
        if o.modifiers.get('Collision'): o.modifiers.remove(o.modifiers['Collision'])
    return co.reshape(-1, 3)
def clearance_pass(ob, min_cm, iters=3):
    """pre-simulation: push any garment vertex closer than min_cm to the body (or inside it) out along the body normal,
    then relax the neighbourhood so the rest garment starts penetration-free and the cloth solver never explodes"""
    me = ob.data; moved = 0
    for _ in range(iters):
        for v in me.vertices:
            loc, nrm, idx, dist = bvh.find_nearest(v.co)
            if loc is None: continue
            sd = (v.co-loc).dot(nrm)
            if sd < min_cm*0.01: v.co = loc+nrm*(min_cm*0.01); moved += 1
    me.update(); return moved
PRECLEAR = os.environ.get('SPH_PRECLEAR', '1') == '1'
log('pre-sim clearance', clearance_pass(trs_ob, 1.0) if PRECLEAR else 'off', clearance_pass(hen_ob, 0.9) if PRECLEAR else 'off')
FRAMES = int(os.environ.get('SPH_CLOTH_FRAMES', '70'))
# cloth 'mass' is per vertex: at ~1 cm vertex spacing 0.08-0.10 kg/vertex keeps the hanging stretch of jersey/twill at a few %
log('simulating trousers'); simulate(trs_ob, FRAMES, mass=0.10, tension=60, bending=2.5, shear=25, air=3.0)
# shirt must start outside the settled trouser shell (radial clearance about the torso centre), except the tucked front
def outside_trousers(shirt, trousers, gap=0.7):
    from mathutils import kdtree
    TPm = ob_pos(trousers); kd = kdtree.KDTree(len(TPm))
    for i, p in enumerate(TPm): kd.insert(Vector(p), i)
    kd.balance(); SP = ob_pos(shirt); moved = 0; tuck = set(group_ids(shirt, 'TUCK'))
    for i, p in enumerate(SP):
        if p[2] > z_band_top+0.6 or i in tuck: continue
        c, f, g = torso_ring(p[2], 0.0, mask=(legw < 0.9) & (armw < 0.3) & (np.arange(NB+NH) < NB)); cc = np.array([c[0], c[1], p[2]])
        loc, idx, dist = kd.find(Vector(bl(p)))
        if loc is None: continue
        tp = TPm[idx]; rs = np.linalg.norm(p[:2]-cc[:2]); rt = np.linalg.norm(tp[:2]-cc[:2])
        if rs < rt+gap:
            q = cc+(p-cc)*((rt+gap)/max(rs, 1e-6)); shirt.data.vertices[i].co = tuple(bl(q)); moved += 1
    shirt.data.update(); return moved
log('simulating henley'); log('shirt outside trousers', outside_trousers(hen_ob, trs_ob)); simulate(hen_ob, FRAMES, mass=float(os.environ.get('SPH_HEN_MASS', '0.3')), tension=float(os.environ.get('SPH_HEN_TENSION', '20')), bending=float(os.environ.get('SPH_HEN_BEND', '0.6')), shear=float(os.environ.get('SPH_HEN_SHEAR', '8')), air=3.0, self_col=HEN_SELFCOL, extra_colliders=((trs_ob,) if os.environ.get('SPH_TRS_COLLIDER', '1') == '1' else ()))

# post-simulation relax: a light Laplacian smoothing of the settled cloth removes solver-scale facets and the small
# fold at the sleeve-cap / shoulder junction; pinned cuffs, neckline and tuck keep their positions
def relax(ob, iters, factor, keep_groups=('PIN',)):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.verts.ensure_lookup_table()
    keep = set()   # only fully pinned vertices (cuffs, neckline, tuck) are frozen; half-pinned shoulder seam may relax
    for g in keep_groups:
        if g in ob.vertex_groups:
            gi = ob.vertex_groups[g].index
            for v in ob.data.vertices:
                for gg in v.groups:
                    if gg.group == gi and gg.weight >= 0.9: keep.add(v.index)
    verts = [v for v in bm.verts if v.index not in keep and not v.is_boundary]
    for _ in range(iters): bmesh.ops.smooth_vert(bm, verts=verts, factor=factor, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
log('post-sim shirt outside trousers', outside_trousers(hen_ob, trs_ob, gap=0.6))
relax(hen_ob, iters=int(os.environ.get('SPH_RELAX_IT', '3')), factor=0.35); relax(trs_ob, iters=1, factor=0.3)
def relax_region(ob, centre, radius, iters, factor):
    """local Laplacian relax (crotch seam pinch): vertices within radius (cm) of centre (UE cm)"""
    Pm = ob_pos(ob); ids = [i for i, p in enumerate(Pm) if np.linalg.norm(p-np.asarray(centre)) < radius]
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.verts.ensure_lookup_table(); vs = [bm.verts[i] for i in ids if not bm.verts[i].is_boundary]
    for _ in range(iters): bmesh.ops.smooth_vert(bm, verts=vs, factor=factor, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.to_mesh(ob.data); bm.free(); ob.data.update(); return len(vs)
log('crotch relax verts', relax_region(trs_ob, (0.0, 3.0, crotch_g+1.0), 9.0, 6, 0.5))
log('post-sim relax done')
# ============================================================ construction details ====================================
def vnormals(ob):
    ob.data.calc_normals_split() if hasattr(ob.data, 'calc_normals_split') else None
    n = np.zeros(len(ob.data.vertices)*3); ob.data.vertices.foreach_get('normal', n); n = n.reshape(-1, 3); n[:, 1] *= -1; return n
def order_loop(ob, ids, pos):
    """order a set of boundary vertices into a chain / loop using mesh edges"""
    ids = set(ids); adj = {i: [] for i in ids}
    for e in ob.data.edges:
        a, b = e.vertices
        if a in ids and b in ids: adj[a].append(b); adj[b].append(a)
    ends = [i for i in ids if len(adj[i]) == 1]; start = ends[0] if ends else min(ids); chain_ = [start]; prev = None
    while True:
        nxt = [x for x in adj[chain_[-1]] if x != prev and x not in chain_[1:]]
        if not nxt: break
        prev = chain_[-1]; chain_.append(nxt[0])
        if chain_[-1] == start: chain_.pop(); break
        if len(chain_) > len(ids): break
    return chain_, (not ends)
def inward_dirs(ob, chain, pos):
    """per chain vertex: unit vector along the garment surface pointing into the garment (mean direction to the
    edge-neighbours that are not part of the chain); robust for boundary loops and slit edges"""
    cs = set(chain); nb = {i: [] for i in chain}
    for e in ob.data.edges:
        a, b = e.vertices
        if a in cs and b not in cs: nb[a].append(b)
        if b in cs and a not in cs: nb[b].append(a)
    out = []
    for i in chain:
        if nb[i]: d = np.mean([pos[j]-pos[i] for j in nb[i]], 0)
        else: d = np.zeros(3)
        n = np.linalg.norm(d); out.append(d/n if n > 1e-6 else np.array([0, 0, -1.0]))
    return np.asarray(out)
def strip_along(builder, pts, normals, width, offset, rect, m, closed, thickness=0.0, inward=False, dirs=None, start=0.0):
    """thin band following a chain of points: pts (n,3) UE cm, normals outward. The band lies 'offset' above the surface
    and spans from 'start' to 'start+width' along dirs (surface-inward unit vectors; start<0 lets it overhang the edge).
    Two layers (boxed) if thickness>0."""
    n = len(pts); ids_a = []; ids_b = []
    if dirs is None:
        tang = np.gradient(pts, axis=0); tang /= np.maximum(np.linalg.norm(tang, axis=1), 1e-6)[:, None]
        dirs = np.cross(normals, tang); dirs /= np.maximum(np.linalg.norm(dirs, axis=1), 1e-6)[:, None]
        if inward: dirs = -dirs
    for k in range(n):
        a = pts[k]+normals[k]*offset+dirs[k]*start; b = a+dirs[k]*width
        ids_a.append(builder.add(a)); ids_b.append(builder.add(b))
    rng = range(n if closed else n-1)
    for k in rng:
        k2 = (k+1) % n
        builder.quad(ids_a[k], ids_a[k2], ids_b[k2], ids_b[k], [uvmap(rect, k/n, 0), uvmap(rect, (k+1)/n, 0), uvmap(rect, (k+1)/n, 1), uvmap(rect, k/n, 1)], m)
    if thickness > 0:
        ids_c = [builder.add(np.asarray(builder.v[i])+normals[k]*thickness) for k, i in enumerate(ids_a)]
        ids_d = [builder.add(np.asarray(builder.v[i])+normals[k]*thickness) for k, i in enumerate(ids_b)]
        for k in rng:
            k2 = (k+1) % n
            builder.quad(ids_d[k], ids_d[k2], ids_c[k2], ids_c[k], [uvmap(rect, k/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, (k+1)/n, 0), uvmap(rect, k/n, 0)], m)
            builder.quad(ids_b[k], ids_b[k2], ids_d[k2], ids_d[k], [uvmap(rect, k/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, k/n, 1)], m)
            builder.quad(ids_c[k], ids_c[k2], ids_a[k2], ids_a[k], [uvmap(rect, k/n, 0), uvmap(rect, (k+1)/n, 0), uvmap(rect, (k+1)/n, 0), uvmap(rect, k/n, 0)], m)
    return ids_a, ids_b
def surface_strip(builder, ob, chain, steps, offset, thickness, rect, m, closed, overhang=0.0, extra_offset=None):
    """band that follows the settled cloth surface: for each chain vertex walk 'steps' edge-neighbours into the garment
    (the polyline rows), optional overhang beyond the edge; lifted by 'offset' along the vertex normals, boxed by 'thickness'"""
    pos = ob_pos(ob); nrm = vnormals(ob); cs = set(chain); adj = {}
    for e in ob.data.edges:
        a, b = e.vertices; adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    indir = inward_dirs(ob, chain, pos); rows = [[] for _ in range(steps+1)]; nrows = [[] for _ in range(steps+1)]
    for k, v in enumerate(chain):
        cur = v; visited = {v}; rows[0].append(pos[v]); nrows[0].append(nrm[v])
        for st in range(1, steps+1):
            cands = [w for w in adj.get(cur, []) if w not in cs and w not in visited]
            if not cands: rows[st].append(rows[st-1][-1]+indir[k]*1.0); nrows[st].append(nrows[st-1][-1]); continue
            w = max(cands, key=lambda w: float(np.dot(pos[w]-pos[cur], indir[k])))
            visited.add(w); cur = w; rows[st].append(pos[w]); nrows[st].append(nrm[w])
    if overhang > 0:
        rows.insert(0, [rows[0][k]-indir[k]*overhang for k in range(len(chain))]); nrows.insert(0, list(nrows[0]))
    R = len(rows); n = len(chain); ids = [[builder.add(np.asarray(rows[r][k])+np.asarray(nrows[r][k])*offset) for k in range(n)] for r in range(R)]
    top = [[builder.add(np.asarray(rows[r][k])+np.asarray(nrows[r][k])*(offset+thickness)) for k in range(n)] for r in range(R)] if thickness > 0 else None
    rng = range(n if closed else n-1)
    for r in range(R-1):
        for k in rng:
            k2 = (k+1) % n; u0, u1 = r/(R-1), (r+1)/(R-1)
            builder.quad(ids[r][k], ids[r][k2], ids[r+1][k2], ids[r+1][k], [uvmap(rect, k/n, u0), uvmap(rect, (k+1)/n, u0), uvmap(rect, (k+1)/n, u1), uvmap(rect, k/n, u1)], m)
            if top: builder.quad(top[r+1][k], top[r+1][k2], top[r][k2], top[r][k], [uvmap(rect, k/n, u1), uvmap(rect, (k+1)/n, u1), uvmap(rect, (k+1)/n, u0), uvmap(rect, k/n, u0)], m)
    if top:  # side walls along the two long edges
        for k in rng:
            k2 = (k+1) % n
            builder.quad(ids[0][k2], ids[0][k], top[0][k], top[0][k2], [uvmap(rect, (k+1)/n, 0), uvmap(rect, k/n, 0), uvmap(rect, k/n, 0), uvmap(rect, (k+1)/n, 0)], m)
            builder.quad(ids[R-1][k], ids[R-1][k2], top[R-1][k2], top[R-1][k], [uvmap(rect, k/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, k/n, 1)], m)
    return ids
def button(builder, c, nrm, r=0.55, h=0.22, rect=None, m=2):
    u = np.cross(nrm, [0, 0, 1.0]); u /= np.linalg.norm(u); v = np.cross(nrm, u); n = 10
    base = [builder.add(c+u*r*np.cos(2*np.pi*k/n)+v*r*np.sin(2*np.pi*k/n)) for k in range(n)]
    top = [builder.add(c+nrm*h+u*r*0.92*np.cos(2*np.pi*k/n)+v*r*0.92*np.sin(2*np.pi*k/n)) for k in range(n)]
    ctr = builder.add(c+nrm*(h+0.05)); ctr_in = builder.add(c+nrm*(h-0.06)); cb = builder.add(c-nrm*0.02)
    for k in range(n):
        k2 = (k+1) % n
        builder.quad(base[k], base[k2], top[k2], top[k], [uvmap(rect, k/n, 0.0), uvmap(rect, (k+1)/n, 0.0), uvmap(rect, (k+1)/n, 0.3), uvmap(rect, k/n, 0.3)], m)
        builder.f.append([top[k], top[k2], ctr]); builder.uv.append([uvmap(rect, 0.5+0.4*np.cos(2*np.pi*k/n), 0.65+0.3*np.sin(2*np.pi*k/n)), uvmap(rect, 0.5+0.4*np.cos(2*np.pi*k2/n), 0.65+0.3*np.sin(2*np.pi*k2/n)), uvmap(rect, 0.5, 0.65)]); builder.mat.append(m)
        builder.f.append([base[k2], base[k], cb]); builder.uv.append([uvmap(rect, 0.5, 0.3), uvmap(rect, 0.5, 0.3), uvmap(rect, 0.5, 0.3)]); builder.mat.append(m)
    # button-hole dimple: 4 tiny holes as a small quad ring
    for k in range(4):
        a = 2*np.pi*k/4+np.pi/4; hc = c+nrm*(h+0.02)+u*0.18*np.cos(a)+v*0.18*np.sin(a)
        hv = [builder.add(hc+u*0.06*np.cos(2*np.pi*q/4)+v*0.06*np.sin(2*np.pi*q/4)-nrm*0.05) for q in range(4)]
        builder.f.append(hv); builder.uv.append([uvmap(rect, 0.5, 0.65)]*4); builder.mat.append(m)
def tube(builder, pts, r, rect, m, n=7, cap=True):
    tang = np.gradient(pts, axis=0); tang /= np.maximum(np.linalg.norm(tang, axis=1), 1e-6)[:, None]
    rings = []
    for k, p in enumerate(pts):
        u = np.cross(tang[k], [0, 1.0, 0.0]);
        if np.linalg.norm(u) < 1e-3: u = np.cross(tang[k], [1.0, 0, 0])
        u /= np.linalg.norm(u); v = np.cross(tang[k], u)
        rings.append([builder.add(p+u*r*np.cos(2*np.pi*q/n)+v*r*np.sin(2*np.pi*q/n)) for q in range(n)])
    for k in range(len(pts)-1):
        for q in range(n):
            q2 = (q+1) % n
            builder.quad(rings[k][q], rings[k][q2], rings[k+1][q2], rings[k+1][q], [uvmap(rect, q/n, k/len(pts)), uvmap(rect, (q+1)/n, k/len(pts)), uvmap(rect, (q+1)/n, (k+1)/len(pts)), uvmap(rect, q/n, (k+1)/len(pts))], m)
    if cap:
        for ring in (rings[0], rings[-1]):
            c = builder.add(np.mean([builder.v[i] for i in ring], 0))
            for q in range(n): builder.f.append([ring[(q+1) % n], ring[q], c]); builder.uv.append([uvmap(rect, 0.5, 0.5)]*3); builder.mat.append(m)
    return rings

# ---- Henley details ----
HP = ob_pos(hen_ob); HN = vnormals(hen_ob)
det = MeshBuilder()
neck_chain, closed = order_loop(hen_ob, group_ids(hen_ob, 'NECK'), HP)
# neck binding: ~1.6 cm band on the neckline edge (0.45 overhang), boxed 0.22
surface_strip(det, hen_ob, neck_chain, steps=1, offset=0.10, thickness=0.22, rect=UV['henley']['binding'], m=1, closed=False, overhang=0.45)
for gname in ('SLIT_L', 'SLIT_R'):
    ch, _ = order_loop(hen_ob, group_ids(hen_ob, gname), HP); ch = sorted(ch, key=lambda i: -HP[i, 2])
    surface_strip(det, hen_ob, ch, steps=2, offset=0.16 if gname == 'SLIT_L' else 0.06, thickness=0.18, rect=UV['henley']['placket'], m=1, closed=False, overhang=0.15)
    if gname == 'SLIT_L': slit_l_chain = ch
    else: slit_r_chain = ch
for gname in ('CUFF_L', 'CUFF_R'):
    ch, _ = order_loop(hen_ob, group_ids(hen_ob, gname), HP)
    surface_strip(det, hen_ob, ch, steps=2, offset=0.08, thickness=0.2, rect=UV['henley']['cuffs'], m=1, closed=True, overhang=0.1)
hem_chain, _ = order_loop(hen_ob, group_ids(hen_ob, 'HEM'), HP)
surface_strip(det, hen_ob, hem_chain, steps=2, offset=0.06, thickness=0.16, rect=UV['henley']['hem'], m=1, closed=True, overhang=0.1)
# buttons (5) along the placket: the top two sit on the exposed right (under) placket, the rest on the closed centre line
zb = np.linspace(neck_front(0)-2.4, z_slit+1.4, 5)
for k, z in enumerate(zb):
    i = min(range(len(slit_r_chain)), key=lambda q: abs(HP[slit_r_chain[q], 2]-z)); p = HP[slit_r_chain[i]]; n_ = HN[slit_r_chain[i]]
    dr = inward_dirs(hen_ob, slit_r_chain, HP)[i]
    c = p+n_*0.34+dr*(1.3 if k < 2 else 0.2)
    button(det, c, n_/np.linalg.norm(n_), rect=UV['henley']['buttons'], m=2)
hen_det = det.to_object('SPH_Henley_Details', [M_HEN, M_HEN_TRIM, M_BTN])
# ---- Trouser details ----
TP = ob_pos(trs_ob); TN = vnormals(trs_ob)
tdet = MeshBuilder()
def ring_sorted(gname):
    ch, _ = order_loop(trs_ob, group_ids(trs_ob, gname), TP)
    return sorted(ch, key=lambda i: (np.arctan2(TP[i, 0], TP[i, 1])) % (2*np.pi))
band_bot = ring_sorted('BAND_BOT'); band_top = ring_sorted('BAND_TOP'); assert len(band_bot) == len(band_top)
band_chain = band_bot; bpts = TP[band_bot].copy(); tpts = TP[band_top].copy()
def flat_n(ids):
    n_ = TN[ids].copy(); n_[:, 2] = 0; n_ /= np.maximum(np.linalg.norm(n_, axis=1), 1e-6)[:, None]; return n_
bn = flat_n(band_bot); tn = flat_n(band_top); up = np.array([0, 0, 1.0])
# waistband: double layer wrapping the pinned band rows (bottom ring -> top ring), outer layer 0.22 out with gentle gathers
n = len(band_bot); a_ids = []; b_ids = []; c_ids = []; d_ids = []
for k in range(n):
    a_ids.append(tdet.add(bpts[k]+bn[k]*0.05)); b_ids.append(tdet.add(tpts[k]+tn[k]*0.05+up*0.15))
    c_ids.append(tdet.add(tpts[k]+tn[k]*0.22+up*0.15)); d_ids.append(tdet.add(bpts[k]+bn[k]*0.22))
rect = UV['trousers']['band']
for k in range(n):
    k2 = (k+1) % n; g = 0.06*np.sin(k*1.7)+0.04*np.sin(k*3.1)   # gentle gathers baked into the band outer layer
    tdet.v[d_ids[k]] = list(np.asarray(tdet.v[d_ids[k]])+bn[k]*g); tdet.v[c_ids[k]] = list(np.asarray(tdet.v[c_ids[k]])+tn[k]*g*0.5)
    tdet.quad(d_ids[k], d_ids[k2], c_ids[k2], c_ids[k], [uvmap(rect, k/n, 0), uvmap(rect, (k+1)/n, 0), uvmap(rect, (k+1)/n, 1), uvmap(rect, k/n, 1)], 1)
    tdet.quad(c_ids[k], c_ids[k2], b_ids[k2], b_ids[k], [uvmap(rect, k/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, k/n, 1)], 1)
    tdet.quad(b_ids[k], b_ids[k2], a_ids[k2], a_ids[k], [uvmap(rect, k/n, 1), uvmap(rect, (k+1)/n, 1), uvmap(rect, (k+1)/n, 0), uvmap(rect, k/n, 0)], 1)
# eyelets + drawstring at centre front of the band
front_k = min(range(n), key=lambda k: abs(np.arctan2(bpts[k, 0], bpts[k, 1])))
fc = np.asarray(tdet.v[d_ids[front_k]]); fnrm = bn[front_k]; ex = np.cross(fnrm, up); ex /= np.linalg.norm(ex)
fc = fc*0.5+np.asarray(tdet.v[c_ids[front_k]])*0.5-up*1.75+fnrm*0.05   # band mid-height at the centre front
eyelets = [fc+up*0.3+ex*1.4*sgn+fnrm*0.35 for sgn in (1, -1)]
for e in eyelets:
    ring = tube(tdet, np.stack([e-fnrm*0.15, e+fnrm*0.25]), 0.45, UV['trousers']['cord'], 3, n=8, cap=False)
knot = fc-up*1.0+fnrm*0.95
for sgn, tail_len, sway in ((1, 11.0, 1.2), (-1, 9.0, -0.6)):
    e = eyelets[0] if sgn > 0 else eyelets[1]
    pts = [e+fnrm*0.3, e+fnrm*0.7+ex*0.6*sgn-up*0.4, knot+ex*0.5*sgn+up*0.3]
    for q in range(1, 9):
        s = q/8; pts.append(knot+ex*(0.5*sgn+sway*s+0.4*sgn*np.sin(s*np.pi))+fnrm*(0.6-0.35*s)-up*tail_len*s)
    pts = np.asarray(pts); tube(tdet, pts, 0.3, UV['trousers']['cord'], 3, n=7)
    tip = tube(tdet, np.stack([pts[-1], pts[-1]-up*0.9+ex*0.1*sgn]), 0.36, UV['trousers']['cord'], 3, n=7)
# knot blob
kn_ring = tube(tdet, np.stack([knot-ex*0.9, knot+ex*0.9]), 0.55, UV['trousers']['cord'], 3, n=8)
# side-seam pocket welts
for gname in ('OUTSEAM_L', 'OUTSEAM_R'):
    ch = sorted(group_ids(trs_ob, gname), key=lambda i: -TP[i, 2]); ch = [i for i in ch if 82 <= TP[i, 2] <= 98]
    if len(ch) > 2:
        fwd = np.tile(np.array([0, 1.0, 0]), (len(ch), 1))    # welt lies just in front of the outseam
        strip_along(tdet, TP[ch], TN[ch], width=1.3, offset=0.16, rect=UV['trousers']['welts'], m=1, closed=False, thickness=0.14, dirs=fwd, start=-0.3)
for gname in ('HEM_L', 'HEM_R'):
    ch, _ = order_loop(trs_ob, group_ids(trs_ob, gname), TP)
    surface_strip(tdet, trs_ob, ch, steps=2, offset=0.06, thickness=0.18, rect=UV['trousers']['hems'], m=1, closed=True, overhang=0.1)
trs_det = tdet.to_object('SPH_Trousers_Details', [M_TRS, M_TRS_TRIM, M_TRS_TRIM, M_CORD])
log('details built')

# ============================================================ QA: clearance / penetration ==============================
def clearance(ob, name):
    Pm = ob_pos(ob); res = {'name': name, 'verts': len(Pm)}; d = []; inside = []
    for p in bl(Pm):
        loc, nrm, idx, dist = bvh.find_nearest(Vector(p))
        if loc is None: d.append(99); inside.append(False); continue
        sgn = (Vector(p)-loc).dot(nrm); d.append(dist*100*(1 if sgn >= 0 else -1))
    d = np.asarray(d); res['min_signed_cm'] = float(d.min()); res['penetrating_verts'] = int((d < -0.05).sum()); res['max_penetration_cm'] = float(-d[d < 0].min()) if (d < 0).any() else 0.0
    res['clearance_p5_cm'] = float(np.percentile(d, 5)); res['clearance_median_cm'] = float(np.median(d)); res['clearance_p95_cm'] = float(np.percentile(d, 95))
    return res, d
qa = {'facts': facts, 'garments': {}}
for ob, nm in ((hen_ob, 'henley'), (trs_ob, 'trousers')):
    r, d = clearance(ob, nm); qa['garments'][nm] = r; log(nm, r)
# fix residual penetrations by pushing along the body normal (tiny, reported)
for ob in (hen_ob, trs_ob):
    Pm = ob_pos(ob); moved = 0
    for i, p in enumerate(bl(Pm)):
        loc, nrm, idx, dist = bvh.find_nearest(Vector(p))
        if loc is not None and (Vector(p)-loc).dot(nrm) < 0.0025:
            q = loc+nrm*0.0025; ob.data.vertices[i].co = q; moved += 1
    ob.data.update(); qa['garments'][ob.name]= {'post_fix_moved': moved}
for ob, nm in ((hen_ob, 'henley'), (trs_ob, 'trousers')):
    r, d = clearance(ob, nm); qa['garments'][nm+'_after_fix'] = r; log(nm, 'after', r)

# ============================================================ export ==================================================
def export(obs, name):
    V = []; T = []; UVs = []; MI = []; parts = []; key = {}
    for ob in obs:
        me = ob.data; me.calc_loop_triangles(); uvl = me.uv_layers.active.data
        co = np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co', co); co = ue(co.reshape(-1, 3))
        for lt in me.loop_triangles:
            tri = []
            for li, vi in zip(lt.loops, lt.vertices):
                uv = uvl[li].uv; k = (ob.name, vi, round(uv[0], 5), round(uv[1], 5))
                if k not in key: key[k] = len(V); V.append(co[vi].tolist()); UVs.append([uv[0], 1-uv[1]]); parts.append(ob.name)
                tri.append(key[k])
            T.append(tri); MI.append(int(me.polygons[lt.polygon_index].material_index))
    mats = [m.name for m in obs[0].data.materials]
    return {'name': name, 'positions': V, 'triangles': T, 'uv': UVs, 'material_ids': MI, 'materials': mats, 'part': parts}
def lod1(obs, name, ratio=0.5):
    """LOD1: joined copy of the garment + details, decimated (collapse, UV-aware) to 'ratio' of the faces"""
    copies = []
    for ob in obs:
        c = ob.copy(); c.data = ob.data.copy(); bpy.context.scene.collection.objects.link(c); copies.append(c)
    with bpy.context.temp_override(active_object=copies[0], selected_objects=copies, selected_editable_objects=copies):
        bpy.ops.object.join()
    j = copies[0]; j.name = name+'_LOD1'
    mod = j.modifiers.new('Decimate', 'DECIMATE'); mod.ratio = ratio; mod.use_collapse_triangulate = True; mod.delimit = {'MATERIAL', 'UV'}
    with bpy.context.temp_override(object=j, active_object=j, selected_objects=[j]):
        bpy.ops.object.modifier_apply(modifier='Decimate')
    return j
hen_l1 = lod1([hen_ob, hen_det], 'SPH_Henley'); trs_l1 = lod1([trs_ob, trs_det], 'SPH_Trousers')
out = {'henley': export([hen_ob, hen_det], 'henley'), 'trousers': export([trs_ob, trs_det], 'trousers'),
       'henley_lod1': export([hen_l1], 'henley_lod1'), 'trousers_lod1': export([trs_l1], 'trousers_lod1'), 'uv_layout': UV, 'coords': 'UE cm', 'facts': facts}
# material name unification for the export (details use their own slot lists)
out['henley']['materials'] = ['M_Henley', 'M_Henley_Trim', 'M_Buttons']; out['trousers']['materials'] = ['M_Trousers', 'M_Trousers_Trim', 'M_Trousers_Trim', 'M_Drawstring']
with gzip.open(os.path.join(OUT, 'outfit_geometry.json.gz'), 'wt') as f: json.dump(out, f)
for nm in ('henley', 'trousers', 'henley_lod1', 'trousers_lod1'): qa['garments'][nm+'_export'] = {'verts': len(out[nm]['positions']), 'tris': len(out[nm]['triangles'])}
open(os.path.join(OUT, 'outfit_build_qa.json'), 'w').write(json.dumps(qa, indent=1))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'SPH_Outfit_Home_20260929.blend'), compress=True)
log('BUILD_OK', json.dumps({k: v for k, v in qa['garments'].items() if k.endswith('export')}))
