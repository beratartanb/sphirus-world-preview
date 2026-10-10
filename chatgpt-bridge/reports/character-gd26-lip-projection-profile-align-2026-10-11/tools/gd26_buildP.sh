#!/bin/bash
# gd26_buildP.sh [TAG=G26A] [OPS=A] : perioral block advancement from GD25 G25S - ONE full-thickness dy(z) field (profield, teeth/saliva move with it;
# depth ramp Y0/Y1, lateral plateau X0/X1) from ops/perioral_<OPS>.json: flat over subnasale..lower lip (lip shapes unchanged), fading up into the nose
# base (tip fixed) and down over sulcus / chin pad (chin bottom fixed). Then checks / flips / relief / profile render / lip prominence (E-line, sn-pg) /
# horizontal proportions / contour shape / zooms / strips.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD26_Identity_20261011; P=Saved/Codex/GD25_Identity_20261011; G=Saved/Codex/GD13_Identity_20261009; O=$G; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
T=${TAG:-G26A}; OPS=${OPS:-A}; SRC=${SRC:-G25S}; EVAL=${EVAL:-1}
H() { echo "$(Wp $N/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $N/tools/gd26_perioral.py)" -- "$(H $SRC)" "$(H ${T})" "$(cat $N/ops/perioral_${OPS}.json)" ${PJ:-157.35 13.45 15.5 158.3 158.9} ${PX:-2.2 3.6} ${PY:-10.0 8.0} 2>&1 | grep -E "PERIORAL|Error|Trace" | cut -c1-120
[ "$EVAL" = "1" ] || exit 0
REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_prof_faceL.png; REFF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(H ${T})" "$(Wp $N/data/checks_${T}.json)" "$(H E)" "$(H G25S)" 2>&1 | grep -E "^CHECKS|^DISP" | cut -c1-330
"$B" -b --factory-startup --python "$(Wp $N/tools/_flips.py)" -- "$(Wp $N/data/head_topo.npz)" "$(H E)" "$(H ${T})" 2>&1 | grep FLIPS
"$B" -b --factory-startup --python "$(Wp $N/tools/gd26_foldloc.py)" -- "$(H ${T})" "$(H E)" "$(Wp $N/data/head_topo.npz)" 2>&1 | grep -E "^folds|area ratio" | head -4
bash $N/tools/gd26_rset.sh $N/data/head_${T}.npy ${T}M $N/data/Ec_cams.json REF_prof_faceL:clay:A REF_front:clay:A REF_q3_faceL:clay:A >/dev/null 2>&1
echo "== lip prominence"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd26_lip_prominence.py)" -- "$(Wp $REFP)" "GD25=$(Wp $P/r/G25PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(E |snpg|line)"
echo "== horizontal proportions"; "$B" -b --factory-startup --python "$(Wp $N/tools/_horiz_profile.py)" -- "$(Wp $REFP)" "GD25=$(Wp $P/r/G25PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "^(pt|tip|ls|sto|li|sm|pg|gn|me) "
echo "== contour shape"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd26_contour_shape.py)" -- "$(Wp $REFP)" "$(Wp $N/r/_contour_REF_GD25_${T}.jpg)" "$(Wp $N/meas/contour_${T}.json)" "GD25=$(Wp $P/r/G25PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "scale|^ (tip-sn|sn-ls|ls-sto|pg-me)|^   (REF|G26)" | cut -c1-150
"$B" -b --factory-startup --python "$(Wp $N/tools/_chin_edge.py)" -- "REF=$(Wp $REFF)" "${T}clay=$(Wp $N/r/${T}M_REF_front_clayA.png)" 2>&1 | grep -E "chin-bottom" | cut -c1-50
for zz in "lips 262 322 30 100" "lower 220 365 25 120"; do set -- $zz; "$B" -b --factory-startup --python "$(Wp $N/tools/_prof_rows_zoom.py)" -- "$(Wp $N/r/_zoom_${1}_${T}.jpg)" $2 $3 $4 $5 "$(Wp $REFP)" "GD25clay=$(Wp $P/r/G25PM_REF_prof_faceL_clayA.png)" "${T}clay=$(Wp $N/r/${T}M_REF_prof_faceL_clayA.png)" 2>&1 | grep -cE "ZOOM_OK" | tr '\n' ' '; done; echo
echo BUILD_${T}_DONE
