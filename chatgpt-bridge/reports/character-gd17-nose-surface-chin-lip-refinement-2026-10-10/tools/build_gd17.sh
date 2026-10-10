#!/bin/bash
# build_gd17.sh --blender-stage : reproduces the GD17 final sculpt G17S from GD16's final sculpt G16S (all Blender batch, deterministic), into data/build/,
# and verifies it against data/head_G17S.npy. Engine stage (fit + 2 residual feedback fits -> auto-rig -> custom brow c4 bind -> captures) = tools/gd17_final17.sh.
#  1 NSb  nose HF sanding (gd17_sand.py): relief high-frequency band removed along normals in 4 nose zones (dorsum/radix, tip lobule, both sidewalls),
#         natural creases excluded (alar creases, columella base, nostril sills); 6 iterations x 0.8
#  2 NLa  displacement low-pass (gd13 'relax' with base = GD15 G15S) of the lower nose and the bridge, 30 iterations, plateau zones (ops/NLa.json)
#  3 NMa  smooth plateau alar-lobule narrowing move 1.0 mm medial, symmetric (ops/NAa.json)
#  4 G17Gc chin CH3: plateau inflate lateral chin pad 1.25 mm + chin-jaw corner 1.05 mm, chin bottom up 1.0 mm, field relax (ops/CH3.json)
#  5 G17G  lateral upper-lip vermilion taper toward the contact line (gd17_lipthin.py K 0.2, centre 1.85, half-width 0.62, Z0 155.55); commissures fixed
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD17_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$W/data/build; mkdir -p $O
ZN='[[-0.23,13.5,161.2,0.9,1.6,2.6],[-0.23,14.9,158.9,1.0,0.9,0.8],[0.75,12.8,160.6,0.7,1.2,1.6],[-1.21,12.8,160.6,0.7,1.2,1.6]]'
EX='[[1.22,12.9,158.4,0.28],[-1.68,12.9,158.4,0.28],[-0.23,13.9,157.9,0.3],[0.5,12.5,157.5,0.22],[-0.96,12.5,157.5,0.22]]'
"$B" -b --factory-startup --python "$(Wp $W/tools/gd17_sand.py)" -- "$(Wp $W/data/head_G16S.npy)" "$(Wp $W/data/head_topo.npz)" "$(Wp $O/head_NSb.npy)" "$ZN" "$EX" 6 0.8 2>&1 | grep SAND
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_NSb.npy)" "$(Wp $W/ops/NLa.json)" "$(Wp $O/head_NLa.npy)" "$(Wp $W/data/head_G15S.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_NLa.npy)" "$(Wp $W/ops/NAa.json)" "$(Wp $O/head_NMa.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_NMa.npy)" "$(Wp $W/ops/CH3.json)" "$(Wp $O/head_G17Gc.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $W/tools/gd17_lipthin.py)" -- "$(Wp $O/head_G17Gc.npy)" "$(Wp $O/head_G17S.npy)" 0.2 1.85 0.62 155.55 2>&1 | grep LIPTHIN
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G17S.npy)'); b=np.load(r'$(Wp $W/data/head_G17S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
