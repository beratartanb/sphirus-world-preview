#!/bin/bash
# run248_e.sh : V2.48 chain E = authored foot-drift probe + long-hold scenario j45_sl2 (turning start -> run loop hand-over) at real time and 60 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh; source $D/lib248.sh
until grep -q TC248_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v248 bash $RUN $REQ/authdrift_req.py v248authdrift 300 | grep -a 'AUTHDRIFT248\|Error\|Traceback' > $D/data/authdrift.out; echo "[authdrift] $(cut -c1-300 $D/data/authdrift.out)" >> $O
relaunch tereal real; WARM=1 ab tereal "j45_sl2:ts j45_sl2:ts:2 j45_sl2:ts:3 j45_sl2:o j45_sl2:o:2 j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:o j45_sl:o:2 jstart:ts taps:ts wstart:ts"
relaunch te60 60; WARM=1 ab te60 "j45_sl2:ts j45_sl2:o"
echo TE248_DONE >> $O
