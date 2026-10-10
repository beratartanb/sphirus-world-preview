#!/bin/bash
# build_gd22.sh : reproduces the GD22 final sculpt G22S from GD19's final sculpt G19S (the natural lower lip) and verifies it against data/head_G22S.npy.
#  1 gd22_profield.py  full-thickness profile field F (ops/profield_final.json): lower lip moved RIGIDLY +1.5 mm (shape kept), lower-lip body / sulcus +3..+6 mm, upper vermilion +2 mm, philtrum +0.4
#  2 ops/N20c.json     infratip / columella +1.3 mm (as GD20)
#  3 gd22_crease_smooth.py  targeted positional rounding of the lip-underside / sulcus crease (outer skin, 8 x 0.5, zone x +-2..3, z 154.5 +-0.2..0.55)
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; V=Saved/Codex/GD22_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$V/data/build; mkdir -p $O
"$B" -b --factory-startup --python "$(Wp $V/tools/gd22_profield.py)" -- "$(Wp $V/data/head_G19S.npy)" "$(Wp $O/head_PF22F.npy)" "$(cat $V/ops/profield_final.json)" 2.0 3.3 10.8 9.4 2>&1 | grep -c PROFIELD
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_PF22F.npy)" "$(Wp $V/ops/N20c.json)" "$(Wp $O/head_G22F0.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $V/tools/gd22_crease_smooth.py)" -- "$(Wp $O/head_G22F0.npy)" "$(Wp $V/data/head_topo.npz)" "$(Wp $O/head_G22S.npy)" '[-0.23,13.0,154.5,3.0,1.4,0.55,2.0,0.6,0.2]' 8 0.5 0.0 2>&1 | grep -c CREASE
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G22S.npy)'); b=np.load(r'$(Wp $V/data/head_G22S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
