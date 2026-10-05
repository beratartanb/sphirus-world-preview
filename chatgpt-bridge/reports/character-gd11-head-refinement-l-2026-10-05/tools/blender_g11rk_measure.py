"""GD11 refinement K: measured 2D deviation of a head npy from the reference picks, in the two reference frames (gd_common VIEWS, solved
cameras). The skin mesh (ears and the neck below z 147.5 removed, so the chin bottom is a true silhouette) is RENDERED as a solid mask with the
solved camera (Workbench, 1600 px square, same projection as gd_common) and resampled into the reference frame. For every CONTOUR pick (ref
pixel + outward image normal n) the candidate edge = last covered pixel walking the pick line from 50 px inside to 50 px outside;
delta = signed distance along n in px and cm (cm/px = 5.95 cm IPD / projected eye-centre distance; + = candidate further out than the reference).
GEO points from the outer midline profile y(z) (front-most vertex per 0.1 cm z bin, y > 5): pronasale = max y (z 156-162), sellion = min y
(z 161-166), subnasale = columella-lip break (max distance from the pronasale..labrale chord, z 154.8-157.2); alar = most lateral skin vertex of the
nose band (z 155.2-158.2, y > 12.5, |x| < 3.2). Draws the reference image with the candidate mask (red tint + edge), ref picks (cyan), candidate
edge points (magenta) -> <out prefix>_<view>.png ; writes <out prefix>.json.
usage: blender -b --factory-startup --python blender_g11rk_measure.py -- <out prefix> <head.npy> [<label>]"""
import bpy, sys, os, json, math, tempfile, numpy as np
from mathutils import Matrix
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix, VIEWS, basis, crop_rect, head_topology
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEAD = a[0], a[1]; LAB = a[2] if len(a) > 2 else os.path.basename(HEAD)
X = np.load(HEAD); NH = 24049; S = X[:NH]; PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))
T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < NH)]
ear = (np.abs(S[:, 0]) > 6.9) & (S[:, 1] < 5.0) & (S[:, 2] > 154.0) & (S[:, 2] < 168.0); drop = ear | (S[:, 2] < 147.5) | ((S[:, 2] < 153.0) & (S[:, 1] < 9.0))      # neck / submental removed: the chin bottom becomes a silhouette
FN = np.cross(S[TT[:, 1]]-S[TT[:, 0]], S[TT[:, 2]]-S[TT[:, 0]]); FN = -FN/np.maximum(np.linalg.norm(FN, axis=1), 1e-9)[:, None]
down = (FN[:, 2] < -0.45) & (S[TT].mean(1)[:, 2] < 153.5)      # under-jaw surface: its silhouette would extend below the visual chin edge
TTm = TT[~drop[TT].any(1) & ~down]
MX = -0.23; z = S[:, 2]; y = S[:, 1]; mid = (np.abs(S[:, 0]-MX) < 0.25) & (y > 5.0)
zb = np.round(z[mid]*10).astype(int); idx = np.flatnonzero(mid); prof = {}
for b in np.unique(zb):
    sel = idx[zb == b]; prof[b] = sel[np.argmax(y[sel])]
def prof_pick(z0, z1, fn):
    cand = [prof[b] for b in prof if z0*10 <= b <= z1*10]; return S[cand[int(fn([y[c] for c in cand]))]]
pron = prof_pick(156, 162, np.argmax); sellion = prof_pick(161, 166, np.argmin); lab = prof_pick(152.5, 154.6, np.argmax)
_c = [prof[b] for b in prof if 1548 <= b <= 1572]; _v = np.array([[y[c], z[c]] for c in _c]); _a = np.array([pron[1], pron[2]]); _b = np.array([lab[1], lab[2]]); _t = (_b-_a)/np.linalg.norm(_b-_a)
_d = (_v-_a)-np.outer((_v-_a)@_t, _t); subn = S[_c[int(np.argmax(np.linalg.norm(_d, axis=1)))]]
zd = (sellion[2]+pron[2])/2; dors = S[prof[min(prof, key=lambda b: abs(b-zd*10))]]
ci = np.flatnonzero((z > 155.2) & (z < 158.2) & (y > 12.5) & (np.abs(S[:, 0]-MX) < 3.2)); alar_l = S[ci[np.argmax(S[ci, 0])]]; alar_r = S[ci[np.argmin(S[ci, 0])]]
GEO = {'pronasale': pron, 'sellion': sellion, 'dorsum_mid': dors, 'subnasale': subn, 'alar_L': alar_l, 'alar_R': alar_r, 'alar_near': alar_r}
eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); res = {'label': LAB, 'geo3d': {k: [round(float(c), 2) for c in v] for k, v in GEO.items()}}
# --- scene: mask render of the trimmed skin mesh
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('head'); me.from_pydata([tuple(map(float, p)) for p in S], [], [tuple(int(i) for i in t) for t in TTm]); me.update()
ob = bpy.data.objects.new('head', me); sc.collection.objects.link(ob)
cam = bpy.data.cameras.new('c'); cam.type = 'PERSP'; cam.sensor_fit = 'HORIZONTAL'; cam.clip_start = 1.0; cam.clip_end = 1000.0
co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
sc.render.engine = 'BLENDER_WORKBENCH'; sc.render.film_transparent = True; R = 1600; sc.render.resolution_x = sc.render.resolution_y = R; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'; sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'SINGLE'
tmp = os.path.join(tempfile.gettempdir(), 'g11rk_mask.png')
def render_mask(view):
    V = VIEWS[view]; o, f, r, u = basis(V['cam']); cam.angle = math.radians(V['fov'])
    co.matrix_world = Matrix(((r[0], u[0], -f[0], o[0]), (r[1], u[1], -f[1], o[1]), (r[2], u[2], -f[2], o[2]), (0, 0, 0, 1)))
    sc.render.filepath = tmp; bpy.ops.render.render(write_still=True); im = bpy.data.images.load(tmp); A = np.array(im.pixels[:], np.float32).reshape(R, R, 4)[::-1]; bpy.data.images.remove(im)
    x0, y0, x1, y1 = crop_rect(view); W, H = V['W'], V['H']; px = np.clip(((x0+(np.arange(W)+0.5)/W*(x1-x0))*R).astype(int), 0, R-1); py = np.clip(((y0+(np.arange(H)+0.5)/H*(y1-y0))*R).astype(int), 0, R-1)
    return A[py][:, px, 3] > 0.5
