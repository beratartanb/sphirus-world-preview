#!/bin/bash
# run231_b1d.sh : the rest of the B1 tests (pr1 / slpr failed: live_cm sat inside abp_flags) in the same editor
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh
echo "B1D start $(date +%T)" >> $O
export WARM=0 MEMPROBE=1
J=""; for v in pr1 slpr; do for s in ter_drop_walk ter_step2 ter_drop_jog; do J="$J $s:$v"; done; done
J="$J map_r1:o map_r1:slpr c30_calm:slpr d_sprint:slpr j24_ph0:slpr"
for v in o slf; do for s in j30_rel_3100 j30_rel_3200 j30_rel_3250 j30_rel_3350 j30_rel_3450 s29_swl12 j24_ph0 j24_dbl w30_rev c30_calm; do J="$J $s:$v"; done; done
J="$J s29_swl12:det s29_swl12:det:2"
ab b1 "$J" $D/vars231.sh
echo "B1D_DONE $(date +%T)" >> $O
