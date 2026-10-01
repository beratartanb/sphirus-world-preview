"""GUARDIAN face pass: fast art-direction preview. Renders head targets (DNA-order npy, UE cm) as neutral clay from the reference-solved
cameras, crops into the reference frames, and writes per view: clay, clay + 50% reference overlay with the reference tracker curves (green)
and the mesh-bound curves (red, from semantic json), plus a clay profile. Several heads side by side for A/B.
usage: blender -b --factory-startup --python blender_gd_preview.py -- <out_prefix> <semantic.json> <head1.npy> [<head2.npy> ...]"""
import bpy, sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import *
a = sys.argv[sys.argv.index('--')+1:]; OUTP, SEM = a[0], json.load(open(a[1])); HEADS = a[2:]
PK = json.load(open(I+'/ref_picks.json')); T, MI = head_topology(); keep = np.isin(MI, [0, 3, 4, 8]); TT = T[keep]; RS = 1600
sc = bpy.context.scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'; sc.display.shading.single_color = (0.78, 0.76, 0.74)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = 'WORLD'; sc.render.film_transparent = True; sc.render.resolution_x = sc.render.resolution_y = RS
sc.view_settings.view_transform = 'Standard'
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.sensor_fit = 'HORIZONTAL'
from mathutils import Matrix, Vector
def set_cam(o, f, r, u, fov):
    X = -r; Y = u; Z = -f; M = Matrix(((X[0], Y[0], Z[0], o[0]), (X[1], Y[1], Z[1], o[1]), (X[2], Y[2], Z[2], o[2]), (0, 0, 0, 1))); cam.matrix_world = M; cam.data.angle = math.radians(fov)
def load_img(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im)
    if x.shape[2] == 3: x = np.concatenate([x, np.ones((h, w, 1), np.float32)], -1)
    return x
def save_img(x, p):
    h, w = x.shape[:2]; im = bpy.data.images.new('o', w, h, alpha=True); im.pixels.foreach_set(np.ascontiguousarray(x[::-1], dtype=np.float32).ravel()); im.filepath_raw = os.path.abspath(p); im.file_format = 'PNG'; im.save(); bpy.data.images.remove(im)
def resample(x, x0, y0, x1, y1, W, H):
    h, w = x.shape[:2]; xs = (x0+(np.arange(W)+0.5)/W*(x1-x0))*w-0.5; ys = (y0+(np.arange(H)+0.5)/H*(y1-y0))*h-0.5
    xi = np.clip(xs, 0, w-1.001); yi = np.clip(ys, 0, h-1.001); X0 = np.floor(xi).astype(int); Y0 = np.floor(yi).astype(int); fx = (xi-X0)[None, :, None]; fy = (yi-Y0)[:, None, None]
    A = x[Y0][:, X0]; B = x[Y0][:, X0+1]; C = x[Y0+1][:, X0]; D = x[Y0+1][:, X0+1]; return (A*(1-fx)+B*fx)*(1-fy)+(C*(1-fx)+D*fx)*fy
def draw(img, pts, col, r=1):
    h, w = img.shape[:2]; p = np.asarray(pts, float)
    for i in range(len(p)-1):
        for t in np.linspace(0, 1, 10):
            q = p[i]*(1-t)+p[i+1]*t; xi, yi = int(round(q[0])), int(round(q[1]))
            if 0 <= xi < w and 0 <= yi < h: img[max(yi-r, 0):yi+r+1, max(xi-r, 0):xi+r+1, :3] = col
def mesh_curves(view, X):
    out = {}
    for k in SEM[view]:
        lst = SEM['front' if ('eyelid' in k or 'lip_' in k) else view][k]
        pts = [np.asarray(e[1])@X[e[0]] for e in lst if e is not None]
        if len(pts) > 1: out[k] = topix(view, np.asarray(pts))
    return out
tmp = os.path.abspath(OUTP+'_tmp.png'); res = {}
for hi, hp in enumerate(HEADS):
    X = np.load(hp); me = bpy.data.meshes.new('h'); me.from_pydata([tuple(v) for v in X], [], [tuple(t[::-1]) for t in TT]); me.validate(); me.update()
    ob = bpy.data.objects.new('h', me); sc.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    tag = os.path.basename(hp).replace('.npy', '')
    for view in VIEWS:
        v = VIEWS[view]; o, f, r, u = basis(v['cam']); set_cam(o, f, r, u, v['fov']); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True)
        img = load_img(tmp)[:, ::-1]                                  # mirrored camera basis (UE is left-handed) -> flip back
        x0, y0, x1, y1 = crop_rect(view); clay = resample(img, x0, y0, x1, y1, v['W'], v['H'])
        ref = load_img(v['ref']); bg = np.zeros_like(clay); bg[..., :3] = 0.35; bg[..., 3] = 1
        cl = clay[..., 3:4]; clayc = clay*cl+bg*(1-cl); clayc[..., 3] = 1; save_img(clayc, f'{OUTP}_{tag}_{view}_clay.png')
        ov = 0.5*clayc+0.5*ref; ov[..., 3] = 1
        for k, pts in ref_curves(view).items(): draw(ov, pts, (0.1, 1.0, 0.2))
        mc = mesh_curves(view, X); json.dump({k: v.tolist() for k, v in mc.items()}, open(f'{OUTP}_{tag}_{view}_curves.json', 'w'))
        for k, pts in mc.items(): draw(ov, pts, (1.0, 0.15, 0.15))
        al = clay[..., 3] > 0.5; edge = al & ~(np.roll(al, 1, 0) & np.roll(al, -1, 0) & np.roll(al, 1, 1) & np.roll(al, -1, 1)); ov[edge, :3] = (1.0, 0.3, 0.1)
        PKV = PK['front' if view == 'front' else 'close']
        for c in PKV['contours']+PKV['points']:
            xr, yr = c['ref']; xi, yi = int(xr), int(yr); ov[max(yi-3, 0):yi+4, max(xi-3, 0):xi+4, :3] = (0.1, 1.0, 0.9)
        save_img(ov, f'{OUTP}_{tag}_{view}_ov.png')
        rc = ref_curves(view); errs = []
        for k in mc:
            rp = np.asarray(rc[k]); cp_ = mc[k]; n = min(len(rp), len(cp_)); errs.append(np.linalg.norm(rp[:n]-cp_[:n], axis=1).mean())
        res[f'{tag}_{view}'] = round(float(np.mean(errs)), 2)
    # clay profile (left side, UE +x looking -x) and 3/4 low
    for nm, c in (('side', [-125, 3, 159, 0, 0]), ('frontstd', [0, 125, 159, -90, 0])):
        o, f, r, u = basis(c); set_cam(o, f, r, u, 15.0); sc.render.filepath = tmp; bpy.ops.render.render(write_still=True)
        img = load_img(tmp)[:, ::-1]; img = img[100:1500, 200:1400]; bg = np.zeros_like(img); bg[..., :3] = 0.35; bg[..., 3] = 1; cl = img[..., 3:4]; img = img*cl+bg*(1-cl); img[..., 3] = 1
        save_img(img, f'{OUTP}_{tag}_{nm}_clay.png')
    bpy.data.objects.remove(ob, do_unlink=True)
print('PREVIEW_OK', json.dumps(res))
