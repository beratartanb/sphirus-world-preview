#!/bin/bash
# build_gd31.sh : reproduce the GD31 sculpt (data/head_G31S.npy = candidate Z1) from GD30's final W4 (data/head_G30S.npy, read-only copy):
# (1) posterior nose-base lowering (sill + posterior rim + alar base, bell |x-MX| 1.0 +- 0.55, columella kept, lip floor 156.7/0.35, up to 2.0 mm at
#     y 13.0-13.3; ops/postdown_Z1.json) - the aperture plane turns toward the camera and the opening slants down toward the back like the photo
# (2) posterior nostril-cavity deepening 1.8 mm into the tissue (gd31_cavdeep.py, cavity set data/cavity_idx.npy, full at y <= 13.6) so the
#     posterior vestibule stays dark. Prints the max deviation from the stored G31S (expected 0.000000 mm).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; Y=Saved/Codex/GD31_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; H() { echo "$(Wp $Y/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $Y/tools/gd31_alabell.py)" -- "$(H G30S)" "$(Wp $Y/data/head_topo.npz)" "$(H G31R_a)" "$(cat $Y/ops/postdown_Z1.json)" "[0,0,1]" 1.0 0.55 0.35 0.55 0.6 156.7 0.35 159.4 3 2>&1 | grep -E "rror"
"$B" -b --factory-startup --python "$(Wp $Y/tools/gd31_cavdeep.py)" -- "$(H G31R_a)" "$(Wp $Y/data/head_topo.npz)" "$(Wp $Y/data/cavity_idx.npy)" "$(H G31R)" 1.8 13.6 14.4 3 2>&1 | grep -E "rror"; rm -f $Y/data/head_G31R_a.npy
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(H G31R)'); S=np.load(r'$(H G31S)'); print('BUILD_GD31 max |rebuilt - G31S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD31
