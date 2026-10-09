#!/bin/bash
# gd16_measnose.sh <tag> [<tag> ...] : fixed-camera measurement dump (gd13_fit iters 0, cam_iters 0) of data/head_<tag>.npy + nose profile lines vs REF / G15 + fold scan
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD16_Identity_20261010; S=Saved/Codex/GD15_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
ARGS=("G15=$(Wp $S/meas/g15_postrig_dumpF.json)")
for t in "$@"; do cp $W/data/head_$t.npy $W/meas/${t}_in.npy; "$B" -b --factory-startup --python "$(Wp $G/tools/gd13_fit.py)" -- "$(Wp $W/meas/${t}_in.npy)" "$(Wp $W/data/Ec_cams.json)" "$(Wp $W/meas/$t)" '{"iters": 0, "dump": 1, "cam_iters": 0}' > $W/meas/$t.log 2>&1; ARGS+=("$t=$(Wp $W/meas/${t}_dumpF.json)"); done
L=$(echo "$*" | tr ' ' '_'); "$B" -b --factory-startup --python "$(Wp $W/tools/gd16_profline.py)" -- "$(Wp SourceAssets/Characters/GD13_IdentityMaster_20261009/references/GD13_REF_panel_prof_faceL.png)" "$(Wp $W/r/PL_$L.jpg)" "$(Wp $W/meas/profline_$L.json)" "${ARGS[@]}" 2>&1 | grep -E "^PROFLINE " | cut -c1-330
for t in "$@"; do echo -n "$t "; "$B" -b --factory-startup --python "$(Wp $W/tools/gd16_foldloc.py)" -- "$(Wp $W/data/head_$t.npy)" "$(Wp $W/data/head_E.npy)" "$(Wp $W/data/head_topo.npz)" 2>&1 | grep -E "^folds"; done
