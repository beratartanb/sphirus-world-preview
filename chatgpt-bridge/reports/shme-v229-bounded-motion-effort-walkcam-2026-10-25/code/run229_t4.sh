#!/bin/bash
# V2.29 t4: first candidate evaluation after the build (production o now includes the RevTurn content fix)
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
until grep -q "BUILD229_DONE\|BUILD229_FAILED" $O; do sleep 20; done
grep -q "BUILD229_FAILED" $O && { echo "T4 SKIPPED (build failed)" >> $O; exit 1; }
echo "T4 START $(date +%T)" >> $O
relaunch t4 30; export WARM=1
ab t4 "s29_cam:o s29_cam2:o b_cam180:o chain_sprint:o j24_m180w:o j23_m180:o"
ab t4 "e29_rest:o e29_rest:ef e29_load:o e29_load:ef e29_recov:o e29_recov:ef e29_chain:o e29_chain:ef chain_sscut:o chain_sscut:ef s29_ws:o s29_ws:ef s29_dbl:o s29_dbl:ef e29_house:o e29_house:ef"
ab t4 "c29_ad:o c29_ad:cw c29_wlook:o c29_wlook:cw c29_diag:o c29_diag:cw c29_look:o c29_look:cw c29_jlook:o c29_jlook:cw d_sprint:o d_sprint:cw"
ab t4 "j24_rel:o j24_rel:rs s29_rel:o s29_rel:rs j24_ph0:rs j24_dbl:rs j24_sw_ph2:rs"
echo "T4 DONE $(date +%T)" >> $O
