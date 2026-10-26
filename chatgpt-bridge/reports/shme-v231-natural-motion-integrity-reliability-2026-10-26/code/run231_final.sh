#!/bin/bash
# run231_final.sh : after S3_DONE -> production switch (all seven V2.31 groups) -> clean reopen verify -> production evidence -> captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out
until grep -aq "S3_DONE" $O; do sleep 30; done
export PROMO='{"slow": true, "exit": true, "fwdrev": true, "inspect": true, "steplift": true, "tipend": true, "loaded": true}'
bash $D/run231_fin.sh || exit 1
bash $D/run231_cap.sh
echo "FINAL_DONE $(date +%T)" >> $O
