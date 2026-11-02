#!/bin/bash
# run248_d.sh : V2.48 chain D = V2.41 curve check/restore on the turn copies, hold-release patch, verify, A/B at 60 (deterministic turn case) +
# captures, real time x4, 30 FPS regressions
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TB248_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v248 bash $RUN $REQ/curveprobe_req.py v248curveprobe 300 | grep -a 'CURVEPROBE248' > $D/data/curveprobe.out
echo "[curveprobe] $(cut -c1-700 $D/data/curveprobe.out)" >> $O
J=/Game/GraceRanger/SHME/Animations/Starts/Jog; CL=""; for s in L R; do for d in 090 135 180; do CL="$CL $J/SHM_JogQ_af_Loco_Jog_Start_Turn$s${d}_${s}foot_AAMS"; done; done
if ! grep -q "SHM241_SYaw" $D/data/curveprobe.out || [ "$(grep -o 'SHM241_SYaw' $D/data/curveprobe.out | wc -l)" -lt 7 ]; then
  "$PY" Tools/SHME_V233_20261027/manifest233.py v248_syaw --assets $CL | tail -1 | cut -c1-120 >> $O
  echo "[syaw restore] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_syaw.json bash $RUN $REQ/syaw_req.py v248syaw 600 | grep -a 'SY241\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | cut -c1-500)" >> $O
  SHME_KIND=measure SHME_OWNER=v248 bash $RUN $REQ/curveprobe_req.py v248curveprobe2 300 | grep -a 'CURVEPROBE248' > $D/data/curveprobe2.out
  echo "[curveprobe2] $(cut -c1-700 $D/data/curveprobe2.out)" >> $O
fi
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp3 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp3.json bash $RUN $REQ/turnbind2_req.py v248turnbind2 900 | grep -a 'TURNBIND248B\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-700)" >> $O
grep -a "turnbind2\]" $O | grep -q '"saved": true' || { echo "BIND2_ABORT install not saved" >> $O; exit 1; }
echo "[verify3] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify3 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-500)" >> $O
relaunch tc60 60; WARM=1 ab tc60 "j45_sl:ts j45_sl:ts:2 j45_sl:o jstart:o"
CAP_START=9.3 CAP_SECS=3.2 ab tccap "j45_sl:tsS j45_sl:tsD j45_sl:oS j45_sl:oD" $D/vars248_cap.sh
relaunch tcreal real; WARM=1 ab tcreal "j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:ts:4 j45_sl:o j45_sl:o:2 jstart:ts taps:ts wstart:ts"
relaunch tc30 30; WARM=1 ab tc30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts"
echo TC248_DONE >> $O
