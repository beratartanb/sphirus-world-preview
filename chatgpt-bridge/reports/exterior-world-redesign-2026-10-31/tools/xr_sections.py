"""xr_sections.py (offline, numpy; no Unreal): terrain sections BEFORE (grey) vs AFTER (red) for the Exterior World Redesign report.
usage: xr_sections.py <height_before.u16> <height_after.u16> <plan.json> <out.png>
Panels (1:1 vertical scale = true slope, metres): 1) longitudinal profile along the new trail; 2..4) cross-sections perpendicular to the
trail at the gate (s 23.5 m), compression (s 43 m) and climb (s 70 m), +-20 m, left = left of travel. Writes an RGB PNG (zlib, no PIL)."""
import sys, json, math, zlib, struct
import numpy as np

HB, HA, PL, OUT = sys.argv[1:5]
OX, OY, N = -50040.0, -50225.0, 1017
ZB = (np.fromfile(HB, dtype='<u2').reshape(N, N).astype(float) - 32768) * 100 / 128
ZA = (np.fromfile(HA, dtype='<u2').reshape(N, N).astype(float) - 32768) * 100 / 128
T = json.load(open(PL))['trail']
sl = [0.0]
for a, b in zip(T, T[1:]):
    sl.append(sl[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def at(s):
    for k in range(len(T) - 1):
        if s <= sl[k + 1] or k == len(T) - 2:
            L = sl[k + 1] - sl[k]; t = (s - sl[k]) / L; a, b = T[k], T[k + 1]
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), (b[0] - a[0]) / L, (b[1] - a[1]) / L


def z(Z, x, y):
    fx, fy = (x - OX) / 100, (y - OY) / 100; ix, iy = int(fx), int(fy); ax, ay = fx - ix, fy - iy
    return (Z[iy, ix] * (1 - ax) * (1 - ay) + Z[iy, ix + 1] * ax * (1 - ay) + Z[iy + 1, ix] * (1 - ax) * ay + Z[iy + 1, ix + 1] * ax * ay) / 100


W, PH, PAD = 1100, 230, 40
panels = []
S = np.arange(0, sl[-1], 50.0)
panels.append(('trail profile (m along trail)', S / 100, [[z(Zg, *at(s)[:2]) for s in S] for Zg in (ZB, ZA)]))
for name, s0 in (('cross-section gate s=23.5 m', 2350), ('cross-section compression s=43 m', 4300), ('cross-section climb s=70 m', 7000)):
    x0, y0, tx, ty = at(s0); off = np.arange(-2000, 2001, 50.0)
    panels.append((name + ' (left of travel <- 0 -> right)', off / 100, [[z(Zg, x0 - ty * o, y0 + tx * o) for o in off] for Zg in (ZB, ZA)]))
img = np.ones((len(panels) * (PH + PAD) + PAD, W, 3))


def put(r, c, col, w=1):
    for dr in range(-w, w + 1):
        for dc in range(-w, w + 1):
            if 0 <= r + dr < img.shape[0] and 0 <= c + dc < W:
                img[r + dr, c + dc] = col


for k, (name, xs, ys) in enumerate(panels):
    top = PAD + k * (PH + PAD); allz = np.concatenate(ys); zmin, zmax = allz.min() - 0.5, allz.max() + 0.5
    xspan = xs.max() - xs.min(); scale = min((W - 80) / xspan, PH / (zmax - zmin))   # same m/px horizontally and vertically
    for zz in np.arange(math.floor(zmin), zmax, 1.0):
        r = int(top + PH - (zz - zmin) * scale)
        if top <= r < top + PH:
            img[r, 40:W - 20] = 0.9 if zz % 5 else 0.75
    for x_ in np.arange(math.ceil(xs.min() / 10) * 10, xs.max(), 10.0):
        c = int(40 + (x_ - xs.min()) * scale)
        if c < W - 20:
            img[top:top + PH, c] = 0.85
    for vals, col in zip(ys, ((0.45, 0.45, 0.45), (0.85, 0.1, 0.1))):
        prev = None
        for x_, v in zip(xs, vals):
            c = int(40 + (x_ - xs.min()) * scale); r = int(top + PH - (v - zmin) * scale)
            if prev:
                n = max(abs(c - prev[0]), abs(r - prev[1]), 1)
                for t in np.linspace(0, 1, n + 1):
                    put(int(prev[1] + (r - prev[1]) * t), int(prev[0] + (c - prev[0]) * t), col)
            prev = (c, r)
b8 = (np.clip(img, 0, 1) * 255).astype(np.uint8); H = b8.shape[0]
raw = b''.join(b'\x00' + b8[r].tobytes() for r in range(H))
ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open(OUT, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
print('SECTIONS', OUT, [p[0] for p in panels])
