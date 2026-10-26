#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; T=Tools/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars229f.sh; cat Saved/Codex/SHME_V227_20261024/req/cap227.sh)" bash $T/ab_safe229.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
echo "CAPTEST start $(date +%T)" >> $O
relaunch ct 30; export WARM=0 CAPV="o ref"
capf 2.6 3.0 capt "j24_rel:oS"
echo "CAPTEST_DONE $(date +%T)" >> $O
