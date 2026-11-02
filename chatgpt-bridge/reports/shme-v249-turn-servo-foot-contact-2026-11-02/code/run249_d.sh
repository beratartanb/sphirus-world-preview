#!/bin/bash
# run249_d.sh : V2.49 chain D = foot-pitch repair DRY run (after the 60 FPS servo batch)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh; source $D/lib249.sh
until grep -q TC249_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v249 bash $RUN $REQ/footfix_dry_req.py v249footdry 900 | grep -a 'FOOTFIX249\|Error\|Traceback' > $D/data/footfix_dry.out
echo "[footfix dry] $(cut -c1-200 $D/data/footfix_dry.out)" >> $O
echo TD249_DONE >> $O
