#!/bin/bash
# run229_fin.sh "<groups>" "<effort dict>" : V2.29 final chain. 1) pre-switch captures (production o = V2.28 + RevTurn fix) and the
# body/camera 2x2 on the same editor; 2) promote229 (save) -> CLEAN reopen verify_fin229 (ALL_OK gate) -> production evidence (fixed 30)
# -> FPS 20 / 60 / 120 -> real time (cold first) -> after-switch captures.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
G="${1:-{\}}"; EFD="${2:-{\}}"; D=Saved/Codex/SHME_V229_20261025; T=Tools/SHME_V229_20261025; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib229.sh
echo "FIN start groups=$G effort=$EFD $(date +%T)" >> $O
# ---- 1) pre-switch: 2x2 body/camera telemetry + captures of the reference
relaunch pre 30; export WARM=1
ab pre "c29_combo:o c29_combo:bn c29_combo:cn c29_combo:fin e29_chain:o e29_chain:bn e29_chain:cn e29_chain:fin e29_rest:o e29_rest:fin" $D/vars229f.sh
capf() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export CAP_START=$1 CAP_SECS=$2; TAG=$3 JOBS="$4" EXTRA_VARS="$(cat $D/vars229f.sh; cat Saved/Codex/SHME_V227_20261024/req/cap227.sh)" bash $T/ab_safe229.sh 2>&1 | grep -a " | rows\|REFUSED\|MEM\|GONE" >> $O; }
export CAPV="o fin"
capf 2.6 10.0 cappre "e29_chain:oS e29_chain:finS e29_chain:oG e29_chain:finG"
capf 1.6 13.4 cappre "c29_combo:oG c29_combo:finG c29_combo:oS c29_combo:finS"
capf 2.6 6.0 cappre "e29_rest:oS e29_rest:finS"
echo "FIN pre done $(date +%T)" >> $O
# ---- 2) switch + clean verify
relaunch pr 30
printf 'import builtins\nbuiltins.V229_PROMO = %s\nbuiltins.V229_EFFORT = %s\nbuiltins.V229_SAVE = True\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V229_20261025/promote229.py", encoding="utf8").read())\n' "$G" "$EFD" > $D/req/promo_fin.py
bash $R $D/req/promo_fin.py promo229 600 > $D/promo_fin.out 2>&1; grep -a "PROMO229" $D/promo_fin.out | cut -c1-900 >> $O
relaunch vf 30
printf 'import builtins\nbuiltins.V229_EXP = %s\nexec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V229_20261025/verify_fin229.py", encoding="utf8").read())\n' "$G" > $D/req/verify_fin_run.py
bash $R $D/req/verify_fin_run.py verify229 900 > $D/verify_fin.out 2>&1; grep -a "VERIFY229" $D/verify_fin.out | cut -c1-1200 >> $O
grep -aq '"ALL_OK": true' $D/verify_fin.out || { echo "VERIFY229_FAILED" >> $O; exit 1; }
# ---- 3) production evidence, fixed 30
relaunch fin 30; export WARM=1
ab fin "s29_ws:o s29_ws_ph:o s29_cam:o s29_cam2:o s29_sa:o s29_dg:o s29_dbl:o s29_rel:o b_s2back:o b_cam180:o chain_sprint:o chain_sscut:o e29_chain:o e29_rest:o e29_load:o e29_recov:o e29_house:o c29_ad:o c29_wlook:o c29_diag:o c29_look:o c29_jlook:o c29_combo:o d_sprint:o a29_ang:o a29_angb:o" $D/vars229f.sh
ab fin "j24_ph0:o j24_ph3:o j24_sw_ph0:o j24_sw_ph2:o j24_rel:o j24_dbl:o j24_ad_ph0:o j24_m180w:o j23_m180:o r_cutrev_r:o s23_jstart:o taps:o ins_ws:o ins_ws2:o ter_drop_walk:o ter_drop_jog:o ter_step2:o ter_bump_jog:o ter_hill8_jog:o legs_slope_sprint:o map_r1:o map_r2:o" $D/vars229f.sh
ab fin "e29_chain:efoff e29_recov:efoff chain_sscut:efoff e29_rest:efoff" $D/vars229f.sh
echo "FIN evidence done $(date +%T)" >> $O
for F in 20 60 120; do relaunch f$F $F; export WARM=1; ab f$F "s29_cam:o e29_chain:o chain_sscut:o c29_ad:o c29_combo:o j24_rel:o j24_ph0:o j24_sw_ph2:o" $D/vars229f.sh; echo "FIN fps $F done $(date +%T)" >> $O; done
relaunch frt real; export WARM=0
ab frt "s29_cam:o" $D/vars229f.sh
export WARM=1; ab frt "e29_chain:o c29_wlook:o j24_rel:o j24_sw_ph2:o map_r2:o" $D/vars229f.sh
echo FIN_EVIDENCE_DONE >> $O
relaunch cap 30; export WARM=1 CAPV="o"
capf 2.6 10.0 capfin "e29_chain:oS e29_chain:oG s29_cam:oS s29_cam:oG"
capf 1.6 13.4 capfin "c29_combo:oG c29_combo:oS"
capf 2.6 6.0 capfin "j24_rel:oS s29_cam2:oG"
echo CAP_DONE >> $O
