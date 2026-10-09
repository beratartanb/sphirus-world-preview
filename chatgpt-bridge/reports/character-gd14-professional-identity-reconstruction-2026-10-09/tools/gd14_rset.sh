#!/bin/bash
# gd14_rset.sh = gd13_rset.sh with all outputs in GD14_Identity_20261009/r (GD13 scene + render tools read-only)
# gd13_rset.sh <head.npy> <label> <cams.json|-> [views...] : renders GD13 views of a head (default: the 4 solved reference cameras, clay A + alpha) + overlays
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; N=Saved/Codex/GD14_Identity_20261009; H=$1; L=$2; CJ=$3; shift 3; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
SET=${*:-"REF_front:clay:A REF_q3_faceR:clay:A REF_q3_faceL:clay:A REF_prof_faceL:clay:A"}
CC=""; [ "$CJ" != "-" ] && CC="\"cams\": \"$(cygpath -m "$(pwd)/$CJ")\", "
J="["; for s in $SET; do IFS=: read c v l <<< "$s"; p=$(cygpath -m "$(pwd)/$N/r/${L}_${c}_${v}${l}.png"); pa=$(cygpath -m "$(pwd)/$N/r/${L}_${c}_alpha.png"); hp=$(cygpath -m "$(pwd)/$H")
J="$J{$CC\"head\": \"$hp\", \"cam\": \"CAM_$c\", \"variant\": \"$v\", \"lights\": \"$l\", \"out\": \"$p\"},"
[[ $c == REF_* ]] && J="$J{$CC\"head\": \"$hp\", \"cam\": \"CAM_$c\", \"variant\": \"clay\", \"lights\": \"A\", \"alpha\": true, \"body\": false, \"out\": \"$pa\"},"; done; J="${J%,}]"
echo "$J" > $N/r/_jobs_$L.json
"$B" -b "$(Wp $O/GD13_scene.blend)" --python "$(Wp $O/tools/gd13_render.py)" -- "$(Wp $N/r/_jobs_$L.json)" 2>&1 | grep -c RENDERED
for s in $SET; do IFS=: read c v l <<< "$s"; [[ $c == REF_* ]] || continue; vw=${c#REF_}
"$B" -b --factory-startup --python "$(Wp $O/tools/gd13_overlay.py)" -- "$(Wp SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_$vw.png)" "$(Wp $N/r/${L}_${c}_${v}${l}.png)" "$(Wp $N/r/${L}_${c}_alpha.png)" "$(Wp $N/r/OV_${L}_${vw}_${v}${l}.jpg)" 2>&1 | grep -c OVL_OK; done
