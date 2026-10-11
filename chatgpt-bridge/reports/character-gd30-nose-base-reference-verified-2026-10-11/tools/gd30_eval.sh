#!/bin/bash
# gd30_eval.sh <TAG> : reference verification of a GD30 nose-base candidate data/head_<TAG>.npy (pre-rig, Blender clay in the solved cameras):
# geometry checks (folds / flips / area ratio vs E), clay+alpha renders in the 4 reference cameras, valley-line comparison REF | GD28 | TAG with
# probe positions in every view (profile anchored on tip + subnasale), and REF | GD28 | TAG clay zooms.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; V=Saved/Codex/GD30_Identity_20261011; N=Saved/Codex/GD28_Identity_20261011; G=Saved/Codex/GD13_Identity_20261009
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; T=$1; H() { echo "$(Wp $V/data/head_$1.npy)"; }; REF=SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_checks.py)" -- "$(H $T)" "$(Wp $V/data/checks_$T.json)" "$(H E)" "$(H G28S)" 2>&1 | grep -E "^CHECKS" | grep -o '"folds": [0-9]*\|"area_ratio_min": [0-9.]*\|"flipped_tris_vs_base": [0-9]*' | paste -sd' '
"$B" -b --factory-startup --python "$(Wp $V/tools/_flips.py)" -- "$(Wp $V/data/head_topo.npz)" "$(H E)" "$(H $T)" 2>&1 | grep FLIPS | cut -c1-200
"$B" -b --factory-startup --python "$(Wp $V/tools/gd30_foldloc.py)" -- "$(H $T)" "$(H E)" "$(Wp $V/data/head_topo.npz)" 2>&1 | grep -E "area ratio" | head -2
bash $V/tools/gd30_rset.sh $V/data/head_$T.npy ${T}M $V/data/Ec_cams.json REF_prof_faceL:clay:A REF_front:clay:A REF_q3_faceL:clay:A REF_q3_faceR:clay:A >/dev/null 2>&1
vc() { local v=$1 roi=$2 S=$3 mm=$4 pr=$5; "$B" -b --factory-startup --python "$(Wp $V/tools/gd30_valcmp.py)" -- "$(Wp $V/r/_vc_${v}_$T.jpg)" "$(Wp ${REF}_$v.png)" $roi $S 0.8 $mm "$pr" "GD28=$(Wp $N/r/G28SM_REF_${v}_clayA.png)|$(Wp $N/r/G28SM_REF_${v}_alpha.png)" "$T=$(Wp $V/r/${T}M_REF_${v}_clayA.png)|$(Wp $V/r/${T}M_REF_${v}_alpha.png)" 2>&1 | grep -vE "^Blender|^Read|^$|VALCMP_OK|^ANCHOR"; }
echo "== profile (anchored tip+sn)"; GD30_ANCHOR=prof vc prof_faceL 38,98,228,272 9 0.65 "nostrilBand:col:55-70:247-258;lobBottomBack:col:74-86:253-266;backCreaseTop:row:236-249:66-96;creaseMid:row:244-254:66-96"
echo "== front"; vc front 215,290,250,295 7 0.62 "nosL:col:246-254:264-279;nosR:col:271-278:264-279;lobBotL:col:244-251:277-292;lobBotR:col:274-280:277-292;lobSideL:row:262-276:228-242"
echo "== q3_faceR"; vc q3_faceR 320,410,225,295 7 0.65 "lobBotQR:col:350-372:276-290;nosQR:col:358-378:264-278;tipBotQR:col:378-392:268-290"
echo "== q3_faceL"; vc q3_faceL 90,180,225,295 7 0.64 "lobBotQL:col:140-154:270-288;nosQL:col:122-140:262-278;tipBotQL:col:108-120:262-284"
for z in "q3_faceL 215 300 80 180" "q3_faceR 215 300 320 420" "prof_faceL 232 272 38 100" "front 250 300 200 285"; do set -- $z
"$B" -b --factory-startup --python "$(Wp $V/tools/_prof_rows_zoom.py)" -- "$(Wp $V/r/_cmp_${1}_$T.jpg)" $2 $3 $4 $5 "$(Wp ${REF}_$1.png)" "GD28=$(Wp $N/r/G28SM_REF_${1}_clayA.png)" "$T=$(Wp $V/r/${T}M_REF_${1}_clayA.png)" 2>&1 | grep -c ZOOM_OK | tr '\n' ' '; done; echo; echo EVAL30_${T}_DONE
