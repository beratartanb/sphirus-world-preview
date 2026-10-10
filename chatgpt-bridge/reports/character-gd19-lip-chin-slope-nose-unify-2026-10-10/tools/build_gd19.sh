#!/bin/bash
# build_gd19.sh : reproduces the GD19 final sculpt G19S from GD18's final sculpt G18S (Blender batch, deterministic) into data/build/ and verifies it
# against data/head_G19S.npy. Engine stage (fit + 2 residual feedback fits -> auto-rig -> custom brow c4 bind -> captures) = tools/gd19_final19.sh.
#  1 ops/N19.json  (relax base = G17S)  lower-nose merge relax (blends the GD18 tip-lobule / alar bulges into one soft unit), tip-ala junction fill, unified lower-nose rounding, dorsum relax
#  2 gd19_sand.py  high-frequency sanding of the lobule + alae (natural creases excluded), 3 x 0.6
#  3 ops/C19.json   first chin pass: mentolabial band -1.5 mm, upper pad -0.7 mm, relax (candidate A)
#  4 ops/N19b.json (relax base = G17S)  tip-ala junction relax + fill, supra-alar relax
#  5 ops/C19c.json  chin bottom restored (-2.0 mm: GD18's shortening undone; the reference chin bottom row 761 = GD17 761 = GD19 762), mentolabial band -1.5 mm,
#                   lateral mentolabial shelf -1.8 mm, pad top -1.4 mm, relax
#  6 ops/C19d.json  S-amplitude smoothing: sulcus +0.9 mm, pad top -0.9 mm, lower pad -1.2 mm, relax
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; Q=Saved/Codex/GD19_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$Q/data/build; mkdir -p $O
ZN='[[-0.23,15.0,158.9,1.3,1.1,1.0],[1.0,13.9,158.6,0.8,0.9,0.8],[-1.46,13.9,158.6,0.8,0.9,0.8]]'; EX='[[1.22,12.9,158.4,0.28],[-1.68,12.9,158.4,0.28],[-0.23,13.9,157.9,0.3],[0.5,12.5,157.5,0.22],[-0.96,12.5,157.5,0.22]]'
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $Q/data/head_G18S.npy)" "$(Wp $Q/ops/N19.json)" "$(Wp $O/head_N19a.npy)" "$(Wp $Q/data/head_G17S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $Q/tools/gd19_sand.py)" -- "$(Wp $O/head_N19a.npy)" "$(Wp $Q/data/head_topo.npz)" "$(Wp $O/head_N19.npy)" "$ZN" "$EX" 3 0.6 2>&1 | grep -c SAND
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_N19.npy)" "$(Wp $Q/ops/C19.json)" "$(Wp $O/head_G19A.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_G19A.npy)" "$(Wp $Q/ops/N19b.json)" "$(Wp $O/head_N19b.npy)" "$(Wp $Q/data/head_G17S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_N19b.npy)" "$(Wp $Q/ops/C19c.json)" "$(Wp $O/head_G19C.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_G19C.npy)" "$(Wp $Q/ops/C19d.json)" "$(Wp $O/head_G19S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G19S.npy)'); b=np.load(r'$(Wp $Q/data/head_G19S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
