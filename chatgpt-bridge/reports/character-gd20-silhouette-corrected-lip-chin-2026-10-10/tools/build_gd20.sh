#!/bin/bash
# build_gd20.sh : reproduces the GD20 final sculpt G20S from GD19's final sculpt G19S (Blender batch, deterministic) into data/build/ and verifies it
# against data/head_G20S.npy. Engine stage = tools/gd20_final20.sh.
#  1 gd20_profield.py  perioral profile field I (smooth z-spline, full tissue thickness incl. teeth, lateral plateau 2.0/3.3 cm): fills the lower-lip body /
#                      labiomental sulcus and brings the upper vermilion forward (the GD18 lip retrusion + GD19 sulcus deepening were driven by a skin-key
#                      contour that drops the dark vermilion / shadowed sulcus; the background-key silhouette shows the reference in FRONT there)
#  2 ops/N20c.json     infratip / columella +1.3 mm forward (background-key: columella 1.4 px behind), nose base relax
#  3 gd20_profield.py  silhouette-fit field L on the outer skin only (y >= 12.6): sulcus +2.8 mm peak, lower lip lower border -0.8 mm
set -eu; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Saved/Codex/GD20_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; O=$T/data/build; mkdir -p $O
CPI='[[153.2,0],[153.6,1.5],[154.0,4.0],[154.4,5.0],[154.8,3.2],[155.2,1.0],[155.6,1.2],[156.0,2.0],[156.5,1.2],[157.0,0.4],[157.3,0]]'
"$B" -b --factory-startup --python "$(Wp $T/tools/gd20_profield.py)" -- "$(Wp $T/data/head_G19S.npy)" "$(Wp $O/head_PF20a.npy)" "$CPI" 2.0 3.3 10.8 9.4 2>&1 | grep -c PROFIELD
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(Wp $O/head_PF20a.npy)" "$(Wp $T/ops/N20c.json)" "$(Wp $O/head_G20I.npy)" 2>&1 | grep -c "^OP"
"$B" -b --factory-startup --python "$(Wp $T/tools/gd20_profield.py)" -- "$(Wp $O/head_G20I.npy)" "$(Wp $O/head_G20S.npy)" "$(cat $T/ops/silfit_final.json)" 2.0 3.3 12.6 11.6 2>&1 | grep -c PROFIELD
"$B" -b --factory-startup --python-expr "import numpy as np; a=np.load(r'$(Wp $O/head_G20S.npy)'); b=np.load(r'$(Wp $T/data/head_G20S.npy)'); d=np.abs(a-b).max()*10; print('BUILD_VERIFY max diff %.6f mm' % d, 'PASS' if d < 1e-4 else 'FAIL')" 2>&1 | grep BUILD_VERIFY
