#!/bin/bash
# build_gd30.sh : reproduce the GD30 sculpt (data/head_G30S.npy = candidate G) from GD28's G28S (read-only copy in GD30/data):
# (1) lobule bottom lowering: bottom shell of the nose base, Gaussian lateral bell (|x-MX| 1.4 +- 0.5 cm, columella kept), up to 2.4 mm at y 13.1
#     (ops/lobbell_B.json), lip floor guard at z 157.25 - front-view lobule bottoms now on the reference rows
# (2) posterior lobule: back-lateral normal push 2.5 mm of the lobule's posterior face + fill-only crease softening 2.0 mm + junction relaxation
#     (gd30_buildpost.sh) - the alar-facial crease moves back to the reference's crease line in profile
# (3) lower nose lift (user: tip looks low / droops in 3/4): bottom shell of tip lobule + columella + subnasale region, midline Gaussian bell
#     (sigma 0.7 cm), shell 2.4 cm, +2.0 mm from y 13.3 to 15.9 (ops/noseup_K.json), lip floor 156.6 / 0.5 - profile tip/sn relation kept
# (4) tip lobule +2.0 mm (user: tip still low; midline bell sigma 0.6, shell 2.0 cm, y 14.7-16.4, ops/tipup_U.json) and nostril-margin lift
#     (posterior 1.5 / anterior 2.0 mm, rim bell |x-MX| 1.0 +- 0.22, ops/rimlift_U.json): larger, higher nostril opening in front / 3/4
# (5) form softening (user: transitions look bony): positional smoothing of the new lobule ridges / nostril-rim junction / lobule back edge
#     (ops/soften_W2_zones.txt 16 it, soften_W3_zones.txt 10 it), one broad nostril-rim arc (ops/rimarc_W4.json), light posterior push 1.5 / fill 1.0,
#     final smoothing 8 it - alar relief hf 0.045 -> 0.035, max 0.72 -> 0.32 mm
# Verified against the reference with gd30_eval.sh (valley lines + probes in the 4 solved cameras). Prints the max deviation (expected 0).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; V=Saved/Codex/GD30_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; H() { echo "$(Wp $V/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H G28S)" "$(Wp $V/data/head_topo.npz)" "$(H G30R_b)" "$(cat $V/ops/lobbell_B.json)" "[0,0,1]" 1.4 0.5 0.35 0.6 0.6 157.25 0.3 2>&1 | grep -E "rror"
bash $V/tools/gd30_buildpost.sh G30R_b G30R_g 2.5 2.0 | grep -v BUILDPOST; rm -f $V/data/head_G30R_b.npy
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H G30R_g)" "$(Wp $V/data/head_topo.npz)" "$(H G30R)" "$(cat $V/ops/noseup_K.json)" "[0,0,1]" 0.0 0.7 -1 -0.5 2.4 156.6 0.5 161.8 4 2>&1 | grep -E "rror"; rm -f $V/data/head_G30R_g.npy; mv $V/data/head_G30R.npy $V/data/head_G30R_k.npy
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H G30R_k)" "$(Wp $V/data/head_topo.npz)" "$(H G30R_t)" "$(cat $V/ops/tipup_U.json)" "[0,0,1]" 0.0 0.6 -1 -0.5 2.0 157.6 0.4 161.6 4 2>&1 | grep -E "rror"
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H G30R_t)" "$(Wp $V/data/head_topo.npz)" "$(H G30R)" "$(cat $V/ops/rimlift_U.json)" "[0,0,1]" 1.0 0.22 0.55 0.75 0.3 157.5 0.2 159.4 3 2>&1 | grep -E "rror"; rm -f $V/data/head_G30R_k.npy $V/data/head_G30R_t.npy
CS() { "$B" -b --factory-startup --python "$(Wp $V/tools/gd30_crease_smooth.py)" -- "$(H G30R)" "$(Wp $V/data/head_topo.npz)" "$(H G30R_s)" "$1" $2 0.5 -1.0 0.3 2>&1 | grep -E "rror"; cp $V/data/head_G30R_s.npy $V/data/head_G30R.npy; }
for Zb in $(cat $V/ops/soften_W2_zones.txt); do CS "$Zb" 16; done; for Zb in $(cat $V/ops/soften_W3_zones.txt); do CS "$Zb" 10; done
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_alabell.py)" -- "$(H G30R)" "$(Wp $V/data/head_topo.npz)" "$(H G30R_a)" "$(cat $V/ops/rimarc_W4.json)" "[0,0,1]" 1.0 0.25 0.55 0.75 0.3 157.5 0.2 159.4 3 2>&1 | grep -E "rror"
bash $V/tools/gd30_buildpost.sh G30R_a G30R 1.5 1.0 | grep -v BUILDPOST; rm -f $V/data/head_G30R_a.npy
for Zb in $(cat $V/ops/soften_W3_zones.txt) "[0.56,14.03,158.56,0.35,0.45,0.3,0.1,0.15,0.1]" "[-1.02,14.03,158.56,0.35,0.45,0.3,0.1,0.15,0.1]"; do CS "$Zb" 8; done; rm -f $V/data/head_G30R_s.npy
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(Wp $V/data/head_G30R.npy)'); S=np.load(r'$(Wp $V/data/head_G30S.npy)'); print('BUILD_GD30 max |rebuilt - G30S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD30
