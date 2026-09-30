"""IDENTITY pass checkpoint (run from the project root, any Python 3): per-file sha1 of every protected group AND of the whole
889b1d9 lookdev candidate folder, before any mutation of this pass. Writes Saved/Codex/CharacterIdentity_20260930/checkpoint_hashes.json."""
import hashlib, pathlib, json, datetime
R = pathlib.Path('Content'); out = {'taken': datetime.datetime.now().isoformat(timespec='seconds'), 'groups': {}}
groups = {'production MH_MainCharacter': 'MetaHumans/MH_MainCharacter', 'accepted B2': 'Sphirus/CharacterLab/NativeBody_20260928',
          'accepted SHCB HelperFix': 'Sphirus/CharacterLab/ShoulderFix_20260928/HighElevCorrective/HelperFix', 'BR v5 candidate': 'Sphirus/CharacterLab/BodyRealism_20260929',
          'Outfit V1 candidate': 'Sphirus/CharacterLab/Outfit_Home_20260929', 'ShoulderFix skeleton copies': 'Sphirus/CharacterLab/ShoulderFix_20260928/Common',
          'CharacterFinal candidate': 'Sphirus/CharacterLab/CharacterFinal_20260929', 'CharacterRevision candidate': 'Sphirus/CharacterLab/CharacterRevision_20260930',
          'Lookdev candidate 889b1d9': 'Sphirus/CharacterLab/CharacterLookdev_20260930'}
for k, d in groups.items():
    files = {}; h = hashlib.sha1()
    for f in sorted((R/d).rglob('*.u*')):
        b = f.read_bytes(); files[f.relative_to(R/d).as_posix()] = hashlib.sha1(b).hexdigest()[:16]; h.update(f.name.encode()); h.update(b)
    out['groups'][k] = {'path': d, 'files': len(files), 'sha1_12': h.hexdigest()[:12], 'per_file': files}
pathlib.Path('Saved/Codex/CharacterIdentity_20260930/checkpoint_hashes.json').write_text(json.dumps(out, indent=1))
print({k: (v['files'], v['sha1_12']) for k, v in out['groups'].items()})
