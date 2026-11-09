#!/bin/bash
# lab.sh <label> <map:house|test> <x> <y> <z> <yaw> <plan> [prelude]: data-only real-time recording (no screenshots, no time
# dilation) with the full telemetry of vid.py -> rec/<label>.json. Used for long idle / gait / camera-framing scenarios.
# The test map (L_Sph_MoveTest) renders black but runs the real pawn, so it is used for long straight runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
. Tools/Grip_20261106/g.sh
LBL=$1; MAP=$2; SV=Saved/SaveGames/SFSaveSlot.sav; O=Saved/Codex/Day_20261107/lab; mkdir -p $O; [ -f $SV ] && cp -p $SV $O/slot_before_$LBL.sav
if [ "$MAP" = "test" ]; then echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep LOADED | cut -c1-100; fi
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
rm -f Saved/Codex/Grip_20261106/rec/$LBL.json
AA; PS; NOTHR; W $([ "$MAP" = "test" ] && echo 8 || echo 16)
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at($3,$4,$5,$6,-12); ${8:-pass}" >/dev/null; W 2
J "import builtins; builtins.VID_NOSHOT=True
exec(open(u.Paths.project_dir()+'Tools/Grip_20261106/gx.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/Day_20261107/vid.py',encoding='utf8').read())
vidrec('$LBL',$7)" measure 1 | grep VIDREC
for i in $(seq 1 150); do W 2; [ -f Saved/Codex/Grip_20261106/rec/$LBL.json ] && break; done
W 1; PE; [ -f $O/slot_before_$LBL.sav ] && cp -p $O/slot_before_$LBL.sav $SV
if [ "$MAP" = "test" ]; then echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep LOADED | cut -c1-100; fi
ls -la Saved/Codex/Grip_20261106/rec/$LBL.json 2>/dev/null | awk '{print $5,$9}'
