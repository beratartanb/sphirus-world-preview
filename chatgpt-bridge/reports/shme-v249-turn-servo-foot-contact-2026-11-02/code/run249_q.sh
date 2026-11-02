#!/bin/bash
# run249_q.sh : V2.49 chain Q = FootPlacement yields while the servo owns the turning start (install249_fpoff.py, knob SHM249_FPOff 0),
# then A/B rmF (knob 1) vs the promoted production at 60 / 30 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until grep -q TM249_DONE $O && [ -f $D/data/GO_Q ]; do sleep 20; done
relaunch q0 60
if [ -f $D/data/BIAS ]; then "$PY" Tools/SHME_V233_20261027/manifest233.py v249_t2bias2 --assets /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_L /Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_R | tail -1 | cut -c1-120 >> $O; echo "[t2bias2] $(SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_t2bias2.json bash $RUN $REQ/t2bias2_req.py v249t2bias2 600 | grep -aE "T2BIAS249|REFUSED|WRITE_GUARD|Error|Traceback" | cut -c1-300)" >> $O; fi
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_fpoff --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_fpoff.json bash $RUN $REQ/fpoff_req.py v249fpoff 900 | grep -a 'FPOFF249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' > $D/data/fpoff_install.out
echo "[fpoff] $(cut -c1-500 $D/data/fpoff_install.out)" >> $O
grep -q '"saved": true' $D/data/fpoff_install.out || { echo "FPOFF_ABORT" >> $O; exit 1; }
relaunch q60 60; WARM=1 ab q60 "j45_sl2:rmF jstart:rmF w43_idle:rmF taps:rmF j45_sl2:oFP"
CAP_START=9.3 CAP_SECS=3.4 ab qcap "j45_sl2:rmFG j45_sl2:rmFD j45_sl2:rmFS j45_sl2:oD j45_sl2:oG" $D/vars249_cap.sh
relaunch q30 30; WARM=1 ab q30 "j45_sl2:rmF jstart:rmF taps:rmF wstart:rmF j41_rl_p10:rmF j40_rlw:rmF gait:rmF"
relaunch qreal real; WARM=1 ab qreal "j45_sl2:rmF j45_sl2:rmF:2 j45_sl2:rmF:3 j45_sl2:rmF:4 jstart:rmF"
echo TQ249_DONE >> $O
