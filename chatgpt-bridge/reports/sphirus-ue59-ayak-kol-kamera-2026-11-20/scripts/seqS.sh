#!/bin/bash
# seqS.sh: sun VSM resolution bias A/B stills + motion (player camera, real-speed 30 Hz video), saved state, house map.
#  per spot: 3 s standing (bias -1.5 for 1.5 s, then 0) then 3 s walking (-1.5, then 0). Same camera, position, light, render size.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
H="exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/hk_shadowab.py',encoding='utf8').read())"
P="[('',3.0,0,-10),('W',3.0,0,-10)]"
for s in ${SP:-trail face interior}; do case $s in
 trail)    VSHOT=1 bash Tools/UE59_20261118/run2.sh S_trail 2640 420 322 -83 "$P" "$H" | grep -c SLOT_OK;;
 face)     VSHOT=1 bash Tools/UE59_20261118/run2.sh S_face 2640 420 322 -83 "[('',1.0,150,-5),('',3.0,0,-5)]" "$H" | grep -c SLOT_OK;;
 interior) VSHOT=1 bash Tools/UE59_20261118/run2.sh S_interior 520 160 241 180 "$P" "$H" | grep -c SLOT_OK;;
esac; done
echo "import unreal as u; u.SystemLibrary.execute_console_command(None,'r.Shadow.Virtual.ResolutionLodBiasDirectional 0'); print('SBV', u.SystemLibrary.get_console_variable_float_value('r.Shadow.Virtual.ResolutionLodBiasDirectional'))" > Saved/UE59Work/cv_sb0.py
SHME_OWNER=emb SHME_KIND=measure bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Saved/UE59Work/cv_sb0.py" cv_sb0 60 2>&1 | grep SBV
echo SEQS_DONE
