"""Protected-folder preservation check: sha1 over sorted .uasset names+bytes (same method as CharacterFinal) + files newer than the pass start."""
import hashlib, pathlib, json, datetime
R = pathlib.Path('Content'); CF = json.load(open('Saved/Codex/CharacterFinal_20260929/preservation_hashes.json'))
START = datetime.datetime(2026, 9, 30, 0, 12).timestamp()
groups = {'production MH_MainCharacter': R/'MetaHumans/MH_MainCharacter', 'accepted B2': R/'Sphirus/CharacterLab/NativeBody_20260928', 'accepted SHCB HelperFix': R/'Sphirus/CharacterLab/ShoulderFix_20260928/HighElevCorrective/HelperFix', 'BR v5 candidate': R/'Sphirus/CharacterLab/BodyRealism_20260929', 'Outfit V1 candidate': R/'Sphirus/CharacterLab/Outfit_Home_20260929', 'ShoulderFix skeleton copies': R/'Sphirus/CharacterLab/ShoulderFix_20260928/Common', 'CharacterFinal candidate (previous)': R/'Sphirus/CharacterLab/CharacterFinal_20260929'}
out = {}
for k, d in groups.items():
    h = hashlib.sha1(); n = 0; newer = []
    for f in sorted(d.rglob('*.uasset')):
        h.update(f.name.encode()); h.update(f.read_bytes()); n += 1
        if f.stat().st_mtime > START: newer.append(str(f.relative_to(R)))
    base = CF.get(k, {}).get('sha1_12')
    out[k] = {'files': n, 'sha1_12': h.hexdigest()[:12], 'cf_baseline': base, 'unchanged_vs_cf': (base == h.hexdigest()[:12]) if base else None, 'modified_since_pass_start': newer}
out['_note'] = 'pass start 2026-09-30 00:12 local; baseline = CharacterFinal preservation_hashes.json (2026-09-29)'
json.dump(out, open('Saved/Codex/CharacterRevision_20260930/preservation_hashes.json', 'w'), indent=1); print(json.dumps(out, indent=1))
