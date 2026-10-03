#!/bin/bash
# gd10_review.sh <round tag> <head npy> [<compare npy> (default head_G)] : sculpt-review sheet REF | CURRENT (G) | NEW for front / 3/4 / profile
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; R=$1; H=$2; K=Saved/Codex/CharacterGuardian12_20261003; CMP=${3:-$K/head_G.npy}; P=$K/pv; T=Tools/CharacterLookdev_20260930
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; TD=Saved/Codex/CharacterIdentity_20260930/track; RB=Saved/Codex/CharacterGuardian2_20261001/refB
cp $H $P/new_$R.npy; cp $CMP $P/cur_$R.npy
EXTRA_VIEWS=1 "$B" -b --factory-startup --python $T/blender_gd_preview.py -- $P/r Saved/Codex/CharacterGuardian_20261001/semantic_j.json $P/cur_$R.npy $P/new_$R.npy 2>&1 | grep -c PREVIEW_OK >/dev/null
for v in front close; do ref=$TD/ref_front_x4.png; [ $v = close ] && ref=$TD/ref_close_x2.png
  for w in cur new; do "$B" -b --factory-startup --python $T/blender_gd10_blend.py -- $P/rb_${w}_${R}_$v.png $ref $P/r_${w}_${R}_${v}_clay.png 0.5 2>&1 | grep -c BLEND_OK >/dev/null; done; done
CROP=120,900,120,680 "$B" -b --factory-startup --python $T/blender_gd_row.py -- $P/RV_${R}_front.png 460 $TD/ref_front_x4.png $P/r_cur_${R}_front_clay.png $P/r_new_${R}_front_clay.png $P/rb_cur_${R}_front.png $P/rb_new_${R}_front.png 2>&1 | grep -c Trace >/dev/null
CROP=200,900,250,794 "$B" -b --factory-startup --python $T/blender_gd_row.py -- $P/RV_${R}_3q.png 460 $TD/ref_close_x2.png $P/r_cur_${R}_close_clay.png $P/r_new_${R}_close_clay.png $P/rb_cur_${R}_close.png $P/rb_new_${R}_close.png 2>&1 | grep -c Trace >/dev/null
"$B" -b --factory-startup --python $T/blender_gd_row.py -- $P/RV_${R}_side.png 460 $RB/turnaround_p5.png $P/r_cur_${R}_side_clay.png $P/r_new_${R}_side_clay.png 2>&1 | grep -c Trace >/dev/null
echo REVIEW_DONE $R
