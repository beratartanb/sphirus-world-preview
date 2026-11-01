#!/bin/bash
# continuation of run245_d after the refused relaunch: save the project walk DB (manifest v245_walk, backup exists), then real time + captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; REQ=$D/req; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
source $D/lib245.sh
WARM=1 ab wa "w42_id:o gait:o taps:o w42_id:o:2"
echo "[savewdb] $(SHME_KIND=write SHME_OWNER=v245 SHME_MANIFEST=$M/v245_walk.json bash $RUN $REQ/save_walkdb.py v245savewdb 300 | grep -a 'SAVEWDB245\|REFUSED\|WRITE_GUARD\|Error' | cut -c1-400)" >> $O
relaunch wareal real; WARM=1 ab wareal "w42_id:o gait:o"
relaunch waend 30
CAP_START=1.9 CAP_SECS=7.0 ab wacap "w42_id:oS w42_id:oD" $D/vars245_cap.sh
echo WALK5_DONE >> $O
