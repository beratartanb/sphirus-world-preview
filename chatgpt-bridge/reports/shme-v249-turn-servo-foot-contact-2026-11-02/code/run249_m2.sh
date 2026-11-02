#!/bin/bash
# run249_m.sh : V2.49 chain M = T2 continuing-pose bias, PROMOTION (turn owner + no timer hold + weighted idle), verify, relaunch,
# clean-session production verification at 60 (+captures S/D/G), real time, 30, 20, 120 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until grep -q TL249_DONE $O && [ -f $D/data/GO_PROMOTE ]; do sleep 20; done
relaunch m0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_t2bias --assets /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_L /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_R | tail -1 | cut -c1-120 >> $O
echo "[t2bias] $(SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_t2bias.json bash $RUN $REQ/t2bias_req.py v249t2bias 600 | grep -a 'T2BIAS249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-300)" >> $O
grep -a "t2bias\]" $O | tail -1 | grep -q 'T2BIAS249' || { echo "BIAS_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_prom --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/SHME/DA_SHM_Response_Default | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_prom.json bash $RUN $REQ/prom_both_req.py v249prom 900 | grep -a 'PROMOTE249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' > $D/data/promote.out
echo "[promote] $(cut -c1-500 $D/data/promote.out)" >> $O
grep -q '"saved": true' $D/data/promote.out || { echo "PROM_ABORT" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify8 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch p60 60; WARM=1 ab p60 "j45_sl2:o jstart:o w43_idle:o taps:o j45_sl:o"
CAP_START=9.3 CAP_SECS=3.4 ab pcap "j45_sl2:oS j45_sl2:oD j45_sl2:oG" $D/vars249_cap.sh
echo TM249_60 >> $O
relaunch preal real; WARM=1 ab preal "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl2:o:4 jstart:o taps:o w43_idle:o j40_rlw:o wstart:o w42_id:o"
relaunch p30 30; WARM=1 ab p30 "j45_sl2:o jstart:o taps:o wstart:o w42_id:o gait:o j41_rl_p10:o j42_lr_p10:o w43_idle:o j40_rlw:o"
relaunch p20 20; WARM=1 ab p20 "j45_sl2:o jstart:o w43_idle:o"
relaunch p120 120; WARM=1 ab p120 "j45_sl2:o jstart:o w43_idle:o"
echo TM249_DONE >> $O
