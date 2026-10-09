"""GD14: warp a UE capture made with a gd14_uecams 'ref' camera (same optical centre as the solved panel camera) onto that reference panel's frame
(SCALE x panel pixels). Exact for a shared centre: panel ray -> world direction -> UE pixel (roll / principal point / focal handled), bilinear.
usage: blender -b --factory-startup --python gd14_warp.py -- <uecams.json> <view> <scale> <in.png> <out.png> [<in2.png> <out2.png> ...]"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'GD13_Identity_20261009', 'tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; J = json.load(open(a[0])); V = a[1]; S = float(a[2]); pairs = list(zip(a[3::2], a[4::2]))
c = J['ref'][V]; R = np.array(c['R']); f = c['f']*S; cx = c['cx']*S; cy = c['cy']*S; W, H = int(round(c['panel'][0]*S)), int(round(c['panel'][1]*S))
yaw, pitch = math.radians(c['cam'][3]), math.radians(c['cam'][4]); FW = np.array([math.cos(pitch)*math.cos(yaw), math.cos(pitch)*math.sin(yaw), math.sin(pitch)])
RT = np.array([-math.sin(yaw), math.cos(yaw), 0.0]); UP = np.array([-math.sin(pitch)*math.cos(yaw), -math.sin(pitch)*math.sin(yaw), math.cos(pitch)])
N = J['size']; fpx = (N/2)/math.tan(math.radians(J['fov'])/2)
py, px = np.mgrid[0:H, 0:W].astype(np.float64); rc = np.stack([(px+0.5-cx)/f, (py+0.5-cy)/f, np.ones_like(px)], -1); d = rc@R   # world dirs (R rows = cam axes)
u = N/2+fpx*(d@RT)/(d@FW)-0.5; v = N/2-fpx*(d@UP)/(d@FW)-0.5
for src, dst in pairs:
    img = gi.load(src); h, w = img.shape[:2]; assert (h, w) == (N, N), (h, w)
    x0 = np.clip(np.floor(u).astype(int), 0, w-2); y0 = np.clip(np.floor(v).astype(int), 0, h-2); fx = np.clip(u-x0, 0, 1)[..., None]; fy = np.clip(v-y0, 0, 1)[..., None]
    o = (img[y0, x0]*(1-fx)*(1-fy)+img[y0, x0+1]*fx*(1-fy)+img[y0+1, x0]*(1-fx)*fy+img[y0+1, x0+1]*fx*fy); o[..., 3] = 1.0
    gi.save(dst, o); print('WARPED', V, dst, W, H)
