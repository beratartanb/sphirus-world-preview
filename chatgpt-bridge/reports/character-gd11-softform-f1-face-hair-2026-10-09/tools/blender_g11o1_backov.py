"""pass O1/H1: BACK-VIEW hair silhouette overlay on ref6_back. The back capture camera mirrors front_f (same distance / height / fov), so the
front similarity (ov5 front scale + vertical shift, from <label>_ov5.json + the front capture) maps capture rows to panel rows; horizontal shift
aligns the neck centre (row ~4 cm below the mouth line). Background-keyed masks (2 px opening). Per row: hair half-widths left / right of the
neck centre, mm (+ = candidate wider); bottom of the mass per column; bun bounding box (darkest/most chromatic blob is not tracked: outline only).
usage: blender -b --python blender_g11o1_backov.py -- <back capture.png> <back capture.json> <front capture.json> <ov5 lines json (front)> <scale> <ty> <out.png> <label>"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.array(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3].copy(); bpy.data.images.remove(im); return x
def save(O, p):
    h, w = O.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(O, 0, 1); o = bpy.data.images.new('o', w, h); o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel())
    o.filepath_raw = os.path.abspath(p); o.file_format = 'PNG'; o.save()
R = load('Saved/Codex/GD11_LikenessW_20261006/ref/ref6_back.png'); C = load(a[0]); h, w = R.shape[:2]
LJ = json.load(open(a[3])); s = float(a[4]); ty = float(a[5]); pxcm = LJ['pxcm']; ey = LJ['ref']['ey']; my = LJ['ref']['my']; d = my-ey
def hsil(I):
    mx_ = I.max(-1); ch = mx_-I.min(-1); lum = I.mean(-1)
    bc = np.median(np.r_[ch[:12, :12].ravel(), ch[:12, -12:].ravel()]); bl = np.median(np.r_[lum[:12, :12].ravel(), lum[:12, -12:].ravel()])
    m = (ch > bc+0.05) | (np.abs(lum-bl) > 0.10)
    for _ in range(2): m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
    for _ in range(2): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m
MR = hsil(R)
# warp candidate: x_ref = s*x_cap + tx, y_ref = s*y_cap + ty; tx from the neck centre at row my + 0.45 d
yn = int(my+0.45*d); MC0 = hsil(C); ync = int(round((yn-ty)/s))
def neck_c(M, y): c = np.nonzero(M[y])[0]; return 0.5*(c.min()+c.max()) if len(c) else None
cr = neck_c(MR, yn); cc = neck_c(MC0, ync); tx = cr-s*cc
yy, xx = np.mgrid[0:h, 0:w]; sx = np.clip(((xx+0.5-tx)/s).astype(int), 0, C.shape[1]-1); sy = np.clip(((yy+0.5-ty)/s).astype(int), 0, C.shape[0]-1); Cw = C[sy, sx]
MC = hsil(Cw); floor = int(my+1.2*d); MC[floor:] = False; MR2 = MR.copy(); MR2[floor:] = False
rep = {'label': a[7], 'neck_centre_ref_px': cr}
def half(M, y):
    c = np.nonzero(M[y])[0]; return (cr-c.min(), c.max()-cr) if len(c) else None
B = [('crown', -2.8, -1.8), ('upper', -1.8, -0.8), ('eartop', -0.8, 0.0), ('ear', 0.0, 0.6), ('nape', 0.6, 1.1)]
for nm, b0, b1 in B:
    L_, R_ = [], []
    for y in range(int(ey+b0*d), int(ey+b1*d)):
        hr, hc = half(MR2, y), half(MC, y)
        if hr and hc: L_.append(hc[0]-hr[0]); R_.append(hc[1]-hr[1])
    if L_: rep[nm] = dict(left=round(float(np.median(L_))/pxcm*10, 1), right=round(float(np.median(R_))/pxcm*10, 1), ref_width_mm=round(float(np.median([sum(half(MR2, y)) for y in range(int(ey+b0*d), int(ey+b1*d)) if half(MR2, y)]))/pxcm*10, 1))
tr = np.nonzero(MR2.any(1))[0]; tc = np.nonzero(MC.any(1))[0]; rep['top_mm'] = round((tc.min()-tr.min())/pxcm*-10, 1) if len(tr) and len(tc) else None
print('BACKOV', json.dumps(rep))
def edge(M):
    e = M & ~(np.roll(M, 1, 0) & np.roll(M, -1, 0) & np.roll(M, 1, 1) & np.roll(M, -1, 1)); return e | np.roll(e, 1, 1)
eR, eC = edge(MR2), edge(MC); CY, CM = (0.1, 0.95, 1.0), (1.0, 0.15, 0.85)
P1 = R.copy(); P1[eR] = CY; P1[eC] = CM; P2 = 0.5*R+0.5*Cw; P2[eR] = CY; P2[eC] = CM; P3 = Cw.copy(); P3[eR] = CY; P3[eC] = CM
for P in (P1, P2, P3):
    for yl in (int(ey), int(ey-1.8*d), int(ey-0.8*d), int(ey+0.6*d)): P[yl, ::4] = (1, 1, 0)
O = np.concatenate([P1, np.ones((h, 4, 3)), P2, np.ones((h, 4, 3)), P3], 1); save(np.repeat(np.repeat(O, 2, 0), 2, 1), a[6]); json.dump(rep, open(os.path.splitext(a[6])[0]+'.json', 'w'), indent=1)
