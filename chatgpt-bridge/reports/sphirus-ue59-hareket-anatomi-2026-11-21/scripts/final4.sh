# final4.sh: reopened-state verification, round 4 (run after an editor relaunch; lock owner emb)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
HKF="$(cat Saved/UE59Work/r4/hkp2_line.txt)"; O=Saved/UE59Work/r4/final4.txt; : > $O
tomap(){ echo "$1" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 300 2>&1 | tail -1 >> $O; }
tomap /Game/Sphirus/Test/L_Sph_MoveTest
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh f4_warm Saved/UE59Work/planV1.txt "$HKF" | grep VIDREC >> $O
# 1 posture / carriage (60 Hz)
DFPS=60.0 bash Tools/UE59_20261120/seqP.sh f4_L_60 Saved/UE59Work/planL1.txt "$HKF" | grep VIDREC >> $O
echo "#### carriage f4_L_60" >> $O; "$PY" Tools/UE59_20261121/an_body4.py f4_L_60 | grep -E "^s|vis" >> $O
# 2 slide / continuity regression
bash Saved/UE59Work/r4/reg.sh f4 "60 30 var" "A:planU_A B:planU_B S:planSt2 Q:planQt R:planR1 K:planK1"
cat Saved/UE59Work/r4/reg_f4.txt >> $O
echo STAGE_A_DONE >> $O
# 3 videos, normal shoulder camera (30 Hz step = real speed)
export VSHOT=1
bash Tools/UE59_20261120/seqP.sh f4v_gaits Saved/UE59Work/planV1.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
bash Tools/UE59_20261120/seqP.sh f4v_turns Saved/UE59Work/planU_A.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
bash Tools/UE59_20261120/seqP.sh f4v_back Saved/UE59Work/planK1.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
for v in side:90 back:180; do VSIDE="(600,${v##*:},0,95,'pelvis')" bash Tools/UE59_20261120/seqP.sh f4v_${v%%:*} Saved/UE59Work/planV1.txt "$HKF" | grep -E "VIDREC|mp4" >> $O; done
unset VSHOT
echo STAGE_B_DONE >> $O
# 4 house
export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse VSHOT=1 VKEEP=1
POS="1300 770 585 180" bash Tools/UE59_20261120/seqP.sh f4h_bed Saved/UE59Work/planBed.txt "$HKF" | grep -E "VIDREC|mp4|LOADED" >> $O
POS="$(cat Saved/UE59Work/r4/maskpos.txt)" bash Tools/UE59_20261120/seqP.sh f4h_mask Saved/UE59Work/planMask.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
unset MAP VKEEP
VSHOT=1 VKEEP=1 bash Tools/UE59_20261119/fin19.sh R4 flow 2>&1 | tail -3 >> $O; "$PY" Tools/UE59_20261119/an_flow19.py F19_flow_R4 2>&1 | grep -E "^==|CHECK" >> $O
echo FINAL4_DONE >> $O
