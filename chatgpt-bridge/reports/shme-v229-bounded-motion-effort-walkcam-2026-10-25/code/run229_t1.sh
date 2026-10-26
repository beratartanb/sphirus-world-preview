#!/bin/bash
# V2.29 t1: production baseline (fixed 30) of the sprint reversal family, effort chains, camera and direction scenarios
source Saved/Codex/SHME_V229_20261025/lib229.sh 2>/dev/null || source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
echo "T1 START $(date +%T)" >> $O
relaunch t1 30
ab t1 "s29_ws:o s29_ws_ph:o s29_cam:o s29_cam2:o s29_sa:o s29_dg:o s29_dbl:o s29_rel:o b_s2back:o b_cam180:o chain_sprint:o chain_sscut:o"
echo "T1 SPRINT_DONE $(date +%T)" >> $O
ab t1 "e29_chain:o e29_rest:o e29_load:o e29_recov:o e29_house:o c29_look:o c29_ad:o c29_wlook:o c29_diag:o c29_jlook:o a29_ang:o a29_angb:o a29_edge:o a29_mag:o a29_kdg:o a29_csweep:o"
echo "T1 DONE $(date +%T)" >> $O
