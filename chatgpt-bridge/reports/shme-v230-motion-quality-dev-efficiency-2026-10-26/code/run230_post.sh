#!/bin/bash
# run230_post.sh : after FIN2 -> T14 (real time stall owner) -> captures (fixed 30)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026
until grep -aq "FIN2_DONE\|FIN2_FAILED" $D/chain.out; do sleep 20; done
grep -aq "FIN2_FAILED" $D/chain.out && exit 1
bash $D/run230_t14.sh; bash $D/run230_cap.sh
