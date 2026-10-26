#!/bin/bash
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
echo "T7B START $(date +%T)" >> $O
relaunch t7b 30; export WARM=1
ab t7b "e29_chain:ef2 e29_chain:ef3 chain_sscut:ef2 chain_sscut:ef3 e29_recov:ef2 e29_recov:ef3 e29_rest:ef2 e29_rest:ef3 s29_ws:ef2 e29_house:ef3 c29_combo:o c29_combo:all2 j24_rel:all2 j24_ph0:all2 s29_cam:all2"
echo "T7B DONE $(date +%T)" >> $O
