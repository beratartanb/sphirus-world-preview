"""manifest234.py <name> [--assets a1 a2 ...] [--new n1 ...] [--from list.json] : V2.33 write manifest + verified backup (engine python,
editor may be open; the runner re-verifies at job start). For every existing asset (game path /Game/... -> Content/... .uasset plus
.uexp / .ubulk siblings) a copy goes to Saved/Codex/SHME_V239_20261030/checkpoint/manifests/<name>/<same relative path>, the copy is read
back and its sha1 must equal the original's. '--new' lists packages the job may CREATE (no backup). '--from' takes a JSON list of game
paths (a generator's dry-run list). Writes .../manifests/<name>.json; prints MANIFEST233 {...}. Refuses when a listed existing asset is missing."""
import sys, os, json, hashlib, shutil
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
MD = os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V239_20261030', 'checkpoint', 'manifests')
def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def rel_file(pkg):
    assert pkg.startswith('/Game/'), pkg
    return os.path.join('Content', *pkg[len('/Game/'):].split('/')) + '.uasset'
a = sys.argv[1:]; name = a[0]; mode = None; assets = []; new = []
for x in a[1:]:
    if x in ('--assets', '--new', '--from'): mode = x; continue
    if mode == '--new': new.append(x)
    elif mode == '--from': assets += json.load(open(x, encoding='utf-8'))
    else: assets.append(x)
fix = lambda p: ('/Game/' + p.replace(chr(92), '/').split('/Game/', 1)[1]) if '/Game/' in p.replace(chr(92), '/') else p   # Git Bash path conversion of /Game/...
assets = [fix(p).split('.')[0] for p in assets]; new = [fix(p).split('.')[0] for p in new]
out = {'name': name, 'assets': [], 'missing': []}
for p in sorted(set(assets)):
    f = rel_file(p); fa = os.path.join(ROOT, f)
    if not os.path.exists(fa): out['missing'].append(p); continue
    s0 = sha1(fa); bk = os.path.join('Saved', 'Codex', 'SHME_V239_20261030', 'checkpoint', 'manifests', name, f)
    os.makedirs(os.path.dirname(os.path.join(ROOT, bk)), exist_ok=True)
    for ext in ('.uasset', '.uexp', '.ubulk'):
        src = fa[:-len('.uasset')] + ext
        if os.path.exists(src): shutil.copy2(src, os.path.join(ROOT, bk)[:-len('.uasset')] + ext)
    s1 = sha1(os.path.join(ROOT, bk))
    if s1 != s0: raise SystemExit('BACKUP VERIFY FAILED %s' % p)
    out['assets'].append({'package': p, 'file': f.replace(os.sep, '/'), 'sha1_before': s0, 'backup': bk.replace(os.sep, '/'), 'backup_sha1': s1})
for p in sorted(set(new)): out['assets'].append({'package': p, 'new': True, 'file': rel_file(p).replace(os.sep, '/')})
if out['missing']: raise SystemExit('MANIFEST233 REFUSED missing assets (use --new for packages the job creates): %s' % out['missing'])
os.makedirs(MD, exist_ok=True); mp = os.path.join(MD, name + '.json'); json.dump(out, open(mp, 'w', encoding='utf-8'), indent=1)
print('MANIFEST233 ' + json.dumps({'manifest': os.path.relpath(mp, ROOT).replace(os.sep, '/'), 'existing': sum(1 for e in out['assets'] if not e.get('new')), 'new': len(new)}))
