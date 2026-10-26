#!/bin/bash
# run229_cap4.sh : V2.29 captures (all earlier V2.29 captures were refused: maximized editor window -> viewport 1741 px; qa_pie fit_window now
# restores a maximized window first). ref = V2.28 behaviour + RevTurn fix via flags; o = final production. Fixed 30 = real speed, full frame.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; T=Tools/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars229f.sh; cat Saved/Codex/SHME_V227_20261024/req/cap227.sh)" bash $T/ab_safe229.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
echo "CAP4 start $(date +%T)" >> $O
relaunch cap4 30; export WARM=1 CAPV="o ref"
capf 2.6 10.0 cap4 "e29_chain:refS e29_chain:oS e29_chain:oG s29_cam:oS s29_cam:oG"
capf 1.6 13.4 cap4 "c29_combo:refG c29_combo:oG c29_combo:oS"
capf 2.6 6.0 cap4 "e29_rest:refS e29_rest:oS j24_rel:refS j24_rel:oS s29_cam2:oG"
capf 5.6 5.4 cap4 "e29_load:refS e29_load:oS e29_load:oG"
echo CAP4_DONE >> $O
