#!/bin/bash
# seqF20.sh (2026-11-20): final evidence from the SAVED state only (no runtime overrides). Movetest map: shoulder videos (3 angles,
# same VSIDE as 2026-11-19 B_final_*), full-body stop video (same plan/camera as L_stops_after), stop set 60/30/variable data,
# shoulder data, turn sets. House map: tight-passage camera video + data, full flow (fin19) with loadfire/emptyfire.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
for part in ${PARTS:-shoulder stops data house}; do case $part in
 shoulder) bash Tools/UE59_20261119/seqB.sh m21 pass | grep -c SLOT;;
 stops) echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
   SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
   SP="[('',1.5,0),('W',3.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('W LeftShift',2.0,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.25,360),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0)]"
   VSHOT=1 VSIDE="(450,90,95,95,'pelvis')" bash Tools/UE59_20261118/run2.sh L_stops_m21 -6000 2000 92 0 "$SP" "pass" | grep -c SLOT;;
 data) VS="V0 VAR" HZ="60" TAG=f bash Tools/UE59_20261119/seqR.sh | grep -c SLOT; VS="V0" HZ="30" TAG=f bash Tools/UE59_20261119/seqR.sh | grep -c SLOT
   VS=base DS="2 10" bash Tools/UE59_20261119/seqW.sh | tail -1; S=f bash Tools/UE59_20261119/seqA.sh | tail -1
   TS="W J" bash Tools/UE59_20261119/seqH.sh f | tail -1;;
 house) echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
   VSHOT=1 bash Tools/UE59_20261118/run2.sh C_cam_video 880 -150 210 100 "$(grep '^P=' Tools/UE59_20261119/seqJ.sh | sed 's/^P=//; s/^"//; s/"$//')" "pass" | grep -c SLOT
   VSHOT=1 bash Tools/UE59_20261119/fin19.sh F20 pieces flow loadfire emptyfire | tail -3;;
esac; echo "PART_DONE $part"; done
echo SEQF20_DONE
