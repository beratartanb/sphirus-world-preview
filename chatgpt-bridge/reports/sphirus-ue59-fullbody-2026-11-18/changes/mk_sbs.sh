#!/bin/bash
# mk_sbs.sh: side-by-side before|after videos for the report (Blender sbs.py), copies singles too
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; V=Saved/Codex/Day_20261107/videos; O=chatgpt-bridge/reports/sphirus-ue59-fullbody-2026-11-18/videos; mkdir -p $O
W(){ cygpath -m "$PWD/$1"; }
for p in ${SBS:-slope_pc slopediag lightpatch lightexit}; do
  [ -f $V/V18_${p}_before.mp4 ] && [ -f $V/V18_${p}_after.mp4 ] || { echo "MISSING $p"; continue; }
  BLWAIT=900 bash Tools/Bio_20261115/bl.sh "$PWD/$O/${p}_before_left_after_right.mp4" --background --factory-startup --python "$(W Tools/UE59_20261116/sbs.py)" -- "$(W $O/${p}_before_left_after_right.mp4)" "$(W $V/V18_${p}_before.mp4)" "$(W $V/V18_${p}_after.mp4)" | tail -1
done
for s in flow_A; do [ -f $V/V18_$s.mp4 ] && cp $V/V18_$s.mp4 $O/$s.mp4; [ -f $V/W18_$s.mp4 ] && cp $V/W18_$s.mp4 $O/$s.mp4; done
ls -la $O
