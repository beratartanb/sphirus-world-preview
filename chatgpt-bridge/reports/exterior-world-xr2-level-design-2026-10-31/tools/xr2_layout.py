"""xr2_layout.py: the XR2 exterior masterplan layout shared by the design, probe and map scripts (Unreal cm; +X east, +Y south).
Run directly to write the probe list: xr2_layout.py <out.json>."""
import math, json, sys

# Route A "Gol Yolu" (pond path, main 1): veranda -> intimate front footpath -> north-shore landing -> east-bank shelf (compression
# between water and a rock bank) -> SE inlet crossing -> south shore -> far-shore glade (destination, refuge lookback to the house).
ROUTE_A = [(950, 1550), (870, 1950), (720, 2330), (620, 2620), (980, 2840), (1400, 2980), (1800, 3250), (2200, 3700), (2520, 4300),
           (2680, 5000), (2620, 5700), (2420, 6350), (2100, 6950), (1650, 7550), (1000, 8050), (250, 8350), (-500, 8600), (-900, 8750)]
# Route B "Sirt Patikasi" (rear trail, main 2): house SE corner -> yard gate -> rock narrows -> hollow crossing -> valley climb -> saddle.
# R1 r5 alignment up to the hollow; r6 climb re-routed through the gap between the two existing shrub masses (x 17-19 m).
ROUTE_B = [(1950, 2110), (2380, 1520), (2600, 700), (2700, -100), (2850, -1000), (2920, -1750), (2700, -2450), (2250, -3150),
           (1850, -3800), (1750, -4500), (1700, -5200), (1550, -5800), (1380, -6250)]
# veranda front -> house SE corner (J2), and J2 -> pond path (small house loop)
CONNECT = [(950, 1550), (1300, 1730), (1650, 1930), (1950, 2110)]
DESCENT = [(1950, 2110), (1850, 2550), (1600, 2900), (1400, 2980)]
# faint optional pond loop (west shore, rough): landing -> north shore west -> west shore -> SW sedge -> glade
WEST_LOOP = [(620, 2620), (-300, 2750), (-1500, 2700), (-2600, 2900), (-3500, 3600), (-3900, 4600), (-3900, 5800), (-3500, 7000),
             (-2700, 7900), (-1800, 8500), (-900, 8750)]
# side pockets (dead ends with an honest endpoint)
SPUR_INLET = [(2100, 6950), (2650, 7300), (3150, 7650), (3550, 7900)]          # SE inlet gully -> pool under a rock step
SPUR_BAY = [(2850, -1000), (3350, -1050), (3850, -1050)]                       # east bay pocket between the spurs (R1)
SPUR_WEST = [(-200, 300), (-800, 450), (-1300, 250), (-1750, 0)]               # house west side -> old felling clearing (bench)

HUBS = {'veranda': (950, 1700), 'J2': (1950, 2110), 'landing': (620, 2620), 'eastbank': (2680, 5000), 'SE': (2100, 6950),
        'glade': (-900, 8750), 'gate': (2700, -100), 'narrows': (2920, -1750), 'hollow': (2250, -3150), 'climb': (1750, -4500),
        'saddle': (1380, -6250), 'backyard': (600, -800), 'west': (-700, 800)}


def poly_len(p):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))


def tangent_at(p, xy):
    best = None
    for a, b in zip(p, p[1:]):
        vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy
        t = max(0, min(1, ((xy[0] - a[0]) * vx + (xy[1] - a[1]) * vy) / L2)); d = math.hypot(a[0] + t * vx - xy[0], a[1] + t * vy - xy[1])
        if best is None or d < best[0]:
            best = (d, math.degrees(math.atan2(vy, vx)))
    return best[1]


def heading(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def probes():
    H = HUBS; P = []
    for hub, yaws in (('backyard', (-120, -90, -60)), ('west', (180, -150, 150, -120)), ('glade', (60, 90, 120, 150, 180)), ('SE', (-30, 0, 30, 60)),
                      ('eastbank', (-30, 0, 30)), ('narrows', (0, -30)), ('gate', (0, 30)), ('saddle', (-150, -90, -45, -20, 180)), ('climb', (180, 0))):
        for y in yaws:
            P.append({'name': 'bnd_%s_%d' % (hub, y), 'set': 'boundary', 'start': list(H[hub]), 'yaw': y, 'dist': 60})
    for rn, route, pts in (('A', ROUTE_A, [(1400, 2980), (2200, 3700), (2680, 5000), (2420, 6350), (1000, 8050), (-500, 8600)]),
                           ('B', ROUTE_B, [(2600, 700), (2850, -1000), (2700, -2450), (1850, -3800), (1700, -5200)])):
        for k, xy in enumerate(pts):
            th = tangent_at(route, xy)
            for side, off in (('L', -90), ('R', 90)):
                P.append({'name': 'lat_%s%d_%s' % (rn, k, side), 'set': 'lateral', 'start': list(xy), 'yaw': round(th + off, 1), 'dist': 25})
    for nm, a, b in (('eastbank_to_narrows', 'eastbank', 'narrows'), ('backyard_to_climb', 'backyard', 'climb'), ('west_to_saddle', 'west', 'saddle'),
                     ('SE_to_gate', 'SE', 'gate'), ('saddle_to_backyard', 'saddle', 'backyard'), ('J2_to_saddle', 'J2', 'saddle'),
                     ('glade_to_westshore', 'glade', None), ('landing_to_westhill', 'landing', None)):
        A_ = H[a]; B_ = H[b] if b else {'glade_to_westshore': (-3500, 5000), 'landing_to_westhill': (-5000, -500)}[nm]
        P.append({'name': 'sc_' + nm, 'set': 'shortcut', 'start': list(A_), 'yaw': round(heading(A_, B_), 1),
                  'dist': round(math.hypot(B_[0] - A_[0], B_[1] - A_[1]) / 100 + 5, 1)})
    return P


if __name__ == '__main__':
    P = probes(); json.dump(P, open(sys.argv[1], 'w'), indent=0)
    print('PROBES', len(P), 'total m', round(sum(p['dist'] for p in P)), {s: sum(1 for p in P if p['set'] == s) for s in ('boundary', 'lateral', 'shortcut')})


# decision points: name -> (pawn position, the point the 'forward' view looks at = where the designed route continues)
DECISIONS = {'D01_veranda': ((950, 1800), (620, 2620)), 'D02_houseSE': ((1950, 2110), (2380, 1520)), 'D03_landing': ((620, 2620), (1400, 2980)),
             'D04_eastbank': ((2680, 5000), (2620, 5700)), 'D05_inlet': ((2100, 6950), (1650, 7550)), 'D06_glade': ((-700, 8650), (760, 600)),
             'D07_gate': ((2700, -100), (2850, -1000)), 'D08_narrows': ((2920, -1750), (2700, -2450)), 'D09_hollow': ((2250, -3150), (1850, -3800)),
             'D10_climb': ((1750, -4500), (1700, -5200)), 'D11_saddle': ((1450, -6200), (760, 600)), 'D12_west': ((-700, 800), (-1750, 0)),
             'D13_backyard': ((600, -800), (2700, -100))}


def views():
    V = []
    for nm, (p, f) in DECISIONS.items():
        fy = heading(p, f)
        for tag, off in (('fwd', 0), ('L90', -90), ('R90', 90), ('back', 180)):
            V.append({'name': '%s_%s' % (nm, tag), 'pawn': list(p), 'yaw': round(fy + off, 1), 'pitch': -6.0})
    return V
