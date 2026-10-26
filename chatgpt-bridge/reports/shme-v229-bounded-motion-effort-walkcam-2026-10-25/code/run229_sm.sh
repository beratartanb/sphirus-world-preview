#!/bin/bash
# run229_sm.sh : production (o, after the pushcancel switch) vs effort floor 0.7 / 0.8, fixed 30, fresh editor.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
echo "SM229 start $(date +%T)" >> $O
relaunch sm 30; export WARM=1
J=""; for s in chain_sprint e29_load e29_chain e29_recov e29_rest chain_sscut s29_swl12 s29_swl14 s29_swl16 d_sprint s29_dg s29_sa; do J="$J $s:sm70 $s:sm80"; done
ab sm "$J" $D/vars229f.sh
echo "SM229_DONE $(date +%T)" >> $O
