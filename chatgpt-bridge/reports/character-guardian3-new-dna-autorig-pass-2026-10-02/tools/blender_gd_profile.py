"""GUARDIAN-2 pass: profile likeness. Extracts the anterior face profile (brow -> chin) from a reference profile panel (uniform grey
background; face pointing image-right) and from candidate heads rendered as orthographic clay silhouettes from the character's right side
(UE camera at -x looking +x, nose pointing image-right), fits scale + translation of the candidate profile onto the reference profile, and
writes an overlay plus per-region anterior differences (candidate - reference, in cm of the candidate head).
usage: blender -b --factory-startup --python blender_gd_profile.py -- <ref panel png> <y0 frac> <y1 frac> <out prefix> <head1.npy> [...]
(y0/y1: brow and chin rows of the reference panel as fractions of its height, used to crop the comparison band)"""
import bpy, sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; REF, Y0, Y1, OUTP = a[0], float(a[1]), float(a[2]), a[3]; HEADS = a[4:]
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im); return x
def save(x, p):
    h, w = x.shape[:2]; im = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :x.shape[2]] = x
    im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(p); im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
R = load(REF)[..., :3]; H, W = R.shape[:2]
bg = np.median(np.concatenate([R[:20, -40:].reshape(-1, 3), R[:20, :40].reshape(-1, 3)]), 0)
diff = np.abs(R-bg[None, None, :]).max(-1); fg = diff > 0.07
ref_pts = []
for y in range(int(Y0*H), int(Y1*H)):
    xs = np.nonzero(fg[y])[0]
    if len(xs): ref_pts.append((xs.max(), y))
ref_pts = np.asarray(ref_pts, float)
# candidate: orthographic render from -x, nose to image right (UE y -> image x, UE z -> image up)
T, MI = head_topology(); keep = np.isin(MI, [0, 3, 4, 8]); TT = T[keep]
res = {}
def profile_of(X, px_per_cm=20.0):
    S = X[:24049]; y, z = S[:, 1], S[:, 2]
    zs = np.arange(144.0, 180.0, 0.05); prof = []
    # silhouette of the head projected on the y-z plane (anterior envelope = max y per z), through all skin vertices
    for zz in zs:
        m = np.abs(z-zz) < 0.12
        if m.any(): prof.append((y[m].max(), zz))
    return np.asarray(prof)
for hp in HEADS:
    X = np.load(hp); tag = os.path.basename(hp).replace('.npy', ''); P = profile_of(X)
    # landmarks on the candidate profile to define the same brow -> chin band: brow = max-y point between z 163-167, chin bottom = menton ~ lowest
    br = P[(P[:, 1] > 163) & (P[:, 1] < 167.5)]; brow_z = br[np.argmax(br[:, 0]), 1]
    lo = P[(P[:, 1] < 156) & (P[:, 1] > 146)]; chin_y = lo[:, 0].max(); men = lo[lo[:, 0] > chin_y-2.6]; men_z = men[:, 1].min()
    band = P[(P[:, 1] <= brow_z) & (P[:, 1] >= men_z)]
    # fit: ref_x = s*y + tx, ref_y = -s*z + ty ; s from band heights, then translation by least squares along the band
    s = (ref_pts[-1, 1]-ref_pts[0, 1])/(brow_z-men_z); ty = ref_pts[0, 1]+s*brow_z
    rz = (ty-ref_pts[:, 1])/s; ry = np.interp(rz, band[:, 1], band[:, 0])   # candidate y at the reference rows
    tx = np.median(ref_pts[:, 0]-s*ry)
    dif = (s*ry+tx-ref_pts[:, 0])/s                                      # cm, + = candidate more anterior
    regions = {}
    for nm, (z0, z1) in {'brow/forehead': (brow_z-1.0, brow_z+0.1), 'nasion': (brow_z-2.6, brow_z-1.0), 'dorsum': (brow_z-5.0, brow_z-2.6), 'nose tip': (brow_z-6.6, brow_z-5.0),
                         'subnasal/upper lip': (brow_z-9.0, brow_z-6.6), 'lips': (brow_z-10.6, brow_z-9.0), 'chin': (men_z, brow_z-10.6)}.items():
        m = (rz >= z0) & (rz <= z1)
        if m.any(): regions[nm] = round(float(np.mean(dif[m])), 2)
    res[tag] = {'scale_px_per_cm': round(float(s), 2), 'brow_z': float(brow_z), 'menton_z': float(men_z), 'regions_cm': regions}
    img = R.copy()
    for (xr, yr) in ref_pts.astype(int): img[max(yr-1, 0):yr+1, max(xr-1, 0):xr+2] = (0.1, 1.0, 0.2)
    full = P; fx = s*full[:, 0]+tx; fy = ty-s*full[:, 1]
    for xi, yi in zip(fx.astype(int), fy.astype(int)):
        if 0 <= yi < H and 0 <= xi < W: img[max(yi-1, 0):yi+1, max(xi-1, 0):xi+2] = (1.0, 0.15, 0.15)
    save(img, f'{OUTP}_{tag}.png')
    # orthographic clay render in the reference panel frame (x_img = s*y + tx, y_img = ty - s*z), 50% blend
    sc = bpy.context.scene
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new('h'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.update(); ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
    for pg in me.polygons: pg.use_smooth = True
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.78, 0.76, 0.74); sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = W, H; sc.view_settings.view_transform = 'Standard'
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'HORIZONTAL'; cam.data.ortho_scale = W/s
    from mathutils import Matrix
    yc = (W/2-tx)/s; zc = (ty-H/2)/s; f_ = np.array([1.0, 0, 0]); r_ = np.array([0, 1.0, 0]); u_ = np.array([0, 0, 1.0]); X_ = -r_; Y_ = u_; Z_ = -f_
    cam.matrix_world = Matrix(((X_[0], Y_[0], Z_[0], -300.0), (X_[1], Y_[1], Z_[1], yc), (X_[2], Y_[2], Z_[2], zc), (0, 0, 0, 1)))
    tmp = os.path.abspath(OUTP+'_tmp.png'); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True)
    cl = load(tmp)[:, ::-1]; a_ = cl[..., 3:4]; clc = cl[..., :3]*a_+R*(1-a_); blend = 0.5*clc+0.5*R
    save(blend, f'{OUTP}_{tag}_blend.png'); side = np.concatenate([R, clc], 1); save(side, f'{OUTP}_{tag}_side.png')
print('PROFILE', json.dumps(res))
