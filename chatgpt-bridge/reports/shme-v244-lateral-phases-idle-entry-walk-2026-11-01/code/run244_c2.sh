#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh
for i in $(seq 1 90); do [ "$(grep -c C1_DONE $D/chain.out)" -ge 2 ] && break; sleep 20; done
source $D/lib244.sh
echo "[chooser] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $REQ/probe_chooser.py v244chooser 300 | grep -a 'CHOOSER244\|REFUSED\|Error' | cut -c1-4000)" >> $O
echo "[walkmet] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $REQ/walkmetrics.py v244walkmet 300 | grep -a 'WALKMET244\|REFUSED\|Error\|Traceback' | cut -c1-2000)" >> $O
echo C2_DONE >> $O
