"""Publish the user-requested equivalence/corrective report package (report, boards, small JSON). Non-force, new folder
only, blob-hash verified, world LATEST untouched. Pattern from publish_rbf_ui_retry.py."""
from pathlib import Path
import base64, hashlib, json, subprocess, datetime
R = Path(__file__).resolve().parents[2]; E = R/'Saved/Codex/CharacterGuardian_20261001'; P = E/'public_report'
REPO = 'beratartanb/sphirus-world-preview'; DEST = 'chatgpt-bridge/reports/character-guardian-face-pass-2026-10-01'
GH = r'C:\Program Files\GitHub CLI\gh.exe'
def api(endpoint, method='GET', payload=None, allow_missing=False):
    cmd = [GH, 'api', '--method', method, endpoint]
    if payload is not None: cmd += ['--input', '-']
    p = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None, encoding='utf-8', capture_output=True)
    if p.returncode:
        if allow_missing and '(HTTP 404)' in p.stderr: return None
        raise RuntimeError(f'{method} {endpoint}: {p.stderr.strip()}')
    return json.loads(p.stdout) if p.stdout.strip() else None
files = {}
for p in sorted(P.rglob('*')):
    if p.is_file():
        assert p.suffix in {'.md', '.json', '.jpg', '.png', '.py', '.txt', '.ps1', '.sh'} and p.stat().st_size < 6_000_000
        data = p.read_bytes(); files[p.relative_to(P).as_posix()] = {'data': data, 'sha': hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
repo = api(f'repos/{REPO}'); user = api('user')
assert repo['full_name'] == REPO and repo['permissions']['push'] and repo['owner']['login'] == user['login'] == 'beratartanb'
branch = repo['default_branch']
latest_before = api(f'repos/{REPO}/contents/chatgpt-bridge/latest/LATEST.json?ref={branch}')['sha']
assert api(f'repos/{REPO}/contents/{DEST}?ref={branch}', allow_missing=True) is None, 'Destination exists; no overwrite.'
entries = []
for n, v in files.items():
    blob = api(f'repos/{REPO}/git/blobs', 'POST', {'content': base64.b64encode(v['data']).decode('ascii'), 'encoding': 'base64'}); assert blob['sha'] == v['sha']
    entries.append({'path': DEST+'/'+n, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
parent = api(f'repos/{REPO}/git/ref/heads/{branch}')['object']['sha']; base = api(f'repos/{REPO}/git/commits/{parent}')['tree']['sha']
tree = api(f'repos/{REPO}/git/trees', 'POST', {'base_tree': base, 'tree': entries})
msg = 'SPHIRUS protagonist GUARDIAN face identity pass candidate (NOT promoted): tracker-measured likeness, re-solved 3/4 reference camera, face H (mouth/eyes/brow-ridge/lower-face restructure), skin c14s, SlightArch brows + short lashes, hair id18, Henley g17e pattern reserve; face gate PARTIAL; production unchanged'
commit = api(f'repos/{REPO}/git/commits', 'POST', {'message': msg, 'tree': tree['sha'], 'parents': [parent]})['sha']
api(f'repos/{REPO}/git/refs/heads/{branch}', 'PATCH', {'sha': commit, 'force': False})
remote = {}
for item in api(f'repos/{REPO}/contents/{DEST}?ref={branch}'):
    if item['type'] == 'file': remote[item['name']] = item
    else:
        for sub in api(f'repos/{REPO}/contents/{DEST}/{item["name"]}?ref={branch}'): remote[item['name']+'/'+sub['name']] = sub
assert set(remote) == set(files) and all(remote[n]['sha'] == v['sha'] for n, v in files.items())
assert api(f'repos/{REPO}/contents/chatgpt-bridge/latest/LATEST.json?ref={branch}')['sha'] == latest_before
out = {'status': 'PUBLISHED_AND_VERIFIED', 'repository': REPO, 'path': DEST, 'commit': commit, 'report_url': remote['README.md']['html_url'],
       'files_verified': len(files), 'world_latest_unchanged': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(E/'github_publish_status.json').write_text(json.dumps(out, indent=2)); print(json.dumps(out))
