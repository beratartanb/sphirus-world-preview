"""xr_maps.py (offline, Blender-bundled Python + numpy; no Unreal): top-down plan renders of the exterior for the Exterior World Redesign.
usage: xr_maps.py <recon dir> <height.u16> <foliage.json> <out.png> <x0> <x1> <y0> <y1> <px_per_m> [mode] [overlay.json]
  mode 'plan'  : hillshade + 0.5 m / 2 m contours + water + canopy masses (big trees by crown, young trees, shrubs) + rocks/deadwood
                 + house + routes (descent, pond-side, rear trail)
  mode 'clay'  : hillshade + contours only (terrain read without any vegetation)
  mode 'mass'  : flat terrain tone, canopy crowns as dark discs (big-mass organisation only)
overlay.json (optional): {"polys": [{"pts": [[x,y],...], "rgb": [r,g,b], "w": px, "closed": bool}], "labels": [{"xy": [x,y], "rgb": [...]}]}
Image axes: +x to the right, +y DOWN (Unreal top view: X east, Y south). Writes an 8-bit RGB PNG (zlib, no PIL)."""
import sys, os, json, zlib, struct, math
import numpy as np

R, HF, FF, OUT = sys.argv[1:5]
X0, X1, Y0, Y1, PPM = map(float, sys.argv[5:10])
MODE = sys.argv[10] if len(sys.argv) > 10 else 'plan'
OVL = json.load(open(sys.argv[11])) if len(sys.argv) > 11 else None
OX, OY, N = -50040.0, -50225.0, 1017
Z = (np.fromfile(HF, dtype='<u2').reshape(N, N).astype(np.float64) - 32768.0) * 100.0 / 128.0   # [row=y, col=x] cm
W, H = int((X1 - X0) / 100 * PPM), int((Y1 - Y0) / 100 * PPM)
xs = X0 + (np.arange(W) + .5) / PPM * 100; ys = Y0 + (np.arange(H) + .5) / PPM * 100
gx, gy = (xs - OX) / 100.0, (ys - OY) / 100.0
GX, GY = np.meshgrid(gx, gy)
ix, iy = np.clip(np.floor(GX).astype(int), 0, N - 2), np.clip(np.floor(GY).astype(int), 0, N - 2); fx, fy = GX - ix, GY - iy
zz = (Z[iy, ix] * (1 - fx) * (1 - fy) + Z[iy, ix + 1] * fx * (1 - fy) + Z[iy + 1, ix] * (1 - fx) * fy + Z[iy + 1, ix + 1] * fx * fy)
dzdx = np.gradient(zz, axis=1) / (100.0 / PPM); dzdy = np.gradient(zz, axis=0) / (100.0 / PPM)
L = np.array([-0.55, -0.55, 0.63]); L /= np.linalg.norm(L)
nrm = np.dstack([-dzdx * 1.6, -dzdy * 1.6, np.ones_like(zz)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
shade = np.clip(nrm @ L, 0, 1)
img = np.zeros((H, W, 3))
base = np.array([0.80, 0.78, 0.72]) if MODE != 'mass' else np.array([0.86, 0.85, 0.82])
img[:] = base * (0.45 + 0.55 * shade[..., None]) if MODE != 'mass' else base
WATER_Z = -100.0
water = zz < WATER_Z
img[water] = img[water] * 0.35 + np.array([0.35, 0.47, 0.58]) * 0.65
if MODE in ('plan', 'clay'):
    for step, a in ((50.0, 0.18), (200.0, 0.45)):
        q = np.floor(zz / step); edge = (np.abs(np.diff(q, axis=0, prepend=q[:1])) + np.abs(np.diff(q, axis=1, prepend=q[:, :1]))) > 0
        img[edge] = img[edge] * (1 - a)


def disc(cx, cy, r_cm, rgb, alpha, ring=0.0):
    px, py, rp = (cx - X0) / 100 * PPM, (cy - Y0) / 100 * PPM, max(r_cm / 100 * PPM, 0.8)
    a0, a1, b0, b1 = int(max(px - rp - 1, 0)), int(min(px + rp + 2, W)), int(max(py - rp - 1, 0)), int(min(py + rp + 2, H))
    if a0 >= a1 or b0 >= b1:
        return
    yy, xx = np.mgrid[b0:b1, a0:a1]; d = np.hypot(xx + .5 - px, yy + .5 - py)
    m = d <= rp
    if ring:
        m = m & (d >= rp - ring)
    img[b0:b1, a0:a1][m] = img[b0:b1, a0:a1][m] * (1 - alpha) + np.array(rgb) * alpha


def line(pts, rgb, w=2.0, closed=False):
    P = list(pts) + ([pts[0]] if closed else [])
    for (ax, ay), (bx, by) in zip(P, P[1:]):
        n = int(max(abs(bx - ax), abs(by - ay)) / 100 * PPM * 2) + 1
        for t in np.linspace(0, 1, n):
            disc(ax + (bx - ax) * t, ay + (by - ay) * t, w / PPM * 50, rgb, 0.9)


if MODE != 'clay':
    F = json.load(open(FF))
    BIG = ('SM_PineTree', 'SM_Fir_Tree', 'SM_Oak')
    order = sorted(F, key=lambda r: r['mesh_bounds'][1][2])   # small first, big crowns on top
    for r in order:
        name = r['mesh'].split('/')[-1]; ext = r['mesh_bounds'][1]; ht = ext[2] * 2
        big = any(name.startswith(b) for b in BIG) and ht > 800
        young = ('Juvenile' in name or 'Young' in name or name.startswith('Pine_08'))
        shrub = name.startswith('SM_Bush')
        rock = ('Rock' in name or 'Stone' in name or 'Embankment' in name) and 'Small' not in name
        dead = ('Dead' in name and 'Trunk' in name) or 'FallenTree' in name or 'Stump' in name
        if MODE == 'mass' and not (big or young):
            continue
        for x, y, z, p, yw, rl, sx, sy, sz in r['xf']:
            if not (X0 - 1500 < x < X1 + 1500 and Y0 - 1500 < y < Y1 + 1500):
                continue
            if big:
                cr = max(ext[0], ext[1]) * sx * 0.62
                disc(x, y, cr, (0.12, 0.25, 0.16) if MODE == 'plan' else (0.10, 0.12, 0.11), 0.42 if MODE == 'plan' else 0.55)
                disc(x, y, 35, (0.25, 0.14, 0.06), 1.0)
            elif young:
                disc(x, y, max(ext[0], ext[1]) * sx * 0.55, (0.30, 0.48, 0.28) if MODE == 'plan' else (0.35, 0.38, 0.36), 0.55)
            elif shrub and MODE == 'plan':
                disc(x, y, max(ext[0], ext[1]) * sx * 0.6, (0.50, 0.55, 0.25), 0.45)
            elif rock and MODE == 'plan':
                disc(x, y, max(ext[0], ext[1]) * sx * 0.7, (0.45, 0.45, 0.48), 0.9)
            elif dead and MODE == 'plan':
                a = math.radians(yw); lx = max(ext[0], ext[1]) * sx
                line([(x - math.cos(a) * lx, y - math.sin(a) * lx), (x + math.cos(a) * lx, y + math.sin(a) * lx)], (0.42, 0.25, 0.10), 3)
A = json.load(open(os.path.join(R, 'actors.json')))
for a in A:
    if a['label'].startswith('Architecture_R4_ATTACHED_EXTERIOR_House'):
        (cx, cy, _), (ex, ey, _) = a['b']; line([(cx - ex, cy - ey), (cx + ex, cy - ey), (cx + ex, cy + ey), (cx - ex, cy + ey)], (0.75, 0.30, 0.10), 3, True)
if OVL:
    for p in OVL.get('polys', []):
        line(p['pts'], p.get('rgb', (0.9, 0.1, 0.1)), p.get('w', 2), p.get('closed', False))
    for d in OVL.get('discs', []):
        disc(d['xy'][0], d['xy'][1], d['r'], d.get('rgb', (0.9, 0.1, 0.1)), d.get('a', 0.5), d.get('ring', 0.0))
# 10 m grid ticks on the border for scale
for gxv in range(int(math.ceil(X0 / 1000)) * 1000, int(X1), 1000):
    c = int((gxv - X0) / 100 * PPM); img[:6, max(c - 1, 0):c + 1] = 0; img[-6:, max(c - 1, 0):c + 1] = 0
for gyv in range(int(math.ceil(Y0 / 1000)) * 1000, int(Y1), 1000):
    rr = int((gyv - Y0) / 100 * PPM); img[max(rr - 1, 0):rr + 1, :6] = 0; img[max(rr - 1, 0):rr + 1, -6:] = 0
b8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
raw = b''.join(b'\x00' + b8[r].tobytes() for r in range(H))
ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open(OUT, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
print('MAP', OUT, W, H, MODE)
