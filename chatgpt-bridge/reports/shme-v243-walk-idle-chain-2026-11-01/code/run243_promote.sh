#!/bin/bash
# usage: run243_promote.sh lat|all   (lat = lateral family + settle gate + needs-look only; all = + idle chain idlg3)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
MODE=${1:-lat}
D=Saved/Codex/SHME_V243_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
S=/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad
source $D/lib243.sh
echo "[promote $MODE] start $(date +%H:%M:%S)" >> $O
"$PY" Tools/SHME_V233_20261027/manifest233.py v243_prom_$MODE --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player /Game/GraceRanger/SHME/DA_SHM_Response_Default | tail -1 >> $O
SHME_KIND=write SHME_OWNER=v243 SHME_MANIFEST=$M/v243_prom_$MODE.json bash Tools/SHME_V2_20261014/run_v2.sh $S/v243/promote_${MODE}_req.py v243prom_$MODE 600 | grep -a 'PROMOTE243\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-900 >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v243 bash Tools/SHME_V2_20261014/run_v2.sh $S/v242/verify241_req.py v243verify_$MODE 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
WARM=1 ab prod "j41_rl_p04:o j41_rl_p10:o j42_lr_p10:o w43_idle:o taps:o gait:o w42_id:o jstart:o wdiag:o wstart:o j40_rlw:o"
relaunch f60 60
WARM=1 ab prod60 "j41_rl_p04:o w42_id:o taps:o"
relaunch freal real
WARM=1 ab prodreal "j41_rl_p04:o j41_rl_p04:o:2 j42_lr_p10:o w42_id:o"
relaunch fend 30
echo PROMOTE_DONE >> $O
