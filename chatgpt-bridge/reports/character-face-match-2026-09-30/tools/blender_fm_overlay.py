"""FACE-MATCH board B: pupil-aligned 50 % overlay of the reference and a candidate capture (similarity transform: the candidate's two
pupils are mapped onto the reference's), + landmark markers (reference = red, candidate = green, transformed) and optional
horizontal level lines at reference landmark heights. Points are fractions of each source image (top-left origin).
Job: ref|cand|dst|refL|refR|candL|candR|crop(x0:y0:x1:y1 of ref)|W[|refmarks x:y;..|candmarks x:y;..]
usage: blender -b --factory-startup --python blender_fm_overlay.py -- job ..."""
import bpy, sys
import numpy as np
def load(p):
    im = bpy.data.images.load(p); w, h = im.size; a = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1, :, :3]; bpy.data.images.remove(im); return a
def pt(s, w, h): x, y = map(float, s.split(':')); return np.array([x*w, y*h])
def sample(a, X, Y):
    h, w = a.shape[:2]; x0 = np.clip(np.floor(X).astype(int), 0, w-2); y0 = np.clip(np.floor(Y).astype(int), 0, h-2); fx = np.clip(X-x0, 0, 1)[..., None]; fy = np.clip(Y-y0, 0, 1)[..., None]
    o = a[y0, x0]*(1-fx)*(1-fy)+a[y0, x0+1]*fx*(1-fy)+a[y0+1, x0]*(1-fx)*fy+a[y0+1, x0+1]*fx*fy
    o[(X < 0) | (Y < 0) | (X > w-1) | (Y > h-1)] = 0.5; return o
def mark(o, x, y, col, r=6):
    H, W = o.shape[:2]; x, y = int(x), int(y)
    if 0 <= x < W and 0 <= y < H: o[max(y-r, 0):y+r+1, max(x-1, 0):x+2] = col; o[max(y-1, 0):y+2, max(x-r, 0):x+r+1] = col
for job in sys.argv[sys.argv.index('--')+1:]:
    f = job.split('|'); R = load(f[0]); Cd = load(f[1]); dst = f[2]; hr, wr = R.shape[:2]; hc, wc = Cd.shape[:2]
    rL, rR = pt(f[3], wr, hr), pt(f[4], wr, hr); cL, cR = pt(f[5], wc, hc), pt(f[6], wc, hc)
    x0, y0, x1, y1 = map(float, f[7].split(':')); W = int(f[8]); H = int(W*(y1-y0)*hr/((x1-x0)*wr))
    vr = rR-rL; vc = cR-cL; s = np.linalg.norm(vc)/np.linalg.norm(vr); ang = np.arctan2(vc[1], vc[0])-np.arctan2(vr[1], vr[0]); ca, sa = np.cos(ang), np.sin(ang)
    gx, gy = np.meshgrid(x0*wr+(np.arange(W)+0.5)*(x1-x0)*wr/W, y0*hr+(np.arange(H)+0.5)*(y1-y0)*hr/H)
    dx, dy = gx-rL[0], gy-rL[1]; cx = cL[0]+s*(ca*dx-sa*dy); cy = cL[1]+s*(sa*dx+ca*dy)           # ref pixel -> candidate pixel
    A = float(__import__("os").environ.get("OV_A", "0.5")); o = (1-A)*sample(R, gx, gy)+A*sample(Cd, cx, cy)
    to_out = lambda p: ((p[0]-x0*wr)*W/((x1-x0)*wr), (p[1]-y0*hr)*H/((y1-y0)*hr))
    inv = lambda p: (lambda q: rL+np.array([ca*q[0]+sa*q[1], -sa*q[0]+ca*q[1]])/s)(p-cL)               # candidate pixel -> ref pixel
    rm = [pt(m, wr, hr) for m in (f[9].split(';') if len(f) > 9 and f[9] else [])]+[rL, rR]
    cm = [inv(pt(m, wc, hc)) for m in (f[10].split(';') if len(f) > 10 and f[10] else [])]+[inv(cL), inv(cR)]
    for p in rm:
        X_, Y_ = to_out(p); mark(o, X_, Y_, (1, 0.1, 0.1)); o[int(np.clip(Y_, 0, H-1)), :] = o[int(np.clip(Y_, 0, H-1)), :]*0.6+np.array([1, 0.1, 0.1])*0.4
    for p in cm:
        X_, Y_ = to_out(p); mark(o, X_, Y_, (0.1, 1, 0.2)); o[int(np.clip(Y_, 0, H-1)), ::3] = np.array([0.1, 1, 0.2])
    out = bpy.data.images.new('ov', W, H); rgba = np.ones((H, W, 4), np.float32); rgba[..., :3] = np.clip(o[::-1], 0, 1)
    out.pixels.foreach_set(rgba.ravel()); out.filepath_raw = dst; out.file_format = 'PNG'; out.save(); print('OVERLAY', dst, W, H, 'scale', round(s, 3), 'rot_deg', round(np.degrees(ang), 2))
