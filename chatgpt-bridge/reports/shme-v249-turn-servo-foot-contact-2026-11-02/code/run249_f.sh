#!/bin/bash
# run249_f.sh : V2.49 ball-pivot repair dry run (editor relaunch first)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh; source $D/lib249.sh
tasklist 2>/dev/null | grep -qi UnrealEditor.exe || relaunch f0 60
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/footpivot_dry_req.py v249fpdry3 1800 | grep -a 'FOOTPIVOT249\|Error\|Traceback' > $D/data/footpivot_dry.out
echo "[footpivot dry] $(cut -c1-200 $D/data/footpivot_dry.out)" >> $O; echo TF249B_DONE >> $O