for view in ('front', 'close'):
    V = VIEWS[view]; pe = topix(view, [eL, eR]); ipd = float(np.linalg.norm(pe[0]-pe[1])); cmpx = 5.95/ipd; cov = render_mask(view)
    img = bpy.data.images.load(os.path.abspath(V['ref'])); W, H = img.size; A = np.array(img.pixels[:], np.float32).reshape(H, W, 4)[::-1].copy()
    A[cov, :3] = 0.75*A[cov, :3]+0.25*np.array([1.0, 0.25, 0.25])
    edge_px = (cov & ~np.roll(cov, 1, 0)) | (cov & ~np.roll(cov, -1, 0)) | (cov & ~np.roll(cov, 1, 1)) | (cov & ~np.roll(cov, -1, 1)); A[edge_px, :3] = (1.0, 0.25, 0.25)
    def dot(px_, py_, col, r=3):
        x0, y0 = int(round(px_)), int(round(py_))
        if 0 <= x0 < W and 0 <= y0 < H: A[max(0, y0-r):y0+r+1, max(0, x0-r):x0+r+1, :3] = col
    rows = []
    for q in PK[view]['contours']:
        n = np.array(q['n'], float); n /= np.linalg.norm(n); r = np.array(q['ref'], float); last = None
        for s in np.arange(-50, 51, 1.0):
            p = r+n*s; xi, yi = int(round(p[0])), int(round(p[1]))
            if 0 <= xi < W and 0 <= yi < H and cov[yi, xi]: last = s
        if last is None: continue
        rows.append({'pick': q['name'], 'kind': 'contour', 'delta_px': round(float(last), 1), 'delta_cm': round(float(last)*cmpx, 2), 'w': q['w']}); dot(*r, (0.2, 1.0, 1.0)); dot(*(r+n*last), (1.0, 0.2, 1.0))
    for q in PK[view]['points']:
        g = GEO.get(q['name'])
        if g is None: dot(*q['ref'], (0.2, 1.0, 1.0), 2); continue
        p = topix(view, [g])[0]; r = np.array(q['ref'], float); d = p-r
        rows.append({'pick': q['name'], 'kind': 'point', 'dx_px': round(float(d[0]), 1), 'dy_px': round(float(d[1]), 1), 'dx_cm': round(float(d[0])*cmpx, 2), 'dy_cm': round(float(d[1])*cmpx, 2), 'w': q['w']}); dot(*r, (0.2, 1.0, 1.0)); dot(*p, (1.0, 0.2, 1.0))
    for e in pe: dot(*e, (1.0, 1.0, 0.2), 2)
    res[view] = {'ipd_px': round(ipd, 1), 'cm_per_px': round(cmpx, 4), 'rows': rows}
    o = bpy.data.images.new('m', W, H); o.pixels.foreach_set(np.ascontiguousarray(A[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT+'_'+view+'.png'); o.file_format = 'PNG'; o.save()
json.dump(res, open(OUT+'.json', 'w'), indent=1)
for view in ('front', 'close'):
    print('MEASURE', LAB, view, 'ipd_px', res[view]['ipd_px'], ' '.join('%s:%s' % (r['pick'], (r['delta_cm'] if r['kind'] == 'contour' else '(%s,%s)' % (r['dx_cm'], r['dy_cm']))) for r in res[view]['rows']))
