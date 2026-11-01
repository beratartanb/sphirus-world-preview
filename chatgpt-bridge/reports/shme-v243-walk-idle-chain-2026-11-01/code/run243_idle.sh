#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101
for i in $(seq 1 120); do grep -q T1_DONE $D/chain.out 2>/dev/null && break; sleep 30; done
source $D/lib243.sh
WARM=1 ab i5 "w43_idle:idlg w43_idle:o"
CAP_START=4.6 CAP_SECS=9.5 ab i5cap "w43_idle:idlgS w43_idle:oS w43_idle:idlgG w43_idle:oG" $D/vars243_cap.sh
CAP_START=5.2 CAP_SECS=9.0 ab i5cap2 "w42_id:idlgS w42_id:idlgG" $D/vars243_cap.sh
echo I5_DONE >> $O
