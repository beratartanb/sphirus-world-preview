#!/bin/bash
# V2.29 t5: after build2 (camera knobs live, lagged effort): effort on/off, walk framing on/off
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
until grep -q "BUILD229B_DONE\|BUILD229B_FAILED" $O; do sleep 20; done
grep -q "BUILD229B_FAILED" $O && { echo "T5 SKIPPED (build2 failed)" >> $O; exit 1; }
echo "T5 START $(date +%T)" >> $O
relaunch t5 30; export WARM=1
ab t5 "c29_ad:o c29_ad:cw c29_diag:o c29_diag:cw c29_wlook:o c29_wlook:cw c29_look:cw c29_jlook:cw d_sprint:cw"
ab t5 "e29_rest:o e29_rest:ef e29_load:o e29_load:ef e29_recov:ef e29_chain:o e29_chain:ef chain_sscut:ef s29_ws:ef s29_dbl:ef e29_house:ef j24_ph0:ef legs_slope_sprint:o legs_slope_sprint:ef"
echo "T5 DONE $(date +%T)" >> $O
