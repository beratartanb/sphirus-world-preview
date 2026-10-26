"""rate230.py label [label ...]: per selected clip, the animation play rate (d clip time / d game time over continuous runs of the same
clip, MM jumps excluded) and the capsule speed while it plays. Rate << 1 on a locomotion loop = a large vendor stride played slowly to
match a small speed (the 'slow-motion' family read). Prints RATE230 rows aggregated over all labels (clip, frames, rate median, speed)."""
import json, sys, pathlib, collections, statistics, math
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
agg = collections.defaultdict(lambda: {'r': [], 'v': []})
for lab in sys.argv[1:]:
    p = E / (lab + '.json')
    if not p.exists(): continue
    R = [r for r in json.load(open(p)) if isinstance(r, dict) and isinstance(r.get('ax'), list)]; R.sort(key=lambda r: float(r['t']))
    for a, b in zip(R, R[1:]):
        oa, ob = str(a.get('av_Phase27_SelectedObject')), str(b.get('av_Phase27_SelectedObject'))
        if oa != ob: continue
        dt = float(b['t']) - float(a['t']); dc = float(b.get('av_Phase27_SelectedTime') or 0) - float(a.get('av_Phase27_SelectedTime') or 0)
        if dt <= 0 or dc < 0 or dc > 3 * dt: continue
        agg[ob]['r'].append(dc / dt); agg[ob]['v'].append(math.hypot(float(b['avx']), float(b['avy'])))
rows = [(k, len(v['r']), statistics.median(v['r']), statistics.median(v['v'])) for k, v in agg.items() if len(v['r']) >= 15]
for k, n, r, s in sorted(rows, key=lambda x: x[2]): print('RATE230 %-44s n%4d rate %.2f speed %4.0f' % (k[-44:], n, r, s))
