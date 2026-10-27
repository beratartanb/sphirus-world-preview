#!/bin/bash
# run232_p2.sh : V2.32 P2 (replaces P1: P1 ran on the LastHitBy-broken orbit block = control yaw 0, and a duplicate P1 instance queued a
# DB rebuild into a PIE session -> hung runner). Fresh editor (reason: the hung runner editor was killed), LastHitBy repair saved,
# camera re-check o vs c2 incl. view-heading invariance (yaw0 30), then P vs o INTERLEAVED, 2 repeats (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
V21=Tools/SHME_V21_20261014
echo "P2b start $(date +%T) (reason: LHB check counted the unlinked old getter; repair in memory, save + continue)" >> $O
# (P2b: same editor p2, the repair is already applied in memory: no relaunch, no revert)
bash $R $D/req/lhb_save.py lhb 900 > $D/lhb_save.out 2>&1; echo "LHB $(grep -a -o 'LHB232 {.\{0,700\}' $D/lhb_save.out | head -1)" >> $O
grep -a "^LHB LHB232" $O | tail -1 | grep -q '"saved": true' || { echo "P2_FAILED lhb $(date +%T)" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J=""; for s in cam32_s90 cam32_s90y cam32_w45 cam32_w45y cam32_look cam32_idlelook cam32_brk2 cam32_wallturn cam32_j90 cam32_analog cam32_chain cam32_s180; do J="$J $s:o $s:c2"; done
ab p2c "$J" $D/vars232.sh
echo "P2C_DONE $(date +%T)" >> $O
J=""; for s in c30_calm cam32_chain cam32_s90 cam32_s90y cam32_brk2 cam32_wallturn cam32_look cam32_w45 e29_load e29_chain e29_recov e31_s2_4750 e31_s2_4900 s29_swl12 j30_slow j30_rel_3200 j30_rel_3450 jback jstart c29_combo a29_angb ter_drop_walk ter_step2 legs_slope_sprint ins_ws map_r1 d_sprint; do for rp in 1 2; do J="$J $s:o:$rp $s:P:$rp"; done; done
ab p2 "$J" $D/vars232.sh
echo "P2_DONE $(date +%T)" >> $O
