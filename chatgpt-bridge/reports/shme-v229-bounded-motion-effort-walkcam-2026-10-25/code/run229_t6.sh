#!/bin/bash
# V2.29 t6: effort v3 (request-latched load, gain 0.9) after build3
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
bash $D/run229_build3.sh > $D/build3.nohup 2>&1
grep -q "BUILD229C_DONE" $O || { echo "T6 SKIPPED (build3 failed)" >> $O; exit 1; }
echo "T6 START $(date +%T)" >> $O
relaunch t6 30; export WARM=1
ab t6 "e29_rest:ef e29_load:ef e29_recov:ef e29_chain:ef chain_sscut:ef s29_ws:ef s29_dbl:ef s29_cam:ef chain_sprint:ef e29_house:ef j24_ph0:ef j24_sw_ph2:ef legs_slope_sprint:ef ter_hill8_jog:o ter_hill8_jog:ef"
echo "T6 DONE $(date +%T)" >> $O
