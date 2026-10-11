#!/bin/bash
# gd27_build.sh [TAG=G27A] [OPS=A] : candidate from GD26 G26S - (1) chin underside wave (bottom shell only, gd27_undershell.py along +z: chin ball bottom
# slightly DOWN, submental line behind it UP -> convex chin bottom rising toward the neck like the reference) (2) lower chin front pulled back (profield dy(z),
# full thickness) (3) nose tip pulled back (gd13_sculpt move, plateau ellipsoid). Then checks / flips / profile render / chin-bottom global residuals /
# lip prominence + proportions / contour shape / front chin-bottom row / zooms.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD27_Identity_20261011; P=Saved/Codex/GD26_Identity_20261011; G=Saved/Codex/GD13_Identity_20261009; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
T=${TAG:-G27A}; OPS=${OPS:-A}; SRC=${SRC:-G26S}; EVAL=${EVAL:-1}
H() { echo "$(Wp $N/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $N/tools/gd27_undershell.py)" -- "$(H $SRC)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_1)" "$(cat $N/ops/underchin_${OPS}.json)" "[0,0,1]" ${UX:-1.5 3.0 1.5 3.0} 9.0 11.0 ${USH:-0.5} 149.0 152.3 2>&1 | grep -E "UNDERSHELL|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd27_profield.py)" -- "$(H ${T}_1)" "$(H ${T}_2)" "$(cat $N/ops/chinback_${OPS}.json)" 1.1 2.8 10.8 9.4 2>&1 | grep -E "PROFIELD|Error" | cut -c1-90
[ -n "${CSZONE:-}" ] && { "$B" -b --factory-startup --python "$(Wp $N/tools/gd27_crease_smooth.py)" -- "$(H ${T}_2)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_2s)" "$CSZONE" ${CSIT:-6} 0.5 -1.0 0.3 2>&1 | grep -E "CREASE|Error"; cp $N/data/head_${T}_2s.npy $N/data/head_${T}_2.npy; }   # optional chin-corner rounding
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_sculpt.py)" -- "$(H ${T}_2)" "$(Wp $N/ops/tip_${OPS}.json)" "$(H ${T})" 2>&1 | grep -E "^OP|Error|Trace"
[ "$EVAL" = "1" ] || exit 0
REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_prof_faceL.png; REFF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(H ${T})" "$(Wp $N/data/checks_${T}.json)" "$(H E)" "$(H G26S)" 2>&1 | grep -E "^CHECKS|^DISP" | cut -c1-330
"$B" -b --factory-startup --python "$(Wp $N/tools/_flips.py)" -- "$(Wp $N/data/head_topo.npz)" "$(H E)" "$(H ${T})" 2>&1 | grep FLIPS
"$B" -b --factory-startup --python "$(Wp $N/tools/gd27_foldloc.py)" -- "$(H ${T})" "$(H E)" "$(Wp $N/data/head_topo.npz)" 2>&1 | grep -E "^folds|area ratio" | head -3
"$B" -b --factory-startup --python "$(Wp $N/tools/gd27_relief.py)" -- "$(Wp $N/data/head_topo.npz)" "GD26=$(H G26S)" "${T}=$(H ${T})" 2>&1 | grep "^RELIEF" | grep -o "RELIEF [A-Z0-9]* *\|tip lobule hf [0-9.]*\|chin pad hf [0-9.]*" | paste -sd' '
bash $N/tools/gd27_rset.sh $N/data/head_${T}.npy ${T}M $N/data/Ec_cams.json REF_prof_faceL:clay:A REF_front:clay:A REF_q3_faceL:clay:A >/dev/null 2>&1
echo "== chin bottom (global frame)"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd27_chinbottom.py)" -- "$(Wp $REFP)" "$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" "$(Wp $N/data/Ec_cams.json)" "$(H ${T})" pg 70 3.5 2>&1 | grep -vE "^Blender|^Read|^$|^global| arc " | awk '{printf "y%s z%s %+.2f | ", $3, $2, $5; if (NR%5==0) print ""}'; echo
echo "== lip prominence"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd27_lip_prominence.py)" -- "$(Wp $REFP)" "GD26=$(Wp $P/r/G26PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(E |line)"
echo "== proportions"; "$B" -b --factory-startup --python "$(Wp $N/tools/_horiz_profile.py)" -- "$(Wp $REFP)" "GD26=$(Wp $P/r/G26PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(pt|tip|pg|gn|me) "
echo "== contour shape"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd27_contour_shape.py)" -- "$(Wp $REFP)" "$(Wp $N/r/_contour_REF_GD26_${T}.jpg)" "$(Wp $N/meas/contour_${T}.json)" "GD26=$(Wp $P/r/G26PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "scale|^ (tip-sn|pg-me)|^   (REF|G27)" | cut -c1-150
"$B" -b --factory-startup --python "$(Wp $N/tools/_chin_edge.py)" -- "REF=$(Wp $REFF)" "GD26=$(Wp $P/r/G26SM_REF_front_clayA.png)" "${T}=$(Wp $N/r/${T}M_REF_front_clayA.png)" 2>&1 | grep -E "chin-bottom" | cut -c1-45
for zz in "chin 325 375 45 140" "lower 220 375 25 140"; do set -- $zz; "$B" -b --factory-startup --python "$(Wp $N/tools/_prof_rows_zoom.py)" -- "$(Wp $N/r/_zoom_${1}_${T}.jpg)" $2 $3 $4 $5 "$(Wp $REFP)" "GD26clay=$(Wp $P/r/G26PM_REF_prof_faceL_clayA.png)" "${T}clay=$(Wp $N/r/${T}M_REF_prof_faceL_clayA.png)" 2>&1 | grep -cE "ZOOM_OK" | tr '\n' ' '; done; echo
echo BUILD_${T}_DONE
