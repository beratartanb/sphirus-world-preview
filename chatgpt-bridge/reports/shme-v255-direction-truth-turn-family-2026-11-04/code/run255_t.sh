#!/bin/bash
# run255_t.sh : after the FPS sweep, on fixed 60: real slope turns (mid ramp) and a wall right ahead of the brake, candidate against production; side captures on the ramp
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_t.out; source $D/lib255.sh
export V219_EDARGS="-UseFixedTimeStep -FPS=60"
until grep -q TS255_DONE $D/run255_s.out 2>/dev/null; do sleep 20; if ! ps -ef | grep -q "[r]un255_s"; then grep -q TS255_DONE $D/run255_s.out || { echo "T_NO_SWEEP $(date +%T)" >> $O; exit 1; }; fi; done
WARM=1 ab t60w "s54_revR:c7h s54_revL:c7h s54_r90:c7h s54_l90:c7h j54_rev:c7h j54_r90:c7h j38_c90l:c7h" $D/vars255.sh
J=""; for s in t255_ramp_s t255_ramp_j t255_ramp90_s t255_rampd_s t255_wall_c; do J="$J $s:c7h $s:o"; done
ab t60 "$J" $D/vars255.sh
echo T_AB_DONE >> $O
CAP_START=3.9 CAP_SECS=3.2 ab tcap "t255_ramp_s:c7hS" $D/vars255.sh
CAP_START=4.5 CAP_SECS=3.2 ab tcap2 "t255_ramp_j:c7hS" $D/vars255.sh
echo TT255_DONE >> $O
