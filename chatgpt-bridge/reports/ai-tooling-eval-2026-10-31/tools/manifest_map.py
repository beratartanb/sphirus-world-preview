"""manifest_map.py <name> <game path> [...] : manifest233-compatible write manifest + verified backup that also accepts MAP packages.
Identical schema and backup folder to Tools/SHME_V233_20261027/manifest233.py (which resolves every package to a .uasset file and so
refuses a .umap); here a package resolves to .umap when that file exists, else .uasset. The gated runner checks entries by 'file'.
Backup: Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<name>/<relative path>; copy read back, sha1 must match."""
import sys, os, json, hashlib, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
MD = os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V233_20261027', 'checkpoint', 'manifests')


def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


name, pkgs = sys.argv[1], sys.argv[2:]
out = {'name': name, 'assets': [], 'missing': [], 'tool': 'Tools/AIToolingEval_20261031/manifest_map.py'}
for p in pkgs:
    p = ('/Game/' + p.replace('\\', '/').split('/Game/', 1)[1]) if '/Game/' in p.replace('\\', '/') else p
    p = p.split('.')[0]
    base = os.path.join('Content', *p[len('/Game/'):].split('/'))
    f = base + '.umap' if os.path.exists(os.path.join(ROOT, base + '.umap')) else base + '.uasset'
    fa = os.path.join(ROOT, f)
    if not os.path.exists(fa):
        out['missing'].append(p); continue
    s0 = sha1(fa); bk = os.path.join('Saved', 'Codex', 'SHME_V233_20261027', 'checkpoint', 'manifests', name, f)
    os.makedirs(os.path.dirname(os.path.join(ROOT, bk)), exist_ok=True)
    shutil.copy2(fa, os.path.join(ROOT, bk))
    for ext in ('.uexp', '.ubulk'):
        if os.path.exists(fa[:fa.rfind('.')] + ext):
            shutil.copy2(fa[:fa.rfind('.')] + ext, os.path.join(ROOT, bk)[:os.path.join(ROOT, bk).rfind('.')] + ext)
    s1 = sha1(os.path.join(ROOT, bk))
    if s1 != s0:
        raise SystemExit('BACKUP VERIFY FAILED %s' % p)
    out['assets'].append({'package': p, 'file': f.replace(os.sep, '/'), 'sha1_before': s0, 'backup': bk.replace(os.sep, '/'), 'backup_sha1': s1})
if out['missing']:
    raise SystemExit('MANIFEST_MAP REFUSED missing: %s' % out['missing'])
os.makedirs(MD, exist_ok=True); mp = os.path.join(MD, name + '.json'); json.dump(out, open(mp, 'w', encoding='utf-8'), indent=1)
print('MANIFEST_MAP ' + json.dumps({'manifest': os.path.relpath(mp, ROOT).replace(os.sep, '/'), 'assets': [(a['file'], a['sha1_before'][:12]) for a in out['assets']]}))
