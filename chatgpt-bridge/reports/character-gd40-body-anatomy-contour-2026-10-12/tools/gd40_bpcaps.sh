#!/bin/bash
# gd38_bpcaps.sh (copy of gd33_bpcaps.sh) (from gd32_caps.sh; every case plays the BP rest pose AS_GD33_Rest_lid60 at 0.5 s like the Blueprint face) <label> <sets> : captures of the SAVED evaluation level (ue_gd32_evalqa.py must have run in this editor session) with the standard
# lookdev harness (Tools/CharacterLookdev_20260930/ue_lk_capture.py). Sets (hair always on, real materials):
#   refS / refF = the 4 solved reference cameras (GD31 data/uecams.json), studio / front light, warped onto the 2x panel frame (ue/<label>_<set>_<view>.png)
#   hs  = the level's head-and-shoulders turnaround cameras CAM_HS_* (fov 24, studio)   body = CAM_BODY_* full-body cameras (fov 15.5, studio)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L=$1; SETS=${2:-refS,hs,body}; W=Saved/Codex/GD40_Body_20261012; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; C=Saved/Codex/CharacterLookdev_20260930/captures; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
run() { "$PY" -c "import json; U=json.load(open('$W/data/uecams.json')); K=json.load(open('$W/data/assembly_check.json'))['cameras']; FA='/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011/Face/AS_GD33_Rest_lid60'; S=$2; json.dump({'label':'$1','cases':S}, open('$C/capture_request.json','w'), indent=1)"; rm -f "$C/$1_results.json" "$C/$1_error.txt"
  bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_lk_capture.py")" lk-cap 120 | tail -1 >/dev/null
  for i in $(seq 1 900); do [ -f "$C/$1_results.json" ] || [ -f "$C/$1_error.txt" ] && break; sleep 2; done
  [ -f "$C/$1_error.txt" ] && { echo "ERROR $1"; head -c 600 "$C/$1_error.txt"; } || { [ -f "$C/$1_results.json" ] && echo "DONE $1" || echo "TIMEOUT $1"; }; }
for s in ${SETS//,/ }; do case $s in
  refS) run ${L}_refS "[dict(name='${L}_refS_'+v, view='custom', cam=c['cam'], fov=U['fov'], garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=161, hide=[], face_anim=FA, face_time=0.5) for v, c in U['ref'].items()]";;
  refF) run ${L}_refF "[dict(name='${L}_refF_'+v, view='custom', cam=c['cam'], fov=U['fov'], garments=True, materials='real', light='front', animation=None, time=0, light_target_z=161, hide=[], face_anim=FA, face_time=0.5) for v, c in U['ref'].items()]";;
  hs) run ${L}_hs "[dict(name='${L}_hs_'+k[7:], view='custom', cam=c[:5], fov=c[5], garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=161, hide=[], face_anim=FA, face_time=0.5) for k, c in K.items() if k.startswith('CAM_HS_')]";;
  body) run ${L}_body "[dict(name='${L}_body_'+k[9:], view='custom', cam=c[:5], fov=c[5], garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=105, hide=[], face_anim=FA, face_time=0.5) for k, c in K.items() if k.startswith('CAM_BODY_')]";;
esac; done
mkdir -p $W/ue
for s in ${SETS//,/ }; do case $s in
  refS|refF) for v in front q3_faceR q3_faceL prof_faceL; do f=$C/${L}_${s}_${v}_custom.png; [ -f $f ] || continue
      "$B" -b --factory-startup --python "$(Wp $W/tools/gd38_warp.py)" -- "$(Wp $W/data/uecams.json)" $v 2 "$(Wp $f)" "$(Wp $W/ue/${L}_${s}_${v}.png)" 2>&1 | grep -c WARPED >/dev/null
      cp "$f" $W/ue/ && cmp -s "$f" "$W/ue/$(basename $f)" && rm -f "$f"; done;;
  hs|body) for f in $C/${L}_${s}_*_custom.png; do [ -f "$f" ] || continue; cp "$f" $W/ue/ && cmp -s "$f" "$W/ue/$(basename "$f")" && rm -f "$f"; done;;
esac; done
echo CAPS_DONE $L
