#!/bin/bash
# gd14_track.sh <label> <set> : warp the label's UE captures of <set> onto the 1x reference panel frame (ue1x/) and run the MetaHuman face tracker
# (MetaHumanCharacterEditorSubsystem.track_face_landmarks_from_image; same tracker as the GD13 reference tracks) -> trk/<label>_<set>.json
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; S=$2; W=Saved/Codex/GD14_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009; C=Saved/Codex/CharacterLookdev_20260930/captures; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
IM=""; for v in front q3_faceR q3_faceL prof_faceL; do [ -f $C/${L}_${S}_${v}_custom.png ] || continue
  "$B" -b --factory-startup --python "$(Wp $W/tools/gd14_warp.py)" -- "$(Wp $W/data/uecams.json)" $v 1 "$(Wp $C/${L}_${S}_${v}_custom.png)" "$(Wp $W/ue1x/${L}_${S}_${v}.png)" 2>&1 | grep -c WARPED >/dev/null
  IM="$IM'$v': r'$(Wp $W/ue1x/${L}_${S}_${v}.png)', "; done
{ echo "import builtins; builtins.GD14_TR = {'images': {$IM}, 'out': r'$(Wp $W/trk/${L}_${S}.json)'}"; sed 1d $G/trk/job_track_ref.py; } > $W/jobs/track_${L}_${S}.py
bash Tools/OutfitHome_20260929/run_of.sh $W/jobs/track_${L}_${S}.py gd14-trk-$L 600 | grep -oE "GD14_TR.*|Traceback.*"
