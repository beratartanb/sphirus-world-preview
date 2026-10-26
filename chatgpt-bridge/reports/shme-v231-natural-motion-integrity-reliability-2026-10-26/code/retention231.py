"""retention231.py [--apply] [--no-delete] [--current v231] [--cap-gb 10] : V2.31 telemetry / evidence retention (no editor; engine python).

Classes (by file label = first token before '_' of the run label, e.g. 'v230fin3', 'v229t4', 'v231a1'):
  FINAL     labels that back a published report: fin*, cap*, h20/h60/h120 (FPS), rt* (real time), and every label named in a
            published tables*.txt under Saved/Codex/SHME_V2xx_*/ -> never deleted; older versions gzip-compressed (lossless)
  CURRENT   the current and the previous version (v231*, v230*) -> kept raw (the A/B tools read them directly)
  TEMP      everything else (older-version candidate / diagnosis runs)
Rules:
  1. Older-version LTP (.ltp) and Evidence (.json): gzip -> .gz (lossless; ltp231.load reads .gz; gunzip on demand for old tools).
  2. Editor logs Saved/Logs/shmv2*.log older than LOG_DAYS (3) except the newest 10: gzip.
  3. TEMP .gz older than TEMP_DAYS (30): delete (FINAL never).
  4. Size cap: if raw LTP + Evidence of the CURRENT class exceeds --cap-gb, compress the oldest CURRENT TEMP files first.
Default is a dry run (prints the plan and the byte totals). Prints RETENTION231 {...}."""
import gzip, json, os, re, shutil, sys, time, glob
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
LTP = os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V1_20260925', 'LTP'); EVD = os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V1_20260925', 'Evidence')
LOGS = os.path.join(ROOT, 'Saved', 'Logs')
APPLY = '--apply' in sys.argv
def arg(n, d):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
CUR = arg('--current', 'v231'); CAP = float(arg('--cap-gb', '10')) * 1e9; LOG_DAYS = 3; TEMP_DAYS = 30
curn = int(CUR[1:]); KEEP_RAW = ('v%d' % curn, 'v%d' % (curn - 1))
FINAL_RE = re.compile(r'^v\d+(fin|cap|h20|h60|h120|rt|real)')
# labels quoted in published tables (any version)
tabled = set()
for f in glob.glob(os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V2*', 'tables*.txt')) + glob.glob(os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V2*', 'pub', '*.md')):
    try: tabled.update(re.findall(r'\bv2\d\d[a-z0-9]*_[A-Za-z0-9_]+_r\d+', open(f, encoding='utf8', errors='replace').read()))
    except Exception: pass
def label(fn):
    b = os.path.basename(fn)
    for ext in ('.ltp.gz', '.json.gz', '.ltp', '.json'):
        if b.endswith(ext): return b[:-len(ext)]
    return b
def klass(fn):
    lb = label(fn); tag = lb.split('_', 1)[0]
    if FINAL_RE.match(tag) or lb in tabled: return 'FINAL'
    if tag.startswith(KEEP_RAW): return 'CURRENT'
    return 'TEMP'
def ver(fn):
    m = re.match(r'^v(\d+)', label(fn)); return int(m.group(1)) if m else 0
now = time.time(); plan = {'gzip': [], 'delete': []}; tot = {}
def size(p):
    try: return os.path.getsize(p)
    except OSError: return 0
files = [os.path.join(LTP, f) for f in os.listdir(LTP)] + [os.path.join(EVD, f) for f in os.listdir(EVD)]
for p in files:
    k = klass(p); raw = not p.endswith('.gz'); tot.setdefault(k + ('_raw' if raw else '_gz'), 0); tot[k + ('_raw' if raw else '_gz')] += size(p)
    if raw and (p.endswith('.ltp') or p.endswith('.json')) and k != 'CURRENT' and not label(p).startswith(KEEP_RAW): plan['gzip'].append(p)
    if not raw and k == 'TEMP' and now - os.path.getmtime(p) > TEMP_DAYS * 86400: plan['delete'].append(p)
cur_raw = sorted([p for p in files if klass(p) == 'CURRENT' and not p.endswith('.gz')], key=os.path.getmtime)
s = sum(size(p) for p in cur_raw)
for p in cur_raw:
    if s <= CAP: break
    if klass(p) == 'CURRENT' and not FINAL_RE.match(label(p).split('_', 1)[0]): plan['gzip'].append(p); s -= size(p)
logs = sorted(glob.glob(os.path.join(LOGS, 'shmv2*.log')), key=os.path.getmtime)
for p in logs[:-10]:
    if now - os.path.getmtime(p) > LOG_DAYS * 86400: plan['gzip'].append(p)
res = {'apply': APPLY, 'current': CUR, 'tabled_labels': len(tabled), 'bytes_by_class': {k: round(v / 1e9, 3) for k, v in tot.items()},
       'gzip_n': len(plan['gzip']), 'gzip_gb_in': round(sum(size(p) for p in plan['gzip']) / 1e9, 3), 'delete_n': len(plan['delete']),
       'delete_gb': round(sum(size(p) for p in plan['delete']) / 1e9, 3)}
if APPLY:
    out_b = 0
    for p in plan['gzip']:
        q = p + '.gz'
        with open(p, 'rb') as a, gzip.open(q, 'wb', compresslevel=6) as b: shutil.copyfileobj(a, b, 1 << 20)
        with gzip.open(q, 'rb') as b:   # verify the archive reads back to the same size before removing the raw file
            n = 0
            while True:
                ch = b.read(1 << 20)
                if not ch: break
                n += len(ch)
        if n == size(p): os.utime(q, (os.path.getatime(p), os.path.getmtime(p))); os.remove(p); out_b += size(q)
        else: os.remove(q); res.setdefault('verify_fail', []).append(p)
    if '--no-delete' not in sys.argv:
        for p in plan['delete']: os.remove(p)
    else: res['delete_skipped'] = len(plan['delete'])
    res['gzip_gb_out'] = round(out_b / 1e9, 3)
print('RETENTION231 ' + json.dumps(res))
