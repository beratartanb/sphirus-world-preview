#!/bin/bash
# run249_e.sh : V2.49 chain E = foot ground-contact repair (22 project start clips) + feed-forward servo, verify, A/B 60 (+captures),
# real time, 30, 20, 120 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
tasklist 2>/dev/null | grep -qi UnrealEditor.exe || relaunch e0 60
"$PY" - <<'PYEOF'
import json
s = open('Saved/Codex/SHME_V249_20261102/data/footfix_dry2.out', encoding='utf8', errors='ignore').read(); d = json.loads(s[s.index('{'):])
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'; V = '/Game/GraceRanger/SHME/Animations/V248/'
paths = [(V if k.startswith('SHM248_') else J) + k for k in d['clips']]
json.dump(paths, open('Saved/Codex/SHME_V249_20261102/data/footfix_clips.json', 'w')); print(len(paths))
PYEOF
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_foot --from $D/data/footfix_clips.json | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_foot.json bash $RUN $REQ/footfix_write_req.py v249footfix 1200 | grep -a 'FOOTFIX249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' > $D/data/footfix_write.out
echo "[footfix] $(grep -o '"saved": [0-9]*\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' $D/data/footfix_write.out | tr '\n' ' ' | cut -c1-300)" >> $O
grep -q '"saved": 22' $D/data/footfix_write.out || { echo "FOOT_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_servo2 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_servo2.json bash $RUN $REQ/servo2_req.py v249servo2 900 | grep -a 'SERVO249B\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' > $D/data/servo2_install.out
echo "[servo2] $(cut -c1-600 $D/data/servo2_install.out)" >> $O
grep -q '"saved": true' $D/data/servo2_install.out || { echo "SERVO2_ABORT" >> $O; exit 1; }
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify3 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch e60 60; WARM=1 ab e60 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o j45_sl:rm"
CAP_START=9.3 CAP_SECS=3.4 ab ecap "j45_sl2:rmS j45_sl2:rmD j45_sl2:oD" $D/vars249_cap.sh
echo TE249_60 >> $O
relaunch ereal real; WARM=1 ab ereal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 j45_sl2:rm:4 j45_sl2:o j45_sl2:o:2 j45_sl:rm jstart:rm jstart:o taps:rm wstart:rm"
relaunch e30 30; WARM=1 ab e30 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o taps:rm wstart:rm w42_id:rm gait:rm j41_rl_p10:rm j42_lr_p10:rm w43_idle:rm"
relaunch e20 20; WARM=1 ab e20 "j45_sl2:rm j45_sl2:o jstart:rm"
relaunch e120 120; WARM=1 ab e120 "j45_sl2:rm j45_sl2:o jstart:rm"
echo TE249_DONE >> $O
