#!/bin/bash
# run254_h.sh : V2.54 chain H = gaze v5 verification + three-condition captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_h.out; source $D/lib254.sh
relaunch h60 60
WARM=1 ab h60 "s54_revR:rvcam s54_revL:rvcam s54_r90:rvcam s54_l90:rvcam s54_tap:rvcam s54_mid:rvcam s54_lr:rvcam j54_rev:rvcam"
CAP_START=4.8 CAP_SECS=2.8 ab hcap "s54_revR:prodS s54_revR:rvcamS s54_revR:prodG s54_revR:rvcamG s54_r90:prodS s54_r90:rvcamS s54_r90:prodG s54_r90:rvcamG s54_tap:prodS s54_tap:rvcamS" $D/vars254_cap.sh
echo TH254_DONE >> $O
