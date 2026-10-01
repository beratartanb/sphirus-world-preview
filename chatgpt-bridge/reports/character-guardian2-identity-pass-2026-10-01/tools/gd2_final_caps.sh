#!/bin/bash
# gd2_final_caps.sh <face tag> <hair tag> <skin> <stem> : GUARDIAN-2 final evidence batch on the final composition (face gate sets + hair + rig + reference
# expression; garment sets henley / shorts / waist / neck / sleeve / full / seam / lod via cr_run_tests.sh). Captures prefix <stem>f / <stem>_<set>.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; HT=$2; SK=$3; S=$4; T=Tools/CharacterLookdev_20260930
NOCYCLE=1 HAIR=g2:$HT SKIN=$SK SETS=clay,real,hair,rig,expr bash $T/gd2_face_run.sh $TAG
for c in Saved/Codex/CharacterLookdev_20260930/captures/g2${TAG}_*; do b=$(basename $c); cp "$c" "Saved/Codex/CharacterLookdev_20260930/captures/${S}f_${b#g2${TAG}_}"; done
bash $T/gd2_frames.sh ${S}f "clay real hair"; bash $T/gd2_expr_frames.sh ${S}f
for set in henley shorts waist neck sleeve full seam lod; do bash $T/cr_run_tests.sh ${S}_$set $set setup; done
echo GD2_FINAL_CAPS_DONE $S
