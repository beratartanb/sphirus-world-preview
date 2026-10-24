#!/bin/bash
# run227_t5.sh : install pass e (Thr from the component episode too + new-intent/lost end kills the hold), then the candidate at fixed 30
# and the 60 / 120 / 20 FPS sweep. Waits for the previous editor to exit first.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V227_20261024; export O=$D/chain.out; source $D/lib227.sh
echo "T5 start $(date +%T)" >> $O
export WARM=1
relaunch i5 30
bash $R $D/req/install_e_save.py install_e 900 | grep -a "RH227E" | cut -c1-1500 >> $O
grep -q 'RH227E .*"saved": true' $O || { echo "T5 INSTALL_FAILED $(date +%T)" >> $O; exit 1; }
relaunch t5 30
ab t5 "j24_ph0:rh j24_ph3:rh j24_sw_ph0:rh j24_sw_ph2:rh j24_rel:rh j24_dbl:rh j24_ad_ph0:rh j24_m180w:rh" $D/vars227.sh
echo "T5 30 done $(date +%T)" >> $O
relaunch w60 60; ab w60 "j24_ph0:rh j24_sw_ph2:rh j24_ph3:rh j24_ovl120:rh j24_dbl:rh" $D/vars227.sh; echo "T5 60 done $(date +%T)" >> $O
relaunch w120 120; ab w120 "j24_ph3:rh j24_ph0:rh j24_sw_ph2:rh j24_ovl120:rh" $D/vars227.sh; echo "T5 120 done $(date +%T)" >> $O
relaunch w20 20; ab w20 "j24_ph0:rh j24_ph3:rh j24_sw_ph2:rh j24_ovl120:rh j24_dbl:rh" $D/vars227.sh; echo "T5 20 done $(date +%T)" >> $O
echo "T5_DONE $(date +%T)" >> $O
