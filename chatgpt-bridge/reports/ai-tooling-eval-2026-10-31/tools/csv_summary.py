"""csv_summary.py <Profile.csv> [out.json] : frame-time summary of a stock 'csvprofile' capture (header row may be repeated at the end)."""
import csv, sys, json, statistics as st
rows = list(csv.reader(open(sys.argv[1], encoding='utf-8', errors='ignore')))
hdrs = [r for r in rows if 'FrameTime' in r]
h = hdrs[-1]
data = [r for r in rows if r and 'FrameTime' not in r and not r[0].startswith('[')]
out = {'file': sys.argv[1], 'frames': len(data), 'stats': {}}
for c in ('FrameTime', 'GameThreadTime', 'RenderThreadTime', 'RHIThreadTime', 'GPUTime', 'GPUMem/LocalUsedMB', 'GPUMem/LocalBudgetMB', 'PhysicalUsedMB', 'GPUSceneInstanceCount'):
    if c not in h:
        continue
    i = h.index(c)
    v = []
    for r in data:
        try:
            v.append(float(r[i]))
        except (IndexError, ValueError):
            pass
    if v:
        v.sort()
        out['stats'][c] = {'n': len(v), 'mean': round(st.mean(v), 2), 'p50': round(v[len(v) // 2], 2), 'p95': round(v[int(.95 * len(v))], 2), 'max': round(v[-1], 2)}
meta = [r for r in rows if r and r[0].startswith('[')]
out['metadata'] = {meta[-1][k]: meta[-1][k + 1] for k in range(0, len(meta[-1]) - 1, 2)} if meta else {}
if len(sys.argv) > 2:
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
for c, s in out['stats'].items():
    print('%-22s n %3d mean %9.2f p50 %9.2f p95 %9.2f max %9.2f' % (c, s['n'], s['mean'], s['p50'], s['p95'], s['max']))
print({k: v for k, v in out['metadata'].items() if k.lower() in ('[platform]', '[config]', '[buildversion]', '[commandline]', '[targetframerate]', '[rhi]', '[deviceprofile]', '[cpu]', '[gpu]')})
