#!/bin/bash
# run234_fin.sh : V2.34 promotion (after the manual FIN_GO marker with the group list) -> clean reopen -> verify234 -> final evidence (30 FPS
# production + A/B/C/D) -> FPS 60 / 120 / 20 / real time (production + pre234 on the key chains) -> normal-speed captures (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V234_20261028; MD=$D/checkpoint/manifests
until grep -aq "^FIN_GO" $O; do sleep 30; done
PG=$(grep -a "^FIN_GO" $O | tail -1 | cut -d' ' -f2)
echo "FIN start $(date +%T) groups $PG (reason: promotion in a fresh fixed-30 editor)" >> $O
relaunch fin 30
MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py promo234 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/SHME/DA_SHM_Response_Default >> $O 2>&1
"$PY" -c "import sys; g=sys.argv[1].split(','); open('$D/req/promo234.py','w').write('import builtins\nbuiltins.V234_PROMO = %s\nbuiltins.V234_SAVE = True\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V234_20261028/promote234.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g})); open('$D/req/verify234.py','w').write('import builtins\nbuiltins.V234_EXP = %s\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V234_20261028/verify234.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g}))" "$PG"
SHME_KIND=write SHME_MANIFEST=$MD/promo234.json bash $R $D/req/promo234.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o 'PROMO234 {.*' $D/promo_fin.out | cut -c1-1500 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promotion not saved" >> $O; exit 1; }
echo "FINV start $(date +%T) (reason: clean reopen = verification on the disk state)" >> $O
relaunch finv 30
SHME_KIND=measure bash $R $D/req/verify234.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out | tail -1 >> $O
grep -a -o 'VERIFY234 {.*' $D/verify_fin.out | grep -q '"ALL_OK": true' || { echo "FIN_FAILED verify" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
S30="j30_slow j34_chain1 j30_rel_3200 j30_rel_3450 jstart wstart c29_combo e29_chain e29_load jback wdiag s29_swl12 s34_straight j34_sbcancel cam33_sturn cam33_wturn cam33_jturnj cam34_wflow cam34_jlook cam34_slook cam34_jcor cam34_jrot cam34_wdrift cam34_jrel cam32_chain cam32_wallturn cam_corr ins_ws cam33_back cam33_idlelook j34_back180 ter_drop_walk ter_step2 ter_drop_jog legs_slope_sprint map_r1"
J=""; for s in $S30; do J="$J $s:o"; done
for s in cam33_sturn cam33_wturn cam33_jturnj cam34_jlook cam34_wflow cam32_chain; do J="$J $s:pad234"; done
for s in cam33_sturn cam33_wturn c29_combo j30_rel_3200 j30_slow cam32_chain s34_straight; do J="$J $s:pre234 $s:body234 $s:cam234"; done
for s in cam33_sturn cam33_wturn; do J="$J $s:pre234p"; done
ab fin "$J" $D/vars234.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
SF="cam33_sturn cam33_wturn cam33_jturnj cam34_jlook c29_combo j30_rel_3200 j30_slow jstart e29_chain s34_straight"
for m in 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  J=""; for s in $SF; do J="$J $s:o $s:pre234"; done; for s in cam33_sturn cam33_wturn; do J="$J $s:pad234"; done
  ab f$m "$J" $D/vars234.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "CAP start $(date +%T) (reason: back to fixed 30 for the normal-speed captures)" >> $O
relaunch cap 30
{ echo "CAPV3='o pre234 pad234 pre234p'"; echo "CAP_START=3.0; CAP_SECS=9.5"; cat $D/vars234.sh; echo 'CAP="\"mcap\":{\"start\":${CAP_START:-3.8},\"seconds\":${CAP_SECS:-7.0},\"fps\":30,\"quality\":88}"'; cat Saved/Codex/SHME_V233_20261027/vars233_cap.sh; } > $D/vars234_capall.sh
export WARM=0
J="cam33_wturn:pre234pG cam33_wturn:pad234G cam33_sturn:pre234pG cam33_sturn:pad234G cam34_wflow:pad234G cam34_jlook:pad234G cam32_chain:pad234G"
J="$J s34_straight:pre234S s34_straight:oS j30_rel_3200:pre234S j30_rel_3200:oS j30_slow:oS c29_combo:pre234S c29_combo:oS"
ab cap "$J" $D/vars234_capall.sh
echo "CAP_DONE $(date +%T)" >> $O
