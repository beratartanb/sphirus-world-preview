#!/bin/bash
# gd4_final_caps.sh <face tag> <stem> : GUARDIAN-4 final evidence on the final composition (face SKM_GD6_Face_<tag> + skin $SKIN + eyes e2 + hair $HAIR +
# Henley g17e + Chaos shorts m1): G4 reference-expression sequence, face sets clay/real/hair/rig/expr -> <stem>f_*, garment sets full/neck/seam/lod -> <stem>_<set>_*
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; S=$2; T=Tools/CharacterLookdev_20260930; C=Saved/Codex/CharacterLookdev_20260930/captures
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
K4=Saved/Codex/CharacterGuardian6_20261002
if [ -z "${SKIP_EXPR:-}" ]; then
  { echo "import builtins; builtins.GD3_SEQ_MESH = '/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002/Face/SKM_GD6_Face_$TAG'"; cat $T/ue_gd6_ref_expression.py; } > "$SC/gd4_expr_$TAG.py"
  bash Tools/OutfitHome_20260929/run_of.sh "$SC/gd4_expr_$TAG.py" gd4-expr-$TAG 600 | grep -E "GD6_EXPR|Traceback" | cut -c1-200
fi
GD3_EYES_TAG=e2 SKIN=${SKIN:-g4k3} HAIR=${HAIR:-g4:h1} SETS=${FSETS:-clay,real,hair,rig,expr} RIGJSON=Saved/Codex/CharacterGuardian3_20261001/gd3_face_cases.json EXPRJSON=$K4/gd6_expr_cases.json bash $T/gd6_face_run.sh $TAG | grep -E "COMP4|DONE|ERROR"
for c in $C/g4${TAG}_*; do b=$(basename $c); cp "$c" "$C/${S}f_${b#g4${TAG}_}"; done
bash $T/gd6_frames.sh ${S}f "clay real hair" >/dev/null; bash $T/gd6_expr_frames.sh ${S}f 2>/dev/null | tail -1
for set in ${GSETS:-full neck seam lod}; do bash $T/cr_run_tests.sh ${S}_$set $set setup | grep -E "DONE|ERROR"; done
echo GD6_FINAL_CAPS_DONE $S
