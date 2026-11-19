#!/bin/bash
# seqC.sh: tight kitchen passage (seqJ route) camera variants, house map, saved state; data 60 Hz unless VSHOT set. VS="tag:prelude".
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
P="[('',1.0,0,-12),('GOTO',2.0,0,-12,(840,-40,220)),('GOTO',2.0,0,-12,(840,60,240)),('GOTO',2.5,0,-12,(1000,200,245)),('GOTO',1.5,0,-12,(1080,200,245)),('GOTO',2.0,0,-12,(1160,320,245)),('GOTO',4.0,0,-12,(1160,760,245)),('GOTO',2.0,0,-12,(1280,800,245)),('GOTO',1.5,0,-12,(1320,840,245)),('',1.5,0,-12)]"
for v in ${YK:-0 0.6 0.8}; do bash Tools/UE59_20261118/run2.sh C_cam_yk$v${TAG:-} 880 -150 210 100 "$P" "import builtins; builtins.VID_CAM={'TightRaise':45.0,'YKeep':float($v)}" | grep -c SLOT_OK; done
echo SEQC_DONE
