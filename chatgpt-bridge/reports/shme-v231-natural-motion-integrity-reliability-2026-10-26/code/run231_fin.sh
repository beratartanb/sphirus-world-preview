#!/bin/bash
# run231_fin.sh : V2.31 production switch -> clean reopen verify -> production evidence (fixed 30) -> captures (test capture first).
# PROMO groups come from env PROMO (json), e.g. '{"slow": true, "exit": true, ...}'.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R="bash Tools/SHME_V2_20261014/run_v2.sh"; export O=$D/chain.out; source $D/lib231.sh; V=Saved/Codex/SHME_V138_20260927/Video
T="C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V231_20261026"
echo "FIN start $(date +%T) PROMO=$PROMO" >> $O
printf 'import builtins, json\nbuiltins.V231_PROMO = json.loads(%s)\nbuiltins.V231_SAVE = True\nexec(open(r"%s/promote231.py", encoding="utf8").read())\n' "'$PROMO'" "$T" > $D/req/promo_save.py
printf 'import builtins, json\nbuiltins.V231_EXP = json.loads(%s)\nexec(open(r"%s/verify231.py", encoding="utf8").read())\n' "'$PROMO'" "$T" > $D/req/verify_fin.py
relaunch fin 30
$R Tools/SHME_V21_20261014/revert_noquit.py revert 300 | grep -a "dirty after" >> $O
$R $D/req/promo_save.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o "PROMO231.*" $D/promo_fin.out | cut -c1-1500 >> $O
grep -a -q '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promo $(date +%T)" >> $O; exit 1; }
relaunch finv 30
$R $D/req/verify_fin.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o "VERIFY231.*" $D/verify_fin.out | cut -c1-2000 >> $O
grep -a -q '"ALL_OK": true' $D/verify_fin.out || { echo "FIN_FAILED verify $(date +%T)" >> $O; exit 1; }
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
