#!/bin/bash
# build_gd26.sh : reproduce the GD26 sculpt (data/head_G26S.npy = candidate B) from GD25's G25S (= GD25 final F) with gd26_perioral.py and ops/perioral_B.json:
# perioral block +2.8 mm forward (skin + teeth/tongue/gums + saliva; flat from the subnasale over both lips, fading over sulcus / chin pad to 0 at z 151.8),
# nose base compressed toward the tip (full at the subnasale y 13.45, 0 at the tip y 15.5; vertical fade z 158.3-158.9, dorsum unchanged).
# Prints the max deviation from the stored G26S (expected 0.000000 mm).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD26_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
TAG=G26R OPS=B SRC=G25S EVAL=0 bash $N/tools/gd26_buildP.sh 2>&1 | grep -E "Error|Trace"
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(Wp $N/data/head_G26R.npy)'); S=np.load(r'$(Wp $N/data/head_G26S.npy)'); print('BUILD_GD26 max |rebuilt - G26S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD26
