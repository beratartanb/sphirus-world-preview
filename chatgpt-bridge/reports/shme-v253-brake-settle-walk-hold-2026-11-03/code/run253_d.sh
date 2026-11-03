#!/bin/bash
# run253_d.sh : V2.53 chain D = walk hold variant + final candidate
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V253_20261104; O=$D/run253_d.out; source $D/lib253.sh
relaunch d60 60
WARM=1 ab d60 "taps:o taps:wh taps:wh3 wstart:o wstart:wh wstart:wh3 w42_id:o w42_id:wh3 j40_rlw:wh3 gait:fin jstart:fin j36_stop:fin j45_sl2:fin w43_idle:fin"
echo TD253_DONE >> $O
