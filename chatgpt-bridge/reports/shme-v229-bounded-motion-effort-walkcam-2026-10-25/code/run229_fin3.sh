#!/bin/bash
# run229_fin3.sh : V2.29 final chain, third switch: effort floor EffortScaleMin 0.7 (sm70 A/B). Groups camera / effort / resume are already saved
# (17:52, VERIFY229 ALL_OK); this run adds pushcancel. 1) pre-switch captures of the sprint S->W lock (o) vs the candidate (pc);
# 2) promote229 {pushcancel} -> CLEAN reopen verify (all four groups, ALL_OK gate) -> full production evidence (fixed 30) + effort off
# -> FPS 20 / 60 / 120 -> real time (cold first) -> after-switch captures.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; T=Tools/SHME_V229_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib229.sh
G="{'camera': True, 'effort': True, 'resume': True, 'pushcancel': True, 'effort_min': 0.7}"
echo "FIN3 start $(date +%T)" >> $O
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars229f.sh; cat Saved/Codex/SHME_V227_20261024/req/cap227.sh)" bash $T/ab_safe229.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
relaunch pr3 30
printf 'import builtins\nbuiltins.V229_PROMO = {"effort": True}
builtins.V229_EFFORT = {"EffortScaleMin": 0.7}\nbuiltins.V229_SAVE = True\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V229_20261025/promote229.py", encoding="utf8").read())\n' > $D/req/promo_fin3.py
bash $R $D/req/promo_fin3.py promo229c 600 > $D/promo_fin3.out 2>&1; grep -a "PROMO229" $D/promo_fin3.out | cut -c1-900 >> $O
relaunch vf3 30
printf 'import builtins\nbuiltins.V229_EXP = %s\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V229_20261025/verify_fin229.py", encoding="utf8").read())\n' "$G" > $D/req/verify_fin3_run.py
bash $R $D/req/verify_fin3_run.py verify229c 900 > $D/verify_fin3.out 2>&1; grep -a "VERIFY229" $D/verify_fin3.out | cut -c1-1200 >> $O
grep -aq '"ALL_OK": true' $D/verify_fin3.out || { echo "VERIFY229C_FAILED" >> $O; exit 1; }
relaunch fn3 30; export WARM=1
ab fn3 "s29_ws:o s29_ws_ph:o s29_cam:o s29_cam2:o s29_sa:o s29_dg:o s29_dbl:o s29_rel:o b_s2back:o b_cam180:o chain_sprint:o chain_sscut:o e29_chain:o e29_rest:o e29_load:o e29_recov:o e29_house:o c29_ad:o c29_wlook:o c29_diag:o c29_look:o c29_jlook:o c29_combo:o d_sprint:o a29_ang:o a29_angb:o" $D/vars229f.sh
ab fn3 "s29_swl08:o s29_swl10:o s29_swl12:o s29_swl14:o s29_swl16:o s29_swl20:o j29_swl10:o j29_swl14:o j29_swl20:o s29_wall:o s29_wstop:o e29_hitch:o j29_hitch:o" $D/vars229f.sh
ab fn3 "j24_ph0:o j24_ph3:o j24_sw_ph0:o j24_sw_ph2:o j24_rel:o j24_dbl:o j24_ad_ph0:o j24_m180w:o j23_m180:o r_cutrev_r:o s23_jstart:o taps:o ins_ws:o ins_ws2:o ter_drop_walk:o ter_drop_jog:o ter_step2:o ter_bump_jog:o ter_hill8_jog:o legs_slope_sprint:o map_r1:o map_r2:o" $D/vars229f.sh
ab fn3 "e29_chain:efoff e29_recov:efoff chain_sscut:efoff e29_rest:efoff e29_load:efoff" $D/vars229f.sh
echo "FIN3 evidence done $(date +%T)" >> $O
for F in 20 60 120; do relaunch h$F $F; export WARM=1; ab h$F "s29_cam:o e29_chain:o e29_load:o s29_swl14:o chain_sscut:o c29_ad:o c29_combo:o j24_rel:o j24_ph0:o j24_sw_ph2:o j24_dbl:o" $D/vars229f.sh; echo "FIN3 fps $F done $(date +%T)" >> $O; done
relaunch hrt real; export WARM=0
ab hrt "s29_cam:o" $D/vars229f.sh
export WARM=1; ab hrt "e29_chain:o e29_load:o s29_swl14:o c29_wlook:o j24_rel:o j24_sw_ph2:o map_r2:o" $D/vars229f.sh
echo FIN3_EVIDENCE_DONE >> $O
relaunch cap3 30; export WARM=1 CAPV="o"
capf 2.6 10.0 capfn3 "e29_chain:oS e29_chain:oG s29_cam:oS s29_cam:oG"
capf 1.6 13.4 capfn3 "c29_combo:oG c29_combo:oS"
capf 2.6 6.0 capfn3 "j24_rel:oS s29_cam2:oG"
capf 5.6 5.4 capfn3 "e29_load:oS e29_load:oG"
echo CAP3_DONE >> $O
