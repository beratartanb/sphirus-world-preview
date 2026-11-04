"""retention.py [--apply] [--keep-rounds 3] [--min-age-days 2]  (engine or any Python 3; run with the editor CLOSED)
SPHIRUS test-output retention (V2.49). DRY RUN by default: lists what it would delete and the sizes; --apply deletes and logs.
Only regenerable test outputs are candidates; everything else is never touched:
  1. Telemetry  Saved/Codex/SHME_V1_20260925/{LTP,Evidence}/<label>*  : label round = leading 'v<NNN>' (v212_warm_* = warm-up, any round)
     deleted when the round is older than the newest --keep-rounds rounds AND the file is older than --min-age-days,
     unless the label is listed in Tools/Retention/protect.txt or named in a REPORT/TABLES/CHANGES *.md of the kept rounds.
  2. Capture frames Saved/Codex/SHME_V138_20260927/Video/<label>/  : same round rule (frames are the raw source of published AVIs/strips).
  3. Bundles  Saved/Codex/*/pub/  : the GitHub-published copy of a round's report; deleted when older than --min-age-days and not the newest round.
  4. Media working copies  Saved/Codex/*/vid/tri_*  (triptych temp dirs older than 6 h - a running build keeps its own).
  5. Logs  Saved/Logs/*.log older than 7 days; Saved/Crashes/* older than 7 days; __pycache__ under Tools and Saved/Codex.
NEVER: Content/, Config/, Plugins/, Source/, *.uasset / *.umap anywhere, any 'checkpoint' directory, Saved/Codex/*/data, report .md files,
Tools/ scripts, DerivedDataCache, Intermediate. Log: Saved/Codex/Retention/retention_<stamp>.txt."""
import os, re, sys, time, shutil, glob
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
APPLY = '--apply' in sys.argv
def opt(name, d):
    return type(d)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else d
KEEP = opt('--keep-rounds', 3); AGE = opt('--min-age-days', 2.0) * 86400; NOW = time.time()
RX = re.compile(r'^v(\d{3})')
def rnd(label):
    if label.startswith('v212_warm'): return None
    m = RX.match(label); return int(m.group(1)) if m else None
def size(p):
    if os.path.isfile(p): return os.path.getsize(p)
    t = 0
    for a, _, fs in os.walk(p):
        for f in fs:
            try: t += os.path.getsize(os.path.join(a, f))
            except OSError: pass
    return t
def never(p):
    q = p.replace('\\', '/')
    return any(s in q for s in ('/Content/', '/Config/', '/Plugins/', '/Source/', 'checkpoint', '/data/', 'DerivedDataCache', 'Intermediate')) or q.endswith(('.uasset', '.umap', '.md'))
rounds = sorted({int(m.group(1)) for d in glob.glob('Saved/Codex/SHME_V2*') for m in [re.search(r'SHME_V(\d{3})_', d)] if m})
kept = set(rounds[-KEEP:]); out = ['retention %s apply=%s keep_rounds=%s (%s) min_age_days=%.1f' % (time.strftime('%Y-%m-%d %H:%M'), APPLY, KEEP, sorted(kept), AGE / 86400)]
protect = set()
if os.path.exists('Tools/Retention/protect.txt'): protect |= {l.strip() for l in open('Tools/Retention/protect.txt', encoding='utf8') if l.strip() and not l.startswith('#')}
for r in kept:
    for md in glob.glob('Saved/Codex/SHME_V%d_*/*.md' % r): protect |= set(re.findall(r'\b(v\d{3}[a-z0-9]*_[A-Za-z0-9_]+?)(?:_r\d+)?\b', open(md, encoding='utf8', errors='ignore').read()))
cands = []
def consider(path, label, grp, age_ok=True):
    if never(path) or not age_ok: return
    if any(label.startswith(p) for p in protect if len(p) > 8): return
    cands.append((grp, path))
for d in ('Saved/Codex/SHME_V1_20260925/LTP', 'Saved/Codex/SHME_V1_20260925/Evidence'):
    for f in os.listdir(d) if os.path.isdir(d) else []:
        p = os.path.join(d, f); r = rnd(f); old = NOW - os.path.getmtime(p) > AGE
        if f.startswith('v212_warm') and old: consider(p, f, 'telemetry_warm')
        elif r is not None and r not in kept and r < max(kept) and old: consider(p, f, 'telemetry_round_%d' % r)
V = 'Saved/Codex/SHME_V138_20260927/Video'
for f in os.listdir(V) if os.path.isdir(V) else []:
    p = os.path.join(V, f); r = rnd(f)
    if r is not None and r not in kept and NOW - os.path.getmtime(p) > AGE: consider(p, f, 'capture_frames')
newest = max(rounds) if rounds else 0
for p in glob.glob('Saved/Codex/*/pub'):
    m = re.search(r'SHME_V(\d{3})_', p)
    if (not m or int(m.group(1)) != newest) and NOW - os.path.getmtime(p) > AGE: consider(p, p, 'published_bundle')
for p in glob.glob('Saved/Codex/*/vid/tri_*'):
    if NOW - os.path.getmtime(p) > 6 * 3600: consider(p, p, 'media_temp')   # never the working dir of a media build that may still run
for p in glob.glob('Saved/Logs/*.log'):
    if NOW - os.path.getmtime(p) > 7 * 86400: consider(p, p, 'logs')
for p in glob.glob('Saved/Crashes/*'):
    if NOW - os.path.getmtime(p) > 7 * 86400: consider(p, p, 'crashes')
for base in ('Tools', 'Saved/Codex'):
    for a, ds, _ in os.walk(base):
        if '__pycache__' in ds: consider(os.path.join(a, '__pycache__'), '__pycache__', 'pycache')
tot = {}
for grp, p in cands:
    s = size(p); tot[grp] = tot.get(grp, [0, 0]); tot[grp][0] += 1; tot[grp][1] += s
    out.append('%s\t%s\t%.1f MB' % (grp, p, s / 1048576.0))
    if APPLY:
        try: shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        except OSError as e: out.append('FAIL %s %s' % (p, e))
summary = ['%-22s %6d items %9.1f MB' % (g, v[0], v[1] / 1048576.0) for g, v in sorted(tot.items())]
free = shutil.disk_usage(ROOT).free / 1e9
summary.append('free space %.1f GB%s' % (free, '  WARNING: below 40 GB' if free < 40 else ''))
os.makedirs('Saved/Codex/Retention', exist_ok=True)
log = 'Saved/Codex/Retention/retention_%s%s.txt' % (time.strftime('%Y%m%d_%H%M'), '' if APPLY else '_dry')
open(log, 'w', encoding='utf8').write('\n'.join(out[:1] + summary + out[1:]) + '\n')
print('\n'.join(out[:1] + summary)); print('log', log)
