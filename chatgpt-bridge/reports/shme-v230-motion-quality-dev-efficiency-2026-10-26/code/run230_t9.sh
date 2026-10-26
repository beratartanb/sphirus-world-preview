#!/bin/bash
# run230_t9.sh : fresh editor after the content edits (re-author + loaded family): WARM-UP runs over every edited family first (PoseSearch indexes
# build on first use -> selection None), wait until the editor log shows no new BuildIndex for 60 s, then the measured runs.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T9 start $(date +%T)" >> $O
[ -n "$NORELAUNCH" ] || relaunch t9 30
R=Tools/SHME_V2_20261014/run_v2.sh
[ -n "$NORELAUNCH" ] || { bash $R $D/req/db230L_write.py db230L 1800 > $D/db230L.out 2>&1; grep -a "RDB226\|Traceback" $D/db230L.out | cut -c1-500 >> $O; }
bash $R $D/req/loadroute_save.py loadroute 900 > $D/loadroute.out 2>&1; grep -a "LOADROUTE230 {\|Traceback" $D/loadroute.out | cut -c1-600 >> $O
grep -aq '"ok": true' $D/loadroute.out || { echo "T9_STOP loadroute" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
ab t9w "j24_ph0:lrL s29_ws:lrL a29_angb:lrL j24_ad_ph0:lrL d_sprint:lrL e29_chain:lrL c29_combo:lrL j24_dbl:lrL" $D/vars230.sh
LOG="Saved/Logs/$LR_LOG"; for i in $(seq 1 40); do n1=$(grep -a -c "BuildIndex" "$LOG"); sleep 15; n2=$(grep -a -c "BuildIndex" "$LOG"); [ "$n1" = "$n2" ] && break; done
echo "T9 index quiet $(date +%T) BuildIndex lines $(grep -a -c 'BuildIndex' "$LOG")" >> $O
J=""; for s in d_sprint s29_ws e29_rest chain_sscut s29_sa c29_combo a29_ang a29_angb j24_ad_ph0 c29_jlook j24_ph0 j24_dbl j24_rel j24_sw_ph2 taps s23_jstart e29_chain e29_load e29_recov s29_swl12 s29_dbl; do J="$J $s:lr2 $s:lrL"; done
ab t9 "$J" $D/vars230.sh
echo "T9_DONE $(date +%T)" >> $O
