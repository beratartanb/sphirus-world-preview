#!/bin/bash
# gd35_caps.sh <label> <sets> : UE captures of the CURRENT qa composition (gd33_comp.sh) at the 4 solved reference cameras (GD31 data/uecams.json),
# warped onto the 2x panel frame (ue/<label>_<set>_<view>.png). LIGHT=studio|front (default studio).
#   refnh = hair hidden (brow / eye measurement)   ref = with hair
#   rest  = every case of data/rest_cases.json (AS_GD33_RestCalm, RigLogic curves on the face) hair hidden -> ue/<label>_x<case>_refnh_<view>.png
#   resth = the same with hair -> ue/<label>_x<case>_ref_<view>.png   (REST=case1,case2 limits the cases)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; SETS=${2:-refnh,ref}; W=Saved/Codex/GD35_Identity_20261011; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures; LI=${LIGHT:-studio}; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
mkdir -p $W/ue
run() { "$PY" -c "import json; U=json.load(open('$W/data/uecams.json')); import os; X=json.load(open('$W/data/'+os.environ.get('RESTF','rest_cases.json'))); S=$2; json.dump({'label':'$1','cases':S}, open('$C/capture_request.json','w'), indent=1)" || { echo "REQ_FAIL $1"; return 1; }; rm -f "$C/$1_results.json" "$C/$1_error.txt"
  bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
  for i in $(seq 1 900); do { [ -f "$C/$1_results.json" ] || [ -f "$C/$1_error.txt" ]; } && break; sleep 2; done
  [ -f "$C/$1_error.txt" ] && { echo "ERROR $1"; head -c 600 "$C/$1_error.txt"; } || { [ -f "$C/$1_results.json" ] && echo "DONE $1" || echo "TIMEOUT $1"; }; }
warp() { local lab=$1; for v in front q3_faceR q3_faceL prof_faceL; do f=$C/${lab}_${v}_custom.png; [ -f $f ] || continue
  "$B" -b --factory-startup --python "$(Wp $W/tools/gd35_warp.py)" -- "$(Wp $W/data/uecams.json)" $v 2 "$(Wp $f)" "$(Wp $W/ue/${lab}_${v}.png)" 2>&1 | grep -c WARPED >/dev/null
  [ -f $W/ue/${lab}_${v}.png ] && rm -f $f; done; }
case_list() { "$PY" -c "import json,os; r=os.environ.get('REST',''); print(' '.join(c['name'] for c in json.load(open('$W/data/'+os.environ.get('RESTF','rest_cases.json')))['cases'] if not r or c['name'] in r.split(',')))"; }
for s in ${SETS//,/ }; do case $s in
  refnh) run ${L}_refnh "[dict(name='${L}_refnh_'+v, view='custom', cam=c['cam'], fov=U['fov'], garments=True, materials='real', light='$LI', animation=None, time=0, light_target_z=161, hide=['HairMain', 'HairLoose']) for v, c in U['ref'].items()]"; warp ${L}_refnh;;
  ref) run ${L}_ref "[dict(name='${L}_ref_'+v, view='custom', cam=c['cam'], fov=U['fov'], garments=True, materials='real', light='$LI', animation=None, time=0, light_target_z=161, hide=[]) for v, c in U['ref'].items()]"; warp ${L}_ref;;
  rest|resth) H="['HairMain', 'HairLoose']"; SX=refnh; [ $s = resth ] && { H="[]"; SX=ref; }
    for k in $(case_list); do run ${L}_x${k}_$SX "[dict(name='${L}_x${k}_${SX}_'+v, view='custom', cam=c['cam'], fov=U['fov'], garments=True, materials='real', light='$LI', animation=None, time=0, light_target_z=161, hide=$H, face_anim=X['animation'], face_time=[x['time'] for x in X['cases'] if x['name']=='$k'][0]) for v, c in U['ref'].items()]"; warp ${L}_x${k}_$SX; done;;
esac; done
echo CAPS_DONE $L
