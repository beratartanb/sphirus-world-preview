#!/bin/bash
# run231_fin_b.sh : production evidence + captures in the finv editor (after the verify rerun ALL_OK)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; export O=$D/chain.out; source $D/lib231.sh
export WARM=1 MEMPROBE=1
ab finw "s29_swl12:o:0 e29_load:o:0 d_sprint:o:0 ins_ws:o:0" $D/vars231.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
export WARM=0
J="c30_calm:o c29_combo:o w30_rev:o a29_angb:o wdiag:o s29_ws:o d_sprint:o s29_cam:o s29_swl12:o s29_swl12:o:2 s29_swl12:o:3 s29_swl14:o s29_swl16:o j30_slow:o"
J="$J e29_chain:o e29_load:o e29_recov:o e29_rest:o j24_rel:o j24_dbl:o j24_dbl:o:2 j24_ph0:o legs_slope_sprint:o ter_drop_walk:o ter_step2:o ter_drop_jog:o map_r1:o ins_ws:o ins_ws2:o ins_qa:o"
for ms in 3100 3200 3250 3300 3350 3400 3450; do J="$J j30_rel_$ms:o"; done
for ms in 4700 4750 4800 4850 4900 4950; do J="$J e31_s2_$ms:o"; done
ab fin "$J" $D/vars231.sh
echo "FIN_EVIDENCE_DONE $(date +%T)" >> $O
bash $D/run231_cap.sh
echo "FINAL_DONE $(date +%T)" >> $O
