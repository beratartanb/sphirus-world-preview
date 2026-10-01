"""CORRECTIVE pass preservation check: recompute the per-file sha1 of every protected group recorded by cr_checkpoint.py and diff
(changed / added / removed). Read-only. Writes Saved/Codex/CharacterCorrective_20261001/preservation_check.json"""
import hashlib, pathlib, json, datetime
R = pathlib.Path('Content'); K = pathlib.Path('Saved/Codex/CharacterGuardian3_20261001'); C = json.loads((K/'checkpoint_hashes.json').read_text())
out = {'checked': datetime.datetime.now().isoformat(timespec='seconds'), 'checkpoint_taken': C['taken'], 'groups': {}}
for k, g in C['groups'].items():
    cur = {}
    for f in sorted((R/g['path']).rglob('*.u*')): cur[f.relative_to(R/g['path']).as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()[:16]
    old = g['per_file']; ch = [f for f in old if f in cur and cur[f] != old[f]]; add = [f for f in cur if f not in old]; rem = [f for f in old if f not in cur]
    out['groups'][k] = {'files': len(cur), 'identical': not (ch or add or rem), 'changed': ch, 'added': add, 'removed': rem}
(K/'preservation_check.json').write_text(json.dumps(out, indent=1))
for k, v in out['groups'].items(): print('PRES', k, v['files'], 'IDENTICAL' if v['identical'] else f"CHANGED {len(v['changed'])} ADDED {len(v['added'])} REMOVED {len(v['removed'])} {(v['changed']+v['added']+v['removed'])[:6]}")
