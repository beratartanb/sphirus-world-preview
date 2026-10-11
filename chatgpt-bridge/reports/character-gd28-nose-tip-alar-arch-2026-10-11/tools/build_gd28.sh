#!/bin/bash
# build_gd28.sh : reproduce the GD28 sculpt (data/head_G28S.npy = candidate F) from GD27's G27S with gd28_build.sh and ops/*_F.json:
# (1) alar rim arch: bottom shell of the ala (band |x-MX| 0.85..2.4, columella / nostril floor excluded) lifted up to 2.5 mm (y 12.8-14.75), shell 6 mm
# (2) tip: supratip back 0.5 mm, upper lobule forward-up 0.45 mm, whole tip 0.1 mm up / 0.2 mm back (3) alar-base corner + alar rim rounding (4 zones)
# (4) light nose sanding. Prints the max deviation from the stored G28S (expected 0.000000 mm).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD28_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
TAG=G28R OPS=F SRC=G27S EVAL=0 ASH=0.6 ABASE="[1.37,12.85,158.1,0.5,0.45,0.4,0.2,0.2,0.15] [-1.83,12.85,158.1,0.5,0.45,0.4,0.2,0.2,0.15] [1.22,13.6,158.25,0.6,0.75,0.35,0.3,0.4,0.15] [-1.68,13.6,158.25,0.6,0.75,0.35,0.3,0.4,0.15]" bash $N/tools/gd28_build.sh 2>&1 | grep -E "Error|Trace"
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(Wp $N/data/head_G28R.npy)'); S=np.load(r'$(Wp $N/data/head_G28S.npy)'); print('BUILD_GD28 max |rebuilt - G28S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD28
