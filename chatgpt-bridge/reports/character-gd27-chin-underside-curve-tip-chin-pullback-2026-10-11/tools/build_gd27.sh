#!/bin/bash
# build_gd27.sh : reproduce the GD27 sculpt (data/head_G27S.npy = candidate B) from GD26's G26S with gd27_build.sh and ops/*_B.json:
# (1) chin underside wave (bottom shell only, +z): submental lifted up to 2.9 mm (y 6.5-11.9, lateral 2.6/4.2 -> 2.0/3.4) so the underside rises toward
# the neck, chin-ball bottom -0.15 mm (2) lower chin front back up to 0.6 mm (z 151.4-153.2) (3) chin-corner rounding (positional smoothing, 6 x 0.5)
# (4) nose tip back 0.7 mm (plateau ellipsoid move). Prints the max deviation from the stored G27S (expected 0.000000 mm).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD27_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
TAG=G27R OPS=B SRC=G26S EVAL=0 UX="2.6 4.2 2.0 3.4" CSZONE='[-0.23,12.6,151.7,1.8,0.7,0.45,1.0,0.3,0.2]' CSIT=6 bash $N/tools/gd27_build.sh 2>&1 | grep -E "Error|Trace"
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(Wp $N/data/head_G27R.npy)'); S=np.load(r'$(Wp $N/data/head_G27S.npy)'); print('BUILD_GD27 max |rebuilt - G27S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD27
