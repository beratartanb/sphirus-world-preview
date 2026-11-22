"""publish_report6.py (round 6: also removes repository files of this report that are gone locally) / publish_report.py <report name> <commit message>: publish one report folder to chatgpt-bridge/reports/<name>/ in one non-force commit through the GitHub Git Data API (no clone, no fetch)."""
import base64, json, os, subprocess, sys, tempfile
REPO = 'repos/beratartanb/sphirus-world-preview'
NAME = sys.argv[1]
SRC = 'chatgpt-bridge/reports/' + NAME
MSG = sys.argv[2] + """

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
"""


def gh(path, body=None, method=None):
    cmd = ['gh', 'api', path]
    f = None
    if body is not None:
        f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf8')
        json.dump(body, f)
        f.close()
        cmd += ['--method', method or 'POST', '--input', f.name]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf8')
    if f:
        os.unlink(f.name)
    if r.returncode:
        raise SystemExit('GH_FAIL %s %s' % (path, (r.stdout + r.stderr)[:400]))
    return json.loads(r.stdout)


head = gh(REPO + '/git/ref/heads/main')['object']['sha']
base = gh(REPO + '/git/commits/' + head)['tree']['sha']
tree = []
for r, _, fs in os.walk(SRC):
    for n in sorted(fs):
        p = os.path.join(r, n)
        b = gh(REPO + '/git/blobs', {'content': base64.b64encode(open(p, 'rb').read()).decode(), 'encoding': 'base64'})
        rel = os.path.relpath(p, SRC).replace(os.sep, '/')
        tree.append({'path': 'chatgpt-bridge/reports/%s/%s' % (NAME, rel), 'mode': '100644', 'type': 'blob', 'sha': b['sha']})
        print('blob', rel, b['sha'][:8])
# round 6: files that exist in the repository folder but no longer locally are removed in the same commit (sha None)
have = {e['path'] for e in tree}; pre = 'chatgpt-bridge/reports/%s/' % NAME
old = gh(REPO + '/git/trees/' + base + '?recursive=1').get('tree', [])
gone = [e['path'] for e in old if e['type'] == 'blob' and e['path'].startswith(pre) and e['path'] not in have]
for p in gone: tree.append({'path': p, 'mode': '100644', 'type': 'blob', 'sha': None}); print('remove', p[len(pre):])
t = gh(REPO + '/git/trees', {'base_tree': base, 'tree': tree})
c = gh(REPO + '/git/commits', {'message': MSG, 'tree': t['sha'], 'parents': [head]})
gh(REPO + '/git/refs/heads/main', {'sha': c['sha'], 'force': False}, 'PATCH')
print('COMMIT', c['sha'], 'FILES', len(tree))
