#!/bin/bash
# run253_c.sh : V2.53 chain C = fresh launch after the settle v2 write, 60 fixed A/B: settle v2 (st), taps repeat, weighted idle with walk entry
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V253_20261104; O=$D/run253_c.out; source $D/lib253.sh
relaunch c60 60
WARM=1 ab c60 "j36_stop:st j36_stopb:st j36_stopr:st jstart:st j45_sl2:st gait:st taps:o taps:weap3 taps:we w43_idle:oi w43_idle:wi3 wstart:oi wstart:wi3 gait:wi3 w42_id:wi3"
echo TC253_DONE >> $O
