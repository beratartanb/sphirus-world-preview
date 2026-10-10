#!/bin/bash
# build_gd18.sh : reproduces the GD18 final sculpt G18S from GD17's final sculpt G17S (Blender batch, deterministic) into data/build/ and verifies it
# against data/head_G18S.npy. Engine stage (fit + 2 residual feedback fits -> auto-rig -> custom brow c4 bind -> captures) = tools/gd18_final18.sh.
#  1 ops/N18E.json  nose: dorsum cartilage +0.6 mm, tip lobule front compressed upward (z scale 0.78 about z 159.55, field limited to y >= 14.4 so the nostril roof / columella stay), lobule rounding, lower lobule front -1.2 mm,
#                   columella tuck (-1.2 mm back / +0.5 up), lateral alar rims -1.0 mm, alar lobule + alar-cheek groove + nasofacial groove soft fills, sidewalls +0.6 mm, relax
#  2 ops/C18c.json  chin: labiomental fold -1.4 mm, lower chin pad +1.5 mm forward, chin bottom +2.0 mm up, lower chin narrowed 8 % (smooth x-scale, |x| 2 cm -> -1.6 mm), prejowl fill, relax
#  3 ops/P18d.json  perioral depth + radix: radix -0.9 mm, upper lip -3.2 mm (incl. vermilion), lower lip -2.2 mm (uniform depth, vermilion shape / GD17 taper kept), relax
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD18_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$N/data/build; mkdir -p $O
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $N/data/head_G17S.npy)" "$(Wp $N/ops/N18E.json)" "$(Wp $O/head_N18C.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_N18C.npy)" "$(Wp $N/ops/C18c.json)" "$(Wp $O/head_G18Cc.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_G18Cc.npy)" "$(Wp $N/ops/P18d.json)" "$(Wp $O/head_G18S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G18S.npy)'); b=np.load(r'$(Wp $N/data/head_G18S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
