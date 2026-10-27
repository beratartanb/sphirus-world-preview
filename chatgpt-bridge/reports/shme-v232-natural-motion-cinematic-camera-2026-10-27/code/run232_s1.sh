#!/bin/bash
# run232_s1.sh : V2.32 session 1 - fresh editor (fixed 30): V2.31 production verify, then production baselines (camera scenarios + open motion defects).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
echo "S1 start $(date +%T) (reason: first V2.32 session, fixed 30)" >> $O
relaunch s1 30
bash $R $D/req/verify_p0.py verify_p0 900 > $D/verify_p0.out 2>&1; grep -a "VERIFY231" $D/verify_p0.out | grep -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' >> $O
export WARM=1 MEMPROBE=1
J=""; for s in cam32_w45 cam32_j90 cam32_s90 cam32_s90l cam32_s180 cam32_brk2 cam32_wallturn cam32_look cam32_idlelook cam32_analog cam32_chain cam_corr s29_wall; do J="$J $s:o"; done
for s in e29_chain e29_load e31_s2_4750 s29_swl12 j30_rel_3200 j30_rel_3450 j30_slow c29_combo a29_angb c30_calm ter_drop_walk ter_step2 d_sprint; do J="$J $s:o"; done
ab s1 "$J" $D/vars232.sh
echo "S1_DONE $(date +%T)" >> $O
