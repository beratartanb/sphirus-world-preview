#!/bin/bash
# run254_e.sh : V2.54 chain E = hand-over yaw ramp + intent cancel + block mid-clip entry; numbers + captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_e.out; source $D/lib254.sh
relaunch e60 60
WARM=1 ab e60 "s54_revR:rvc s54_revL:rvc s54_r90:rvc s54_l90:rvc s54_tap:rvc s54_tap:o s54_mid:rvc s54_mid:o s54_lr:rvc s54_lr:o"
CAP_START=4.8 CAP_SECS=2.6 ab ecap "s54_revR:prodS s54_revR:rvcS s54_r90:prodS s54_r90:rvcS s54_revR:rvcG" $D/vars254_cap.sh
echo TE254_DONE >> $O
