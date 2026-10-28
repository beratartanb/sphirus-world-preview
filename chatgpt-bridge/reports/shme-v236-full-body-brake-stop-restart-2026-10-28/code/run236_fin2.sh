#!/bin/bash
# run236_fin2.sh : the V2.36 final chain continued in the SAME clean finv editor after the verify filter fix (the first verify flagged only the deliberate V2.36 loaded DB value of the V2.31 contract; no write since the reopen).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V236_20261028; export O=$D/chain.out; source $D/lib236.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V236_20261028; MD=$D/checkpoint/manifests
echo "FINV2 start $(date +%T) (same clean finv editor, read-only verify)" >> $O
printf "import builtins\nbuiltins.V236_EXP = {'stop': True, 'start': True, 'rev': True, 'load': True, 'resume': False}\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V236_20261028/verify236.py', encoding='utf8').read())\n" > $D/req/verify236.py
SHME_KIND=measure bash $R $D/req/verify236.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out | tail -1 >> $O
grep -a -o 'VERIFY236 {.*' $D/verify_fin.out | grep -q '"ALL_OK": true' || { echo "FIN_FAILED verify" >> $O; exit 1; }
echo "COLD start $(date +%T) (first use of every V2.36 database in this clean editor, NO warm run)" >> $O
unset WARM; ab cold "j36_stop:o j35_rev:o e29_load:o j34_chain1:o" $D/vars236.sh
echo "COLD_DONE $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
S30="j36_stop j36_stopb j36_stopr j36_rse j36_rsm j36_rsl j36_rsx j36_wjs j36_wjsb j36_sside j35_rev j35_rev2 j35_relstop j30_rel_3200 j30_rel_3450 j30_slow j34_chain1 jstart wstart c29_combo e29_chain e29_load jback wdiag s29_swl12 s34_straight cam33_sturn cam33_wturn cam34_wflow cam33_back ter_drop_jog map_r1"
J=""; for s in $S30; do J="$J $s:o"; done
for s in cam33_sturn cam33_wturn cam34_wflow; do J="$J $s:pad235"; done
for s in j36_stop j36_stopb j36_stopr j36_rsl j36_wjs j36_wjsb j35_rev j35_rev2 j35_relstop j30_rel_3200 j30_rel_3450 j30_slow j34_chain1 jstart c29_combo e29_chain e29_load jback s29_swl12 cam33_wturn cam33_sturn; do J="$J $s:pre236"; done
ab fin "$J" $D/vars236.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
SF="j36_stop j36_stopb j36_stopr j36_wjs j35_rev j35_rev2 j30_rel_3200 j30_slow j34_chain1 jstart c29_combo e29_chain e29_load"
for m in 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  J=""; for s in $SF; do J="$J $s:o $s:pre236"; done
  ab f$m "$J" $D/vars236.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "CAP start $(date +%T) (reason: back to fixed 30 for the normal-speed captures)" >> $O
relaunch cap 30
{ echo "CAPV4='o pre236 pad235'"; echo "CAP_START=3.5; CAP_SECS=9.5"; cat $D/vars236.sh $D/capblock236.sh; } > $D/vars236_capfin.sh
export WARM=1
J="j36_stopr:oS j36_stopr:pre236S j36_stopr:oG j36_stopr:oD j36_stopb:oS j36_wjs:oS j36_wjs:pre236S j36_rsl:oS j35_rev:oS j35_rev:pre236S j35_rev:oG e29_load:oS e29_load:pre236S j34_chain1:oS j36_sside:oG"
ab cap "$J" $D/vars236_capfin.sh
echo "CAP_DONE $(date +%T)" >> $O
