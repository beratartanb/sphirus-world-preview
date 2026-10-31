"""xr2_walkmap.py (offline numpy, Blender-bundled Python): permeability / walkability analysis of the exterior for XR2.
usage: xr2_walkmap.py <height.u16> <foliage.json> <actors.json> <out_prefix> [spawn.json|-] [x0 x1 y0 y1]
Grid 50 cm. A cell is BLOCKED when the local terrain slope exceeds the CMC walkable angle (44.77 deg, measured over 1 m) or a collision
footprint covers it (collision foliage trunks: radius by mesh class; rocks/logs/stumps: oriented box from mesh bounds x scale; house
level actors: bounds; spawned XR2 actors from spawn.json). The capsule (r 35 cm) is accounted for by eroding the free space by one cell.
Reachability = 8-connected flood fill from the veranda (8.5, 16.5 m); a neighbour step rising > 45 cm (MaxStepHeight) is refused.
Water deeper than 1.1 m below the pond plane is blocked.
Writes <out_prefix>_walk.png (reachable tinted by ease: green easy / yellow medium / orange hard; red = slope-blocked; black = obstacle;
grey = unreachable; 10 m grid) and <out_prefix>_walk.json (reachable area, map-edge leak, straight-line escape distance per heading)."""
import sys, json, math, zlib, struct
from collections import deque
import numpy as np

HF, FF, AF, OUTP = sys.argv[1:5]
SPAWN = json.load(open(sys.argv[5])) if len(sys.argv) > 5 and sys.argv[5] != '-' else []
X0, X1, Y0, Y1 = (map(float, sys.argv[6:10]) if len(sys.argv) > 9 else (-12000.0, 12000.0, -16000.0, 14000.0))
OX, OY, N = -50040.0, -50225.0, 1017
Z = (np.fromfile(HF, dtype='<u2').reshape(N, N).astype(np.float64) - 32768.0) * 100.0 / 128.0
C = 50.0
W, H = int((X1 - X0) / C), int((Y1 - Y0) / C)
xs = X0 + (np.arange(W) + .5) * C; ys = Y0 + (np.arange(H) + .5) * C
GX, GY = np.meshgrid((xs - OX) / 100.0, (ys - OY) / 100.0)
ix, iy = np.floor(GX).astype(int), np.floor(GY).astype(int); fx, fy = GX - ix, GY - iy
zz = Z[iy, ix] * (1 - fx) * (1 - fy) + Z[iy, ix + 1] * fx * (1 - fy) + Z[iy + 1, ix] * (1 - fx) * fy + Z[iy + 1, ix + 1] * fx * fy
gx = (np.roll(zz, -1, 1) - np.roll(zz, 1, 1)) / (2 * C); gy = (np.roll(zz, -1, 0) - np.roll(zz, 1, 0)) / (2 * C)
slope = np.degrees(np.arctan(np.hypot(gx, gy)))
blocked_slope = slope > 44.77
water = zz < -210.0
obst = np.zeros_like(zz, bool)


def _win(x, y, r):
    i0, i1 = max(int((x - r - X0) / C), 0), min(int((x + r - X0) / C) + 1, W)
    j0, j1 = max(int((y - r - Y0) / C), 0), min(int((y + r - Y0) / C) + 1, H)
    return i0, i1, j0, j1


def stamp_disc(x, y, r):
    i0, i1, j0, j1 = _win(x, y, r)
    if i0 >= i1 or j0 >= j1: return
    X, Y = np.meshgrid(xs[i0:i1], ys[j0:j1]); obst[j0:j1, i0:i1] |= (X - x) ** 2 + (Y - y) ** 2 <= r * r


def stamp_box(x, y, yaw, hx, hy):
    i0, i1, j0, j1 = _win(x, y, math.hypot(hx, hy))
    if i0 >= i1 or j0 >= j1: return
    X, Y = np.meshgrid(xs[i0:i1], ys[j0:j1]); c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    u_, v_ = (X - x) * c + (Y - y) * s, -(X - x) * s + (Y - y) * c
    obst[j0:j1, i0:i1] |= (np.abs(u_) <= hx) & (np.abs(v_) <= hy)


TRUNK = {'SM_PineTree': 30, 'SM_Fir_Tree': 22, 'SM_Oak': 55, 'SM_Pine_Juvenile': 9}
for r in json.load(open(FF)):
    if not r['collision'].startswith('QUERY'): continue
    n = r['mesh'].split('/')[-1]; e = r['mesh_bounds'][1]; o = r['mesh_bounds'][0]
    tr = next((v for k, v in TRUNK.items() if n.startswith(k)), None)
    for t in r['xf']:
        if not (X0 < t[0] < X1 and Y0 < t[1] < Y1): continue
        if tr is not None:
            stamp_disc(t[0], t[1], tr * t[6])
        elif e[2] * t[8] > 22:
            c, s = math.cos(math.radians(t[4])), math.sin(math.radians(t[4]))
            cx, cy = t[0] + (o[0] * c - o[1] * s) * t[6], t[1] + (o[0] * s + o[1] * c) * t[7]
            stamp_box(cx, cy, t[4], e[0] * t[6] * 0.85, e[1] * t[7] * 0.85)
