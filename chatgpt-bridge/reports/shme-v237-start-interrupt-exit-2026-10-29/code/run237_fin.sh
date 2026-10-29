#!/bin/bash
# run237_fin.sh : V2.37 promotion (start, resume, stop) in a fresh fixed-30 editor -> clean reopen -> verify237 -> cold first use (no warm)
# -> final evidence 30 FPS (o vs pre237 + gamepad + camera off) -> FPS 60 / 120 / 20 / real -> normal-speed captures (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
echo "FIN start $(date +%T) groups start,resume,stop (reason: promotion in a fresh fixed-30 editor)" >> $O
relaunch fin 30
AP=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py promo237 --assets $AP ${AP/Base/} | tail -1 | cut -c1-160 >> $O
printf "import builtins\nbuiltins.V237_PROMO = {'stop': True, 'start': True, 'resume': True}\nbuiltins.V237_SAVE = True\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/promote237.py', encoding='utf8').read())\n" > $D/req/promo237.py
SHME_KIND=write SHME_MANIFEST=$MD/promo237.json bash $R $D/req/promo237.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o 'PROMO237 {.*' $D/promo_fin.out | cut -c1-1500 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promotion not saved" >> $O; exit 1; }
echo "FINV start $(date +%T) (reason: clean reopen = verification on the disk state)" >> $O
relaunch finv 30
printf "import builtins\nbuiltins.V237_EXP = {'stop': True, 'start': True, 'resume': True}\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/verify237.py', encoding='utf8').read())\n" > $D/req/verify237.py
SHME_KIND=measure bash $R $D/req/verify237.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out | tail -1 >> $O
grep -a -o 'VERIFY237 {.*' $D/verify_fin.out | grep -q '"ALL_OK": true' || { echo "FIN_FAILED verify" >> $O; exit 1; }
echo "COLD start $(date +%T) (first use of every V2.37 database in this clean editor, NO warm run)" >> $O
unset WARM; ab cold "j36_stop:o j36_rsm:o j36_wjs:o j34_chain1:o j35_rev:o" $D/vars237.sh
echo "COLD_DONE $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
S30="j36_stop j36_stopb j36_stopr j36_rse j36_rsm j36_rsl j36_rsx j36_wjs j36_wjsb j36_sside j35_rev j35_rev2 j35_relstop j30_rel_3200 j30_rel_3450 j30_slow j34_chain1 jstart wstart c29_combo e29_chain e29_load jback wdiag s29_swl12 s34_straight cam33_sturn cam33_wturn cam34_wflow cam33_back ter_drop_jog map_r1"
J=""; for s in $S30; do J="$J $s:o"; done
for s in cam33_sturn cam33_wturn cam34_wflow; do J="$J $s:pad235"; done
for s in j36_stopr cam34_wflow cam33_sturn; do J="$J $s:camoff"; done
for s in j36_stop j36_stopb j36_stopr j36_rse j36_rsm j36_rsl j36_rsx j36_wjs j36_wjsb j36_sside j35_rev j35_rev2 j30_rel_3450 j34_chain1 jstart c29_combo e29_chain e29_load jback ter_drop_jog cam33_wturn cam33_sturn; do J="$J $s:pre237"; done
ab fin "$J" $D/vars237.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
SF="j36_stop j36_stopr j36_rsm j36_wjs j34_chain1 j35_rev j30_rel_3450 jstart c29_combo e29_chain e29_load j36_sside"
for m in 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  J=""; for s in $SF; do J="$J $s:o $s:pre237"; done
  ab f$m "$J" $D/vars237.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "CAP start $(date +%T) (reason: back to fixed 30 for the normal-speed captures)" >> $O
relaunch cap 30
{ echo "CAPV4='o pre237 pad235'"; echo "CAP_START=3.5; CAP_SECS=9.5"; cat $D/vars237.sh Saved/Codex/SHME_V236_20261028/capblock236.sh; } > $D/vars237_capfin.sh
export WARM=1
J="j36_stopr:oS j36_stopr:pre237S j36_stopr:oG j36_stopr:oD j36_stopb:oS j36_wjs:oS j36_wjs:pre237S j36_rsm:oS j36_rsm:pre237S j36_rse:oS j36_rsl:oS j36_rsx:oS j35_rev:oS j35_rev:pre237S e29_load:oS j34_chain1:oS j36_sside:oG j36_sside:oS"
ab cap "$J" $D/vars237_capfin.sh
echo "CAP_DONE $(date +%T)" >> $O
