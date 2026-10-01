#!/bin/bash
# gd3_final_caps.sh <face tag> <stem> : GUARDIAN-3 final evidence on the final composition (face <tag> + skin g3s1 + eyes e2 + hair g3:id21 + Henley g17e + Chaos shorts m1):
# reference-expression sequence (plugin face skeleton), face sets clay/real/hair/rig/expr -> <stem>f_*, garment sets full/neck/seam/lod/henley/shorts -> <stem>_<set>_*
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; S=$2; T=Tools/CharacterLookdev_20260930; C=Saved/Codex/CharacterLookdev_20260930/captures
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
{ echo "import builtins; builtins.GD3_SEQ_MESH = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Face/SKM_GD3_Face_$TAG'"; cat $T/ue_gd3_ref_expression.py; } > "$SC/gd3_expr_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/gd3_expr_$TAG.py" gd3-expr-$TAG 600 | grep -E "GD3_EXPR|Traceback" | cut -c1-200
GD3_EYES_TAG=e2 SKIN=g3s1 HAIR=g3:id21 SETS=clay,real,hair,rig,expr RIGJSON=Saved/Codex/CharacterGuardian3_20261001/gd3_face_cases.json EXPRJSON=Saved/Codex/CharacterGuardian3_20261001/gd3_expr_cases.json bash $T/gd3_face_run.sh $TAG | grep -E "COMP3|DONE|ERROR"
for c in $C/g3${TAG}_*; do b=$(basename $c); cp "$c" "$C/${S}f_${b#g3${TAG}_}"; done
bash $T/gd3_frames.sh ${S}f "clay real hair" >/dev/null; bash $T/gd3_expr_frames.sh ${S}f | tail -1
for set in full neck seam lod henley shorts; do bash $T/cr_run_tests.sh ${S}_$set $set setup | grep -E "DONE|ERROR"; done
echo GD3_FINAL_CAPS_DONE $S
