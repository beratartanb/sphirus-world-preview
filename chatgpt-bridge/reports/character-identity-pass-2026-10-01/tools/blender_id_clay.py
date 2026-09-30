"""IDENTITY pass: fast clay review renders of head shapes (package-order .npy, UE cm) with the SOLVED reference cameras
(weak perspective from recon.json -> Blender orthographic camera) so every render is pixel-aligned with its reference image,
plus a free profile camera. Workbench studio clay, no hair. Writes <out>/<tag>_<view>.png and 50 % overlays <tag>_<view>_ov.png.
usage: blender -b -P blender_id_clay.py -- <recon.json> <out_dir> <tag>=<npy> [<tag>=<npy> ...]"""
import bpy, sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import *
a = sys.argv[sys.argv.index('--')+1:]; RJ, OUT = a[0], a[1]; SH = [x.split('=') for x in a[2:]]; os.makedirs(OUT, exist_ok=True)
RC = json.load(open(RJ)); P = pkg(); T = np.asarray(P['head']['triangles']); MI = np.asarray(P['head']['material_ids'])
IMG = {'front': ('ref_front_x4', 800, 960), 'close': ('ref_close_x2', 794, 940)}; TD = 'Saved/Codex/CharacterIdentity_20260930/track'
keep = np.isin(MI, [0, 3, 4, 1])                               # skin + eyes + teeth
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'; sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.62, 0.6, 0.57)
sh.show_cavity = True; sh.cavity_type = 'WORLD'; sh.curvature_ridge_factor = 0.6; sh.curvature_valley_factor = 0.8; sh.show_shadows = False; sc.render.film_transparent = True
sc.display_settings.display_device = 'sRGB'; sc.view_settings.view_transform = 'Standard'
def to_b(v): return np.array([v[0], -v[1], v[2]])                  # UE (left-handed) -> Blender
def mesh(name, X):
    Xb = X.copy(); Xb[:, 1] *= -1; me = bpy.data.meshes.new(name); me.from_pydata(Xb.tolist(), [], T[keep][:, ::-1].tolist()); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); return ob
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
def set_cam(R, s, t, W, H, center):
    R = np.asarray(R); t = np.asarray(t); cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(W, H)/s
    sc.render.resolution_x, sc.render.resolution_y = W, H
    c2 = np.array([W/2, H/2]); xy = (c2-t)/s; depth = R[2]@center-80
    pos = R[0]*xy[0]+R[1]*xy[1]+R[2]*depth                              # world point on the principal ray, 80 cm in front of the head
    right, down, fwd = to_b(R[0]), to_b(R[1]), to_b(R[2]); M = np.eye(4); M[:3, 0] = right; M[:3, 1] = -down; M[:3, 2] = -fwd; M[:3, 3] = to_b(pos)
    from mathutils import Matrix; cam.matrix_world = Matrix(M.tolist())
def render(path): sc.render.filepath = path; bpy.ops.render.render(write_still=True)
def overlay(ref, rend, out, alpha=0.5):
    A = bpy.data.images.load(ref); B = bpy.data.images.load(rend); w, h = A.size
    a_ = np.asarray(A.pixels[:], np.float32).reshape(h, w, A.channels)[..., :3]; b_ = np.asarray(B.pixels[:], np.float32).reshape(h, w, 4)
    m = b_[..., 3:4]*alpha; o = a_*(1-m)+b_[..., :3]*m; im = bpy.data.images.new('ov', w, h); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = o; im.pixels.foreach_set(rgba.ravel())
    im.filepath_raw = out; im.file_format = 'PNG'; im.save()
for tag, npy in SH:
    X = np.load(npy); ob = mesh(tag, X); center = X[:24049].mean(0)
    for vk, (img, W, H) in IMG.items():
        c = RC['cams'][vk]; set_cam(c['R'], c['s'], c['t'], W, H, center); p = os.path.abspath(f'{OUT}/{tag}_{vk}.png'); render(p)
        overlay(os.path.abspath(f'{TD}/{img}.png'), p, p.replace('.png', '_ov.png'))
    # profile (character right side) and matched 3/4 from the front camera rotated 35 deg, orthographic, same scale as front
    c = RC['cams']['front']; R = np.asarray(c['R']); th = math.radians(90)
    Ry = lambda a_: np.array([[math.cos(a_), -math.sin(a_), 0], [math.sin(a_), math.cos(a_), 0], [0, 0, 1]])
    Rp = R@Ry(-th); set_cam(Rp, c['s'], [400-c['s']*(Rp[0]@center), 480-c['s']*(Rp[1]@center)], 800, 960, center); render(os.path.abspath(f'{OUT}/{tag}_side.png'))
    bpy.data.objects.remove(ob, do_unlink=True)
print('CLAY_OK')
