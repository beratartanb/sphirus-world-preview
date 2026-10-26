#!/bin/bash
# run229_ems.sh : pc vs ems (pc + RedirectEpisodeMinSpeed 70) on the effort chains and walk / jog regressions, fixed 30, fresh editor.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; export O=$D/chain.out; source $D/lib229.sh
echo "EMS229 start $(date +%T)" >> $O
relaunch em 30; export WARM=1
J=""; for s in e29_load e29_chain e29_recov s29_swl12 s29_swl16 j29_swl10 c29_combo c29_ad c29_diag taps s23_jstart j24_ph0 j24_dbl j24_rel e29_rest chain_sscut ins_ws map_r1; do J="$J $s:pc $s:ems"; done
ab em "$J" $D/vars229f.sh
ab em "e29_load:pcoff e29_chain:pcoff s29_swl12:pcoff s29_swl14:pcoff s29_swl12:ems40 s29_swl14:ems40 e29_chain:ems40 e29_load:ems40" $D/vars229f.sh
echo "EMS229_DONE $(date +%T)" >> $O
