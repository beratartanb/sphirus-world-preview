# final5.sh <stage> : round-5 final verification on the saved + reopened state. Stages: slide | posture | contact | terrain | house | video | perf
# Results: Saved/UE59Work/r5/final5_<stage>.txt (+ recordings under Saved/Codex/Grip_20261106/rec, videos under Saved/Codex/Day_20261107/videos)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; S=$1; O=Saved/UE59Work/r5/final5_$S.txt; : > $O
PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; P=Saved/UE59Work; HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"
rec() { # label plan mode
  if [ $3 = var ]; then HZ=60.0; X="$HKF; builtins.VID_VARDT=(22.0,60.0)"; else HZ=$3.0; X="$HKF"; fi
  DFPS=$HZ bash Tools/UE59_20261120/seqP.sh $1 $P/$2.txt "$X" > /dev/null 2>&1; }
if [ $S = slide ]; then
  for m in 60 30 var; do
    if [ $m = 60 ]; then L="A:planU_A B:planU_B S:planSt2 Q:planQt K:planK1 T:planT1 C:planC1 W:planC2 D:planDm P:planSp R:planR1"; elif [ $m = 30 ]; then L="A:planU_A B:planU_B S:planSt2 K:planK1 C:planC1 W:planC2"; else L="A:planU_A C:planC1 W:planC2"; fi
    for p in $L; do l=f5_${p%%:*}_$m; rec $l ${p##*:} $m
      echo "#### $l (${p##*:})" >> $O; "$PY" Tools/UE59_20261122/an_slide3.py $l $P/${p##*:}.txt 10 2>&1 | cut -c1-230 >> $O
      "$PY" Tools/UE59_20261121/an_contw.py $l 6 120 0 2>&1 | head -1 >> $O; "$PY" Tools/UE59_20261121/an_popsum.py $l 2>&1 | tail -2 | cut -c1-230 >> $O
    done; done
  "$PY" Tools/UE59_20261122/an_turn5.py f5_T_60 >> $O 2>&1
fi
if [ $S = posture ]; then
  for m in 60 30 var; do l=f5_L_$m; rec $l planL1 $m; echo "#### $l" >> $O; "$PY" Tools/UE59_20261122/an_carry5.py $l 2>&1 | cut -c1-330 >> $O; done
  rec f5_F_60 planF1 60; echo "#### f5_F_60 (fatigue)" >> $O; "$PY" Tools/UE59_20261122/an_carry5.py f5_F_60 2>&1 | cut -c1-330 >> $O; "$PY" Tools/UE59_20261122/an_fat5.py f5_F_60 >> $O 2>&1
fi
if [ $S = contact ]; then
  bash Saved/UE59Work/r5/ctall.sh f5 > /dev/null 2>&1; cat Saved/UE59Work/r5/ct_f5.txt | grep -v approach >> $O
  CTPOS="-5500 -7000 92 0" bash Saved/UE59Work/r5/ct.sh f5_knee_walk_tired None $P/plan_ct_walk.txt 0.9 > /dev/null 2>&1; "$PY" Tools/UE59_20261122/an_ct.py f5_knee_walk_tired | grep -v approach >> $O
  for sc in "wall_run run -6000 -6000" "knee_walk walk -5500 -7000" "knee_tempo tempo -6000 -7000" "knee_run runlong -6000 -7000"; do set -- $sc
    CTHZ=30.0 CTPOS="$3 $4 92 0" bash Saved/UE59Work/r5/ct.sh f5h30_$1 None $P/plan_ct_$2.txt > /dev/null 2>&1; "$PY" Tools/UE59_20261122/an_ct.py f5h30_$1 | grep -v approach | sed 's/^/30Hz /' >> $O; done
fi
if [ $S = terrain ]; then bash Saved/UE59Work/r5/terr.sh f5 > /dev/null 2>&1; cat Saved/UE59Work/r5/terr_f5.txt >> $O; fi
if [ $S = house ]; then
  export MAP=/Game/GraceRanger/Maps/L_GR_SphirusHouse VSHOT=1 VKEEP=1
  POS="1300 770 585 180" bash Tools/UE59_20261120/seqP.sh f5h_bed $P/planBed.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
  POS="$(cat Saved/UE59Work/r4/maskpos.txt)" bash Tools/UE59_20261120/seqP.sh f5h_mask $P/planMask.txt "$HKF" | grep -E "VIDREC|mp4" >> $O
  unset MAP; VSHOT=1 VKEEP=1 bash Tools/UE59_20261119/fin19.sh R5 flow 2>&1 | tail -3 >> $O; "$PY" Tools/UE59_20261119/an_flow19.py F19_flow_R5 2>&1 | grep -E "^==|CHECK" >> $O
  sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-12 >> $O
fi
if [ $S = video ]; then
  export VSHOT=1 VKEEP=1
  v() { # label plan pos [side-angle]
    if [ -n "$4" ]; then export VSIDE="(600,$4,0,95,'pelvis')"; else unset VSIDE; fi
    POS="$3" bash Tools/UE59_20261120/seqP.sh $1 $P/$2.txt "import builtins; builtins.CT_SCENE=None; builtins.CT_FAT=None; exec(open(u.Paths.project_dir()+'Tools/UE59_20261122/hk_ct.py',encoding='utf8').read())" | grep -E "VIDREC|mp4" >> $O; }
  v f5v_loco_sh planL1 "-6000 2000 92 0"; v f5v_loco_side planL1 "-6000 2000 92 0" 90
  v f5v_turn_sh planT1 "-6000 2000 92 0"; v f5v_cases_sh planC1 "-6000 2000 92 0"; v f5v_cam_sh planC2 "-6000 2000 92 0"
  v f5v_wall_sh plan_ct_run "-6000 -6000 92 0"; v f5v_wall_side plan_ct_run "-6000 -6000 92 0" 90
  v f5v_kneewalk_sh plan_ct_walk "-5500 -7000 92 0"; v f5v_kneewalk_side plan_ct_walk "-5500 -7000 92 0" 90
  v f5v_kneetempo_sh plan_ct_tempo "-6000 -7000 92 0"; v f5v_kneetempo_side plan_ct_tempo "-6000 -7000 92 0" 90
  v f5v_kneerun_sh plan_ct_runlong "-6000 -7000 92 0"; v f5v_kneerun_side plan_ct_runlong "-6000 -7000 92 0" 90
  v f5v_graze_sh plan_ct_graze "-6000 -7500 92 0"; v f5v_graze_back plan_ct_graze "-6000 -7500 92 0" 180
  v f5v_stair_side plan_ct_stair "-6000 -4000 92 0" 90; v f5v_stairrun_side plan_ct_stairrun "-6000 -4000 92 0" 90; v f5v_ramp_side plan_ct_ramp "-6000 -9500 92 0" 90
  v f5v_jump_sh planJ "-6000 2000 92 0"; v f5v_fat_sh planF1 "-6000 2000 92 0"
fi
echo FINAL5_DONE_$S >> $O
