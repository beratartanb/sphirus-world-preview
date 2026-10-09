#!/bin/bash
# gd16_dedup.sh : remove raw captures in the shared captures folder whose SHA-1 identical copy exists in GD16/ue (non-ref sets are plain copies)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD16_Identity_20261010
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - <<'PYE'
import os, hashlib, json
def h(p):
    s = hashlib.sha1(); f = open(p, 'rb'); [s.update(b) for b in iter(lambda: f.read(1 << 20), b'')]; f.close(); return s.hexdigest()
C = 'Saved/Codex/CharacterLookdev_20260930/captures'; U = 'Saved/Codex/GD16_Identity_20261010/ue'; M = 'Saved/Codex/GD16_Identity_20261010/data/disk_cleanup_manifest.json'
man = json.load(open(M)); n = 0; fr = 0
for f in os.listdir(U):
    r, u = os.path.join(C, f), os.path.join(U, f)
    if os.path.exists(r) and os.path.getsize(r) == os.path.getsize(u) and h(r) == h(u):
        s = os.path.getsize(r); os.remove(r); man['removed'].append({'removed': r.replace(os.sep, '/'), 'identical_copy_kept': u.replace(os.sep, '/'), 'bytes': s}); n += 1; fr += s
json.dump(man, open(M, 'w'), indent=1); print('DEDUP removed %d, %.2f GB' % (n, fr/1e9))
PYE
