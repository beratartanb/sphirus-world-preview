#!/bin/bash
# run230_fin2.sh : FIN after the verify fix (the clean-reopen editor of FIN is still open: read-only verify again, then production evidence)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
V2=Tools/SHME_V2_20261014; R="bash $V2/run_v2.sh"; D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "FIN2 start $(date +%T)" >> $O
$R $D/req/verify_fin.py verify 600 | grep -a "VERIFY229\|VERIFY230\|Traceback\|Error" | cut -c1-2500 | tee $D/verify_fin2.out >> $O
grep -q '"ALL_OK": true}' $D/verify_fin2.out || { echo "FIN2_FAILED verify $(date +%T)" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
ab fw "j24_ph0:o e29_chain:o d_sprint:o w30_rev:o" $D/vars230c.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
J=""; for s in c30_calm c29_combo w30_rev w30_postsprint s29_swl12 s29_swl14 s29_swl16 j30_slow j24_rel j24_dbl j24_ph0 e29_chain e29_load e29_recov e29_rest s29_cam s29_ws s29_dg d_sprint legs_slope_sprint ter_drop_walk ter_step2 map_r1 wdiag; do J="$J $s:o"; done
ab fin "$J" $D/vars230c.sh
echo "FIN2_DONE $(date +%T)" >> $O
