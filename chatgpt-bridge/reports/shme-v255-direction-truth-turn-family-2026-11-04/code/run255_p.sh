#!/bin/bash
# run255_p.sh : V2.55 AO head candidate on the final build: capture at 60, head pop at 120 against the same build without it
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_p.out; source $D/lib255.sh
export V219_EDARGS="-UseFixedTimeStep -FPS=60"
ab p60 "s54_revR:c7h s54_revL:c7h s54_r90:c7h j54_rev:c7h j54_r90:c7h j54_r135:c7h" $D/vars255.sh
CAP_START=4.6 CAP_SECS=3.2 ab pcap "s54_revR:c7hS s54_revR:c7hG j54_rev:c7hS" $D/vars255.sh
relaunch p120 120
WARM=1 ab p120w "s54_revR:c7 s54_revL:c7 s54_r90:c7 s54_l90:c7 j54_rev:c7 j54_r90:c7 j38_c90l:c7" $D/vars255.sh
ab p120 "s54_revR:c7 s54_revR:c7h s54_revL:c7 s54_revL:c7h s54_r90:c7 s54_r90:c7h j54_rev:c7 j54_rev:c7h fz_sprint_m:c7 fz_sprint_m:c7h" $D/vars255.sh
relaunch pend 60
echo TP255_DONE >> $O
