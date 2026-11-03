#!/bin/bash
# run254_i.sh : V2.54 chain I = + V2.40 head priority (SHM240_HeadOn) on the turn-around candidate; regression; captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_i.out; source $D/lib254.sh
relaunch i60 60
WARM=1 ab i60 "s54_revR:rvcamh s54_revL:rvcamh s54_r90:rvcamh s54_tap:rvcamh s54_mid:rvcamh wstart:rvcamh w42_id:rvcamh taps:rvcamh jstart:rvcamh gait:rvcamh w43_idle:rvcamh j40_rlw:rvcamh j45_sl2:rvcamh j36_stop:rvcamh"
CAP_START=4.8 CAP_SECS=2.8 ab icap "s54_revR:rvcamhS s54_revR:rvcamhG s54_r90:rvcamhS s54_r90:rvcamhG" $D/vars254_cap.sh
relaunch i120 120
WARM=1 ab i120 "s54_revR:rvcamh s54_r90:rvcamh"
echo TI254_DONE >> $O
