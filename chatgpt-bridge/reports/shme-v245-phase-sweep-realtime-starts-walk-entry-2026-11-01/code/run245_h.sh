#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101
for i in $(seq 1 360); do grep -q SWEEP4_DONE $D/chain.out && break; sleep 20; done
source $D/lib245.sh
WARM=1 ab own "w42_id:oow w42_id:osw w42_id:ofp w42_id:oRAW w42_id:oSCR w42_id:oPBI"
echo OWN_DONE >> $O
