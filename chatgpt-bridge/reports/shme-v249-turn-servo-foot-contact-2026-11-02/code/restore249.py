"""restore249.py <manifest.json> [--apply] [--only sub1,sub2,...] (any Python 3, EDITOR CLOSED): restore every asset of a manifest233 write manifest from its
verified backup (backup -> file), then check sha1(file) == sha1_before. Dry by default. Prints RESTORE249 {...}."""
import sys, json, os, shutil, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(ROOT)
def lp(p): return '\\\\?\\' + os.path.abspath(p) if os.name == 'nt' and not p.startswith('\\\\?\\') else p
def sha1(p):
    h = hashlib.sha1()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
m = json.load(open(sys.argv[1], encoding='utf8')); APPLY = '--apply' in sys.argv; out = {'apply': APPLY, 'ok': 0, 'bad': []}
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
for a in m['assets']:
    if ONLY and not any(x in a['package'] for x in ONLY): continue
    f, b, s0 = a['file'], a['backup'], a['sha1_before']
    if not os.path.exists(lp(b)) or sha1(b) != s0: out['bad'].append([a['package'], 'backup missing or sha1 mismatch']); continue
    if APPLY: shutil.copy2(lp(b), lp(f))
    if not APPLY or sha1(f) == s0: out['ok'] += 1
    else: out['bad'].append([a['package'], 'restored file sha1 mismatch'])
print('RESTORE249 ' + json.dumps(out))
