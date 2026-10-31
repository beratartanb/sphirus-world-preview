"""probe_summary.py <probe_log.json> [more logs...]: one line per probe + per-set summary."""
import json, sys
for f in sys.argv[1:]:
    d = json.load(open(f)); print('==', f.split('/')[-2], 'capsule', d.get('capsule'), 'n', len(d['probes']), 'errors', d.get('errors'))
    for p in d['probes']:
        b = p.get('blocker') or {}
        k = b.get('knee') or b.get('chest') or {}
        print('%-28s %-8s prog %6.1f/%-5s m  path %6.1f  %5.1f s  v %5.0f av %2d  %s %s slope %s' % (p['name'], p['result'], p.get('progress_m', p['straight_m']), p['dist_target_m'], p['path_m'], p['game_s'],
              p['mean_speed'], p.get('avoids', 0), k.get('actor') or '', k.get('mesh') or '', b.get('slope_deg', '')))
    for s in ('boundary', 'lateral', 'shortcut'):
        P = [p for p in d['probes'] if p['set'] == s]
        if P:
            print('  %s: %d probes, reached %d, mean progress %.1f m' % (s, len(P), sum(p['result'] == 'REACHED' for p in P), sum(p.get('progress_m', p['straight_m']) for p in P) / len(P)))
