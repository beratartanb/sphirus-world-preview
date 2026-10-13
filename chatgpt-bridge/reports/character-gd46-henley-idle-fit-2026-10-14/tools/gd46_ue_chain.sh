#!/bin/bash
# gd46_ue_chain.sh <stage> [build_dir] [tag] : GD46 garment-fit UE side. Stages:
#   guard   - refuse when an UnrealEditor WITHOUT the automation runner is running (the user's own session: never killed by automation)
#   editor  - memguard start (runner editor)             pose <tag>  - PIE idle-pose dump + 4 camera screenshots (tag = before/after label)
#   build <build_dir> <tag> - SKM_GD46_Henley_<tag> from the settled build dir (isolated GD46 folder, nothing else saved)
#   swap <tag>  - checkpoint3 copies of the 3 pawn Blueprints (hash-verified) then Henley -> SKM_GD46_Henley_<tag> (compile + save)
#   close   - end the runner editor, move PackageRestoreData aside
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD46_GarmentFit_20261013; R=Tools/OutfitHome_20260929/run_of.sh
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; Wp() { cygpath -w "$(pwd)/$1"; }; STAGE=${1:-guard}
guard() {
  local cl; cl=$(powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"name='UnrealEditor.exe'\" | ForEach-Object { \$_.CommandLine }" | tr -d '\r')
  if [ -n "$cl" ] && ! echo "$cl" | grep -q "runner.py"; then echo "USER_EDITOR_OPEN: $cl" | cut -c1-200; return 1; fi
  echo "GUARD_OK ${cl:+(runner editor running)}"; return 0; }
case "$STAGE" in
  guard) guard ;;
  editor) guard || exit 2; bash Saved/Codex/GD38_Identity_20261011/tools/gd38_memguard.sh 22 | tail -1 ;;
  pose) TAG=${2:-before}; { echo "import builtins; builtins.GD46_TAG = 'gd46_$TAG'"; cat $N/jobs/pie_pose_dump.py; } > $N/jobs/_pie_$TAG.py
        MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/_pie_$TAG.py)" gd46-pie-$TAG 900 | grep -oE 'GD46_POSE_DONE.{0,700}|Traceback.*|Error.*' | head -3
        for s in front34 side back front player; do f="Saved/Screenshots/WindowsEditor/gd46_${TAG}_$s.png"; [ -f "$f" ] && mv -f "$f" "$N/data/gd46_${TAG}_$s.png" && echo "shot $s ok" || echo "shot $s MISSING"; done ;;
  build) BD=$2; TAG=$3; { echo "import builtins; builtins.GD46_BUILD = r'$(Wp $BD)'; builtins.GD46_TAG = '$TAG'"; cat $N/jobs/ue_gd46_build_henley.py; } > $N/jobs/_build_$TAG.py
        MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/_build_$TAG.py)" gd46-build-$TAG 1800 | grep -oE 'GD46_BUILD_DONE.{0,900}|Traceback.*|AssertionError.*|rejected.*' | head -4
        ls -la Content/Sphirus/CharacterLab/GD46_GarmentFit_20261013/Outfit/SKM_GD46_Henley_$TAG.uasset 2>/dev/null | awk '{print "asset", $5, "bytes"}' ;;
  swap) TAG=$2; CK=$N/checkpoint_swap_$TAG; mkdir -p "$CK"
        for f in Content/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM.uasset Content/GraceRanger/BP_GR_Player.uasset Content/GraceRanger/Experimental/BodyInertia/BP_PBI_Player.uasset; do
          mkdir -p "$CK/$(dirname $f)"; cp -f "$f" "$CK/$f"; a=$(sha256sum "$f" | cut -c1-16); b=$(sha256sum "$CK/$f" | cut -c1-16); [ "$a" = "$b" ] && echo "checkpoint3 $(basename $f) $a" || { echo "CHECKPOINT_HASH_MISMATCH $f"; exit 3; }; done
        { echo "import builtins; builtins.GD46_HENLEY = '/Game/Sphirus/CharacterLab/GD46_GarmentFit_20261013/Outfit/SKM_GD46_Henley_$TAG'"; cat $N/jobs/swap_henley.py; } > $N/jobs/_swap_$TAG.py
        MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/_swap_$TAG.py)" gd46-swap-$TAG 900 | grep -oE 'GD46_SWAP.{0,900}|Traceback.*|AssertionError.*|KeyError.*' | head -3 ;;
  close) powershell -NoProfile -Command "Stop-Process -Name UnrealEditor -Force -ErrorAction SilentlyContinue; Start-Sleep 8; (Get-Process UnrealEditor -ErrorAction SilentlyContinue | Measure-Object).Count" | tr -d '\r'
         mkdir -p $N/restore_data_aside; f=Saved/Autosaves/PackageRestoreData.json; [ -f "$f" ] && mv "$f" "$N/restore_data_aside/PackageRestoreData_$(date +%H%M%S).json" && echo RESTOREDATA_MOVED || echo NO_RESTOREDATA ;;
  *) echo "unknown stage $STAGE"; exit 1 ;;
esac
