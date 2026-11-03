#!/bin/bash
# run254_d.sh : V2.54 chain D = smoothed turn-around + sprint 90 cut, numbers + side captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_d.out; source $D/lib254.sh
relaunch d60 60
WARM=1 ab d60 "s54_revR:rvc s54_revL:rvc s54_r90:o s54_r90:rvc s54_l90:o s54_l90:rvc j54_rev:rvc s54_tap:rvc s54_mid:rvc s54_lr:rvc"
CAP_START=4.8 CAP_SECS=2.6 ab dcap "s54_revR:preS s54_revR:rvcS s54_r90:preS s54_r90:rvcS"
echo TD254_DONE >> $O
