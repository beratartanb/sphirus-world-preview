#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh; source $D/lib249.sh
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/footpivot_dryself_req.py v249pvdry2 2400 | grep -a 'FOOTPIVOT249\|Error\|Traceback' > $D/data/footpivot_dryself.out
echo TH249B_DONE >> $O
