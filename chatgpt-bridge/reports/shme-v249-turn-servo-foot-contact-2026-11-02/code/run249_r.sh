#!/bin/bash
# run249_r.sh : V2.49 chain R = raw vs compressed pose probe of the repaired turn clips (read-only measure job)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh
source $D/lib249.sh
until grep -q TQ249_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/cmpprobe_req.py v249cmpprobe 600 | grep -a 'CMPPROBE249\|REFUSED\|Error\|Traceback' > $D/data/cmpprobe.out
echo "[cmpprobe] $(cut -c1-300 $D/data/cmpprobe.out)" >> $O
echo TR249_DONE >> $O
