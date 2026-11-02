#!/bin/bash
# run248_l.sh : V2.48 chain L = cropped turning-start clips -> T2 databases -> route, verify, A/B 60 (+captures), real time, 30 FPS (+ production pairs)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib248.sh
for i in $(seq 1 60); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe && break; sleep 5; done
V=/Game/GraceRanger/SHME/Animations/V248; CR=""; for s in L R; do for d in 090 135 180; do CR="$CR $V/SHM248_Jog_Start_Turn$s${d}_crop"; done; done
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_crop --new $CR | tail -1 | cut -c1-120 >> $O
echo "[turncrop] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_crop.json bash $RUN $REQ/turncrop_req.py v248turncrop 900 | grep -a 'TURNCROP248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-1200)" >> $O
grep -a "turncrop\]" $O | grep -q '"saved": 6' || { echo "CROP_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_tdb3 --from $D/data/turnstart_clips.json --assets $CR --new $V/PSD_SHM248_JogStartT2_L $V/PSD_SHM248_JogStartT2_R | tail -1 | cut -c1-120 >> $O
echo "[tdb T2] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_tdb3.json bash $RUN $REQ/tdb_t2_req.py v248tdbt2 900 | grep -a 'DB248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | grep -o '"entries": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*\|Assertion.*' | tr '\n' ' ' | cut -c1-1500)" >> $O
grep -a "tdb T2\]" $O | grep -q 'crop' || { echo "TDB3_ABORT" >> $O; exit 1; }
"$PY" Tools/SHME_V233_20261027/manifest233.py v248_abp11 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-120 >> $O
echo "[t2 route] $(SHME_KIND=write SHME_OWNER=v248 SHME_MANIFEST=$M/v248_abp11.json bash $RUN $REQ/t2_req.py v248t2 600 | grep -a 'T2_248\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|Assertion' | cut -c1-500)" >> $O
grep -a "t2 route\]" $O | grep -q '"saved": true' || { echo "T2_ABORT" >> $O; exit 1; }
echo "[verify9] $(SHME_KIND=measure SHME_OWNER=v248 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v248verify9 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch tl60 60; WARM=1 ab tl60 "j45_sl2:ts j45_sl2:o j45_sl:ts"
CAP_START=9.3 CAP_SECS=3.4 ab tlcap "j45_sl2:tsS j45_sl2:tsD j45_sl2:oD" $D/vars248_cap.sh
relaunch tlreal real; WARM=1 ab tlreal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:ts:4 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 jstart:ts taps:ts wstart:ts"
relaunch tl30 30; WARM=1 ab tl30 "j45_sl2:ts taps:ts wstart:ts jstart:ts jstart:o j41_rl_p10:ts j41_rl_p10:o w42_id:ts gait:ts"
echo TL248_DONE >> $O
