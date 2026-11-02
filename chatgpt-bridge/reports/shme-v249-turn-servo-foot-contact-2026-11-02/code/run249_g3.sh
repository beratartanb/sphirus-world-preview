#!/bin/bash
# run249_g.sh : V2.49 chain G = restore the 22 start clips from their pre-v2 backups (editor closed), ball-pivot stance repair (v3b,
# self source), ground-truth re-dump, verify, A/B 60 (+captures), real time, 30 / 20 / 120 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_pivot3 --from $D/data/footfix_clips.json | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_pivot3.json bash $RUN $REQ/footpivot_write_req.py v249pivot3 2400 | grep -a 'FOOTPIVOT249\|REFUSED\|WRITE_GUARD\|Error\|Traceback\|LEG_GUARD' > $D/data/footpivot_write.out
echo "[footpivot] $(grep -o '"saved": [0-9]*\|"skipped": \[[^]]*\]\|REFUSED.*\|WRITE_GUARD.*\|LEG_GUARD[^"]*\|Error.*\|Traceback.*' $D/data/footpivot_write.out | tr '\n' ' ' | cut -c1-400)" >> $O
grep -q '"saved": 22' $D/data/footpivot_write.out || { echo "PIVOT_ABORT" >> $O; exit 1; }
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/clipdump_req.py v249clipdump3 600 | grep -a 'CLIPDUMP249' | cut -c1-120 >> $O
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify4b 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch g60 60; WARM=1 ab g60 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o"
CAP_START=9.3 CAP_SECS=3.4 ab gcap "j45_sl2:rmS j45_sl2:rmD j45_sl2:oD" $D/vars249_cap.sh
echo TG249_60 >> $O
relaunch greal real; WARM=1 ab greal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 j45_sl2:rm:4 j45_sl2:rm:5 j45_sl2:o j45_sl2:o:2 j45_sl:rm jstart:rm jstart:o taps:rm wstart:rm"
relaunch g30 30; WARM=1 ab g30 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o taps:rm wstart:rm w42_id:rm gait:rm j41_rl_p10:rm j42_lr_p10:rm w43_idle:rm"
relaunch g20 20; WARM=1 ab g20 "j45_sl2:rm j45_sl2:o jstart:rm"
relaunch g120 120; WARM=1 ab g120 "j45_sl2:rm j45_sl2:o jstart:rm"
echo TG249_DONE >> $O
