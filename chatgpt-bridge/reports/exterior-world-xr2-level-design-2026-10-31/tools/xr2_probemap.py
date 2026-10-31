"""xr2_probemap.py <probe_log.json> <height.u16> <foliage_full.json> <out.png> [ring overlay json]: probe paths on a clay plan.
red = REACHED (the player walked out / across freely), green = BLOCKED (stopped by a natural barrier), orange = TIMEOUT; white dot = start."""
import json, sys, os, subprocess
log, hf, ff, out = sys.argv[1:5]; extra = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {'polys': []}
C = {'REACHED': [0.95, 0.1, 0.1], 'BLOCKED': [0.1, 0.75, 0.2], 'TIMEOUT': [1.0, 0.6, 0.0], 'FELL': [0.5, 0, 0.5]}
ov = {'polys': [p for p in extra.get('polys', []) if p.get('w', 1) >= 2][:12], 'discs': []}
for p in json.load(open(log))['probes']:
    pts = [[q[0], q[1]] for q in p['path']] + [p['end'][:2]]
    ov['polys'].append({'pts': pts, 'rgb': C[p['result']], 'w': 2})
    ov['discs'].append({'xy': p['start'][:2], 'r': 60, 'rgb': [1, 1, 1], 'a': 1.0})
    if p['result'] != 'REACHED':
        ov['discs'].append({'xy': p['end'][:2], 'r': 90, 'rgb': C[p['result']], 'a': 1.0})
oj = out.replace('.png', '_ov.json'); json.dump(ov, open(oj, 'w'))
PY = sys.executable; R = 'Saved/Codex/ExteriorRedesign_20261031/recon'
subprocess.run([PY, 'Tools/ExteriorRedesign_20261031/xr_maps.py', R, hf, ff, out, '-9000', '8500', '-12500', '13000', '4', 'clay', oj], check=True)
