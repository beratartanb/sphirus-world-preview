#!/bin/bash
# run235_fin.sh : V2.35 promotion (after the manual FIN_GO marker with the group list) -> clean reopen -> verify235 -> final evidence (30 FPS
# production + pre235 + A/B/C/D) -> FPS 60 / 120 / 20 / real time on the key chains -> normal-speed captures (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; export O=$D/chain.out; source $D/lib235.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V235_20261028; MD=$D/checkpoint/manifests
until grep -aq "^FIN_GO" $O; do sleep 30; done
PG=$(grep -a "^FIN_GO" $O | tail -1 | cut -d' ' -f2)
echo "FIN start $(date +%T) groups $PG (reason: promotion in a fresh fixed-30 editor)" >> $O
relaunch fin 30
MSYS_NO_PATHCONV=1 "$PY" $T/manifest235.py promo235 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/SHME/DA_SHM_Response_Default /Game/GraceRanger/BP_GR_Player >> $O 2>&1
"$PY" -c "import sys; g=sys.argv[1].split(','); open('$D/req/promo235.py','w').write('import builtins\nbuiltins.V235_PROMO = %s\nbuiltins.V235_SAVE = True\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V235_20261028/promote235.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g})); open('$D/req/verify235.py','w').write('import builtins\nbuiltins.V235_EXP = %s\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V235_20261028/verify235.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g}))" "$PG"
SHME_KIND=write SHME_MANIFEST=$MD/promo235.json bash $R $D/req/promo235.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o 'PROMO235 {.*' $D/promo_fin.out | cut -c1-1500 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promotion not saved" >> $O; exit 1; }
echo "FINV start $(date +%T) (reason: clean reopen = verification on the disk state)" >> $O
relaunch finv 30
SHME_KIND=measure bash $R $D/req/verify235.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out | tail -1 >> $O
grep -a -o 'VERIFY235 {.*' $D/verify_fin.out | grep -q '"ALL_OK": true' || { echo "FIN_FAILED verify" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
S30="j35_rev j35_rev2 j35_relstop j30_rel_3200 j30_rel_3450 j30_slow j34_chain1 jstart wstart c29_combo e29_chain e29_load jback wdiag s29_swl12 s34_straight cam33_sturn cam33_wturn cam33_jturnj cam34_wflow cam34_jlook cam33_back cam32_chain cam_corr ins_ws cam33_idlelook ter_drop_walk ter_step2 ter_drop_jog map_r1"
J=""; for s in $S30; do J="$J $s:o"; done
for s in cam33_sturn cam33_wturn cam34_wflow cam34_jlook cam32_chain; do J="$J $s:pad235"; done
for s in j35_rev j35_rev2 j35_relstop j30_rel_3200 j30_slow j34_chain1 jstart c29_combo e29_chain e29_load s29_swl12 cam33_wturn cam33_sturn; do J="$J $s:pre235"; done
for s in j35_rev j30_rel_3200 cam33_wturn cam33_sturn; do J="$J $s:body235 $s:cam235"; done
ab fin "$J" $D/vars235.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
SF="j35_rev j35_rev2 j30_rel_3200 j30_slow j34_chain1 jstart c29_combo e29_chain s29_swl12 cam33_wturn"
for m in 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  J=""; for s in $SF; do J="$J $s:o $s:pre235"; done
  ab f$m "$J" $D/vars235.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "CAP start $(date +%T) (reason: back to fixed 30 for the normal-speed captures)" >> $O
relaunch cap 30
{ echo "CAPV3='o pre235 pad235'"; echo "CAP_START=3.0; CAP_SECS=10.5"; cat $D/vars235.sh $D/capblock235.sh; } > $D/vars235_capfin.sh
export WARM=1
J="j35_rev:oS j35_rev:pre235S j35_rev:oG j35_rev2:oS j30_slow:oS j34_chain1:oS j30_rel_3200:oS j30_rel_3200:pre235S cam33_wturn:oG cam33_wturn:pre235G cam34_wflow:pad235G j35_rev:oD"
ab cap "$J" $D/vars235_capfin.sh
echo "CAP_DONE $(date +%T)" >> $O
