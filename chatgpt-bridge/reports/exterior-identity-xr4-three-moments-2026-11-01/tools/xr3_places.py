"""xr3_places.py <views.json> : the three key places of the identity slice (route A, house -> pond) and their player-camera stations.
Each place gets a composition card in the report: first read / second read / background, judged in clay and in the lit player camera."""
import json, sys, math, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ExteriorWorld_XR2_20261031'))
import xr2_layout as LY

PLACES = {
    'P0_refuge': ((700, 1250), (620, 2620), {'house_back': ((1050, 2350), (760, 600)), 'front_path': ((850, 1950), (620, 2620))}),
    # name: (pawn xy, look-at xy, extra stations)
    'P1_landing': ((620, 2620), (980, 2840), {'from_veranda': ((950, 1800), (620, 2620)), 'boat': ((500, 2750), (330, 2980))}),
    'P2_rockshelf': ((2520, 4300), (2680, 5000), {'entry': ((2200, 3700), (2520, 4300)), 'exit_back': ((2620, 5700), (2520, 4300))}),
    'P3_glade': ((-700, 8650), (760, 600), {'arrive': ((250, 8350), (-900, 8750)), 'seat': ((-1000, 8900), (-1250, 9050))}),
}
SLICE = [(-3200, 1200), (3400, 1200), (3700, 3400), (3500, 6500), (3400, 8200), (2200, 9400), (-500, 9700), (-2600, 9500), (-3700, 8300), (-3600, 5200), (-3300, 2800)]


def views():
    V = []
    for nm, (p, f, extra) in PLACES.items():
        fy = LY.heading(p, f)
        for tag, off in (('fwd', 0), ('L90', -90), ('R90', 90), ('back', 180)):
            V.append({'name': '%s_%s' % (nm, tag), 'pawn': list(p), 'yaw': round(fy + off, 1), 'pitch': -6.0})
        for tag, (pp, ff) in extra.items():
            V.append({'name': '%s_%s' % (nm, tag), 'pawn': list(pp), 'yaw': round(LY.heading(pp, ff), 1), 'pitch': -6.0})
    return V


if __name__ == '__main__':
    json.dump(views(), open(sys.argv[1], 'w')); print('VIEWS', len(views()))
