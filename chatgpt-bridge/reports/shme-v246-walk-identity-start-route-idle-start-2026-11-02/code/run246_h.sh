#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; RUN=Tools/SHME_V2_20261014/run_v2.sh
for i in $(seq 1 540); do grep -q IN3_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
WARM=1 ab fin "w42_id:o taps:o w42_id:o:2"
CAP_START=1.9 CAP_SECS=7.0 ab fincap "w42_id:oS w42_id:oD" $D/vars246_cap.sh
echo "[probe] $(SHME_KIND=measure SHME_OWNER=v246 bash $RUN /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v243/probe243_cdo.py v246probe 300 | grep -a 'PROBE243' | grep -o '"dirty".*' | cut -c1-200)" >> $O
echo FINAL246_DONE >> $O