for a in json.load(open(AF)):
    if a['level'] == 'L_GR_CurrentHouseContent' and a['class'] == 'StaticMeshActor' and a['b'][1][2] > 40 and a['b'][1][0] < 2500 \
       and a['b'][1][1] < 2500 and a['b'][0][2] - a['b'][1][2] < 150:
        stamp_box(a['b'][0][0], a['b'][0][1], 0, a['b'][1][0], a['b'][1][1])
for s in SPAWN:
    if s.get('block', True) and s.get('top_cm', 999) > 45:
        stamp_box(s['fx'], s['fy'], s['yaw'], s['hx'], s['hy'])
free = ~(blocked_slope | water | obst)
er = free.copy(); er[1:, :] &= free[:-1, :]; er[:-1, :] &= free[1:, :]; er[:, 1:] &= free[:, :-1]; er[:, :-1] &= free[:, 1:]
reach = np.zeros_like(er); dist = np.full(er.shape, -1.0)
sx, sy = int((850 - X0) / C), int((1650 - Y0) / C)
if not er[sy, sx]:
    cand = np.argwhere(er[sy - 6:sy + 7, sx - 6:sx + 7]); sy, sx = sy - 6 + cand[0][0], sx - 6 + cand[0][1]
q = deque([(sy, sx)]); reach[sy, sx] = True; dist[sy, sx] = 0
NB = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)]
while q:
    j, i = q.popleft()
    for dj, di, w in NB:
        jj, ii = j + dj, i + di
        if 0 <= jj < H and 0 <= ii < W and not reach[jj, ii] and er[jj, ii] and abs(zz[jj, ii] - zz[j, i]) < 45:
            reach[jj, ii] = True; dist[jj, ii] = dist[j, i] + w * C / 100; q.append((jj, ii))
k = 3; dens = np.zeros_like(zz); ob = (~free).astype(float)
for dj in range(-k, k + 1):
    for di in range(-k, k + 1):
        dens += np.roll(np.roll(ob, dj, 0), di, 1)
dens /= (2 * k + 1) ** 2
img = np.zeros((H, W, 3))
L = np.array([-0.55, -0.55, 0.63]); L /= np.linalg.norm(L)
nrm = np.dstack([-gx * 1.6, -gy * 1.6, np.ones_like(zz)]); nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
base = 0.55 + 0.45 * np.clip(nrm @ L, 0, 1)[..., None]
img[:] = np.array([0.62, 0.62, 0.62]) * base
easy = reach & (slope < 15) & (dens < 0.08); mid = reach & ~easy & (slope < 30); hard = reach & ~easy & ~mid
img[easy] = (np.array([0.55, 0.85, 0.45]) * base)[easy]
img[mid] = (np.array([0.95, 0.85, 0.35]) * base)[mid]
img[hard] = (np.array([0.95, 0.55, 0.25]) * base)[hard]
img[blocked_slope] = np.array([0.75, 0.1, 0.1]); img[obst] = np.array([0.1, 0.1, 0.1]); img[water] = np.array([0.3, 0.45, 0.7])
for step, a in ((100.0, 0.12), (500.0, 0.35)):
    qz = np.floor(zz / step); edge = (np.abs(np.diff(qz, axis=0, prepend=qz[:1])) + np.abs(np.diff(qz, axis=1, prepend=qz[:, :1]))) > 0
    img[edge] *= (1 - a)
for gl in range(int(math.ceil(X0 / 1000)) * 1000, int(X1), 1000):
    img[:, int((gl - X0) / C)] *= 0.75
for gl in range(int(math.ceil(Y0 / 1000)) * 1000, int(Y1), 1000):
    img[int((gl - Y0) / C), :] *= 0.75
im8 = (np.clip(img, 0, 1) * 255).astype(np.uint8)
raw = b''.join(b'\x00' + im8[r].tobytes() for r in range(H))
ch = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
open(OUTP + '_walk.png', 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)) + ch(b'IDAT', zlib.compress(raw, 6)) + ch(b'IEND', b''))
esc = {}
for a in range(0, 360, 15):
    d = 0.0
    while d < 25000:
        x, y = 850 + math.cos(math.radians(a)) * d, 1650 + math.sin(math.radians(a)) * d
        i, j = int((x - X0) / C), int((y - Y0) / C)
        if not (0 <= i < W and 0 <= j < H) or not er[j, i]: break
        d += 25
    esc[a] = round(d / 100, 1)
st = {'reach_area_m2': int(reach.sum() * C * C / 1e4), 'reach_touches_map_edge': bool(reach[0].any() or reach[-1].any() or reach[:, 0].any() or reach[:, -1].any()),
      'blocked_slope_m2': int(blocked_slope.sum() * C * C / 1e4), 'obstacle_m2': int(obst.sum() * C * C / 1e4), 'radial_straight_escape_m': esc,
      'extent_cm': [X0, X1, Y0, Y1], 'cell_cm': C}
np.save(OUTP + '_reach.npy', reach); np.save(OUTP + '_dist.npy', dist); np.save(OUTP + '_free.npy', er); np.save(OUTP + '_z.npy', zz.astype(np.float32))
json.dump(st, open(OUTP + '_walk.json', 'w'), indent=1)
print('WALKMAP', json.dumps({k: v for k, v in st.items() if k != 'radial_straight_escape_m'}), 'radial', esc)
