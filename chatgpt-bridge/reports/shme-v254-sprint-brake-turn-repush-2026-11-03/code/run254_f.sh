#!/bin/bash
# run254_f.sh : V2.54 chain F = cancel releases clip speed + own to clip end + generator block; camera candidate; captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_f.out; source $D/lib254.sh
relaunch f60 60
WARM=1 ab f60 "s54_revR:rvc s54_revL:rvc s54_r90:rvc s54_l90:rvc s54_tap:rvc s54_mid:rvc s54_lr:rvc s54_revR:rvc:2 gait:o gait:cam taps:o taps:cam cam32_wallturn:o cam32_wallturn:cam s54_revR:rvcam s54_revR:o"
CAP_START=4.8 CAP_SECS=2.8 ab fcap "s54_revR:prodS s54_revR:rvcS s54_r90:prodS s54_r90:rvcS s54_revR:rvcG s54_revR:rvcamG" $D/vars254_cap.sh
echo TF254_DONE >> $O
