#!/bin/bash
# run249_l.sh : V2.49 chain L = final candidate check (rmh = turn owner + no timer hold; rmhi = + weighted idle) at 60 / 30 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; source $D/lib249.sh
until grep -q TK249_DONE $O; do sleep 20; done
relaunch l60 60; WARM=1 ab l60 "jstart:rmh j45_sl2:rmh jstart:rmhi w43_idle:rmhi"
relaunch l30 30; WARM=1 ab l30 "jstart:rmh jstart:o j41_rl_p10:rmh j41_rl_p10:o j40_rlw:rmhi j40_rlw:o taps:rmhi taps:o w43_idle:rmhi w43_idle:o wstart:rmhi gait:rmhi w42_id:rmhi j42_lr_p10:rmhi"
relaunch lreal real; WARM=1 ab lreal "j45_sl2:rmhi j45_sl2:rmhi:2 j45_sl2:rmhi:3 jstart:rmhi taps:rmhi j40_rlw:rmhi w43_idle:rmhi"
echo TL249_DONE >> $O
