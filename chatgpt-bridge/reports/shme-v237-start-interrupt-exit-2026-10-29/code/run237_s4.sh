#!/bin/bash
# run237_s4.sh : V2.37 start + re-push regenerated with the FootPlacement pelvis curve, re-push family from the V237 stops, DBs rebuilt, then
# the combined candidate s8 vs production o over the chain set (fixed 30)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
V7=/Game/GraceRanger/SHME/Animations/V237; ST="$V7/SHM237_JogStart_F_Lfoot $V7/SHM237_JogStart_F_Rfoot"
echo "S4 start $(date +%T)" >> $O
SHME_KIND=measure bash $R $D/req/grp_dry.py grpd4 1800 > $D/last_grpd4.out 2>&1
"$PY" -c "
import json; c=json.load(open('$D/gen237_start_dry.json'))['clips']; ok={n:v for n,v in c.items() if 'error' not in v}
bad=[n for n,v in ok.items() if v['foot_err']>6 or v['pelvis_drop_max']>3 or v['entry_err']>0.5 or max(v['planted_drift'].values())>3]
print('REPUSH4_DRY n=%d err=%d bad=%d %s' % (len(c), len(c)-len(ok), len(bad), bad[:5]))" >> $O
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py st2 --assets $ST $V7/SHM237_RePush_Br_P00_T038 $(cat $D/repush_paths.txt) | tail -1 | cut -c1-160 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/st2.json bash $R $D/req/gst_w2.py gstw2 900 > $D/last_gstw2.out 2>&1; cp $D/gen237_start_write.json $D/gen237_start_write_st2.json
echo "START_WRITE2 saved=$(grep -a -o '"saved": true' $D/last_gstw2.out | wc -l)" >> $O
SHME_KIND=write SHME_MANIFEST=$MD/st2.json bash $R $D/req/grp_w.py grpw4 1800 > $D/last_grpw4.out 2>&1; cp $D/gen237_start_write.json $D/gen237_repush_write4.json
n=$(grep -a -o '"saved": true' $D/last_grpw4.out | wc -l); echo "REPUSH_WRITE4 saved=$n" >> $O; [ "$n" = 96 ] || { echo "S4_FAILED repush write" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py db4 --assets $V7/PSD_SHM237_JogResume $V7/PSD_SHM237_JogStartS_L $V7/PSD_SHM237_JogStartS_R $ST $V7/SHM237_RePush_Br_P00_T038 $(cat $D/repush_paths.txt) | tail -1 | cut -c1-160 >> $O
sed "s/'groups': \['resume'\]/'groups': ['start_L', 'start_R', 'resume']/" $D/req/db2.py > $D/req/db4.py
SHME_KIND=write SHME_MANIFEST=$MD/db4.json bash $R $D/req/db4.py db4 1800 > $D/last_db4.out 2>&1
grep -a -o '"entries": \[[^]]*\]' $D/last_db4.out | while read l; do echo "$l" | grep -o 'SHM237' | wc -l; done | tr '\n' ' ' >> $O; echo >> $O
grep -aq '"entries"' $D/last_db4.out || { echo "S4_FAILED db4" >> $O; exit 1; }
echo "S4 AB $(date +%T) (warm-ups: one run per candidate DB group, discarded)" >> $O
export WARM=1
J="j36_rsm:s8:0 j36_wjs:s8:0 j36_stopr:s8:0"
for s in j36_wjs j34_chain1 j36_rsm j36_rse j36_rsl j36_rsx j36_stop j36_stopb j36_stopr j36_sside jstart c29_combo e29_chain e29_load j30_rel_3450 j35_rev jback wdiag ter_drop_jog map_r1; do J="$J $s:o $s:s8"; done
ab s4 "$J" $D/vars237.sh
echo "S4_DONE $(date +%T)" >> $O
