#!/bin/bash
# gd25_build.sh [TAG=G25A] [OPS=A] : candidate from GD24 G24S using ops/<name>_<OPS>.json - (1) lips: one outer-skin dy(z) field (upper-lip lower vermilion back,
# lower-lip top forward, 0 at the contact line) (2) lower-lip lower half smoothing (outer zone) (3) nose underside shell field (infratip lobule + columella
# down-forward, convex tip->subnasale outline) (4) chin pad dy(z) (upper/mid pad forward, lower front back) (5) sulcus floor outer fill (6) chin corner
# normal push (front-down faces) (7) chin smoothing (8) light nose sanding. Then checks / flips / relief / profile render / contour shape / anchored residuals / zooms.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD25_Identity_20261011; P=Saved/Codex/GD24_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009; O=$G; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
T=${TAG:-G25A}; OPS=${OPS:-A}; SRC=${SRC:-G24S}; EVAL=${EVAL:-1}
H() { echo "$(Wp $N/data/head_$1.npy)"; }
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_profield2.py)" -- "$(H $SRC)" "$(H ${T}_1)" "$(cat $N/ops/lips_${OPS}.json)" "[]" 1.0 2.0 ${LIPY:-13.3 12.9} 13.3 12.9 -1.4 0 2>&1 | grep -E "PROFIELD2|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_crease_smooth.py)" -- "$(H ${T}_1)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_2)" "${LLZONE:-[-0.23,13.3,154.65,1.8,0.5,0.35,1.2,0.25,0.15]}" ${LLIT:-6} 0.5 -1.0 0.3 2>&1 | grep -E "CREASE|Error"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_undershell.py)" -- "$(H ${T}_2)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_3)" "$(cat $N/ops/nose_${OPS}.json)" "${NDIR:-[0,0.55,-0.83]}" 0.25 0.55 0.5 1.0 14.2 14.6 ${NSH:-0.12} 2>&1 | grep -E "UNDERSHELL|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_profield.py)" -- "$(H ${T}_3)" "$(H ${T}_4)" "$(cat $N/ops/chin_${OPS}.json)" 1.1 2.8 10.8 9.4 2>&1 | grep -E "PROFIELD|Error" | cut -c1-90
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_profield2.py)" -- "$(H ${T}_4)" "$(H ${T}_5)" "$(cat $N/ops/sulcus_${OPS}.json)" "[]" 1.0 2.4 12.9 12.4 12.9 12.4 -1.4 0 2>&1 | grep -E "PROFIELD2|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_normal_push.py)" -- "$(H ${T}_5)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_6)" "${CZONE:-[-0.23,12.45,151.6,1.6,0.6,0.35,0.9,0.25,0.12]}" ${CORNER:-0.6} '[0,0.6,-0.8]' 0.3 ${CMOVE:+"$CMOVE"} 2>&1 | grep -E "NORMAL_PUSH|Error|Trace"
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_crease_smooth.py)" -- "$(H ${T}_6)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_7)" "${CSZONE:-[-0.23,12.7,152.0,2.0,1.0,0.7,1.2,0.5,0.35]}" ${CSIT:-4} 0.5 -1.0 0.3 2>&1 | grep -E "CREASE|Error"
[ -n "${JRELAX:-}" ] && { "$B" -b --factory-startup --python "$(Wp $N/tools/gd25_crease_smooth.py)" -- "$(H ${T}_7)" "$(Wp $N/data/head_topo.npz)" "$(H ${T}_7r)" "$JRELAX" ${JIT:-4} 0.5 -1.0 0.3 2>&1 | grep -E "CREASE|Error"; cp $N/data/head_${T}_7r.npy $N/data/head_${T}_7.npy; }   # optional local relax (nostril-roof junction)
ZN='[[-0.23,13.5,161.2,0.9,1.6,2.6],[-0.23,15.0,158.9,1.3,1.1,1.0],[1.0,13.9,158.6,0.9,1.0,0.9],[-1.46,13.9,158.6,0.9,1.0,0.9],[1.65,12.7,158.3,0.6,0.6,0.7],[-2.11,12.7,158.3,0.6,0.6,0.7]]'; EX='[[-0.23,13.9,157.9,0.3],[0.5,12.5,157.5,0.22],[-0.96,12.5,157.5,0.22]]'
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_sand.py)" -- "$(H ${T}_7)" "$(Wp $N/data/head_topo.npz)" "$(H ${T})" "$ZN" "$EX" 2 0.5 2>&1 | grep SAND
[ "$EVAL" = "1" ] || exit 0
# ---- checks / measurements / renders
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(H ${T})" "$(Wp $N/data/checks_${T}.json)" "$(H E)" "$(H G24S)" 2>&1 | grep -E "^CHECKS|^DISP" | cut -c1-330
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_foldloc.py)" -- "$(H ${T})" "$(H E)" "$(Wp $N/data/head_topo.npz)" 2>&1 | grep -E "^folds|area ratio" | head -5
"$B" -b --factory-startup --python "$(Wp $N/tools/_flips.py)" -- "$(Wp $N/data/head_topo.npz)" "$(H E)" "$(H ${T})" 2>&1 | grep FLIPS
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_relief.py)" -- "$(Wp $N/data/head_topo.npz)" "GD24=$(H G24S)" "${T}=$(H ${T})" 2>&1 | grep "^RELIEF" | cut -c1-300
bash $N/tools/gd25_rset.sh $N/data/head_${T}.npy ${T}M $N/data/Ec_cams.json "REF_prof_faceL:clay:A" >/dev/null 2>&1
REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_prof_faceL.png; REFF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_front.png
"$B" -b --factory-startup --python "$(Wp $N/tools/gd25_contour_shape.py)" -- "$(Wp $REFP)" "$(Wp $N/r/_contour_REF_GD24_${T}.jpg)" "$(Wp $N/meas/contour_${T}.json)" "GD24=$(Wp $P/r/G24PM_REF_prof_faceL_alpha.png)" "${T}=$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" 2>&1 | grep -E "scale|^ (tip-sn|sn-ls|ls-sto|sto-li|li-sm|sm-pg|pg-me)|^   (REF|GD24|G25)" | cut -c1-150
for an in "tip sn 0.05,0.05" "sn sm 0,0" "sm gn 0,0.3"; do set -- $an; echo "== anchored $1-$2"; "$B" -b --factory-startup --python "$(Wp $N/tools/gd25_anchored.py)" -- "$(Wp $REFP)" "$(Wp $N/r/${T}M_REF_prof_faceL_alpha.png)" "$(Wp $N/data/Ec_cams.json)" "$(H ${T})" $1 $2 $3 2.0 2>&1 | grep -vE "^Blender|^Read|^$|^anchors| t  " | awk '{printf "z%s %s %+.2f |", $2, $4, $5; if (NR%6==0) print ""}'; echo; done
for zz in "lips 270 320 35 100" "tip 220 275 25 95" "chin 300 365 40 115"; do set -- $zz; "$B" -b --factory-startup --python "$(Wp $N/tools/_prof_rows_zoom.py)" -- "$(Wp $N/r/_zoom_${1}_${T}.jpg)" $2 $3 $4 $5 "$(Wp $REFP)" "GD24clay=$(Wp $P/r/G24PM_REF_prof_faceL_clayA.png)" "${T}clay=$(Wp $N/r/${T}M_REF_prof_faceL_clayA.png)" 2>&1 | grep -cE "ZOOM_OK" | tr '\n' ' '; done
CAMS="$(cygpath -m "$(pwd)/$N/data/Ec_cams.json")"; HEAD="$(cygpath -m "$(pwd)/$N/data/head_${T}.npy")"; OUTD="$(cygpath -m "$(pwd)/$N/r")"
echo "[{\"cams\": \"$CAMS\", \"head\": \"$HEAD\", \"cam\": \"CAM_REF_front\", \"variant\": \"clay\", \"lights\": \"A\", \"scale\": 4.0, \"body\": false, \"out\": \"$OUTD/${T}_front4x_clayA.png\"},{\"cams\": \"$CAMS\", \"head\": \"$HEAD\", \"cam\": \"CAM_REF_q3_faceL\", \"variant\": \"clay\", \"lights\": \"B\", \"scale\": 4.0, \"body\": false, \"out\": \"$OUTD/${T}_q3L4x_clayB.png\"}]" > $N/r/_jobs_4x_${T}.json
"$B" -b "$(Wp $O/GD13_scene.blend)" --python "$(Wp $O/tools/gd13_render.py)" -- "$(Wp $N/r/_jobs_4x_${T}.json)" 2>&1 | grep -c RENDERED | tr '\n' ' '
"$B" -b --factory-startup --python "$(Wp $N/tools/_mouth_strip.py)" -- "$(Wp $N/r/_mouth_clay4x_REF_GD24_${T}.jpg)" "$(Wp $REFF)" "$(Wp $P/r/G24D4_front4x_clayA.png)" "$(Wp $N/r/${T}_front4x_clayA.png)" 2>&1 | grep -cE "STRIP_OK" | tr '\n' ' '
"$B" -b --factory-startup --python "$(Wp $N/tools/_nose8x.py)" -- "$(Wp $N/r/_nose8x_REF_GD24_${T}.jpg)" "$(Wp $REFF)" "$(Wp $P/r/G24D4_front4x_clayA.png)" "$(Wp $N/r/${T}_front4x_clayA.png)" 2>&1 | grep -cE "STRIP_OK"
echo BUILD_${T}_DONE
