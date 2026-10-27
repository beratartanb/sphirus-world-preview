#!/bin/bash
# run232_fin.sh : V2.32 promotion (after FALL_DONE and the manual PROMOTE_GO marker): fresh editor -> promote232 (camera / bfexit /
# loadedbf / floorguard) -> clean reopen -> verify232 -> production evidence (fixed 30) + body x camera matrix -> captures.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "FALL_DONE" $O && grep -aq "PROMOTE_GO" $O; do sleep 30; done
echo "FIN start $(date +%T) (reason: promotion in a fresh fixed-30 editor)" >> $O
relaunch fin 30
bash $R $D/req/promo_save.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o 'PROMO232 {.*' $D/promo_fin.out | cut -c1-900 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promotion not saved" >> $O; exit 1; }
echo "FINV start $(date +%T) (reason: clean reopen after the save = verification on disk state)" >> $O
relaunch finv 30
bash $R $D/req/verify_fin.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out >> $O
cat $D/vars232.sh $D/vars232_post.sh > $D/vars232_fin.sh
export WARM=1 MEMPROBE=1
J=""; for s in c30_calm cam32_chain cam32_s90 cam32_s90l cam32_brk2 cam32_wallturn cam32_look cam32_idlelook cam32_analog cam32_w45 cam32_j90 cam_corr s29_wall e29_load e29_chain e29_recov e31_s2_4750 s29_swl12 j30_slow j30_rel_3200 j30_rel_3450 jback jstart c29_combo a29_angb wdiag ter_drop_walk ter_step2 legs_slope_sprint ins_ws map_r1 d_sprint s29_cam; do J="$J $s:o"; done
for s in cam32_chain cam32_s90 cam32_brk2 cam32_wallturn cam32_look cam32_analog; do J="$J $s:pre232 $s:ncam $s:ocam"; done
ab fin "$J" $D/vars232_fin.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
