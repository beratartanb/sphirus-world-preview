#!/bin/bash
# seq13.sh: 60 Hz fixed-step video pair (diagnostic side camera) so the video matches the 60 Hz data step of T12.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
R=/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases
CMA="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
CHS="exec(open(u.Paths.project_dir()+'Tools/UE59_20261118b/ch_set.py',encoding='utf8').read())"
BEF="import builtins; builtins.VID_FPS=60.0; builtins.CH_EDGES=(170,400); $CHS; builtins.CM_ADD={'$R/Relaxed/PSD_Relaxed_Stand_Run_Stops':'$R/Dense/PSD_Dense_Stand_Run_Stops','$R/Relaxed/PSD_Relaxed_Stand_Walk_Stops':'$R/Dense/PSD_Dense_Stand_Walk_Stops'}; $CMA"
AFT="import builtins; builtins.VID_FPS=60.0; builtins.CH_EDGES=(200,440); $CHS"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
P="[('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift',3.3,0),('',2.5,0),('W',3.0,0),('',2.0,0)]"
export VSIDE="(260,90,20,95,'pelvis')" VSHOT=1 VFPS=60
bash Tools/UE59_20261118/run2.sh V19_jstop60_before -6000 2000 92 0 "$P" "$BEF"
bash Tools/UE59_20261118/run2.sh V19_jstop60_after -6000 2000 92 0 "$P" "$AFT"
unset VSIDE VSHOT VFPS
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118b/ch_saved.py" emb_probe 60 2>&1 | grep CHSET
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261118/dirty.py" emb_probe 60 2>&1 | grep DIRTY
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
echo SEQ13_DONE
