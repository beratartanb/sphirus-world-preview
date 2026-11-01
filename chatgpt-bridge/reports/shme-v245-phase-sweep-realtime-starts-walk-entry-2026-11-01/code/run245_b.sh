#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh
for i in $(seq 1 360); do grep -q SWEEP245_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
echo "[walk245dry] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN $REQ/walk245_dry.py v245wdry 300 | grep -a 'G245W \|REFUSED\|Error\|Traceback' | grep -o '"before".*' | cut -c1-500)" >> $O
echo "[cht] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN $REQ/probe_cht.py v245cht 300 | grep -a 'CHT245\|REFUSED\|Error\|Traceback' | cut -c1-2500)" >> $O
WARM=1 ab sl "j45_sl:o j45_sl:o:2"
relaunch slreal real; WARM=1 ab slreal "j45_sl:o j45_sl:o:2 j45_sl:o:3"
relaunch slend 30
echo SL245_DONE >> $O
