#!/bin/bash
# run249_j.sh : V2.49 chain J = keep the foot repair on the turn clips only: restore the 8 straight / lateral / backward start copies to
# their originals (pre-repair backups, editor closed), verify, jog-start + back-pedal regressions at 60 / real / 30
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
source $D/lib249.sh
until grep -q TI249_DONE $O; do sleep 20; done
if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then SHME_KIND=measure SHME_OWNER=v249 bash $RUN Tools/SHME_V21_20261014/revert_quit.py rq_j0 300 | grep -a -E "dirty after|QUIT|REFUSED" >> $O; fi
for i in $(seq 1 90); do tasklist 2>/dev/null | grep -qi UnrealEditor.exe || break; sleep 2; done
tasklist 2>/dev/null | grep -qi UnrealEditor.exe && { echo "J_ABORT editor did not close" >> $O; exit 1; }
echo "[restore10] $("$PY" Tools/SHME_V249_20261102/restore249.py $M/v249_foot3.json --apply --only Jog_Bwd_Start,Jog_Fwd_Start,Jog_Left_Start,Jog_Right_Start,TurnL045,TurnR045 | cut -c1-200)" >> $O
grep -a "restore10\]" $O | tail -1 | grep -q '"ok": 10, "bad": \[\]' || { echo "J_ABORT restore" >> $O; exit 1; }
relaunch j60 60
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v249 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v249verify6 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-400)" >> $O
WARM=1 ab j60 "jstart:rm jstart:o j45_sl2:rm"
relaunch jreal real; WARM=1 ab jreal "jstart:rm jstart:o j45_sl2:rm j45_sl2:rm:2 j45_sl2:rm:3"
relaunch j30 30; WARM=1 ab j30 "jstart:rm jstart:o taps:rm wstart:rm j41_rl_p10:rm j41_rl_p10:o j40_rlw:rm j40_rlw:rmi"
echo TJ249_DONE >> $O
