"""GUARDIAN-2 pass: Tier B turnaround comparison. The turnaround sheet panels share one orthographic scale and vertical placement, so the
right-profile fit (brow -> menton band, same as blender_gd_profile.py) gives one scale s / row offset ty for all panels. Each candidate head is
rendered as orthographic neutral clay in the frame of: front (p0), left profile (p3), right profile (p5), back (p4) and written as
[reference | clay | 50% blend] rows, so the bald cranium, face silhouette and neck can be judged against the sheet from every side.
Tier B is a modelling aid only (AI sheet): Tier A front / 3/4 decide feature identity.
usage: blender -b --factory-startup --python blender_gd_sheet.py -- <panel prefix (…/turnaround_p)> <y0 frac> <y1 frac> <front cx> <back cx> <out prefix> <head.npy> [...]"""
import bpy, sys, os, json, numpy as np
from mathutils import Matrix
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; PFX, Y0, Y1, FCX, BCX, OUTP = a[0], float(a[1]), float(a[2]), float(a[3]), float(a[4]), a[5]; HEADS = a[6:]
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im)
    if x.shape[2] == 3: x = np.concatenate([x, np.ones((h, w, 1), np.float32)], -1)
    return x
def save(x, p):
    h, w = x.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = x[..., :3]; im = bpy.data.images.new('o', w, h, alpha=True)
    im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(p); im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
def ref_profile(R):
    H = R.shape[0]; bg = np.median(R[:20, -40:, :3].reshape(-1, 3), 0); fg = np.abs(R[..., :3]-bg).max(-1) > 0.07; pts = []
    for y in range(int(Y0*H), int(Y1*H)):
        xs = np.nonzero(fg[y])[0]
        if len(xs): pts.append((xs.max(), y))
    return np.asarray(pts, float)
def cand_profile(X):
    S = X[:24049]; out = []
    for zz in np.arange(144.0, 180.0, 0.05):
        m = np.abs(S[:, 2]-zz) < 0.12
        if m.any(): out.append((S[m, 1].max(), zz))
    return np.asarray(out)
def fit(R, X, sign=1):
    """profile fit; sign=+1 right profile (nose toward image right, image x = s*y + tx), -1 left profile on a mirrored panel"""
    rp = ref_profile(R); P = cand_profile(X)
    br = P[(P[:, 1] > 163) & (P[:, 1] < 167.5)]; brow_z = br[np.argmax(br[:, 0]), 1]
    lo = P[(P[:, 1] < 156) & (P[:, 1] > 146)]; chin_y = lo[:, 0].max(); men_z = lo[lo[:, 0] > chin_y-2.6][:, 1].min()
    band = P[(P[:, 1] <= brow_z) & (P[:, 1] >= men_z)]
    s = (rp[-1, 1]-rp[0, 1])/(brow_z-men_z); ty = rp[0, 1]+s*brow_z
    rz = (ty-rp[:, 1])/s; ry = np.interp(rz, band[:, 1], band[:, 0]); tx = np.median(rp[:, 0]-s*ry); return s, tx, ty
T, MI = head_topology(); TT = T[np.isin(MI, [0, 3, 4, 8])]
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.78, 0.76, 0.74)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'WORLD'; sc.render.film_transparent = True; sc.view_settings.view_transform = 'Standard'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'HORIZONTAL'
def render(X, W, H, s, f, r, centre):
    for o in list(bpy.data.objects):
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new('h'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.update(); ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
    for pg in me.polygons: pg.use_smooth = True
    sc.render.resolution_x, sc.render.resolution_y = W, H; cam.data.ortho_scale = W/s
    f = np.asarray(f, float); r = np.asarray(r, float); u = np.array([0, 0, 1.0]); o = np.asarray(centre, float)-300*f; Xa = -r; Za = -f
    cam.matrix_world = Matrix(((Xa[0], u[0], Za[0], o[0]), (Xa[1], u[1], Za[1], o[1]), (Xa[2], u[2], Za[2], o[2]), (0, 0, 0, 1)))
    tmp = os.path.abspath(OUTP+'_tmp.png'); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True); return load(tmp)[:, ::-1]   # flip: UE (left-handed) data in Blender
rows = []
for hp in HEADS:
    X = np.load(hp); tag = os.path.basename(hp).replace('.npy', ''); row = []
    RR = load(PFX+'5.png'); H, W = RR.shape[:2]; s, tx, ty = fit(RR, X)
    zc = (ty-H/2)/s
    # right profile: image x = s*y + tx  -> centre y = (W/2 - tx)/s ; camera looks +x (from -x)
    views = [('front', PFX+'0.png', [0, -1, 0], [1, 0, 0], [(FCX*0+0) if False else 0, 0, zc], FCX),
             ('right', PFX+'5.png', [1, 0, 0], [0, 1, 0], [0, (W/2-tx)/s, zc], None)]
    RL = load(PFX+'3.png'); sL, txL, tyL = fit(RL[:, ::-1], X)                     # left profile fitted on the mirrored panel; use the right-profile scale for consistency
    txL = np.median(ref_profile(RL[:, ::-1])[:, 0]-s*np.interp((ty-ref_profile(RL[:, ::-1])[:, 1])/s, *cand_profile(X)[:, ::-1].T))
    views.append(('left', PFX+'3.png', [-1, 0, 0], [0, -1, 0], [0, (W/2-txL)/s, zc], None))
    views.append(('back', PFX+'4.png', [0, 1, 0], [-1, 0, 0], [0, 0, zc], BCX))
    for nm, rp, f, r, centre, cx in views:
        R = load(rp); Hh, Ww = R.shape[:2]; centre = list(centre)
        if cx is not None:   # horizontal: face / head midline x = 0 at reference column cx
            sgn = 1 if nm == 'front' else -1; centre[0] = sgn*(Ww/2-cx)/s
        cl = render(X, Ww, Hh, s, f, r, centre); al = cl[..., 3:4]; clc = cl[..., :3]*al+R[..., :3]*(1-al); bl = 0.5*clc+0.5*R[..., :3]
        row.append(np.concatenate([R[..., :3], clc, bl], 1)); save(np.concatenate([R[..., :3], clc, bl], 1), f'{OUTP}_{tag}_{nm}.png')
    print('SHEET', tag, json.dumps({'s': round(float(s), 3), 'tx': round(float(tx), 1), 'ty': round(float(ty), 1), 'txL': round(float(txL), 1)}))
