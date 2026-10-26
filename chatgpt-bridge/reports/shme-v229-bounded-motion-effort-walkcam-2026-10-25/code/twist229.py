"""twist229.py label from to: per frame actor yaw, speed, velocity heading, pelvis / spine_03 / neck heading (MM mesh Z axes) and the
spine-minus-pelvis twist, selected clip / time / database, PBI and orientation-related ABP values when present."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
lab, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list)], key=lambda r: float(r['t']))
h = lambda v: math.degrees(math.atan2(v[1], v[0])); w = lambda x: (x + 180) % 360 - 180
seen = set()
for r in R:
    t = float(r['t'])
    if a <= t <= b and t not in seen:
        seen.add(t); vx, vy = float(r['avx']), float(r['avy'])
        pz, sz = h(r['maz_pelvis']), h(r['maz_spine_03'])
        print('%.2f ay %6.1f spd %4.0f vh %5.0f | pelv %5.0f sp03 %5.0f tw %5.0f | %-30s %4.2f %-28s | rootc %s mry %s' % (t, float(r['ay']), math.hypot(vx, vy), h((vx, vy)) if math.hypot(vx, vy) > 5 else 0, w(pz - float(r['ay'])), w(sz - float(r['ay'])), w(sz - pz), str(r.get('av_Phase27_SelectedObject'))[-30:], float(r.get('av_Phase27_SelectedTime') or 0), str(r.get('av_CurrentSelectedDatabase'))[-28:], r.get('av_DI_StartRootCompensation'), r.get('mry')))
