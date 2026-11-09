#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
PR=Saved/Codex/Day_20261107/phys_m_progress.txt; : > $PR
log(){ echo "$(date +%H:%M:%S) $*" | tee -a $PR; }
RL(){ for i in 1 2 3; do R=$(bash Tools/Embodied_20261105/relaunch.sh emb_$1$i 2>&1 | tail -1); log "RELAUNCH $R"; [[ "$R" != STOP_* ]] && break; done; }
PLAN="[('',1.0,0),('W',2.5,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.2,0),('W LeftShift',2.5,0),('',2.0,0),('W LeftShift',2.0,0),('S LeftShift',1.5,0),('',1.5,0)]"
P="/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player"
RL 453; log REV2; TAILN=8 CUTN=400 bash Tools/Day_20261107/wjob.sh Tools/Day_20261107/cm_rev2.py rev2 300 --assets $P 2>&1 | tee -a $PR | grep -E "WRITE_END|rror|DONE|CHANGED|RAISED" | cut -c1-200
RL 454; log LAB; bash Tools/Day_20261107/lab.sh P_phys_m test -3000 500 92 0 "$PLAN" 2>&1 | tail -1 | tee -a $PR
PP="[('',0.8,0),('W LeftShift',1.7,0),('',1.8,0),('S',2.0,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.5,0)]"
PC="[('',0.8,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0),('W A',2.0,0),('',0.8,0),('W D',2.0,0),('',0.8,0),('W',1.5,0),('S',2.0,0),('',1.2,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|VIDEO|mp4" | tee -a $PR; }
RL 455; log VID_PH; V PH_phys_shme3 2200 -700 190 180 "$PP"
RL 456; log VID_CL; V CL_strafe_shme3 2200 -700 190 180 "$PC"
RL 457; log VID_B; V B_turns_shme3 1400 -700 190 0 "$PB"
log END
