#!/bin/bash
# build_gd25.sh : reproduce the GD25 sculpt (data/head_G25S.npy = candidate F) from GD24's G24S with the GD25 tools (gd25_build.sh, ops/*_F.json) and print
# the max deviation from the stored G25S (expected 0.000000 mm). Steps: (1) lips outer dy(z) field: upper-lip lower vermilion back up to -2.45 mm, lower lip
# +0.12..0.5 mm, 0 at the contact line (2) lower-lip front smoothing (one convex volume instead of two ridges) (3) nose underside shell field: infratip
# lobule + columella down-forward up to 3.2 mm (convex tip->subnasale outline), shell 3 mm (4) chin pad dy(z): +0.2..1.3 mm (5) sulcus floor outer +0.4
# (6) chin corner rounded FORWARD 1.7 mm (front-down faces, no downward move - chin bottom unchanged) (7) chin smoothing (8) nostril-roof junction relax (9) light nose sanding.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD25_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
TAG=G25R OPS=F SRC=G24S EVAL=0 NSH=0.3 LLZONE='[-0.23,13.35,154.95,1.8,0.45,0.5,1.2,0.25,0.3]' LLIT=10 CORNER=1.7 CMOVE='[0,1,0]' CZONE='[-0.23,12.35,151.6,1.9,0.8,0.5,1.1,0.35,0.2]' JRELAX='[-0.23,14.49,158.58,0.55,0.22,0.16,0.4,0.1,0.06]' JIT=4 bash $N/tools/gd25_build.sh 2>&1 | grep -E "Error|Trace"
"$B" -b --factory-startup --python-expr "
import numpy as np; A=np.load(r'$(Wp $N/data/head_G25R.npy)'); S=np.load(r'$(Wp $N/data/head_G25S.npy)'); print('BUILD_GD25 max |rebuilt - G25S| = %.6f mm' % (np.abs(A-S).max()*10))" 2>&1 | grep BUILD_GD25
