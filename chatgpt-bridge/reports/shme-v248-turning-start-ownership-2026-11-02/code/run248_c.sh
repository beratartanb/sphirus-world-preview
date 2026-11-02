#!/bin/bash
# run248_c.sh : V2.48 chain C = turning-start clip-bound contract (curves on the 6 project turn copies + ABP bind/hold/LS-block) + A/B
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
until grep -q TS248_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v248 bash $RUN $REQ/curves_dry_req.py v248curvesdry 300 | grep -a 'TURNCURVES248\|Error\|Traceback' > $D/data/curves_dry.out
echo "[curves dry] $(cut -c1-1500 $D/data/curves_dry.out)" >> $O
"$PY" - <<'PYEOF' >> $O
import json
s = open('Saved/Codex/SHME_V248_20261102/data/curves_dry.out', encoding='utf8', errors='ignore').read(); d = json.loads(s[s.index('{'):])
bad = [k for k, v in d['clips'].items() if not isinstance(v, dict) or abs(v['root_yaw_total']) < 60]
print('CURVES_PLAN %d clips, bad %s, yaw %s' % (len(d['clips']), bad, {k: v['root_yaw_total'] for k, v in d['clips'].items() if isinstance(v, dict)}))
PYEOF
grep -q "CURVES_PLAN 6 clips, bad \[\]" $O || { echo "CURVES_ABORT root yaw missing" >> $O; exit 1; }
J=/Game/GraceRanger/SHME/Animations/Starts/Jog; CL=""; for s in L R; do for d in 090 135 180; do CL="$CL $J/SHM_JogQ_af_Loco_Jog_Start_Turn$s${d}_${s}foot_AAMS"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_curves --assets $CL | tail -1 | cut -c1-160 >> $O
echo "[curves write] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_curves.json bash $RUN $REQ/curves_write_req.py v248curves 600 | grep -a 'TURNCURVES248\|REFUSED\|WRITE_GUARD\|Error\|Traceback' | grep -o '"saved": [0-9]*\|"dirty".*\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' | tr '\n' ' ' | cut -c1-400)" >> $O
grep -q '"saved": 6' $O || { echo "CURVES_ABORT not saved" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp2 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[turnbind] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp2.json bash $RUN $REQ/turnbind_req.py v248turnbind 900 | grep -a 'TURNBIND248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-900)" >> $O
grep -a "turnbind\]" $O | grep -q '"saved": true' || { echo "BIND_ABORT install not saved" >> $O; exit 1; }
echo "[verify2] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*')" >> $O
relaunch tb30 30; WARM=1 ab tb "j45_sl:ts j45_sl:o"
relaunch tbreal real; WARM=1 ab tbreal "j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:ts:4 jstart:ts taps:ts wstart:ts j45_sl:o"
relaunch tb60 60; WARM=1 ab tb60 "j45_sl:ts j45_sl:ts:2"
echo TB248_DONE >> $O
