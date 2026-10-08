"""pass O1: crop + resize UE captures around the projected head centre so the MetaHuman tracker sees them at the scale of the 6-view
reference panels (~500 px). Writes <dst.png> and <dst.json> {src, cam, fov, W, x0, y0, side, out} so tracker pixels map back to the capture.
usage: blender -b --python blender_g11o1_prep.py -- <capture.png> <capture.json> <dst.png> [side_px=1150] [out_px=512] [centre x,y,z=-0.23,8,158]"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; SIDE = int(a[3]) if len(a) > 3 else 1150; OUT = int(a[4]) if len(a) > 4 else 512
CEN = np.array([float(v) for v in a[5].split(',')]) if len(a) > 5 else np.array([-0.23, 8.0, 158.0])
J = json.load(open(a[1])); cam, fov = J['cam'], float(J['fov'])
def basis(cam):
    x, y, z, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
    return np.array([x, y, z], float), np.array([cy*cp, sy*cp, sp]), np.array([-sy, cy, 0.0]), np.array([-cy*sp, -sy*sp, cp])
im = bpy.data.images.load(os.path.abspath(a[0])); W, H = im.size; P = np.array(im.pixels[:], np.float32).reshape(H, W, 4)[::-1]
o, f, r, u = basis(cam); t = math.tan(math.radians(fov)/2); d = CEN-o; dd = d@f
cx = (0.5+0.5*(d@r)/dd/t)*W; cy = (0.5-0.5*(d@u)/dd/t)*H
x0 = int(round(cx-SIDE/2)); y0 = int(round(cy-SIDE/2)); x0 = min(max(x0, 0), W-SIDE); y0 = min(max(y0, 0), H-SIDE)
C = P[y0:y0+SIDE, x0:x0+SIDE]; k = SIDE/OUT; ys = ((np.arange(OUT)+0.5)*k).astype(int); xs = ((np.arange(OUT)+0.5)*k).astype(int)
# box filter downscale (average k x k blocks) to avoid aliasing on hair
acc = np.zeros((OUT, OUT, 4), np.float32); n = 0; s = max(int(k), 1)
for dy in range(s):
    for dx in range(s):
        acc += C[np.clip(ys-s//2+dy, 0, SIDE-1)][:, np.clip(xs-s//2+dx, 0, SIDE-1)]; n += 1
O = acc/n; O[..., 3] = 1
o_ = bpy.data.images.new('p', OUT, OUT); o_.pixels.foreach_set(np.ascontiguousarray(O[::-1]).ravel()); o_.filepath_raw = os.path.abspath(a[2]); o_.file_format = 'PNG'; o_.save()
json.dump(dict(src=a[0], cam=cam, fov=fov, W=W, H=H, x0=x0, y0=y0, side=SIDE, out=OUT), open(os.path.splitext(a[2])[0]+'.json', 'w'))
print('PREP_OK', a[2], 'centre px %.0f,%.0f box %d,%d' % (cx, cy, x0, y0))
