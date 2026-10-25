#!/bin/bash
# run228_t4c.sh : (cancel install already saved in editor i4b) look-axis install -> fixed-30 batch (cancel paths, look fix in production mode, regular reversal).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; export O=$D/chain.out; source $D/lib228.sh
echo "T4d start $(date +%T)" >> $O
export WARM=1; relaunch t4 30
ab t4 "j24_rel:rhCR j24_dbl:rhCR j24_rel:rhCRr j24_dbl:rhCRr j24_ph0:rhCR j24_ph3:rhCR j24_sw_ph2:rhCR ins_ws:o ins_ws2:o j24_sw_ph0:rhCR" $D/vars228.sh
echo "T4d_DONE $(date +%T)" >> $O
