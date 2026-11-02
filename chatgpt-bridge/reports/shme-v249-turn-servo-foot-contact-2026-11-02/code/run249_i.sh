#!/bin/bash
# run249_i.sh : V2.49 chain I = restore the 22 start clips (pre-repair backups), apply the v2 ankle-pivot ground-contact repair, verify,
# full A/B (60 + captures, real time, 30, 20, 120) for the servo turning start, and the weighted idle on top of it (rmi)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until ! ps -ef | grep -v grep | grep -q "run249_g4"; do sleep 20; done
if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then SHME_KIND=measure SHME_OWNER=v249 bash $RUN Tools/SHME_V21_20261014/revert_quit.py rq_i0 300 | grep -a -E "dirty after|QUIT|REFUSED" >> $O; fi
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "I_ABORT editor did not close" >> $O; exit 1; }
echo "[restore2] $("$PY" Tools/SHME_V249_20261102/restore249.py $M/v249_foot.json --apply | cut -c1-200)" >> $O
grep -a "restore2\]" $O | tail -1 | grep -q '"ok": 22, "bad": \[\]' || { echo "I_ABORT restore" >> $O; exit 1; }
relaunch i0 60
"$PY" Tools/SHME_V233_20261027/manifest233.py v249_foot3 --from $D/data/footfix_clips.json | tail -1 | cut -c1-120 >> $O
SHME_KIND=write SHME_OWNER=v249 SHME_MANIFEST=$M/v249_foot3.json bash $RUN $REQ/footfix_write_req.py v249footfix3 1200 | grep -a 'FOOTFIX249\|REFUSED\|WRITE_GUARD\|Error\|Traceback' > $D/data/footfix_write3.out
echo "[footfix3] $(grep -o '"saved": [0-9]*\|REFUSED.*\|WRITE_GUARD.*\|Error.*\|Traceback.*' $D/data/footfix_write3.out | tr '\n' ' ' | cut -c1-300)" >> $O
grep -q '"saved": 22' $D/data/footfix_write3.out || { echo "FOOT3_ABORT" >> $O; exit 1; }
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/clipdump_req.py v249clipdump5 600 | grep -a 'CLIPDUMP249' | cut -c1-80 >> $O
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/footpitch_req.py v249footpitch2 600 | grep -a 'FOOTPITCH249' > $D/data/footpitch_after.out
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify5 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
relaunch i60 60; WARM=1 ab i60 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o j45_sl:rm"
CAP_START=9.3 CAP_SECS=3.4 ab icap "j45_sl2:rmS j45_sl2:rmD j45_sl2:oD" $D/vars249_cap.sh
echo TI249_60 >> $O
relaunch ireal real; WARM=1 ab ireal "j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3 j45_sl2:rm:4 j45_sl2:rm:5 j45_sl2:o j45_sl2:o:2 j45_sl:rm jstart:rm jstart:o taps:rm wstart:rm w43_idle:rmi taps:rmi j40_rlw:rmi j40_rlw:rm"
relaunch i30 30; WARM=1 ab i30 "j45_sl2:rm j45_sl2:o jstart:rm jstart:o taps:rm wstart:rm w42_id:rm gait:rm j41_rl_p10:rm j42_lr_p10:rm w43_idle:rm w43_idle:rmi taps:rmi jstart:rmi j40_rlw:rmi j40_rlw:rm"
relaunch i20 20; WARM=1 ab i20 "j45_sl2:rm j45_sl2:o jstart:rm w43_idle:rmi"
relaunch i120 120; WARM=1 ab i120 "j45_sl2:rm j45_sl2:o jstart:rm w43_idle:rmi"
echo TI249_DONE >> $O
