#!/bin/bash
# gd28_build.sh [TAG=G28A] [OPS=A] : candidate from GD27 G27S - (1) alar rim arch: bottom shell of the ala lifted by f(y) (gd28_undershell.py band mode:
# columella / nostril floor |x-MX| < XI excluded, ala band to X0/X1) so the sagging rim becomes an arch and the nostril opening shows from the side like the
# reference (2) tip rotation: gd13_sculpt plateau moves (supratip back, upper lobule forward-up, infratip up) (3) light nose sanding. Then checks / flips /
# area ratio / relief / renders / nose-tip contour (dorsum+sn anchored, tangent profile) / nostril arch vs reference / proportions / zooms.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD28_Identity_20261011; P=Saved/Codex/GD27_Identity_20261011; G=Saved/Codex/GD13_Identity_20261009; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
T=${TAG:-G28A}; OPS=${OPS:-A}; SRC=${SRC:-G27S}; EVAL=${EVAL:-1}
H() { echo "$(Wp $N/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $N/tools/gd28_undershell.py)" -- "$(H $SRC)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_1)" "$(cat $N/ops/alarrim_${OPS}.json)" "[0,0,1]" ${AX:-1.9 2.4 1.9 2.4} 13.0 14.0 ${ASH:-0.35} 157.3 159.2 ${AXI:-0.85 1.05} 2>&1 | grep -E "UNDERSHELL|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(H ${T}_1)" "$(Wp $N/ops/tip_${OPS}.json)" "$(H ${T}_2)" 2>&1 | grep -E "^OP|Error|Trace"
for Zb in ${ABASE:-}; do "$B" -b --factory-startup --python "$(Wp $N/tools/gd28_crease_smooth.py)" -- "$(H ${T}_2)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_2s)" "$Zb" ${ABIT:-4} 0.5 -1.0 0.3 2>&1 | grep -E "CREASE|Error"; cp $N/data/head_${T}_2s.npy $N/data/head_${T}_2.npy; done   # optional alar-base corner rounding zones
ZN='[[-0.23,13.5,161.2,0.9,1.6,2.6],[-0.23,15.0,158.9,1.3,1.1,1.0],[1.0,13.9,158.6,0.9,1.0,0.9],[-1.46,13.9,158.6,0.9,1.0,0.9],[1.65,12.7,158.3,0.6,0.6,0.7],[-2.11,12.7,158.3,0.6,0.6,0.7]]'; EX='[[-0.23,13.9,157.9,0.3],[0.5,12.5,157.5,0.22],[-0.96,12.5,157.5,0.22]]'
"$B" -b --factory-startup --python "$(Wp $N/tools/gd28_sand.py)" -- "$(H ${T}_2)" "$(Wp $N/data/head_topo.npz)" "$(H ${T})" "$ZN" "$EX" ${SANDIT:-2} 0.5 2>&1 | grep SAND
[ "$EVAL" = "1" ] || exit 0
REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_prof_faceL.png; REFF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(H ${T})" "$(Wp $N/data/checks_${T}.json)" "$(H E)" "$(H G27S)" 2>&1 | grep -E "^CHECKS" | grep -o '"folds": [0-9]*\|"area_ratio_min": [0-9.]*\|"area_ratio_max": [0-9.]*\|"flipped_tris_vs_base": [0-9]*' | paste -sd' '
"$B" -b --factory-startup --python "$(Wp $N/tools/_flips.py)" -- "$(Wp $N/data/head_topo.npz)" "$(H E)" "$(H ${T})" 2>&1 | grep FLIPS
"$B" -b --factory-startup --python "$(Wp $N/tools/gd28_foldloc.py)" -- "$(H ${T})" "$(H E)" "$(Wp $N/data/head_topo.npz)" 2>&1 | grep -E "^folds|area ratio" | head -3
"$B" -b --factory-startup --python "$(Wp $N/tools/gd28_relief.py)" -- "$(Wp $N/data/head_topo.npz)" "GD27=$(H G27S)" "${T}=$(H ${T})" 2>&1 | grep "^RELIEF" | grep -o "RELIEF [A-Z0-9]* *\|tip lobule hf [0-9.]*\|alar wings + alar crease hf [0-9.]*\|nostril sill / columella hf [0-9.]*" | paste -sd' '
"$B" -b --factory-startup --python "$(Wp $N/tools/_alar_rim.py)" -- "${T}=$(H ${T})" 2>&1 | grep -vE "^Blender|^Read|^$" | sed -n '2,12p' | tr '\n' '|' | cut -c1-600; echo
bash $N/tools/gd28_rset.sh $N/data/head_${T}.npy ${T}M $N/data/Ec_cams.json REF_prof_faceL:clay:A REF_front:clay:A REF_q3_faceL:clay:A >/dev/null 2>&1
echo "== nose tip contour"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd28_nosecontour.py)" -- "$(Wp $REFP)" "$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" "$(Wp $N/data/Ec_cams.json)" "$(H ${T})" 28 3.5 2>&1 | grep -vE "^Blender|^Read|^$" | awk 'NR<=1 {print; next} /tangent|REF|CAN/ {print; next} NR>2 {printf "z%s %+.2f | ", $2, $5; if (++c%6==0) print ""}'; echo
echo "== nostril arch"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd28_nostril.py)" -- "$(Wp $N/r/_nostril_REF_${T}.jpg)" 44 92 238 268 14 "REF=$(Wp $REFP):1:42.0,242.7,65.0,267.4" "GD27clay=$(Wp $P/r/G27PM_REF_prof_faceL_clayA.png):2:44.0,243.0,66.5,266.0|46,72,243,262|$(Wp $P/r/G27PM_REF_prof_faceL_alpha.png)" "${T}clay=$(Wp $N/r/${T}M_REF_prof_faceL_clayA.png):2:44.0,243.0,66.5,266.0|44,74,242,263|$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(label|REF|GD27|G28)"
echo "== proportions"; "$B" -b --factory-startup --python "$(Wp $N/tools/_horiz_profile.py)" -- "$(Wp $REFP)" "GD27=$(Wp $P/r/G27PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(pt|tip) "
"$B" -b --factory-startup --python "$(Wp $N/tools/gd28_contour_shape.py)" -- "$(Wp $REFP)" "$(Wp $N/r/_contour_REF_GD27_${T}.jpg)" "$(Wp $N/meas/contour_${T}.json)" "GD27=$(Wp $P/r/G27PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -A3 "^ tip-sn" | cut -c1-150
"$B" -b --factory-startup --python "$(Wp $N/tools/_prof_rows_zoom.py)" -- "$(Wp $N/r/_zoom_nose_${T}.jpg)" 215 272 30 100 "$(Wp $REFP)" "GD27clay=$(Wp $P/r/G27PM_REF_prof_faceL_clayA.png)" "${T}clay=$(Wp $N/r/${T}M_REF_prof_faceL_clayA.png)" 2>&1 | grep -cE "ZOOM_OK"
echo BUILD_${T}_DONE
