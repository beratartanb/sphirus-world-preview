#!/bin/bash
# build_gd21.sh : reproduces the GD21 final sculpt G21S from GD20's final sculpt G20S and verifies it against data/head_G21S.npy. Engine stage = tools/gd21_final21.sh.
#  1 gd21_profield.py  outer-skin (y >= 12.6) profile field: labiomental curl reduced from both walls - pad top -0.8 mm, sulcus +2.3..+2.8 mm, lower-lip lower border -1.3 mm (ops/silfit_final.json)
#  2 ops/R21.json      displacement relax (base = G20S) over the lower-lip border step
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; U=Saved/Codex/GD21_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$U/data/build; mkdir -p $O
"$B" -b --factory-startup --python "$(Wp $U/tools/gd21_profield.py)" -- "$(Wp $U/data/head_G20S.npy)" "$(Wp $O/head_G21B.npy)" "$(cat $U/ops/silfit_final.json)" 2.0 3.3 12.6 11.6 2>&1 | grep -c PROFIELD
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_G21B.npy)" "$(Wp $U/ops/R21.json)" "$(Wp $O/head_G21S.npy)" "$(Wp $U/data/head_G20S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G21S.npy)'); b=np.load(r'$(Wp $U/data/head_G21S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
