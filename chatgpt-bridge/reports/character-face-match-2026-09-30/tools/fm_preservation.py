"""FACE-MATCH protected-folder preservation check (run from the project root with any Python 3):
  1. sha1 over sorted .uasset names+bytes of every protected group, compared with the hashes recorded by the previous (final-art,
     commit 4003557) pass in Saved/Codex/CharacterFinalArt_20260930/preservation_hashes.json
  2. the 4003557 lookdev candidate itself: every lookdev .uasset that existed before this pass started must be unmodified
     (pass start = oldest file of Saved/Codex/CharacterFaceMatch_20260930); files created by this pass are listed separately."""
import hashlib, pathlib, json, datetime, os
R = pathlib.Path('Content'); PREV = json.load(open('Saved/Codex/CharacterFinalArt_20260930/preservation_hashes.json'))
FM = pathlib.Path('Saved/Codex/CharacterFaceMatch_20260930'); START = min(f.stat().st_ctime for f in FM.rglob('*') if f.is_file())
groups = {'production MH_MainCharacter': R/'MetaHumans/MH_MainCharacter', 'accepted B2': R/'Sphirus/CharacterLab/NativeBody_20260928',
          'accepted SHCB HelperFix': R/'Sphirus/CharacterLab/ShoulderFix_20260928/HighElevCorrective/HelperFix', 'BR v5 candidate': R/'Sphirus/CharacterLab/BodyRealism_20260929',
          'Outfit V1 candidate': R/'Sphirus/CharacterLab/Outfit_Home_20260929', 'ShoulderFix skeleton copies': R/'Sphirus/CharacterLab/ShoulderFix_20260928/Common',
          'CharacterFinal candidate (previous)': R/'Sphirus/CharacterLab/CharacterFinal_20260929', 'CharacterRevision candidate (rejected, read-only reference)': R/'Sphirus/CharacterLab/CharacterRevision_20260930'}
out = {}
for k, d in groups.items():
    h = hashlib.sha1(); n = 0
    for f in sorted(d.rglob('*.uasset')): h.update(f.name.encode()); h.update(f.read_bytes()); n += 1
    prev = PREV.get(k, {}).get('sha1_12'); out[k] = {'files': n, 'sha1_12': h.hexdigest()[:12], 'final_art_pass_hash': prev, 'unchanged_vs_4003557': (prev == h.hexdigest()[:12]) if prev else None}
LK = R/'Sphirus/CharacterLab/CharacterLookdev_20260930'; pre_mod, new = [], []
for f in sorted(LK.rglob('*.uasset')):
    st = f.stat()
    if st.st_ctime >= START: new.append(str(f.relative_to(LK)))
    elif st.st_mtime >= START: pre_mod.append(str(f.relative_to(LK)))
out['lookdev 4003557 candidate'] = {'pre_existing_files_modified_this_pass': pre_mod, 'new_files_this_pass': len(new), 'new_files': new}
out['_note'] = 'pass start = %s (oldest face-match evidence file); baseline = final-art pass preservation_hashes.json (commit 4003557)' % datetime.datetime.fromtimestamp(START).isoformat(timespec='minutes')
json.dump(out, open(FM/'preservation_hashes.json', 'w'), indent=1)
print(json.dumps({k: ((v['files'], v['unchanged_vs_4003557']) if 'files' in v else (len(v['pre_existing_files_modified_this_pass']), v['new_files_this_pass'])) if isinstance(v, dict) else v for k, v in out.items()}, indent=1))
