"""timing230.py <version dir> <log prefix>: development-time accounting from the chain / ab / build logs and the editor logs.
editor launch = first line of Saved/Logs/<prefix>*.log -> SPH_V2_RUNNER_READY; PIE runs = consecutive '== <label> HH:MM:SS' lines in ab_*.log
(duration to the next line; warm-ups and memory samples included in the run cost); MEM_RESTART / RELAUNCH / crash (Fatal error) counts.
Prints TIMING {...}."""
import sys, re, pathlib, json, datetime, collections
root = pathlib.Path(__file__).resolve().parents[2]; D = root / sys.argv[1]; pref = sys.argv[2]
def ts(s):
    m = re.search(r'\[(\d{4})\.(\d\d)\.(\d\d)-(\d\d)\.(\d\d)\.(\d\d):(\d{3})\]', s)
    return datetime.datetime(*map(int, m.groups()[:6])) if m else None
launch = []
for f in sorted((root / 'Saved/Logs').glob(pref + '*.log')):
    t0 = t1 = None; crash = False
    with open(f, 'rb') as fh:
        for raw in fh:
            l = raw.decode('utf8', 'replace')
            if t0 is None: t0 = ts(l)
            if t1 is None and 'SPH_V2_RUNNER_READY' in l: t1 = ts(l)
            if 'Fatal error' in l: crash = True
    if t0 and t1: launch.append({'log': f.name, 'ready_s': (t1 - t0).total_seconds(), 'crash': crash})
runs = []
for f in sorted(D.glob('ab_*.log')):
    prev = None
    for l in open(f, encoding='utf8', errors='replace'):
        m = re.match(r'== (\S+) (\d\d):(\d\d):(\d\d)', l)
        if m:
            t = int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
            if prev: runs.append((prev[0], (t - prev[1]) % 86400))
            prev = (m.group(1), t)
chain = (D / 'chain.out').read_text(encoding='utf8', errors='replace') if (D / 'chain.out').exists() else ''
res = {'editor_launches': len(launch), 'launch_ready_s_total': round(sum(x['ready_s'] for x in launch)), 'launch_ready_s_median': sorted(x['ready_s'] for x in launch)[len(launch) // 2] if launch else None,
       'crashed_sessions': sum(1 for x in launch if x['crash']), 'mem_restarts': chain.count('MEM_RESTART'), 'relaunch_lines': len(re.findall(r'^RELAUNCH ', chain, re.M)),
       'runner_not_ready': chain.count('RUNNER_NOT_READY'), 'pie_runs': len(runs), 'pie_run_s_total': sum(d for _, d in runs if d < 900), 'pie_run_s_median': sorted(d for _, d in runs)[len(runs) // 2] if runs else None}
print('TIMING ' + json.dumps(res))
