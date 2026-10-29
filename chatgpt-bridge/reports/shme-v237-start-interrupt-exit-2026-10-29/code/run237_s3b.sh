#!/bin/bash
# run237_s3b.sh : (V236 pelvis plan + curve only) V2.37 pelvis candidate: ABP FootPlacement DisablePelvisCurveName (no-op for production clips) + V237 stop family copy with
# the curve + its DB; o check (production unchanged after the ABP edit) + stop A/B with the pelvis chain
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
V7=/Game/GraceRanger/SHME/Animations/V237; AP=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase
echo "S3B start $(date +%T)" >> $O
SHME_KIND=measure bash $R $D/req/gstop_dry.py gstopd 1200 > $D/last_gstopd.out 2>&1
"$PY" -c "
import json; d=json.load(open('$D/gen237_stop_dry.json'))['clips']
print('STOP237_DRY n=%d foot_err %.1f drift %.1f entry %.1f drop %.1f pz_min %.1f' % (len(d), max(c['foot_err'] for c in d.values()), max(c['planted_drift'] for c in d.values()), max(c['entry_err'] for c in d.values()), max(c['reach_drop_max'] for c in d.values()), min(min(c['pelvis_z'][1:]) for c in d.values())))" >> $O
MSYS_NO_PATHCONV=1 "$PY" $T/true
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py stop2 --assets $(cat $D/stop237_paths.txt) | tail -1 | cut -c1-160 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/stop2.json bash $R $D/req/gstop_w.py gstopw 1800 > $D/last_gstopw.out 2>&1
n=$(grep -a -o '"saved": true' $D/last_gstopw.out | wc -l); echo "STOP237_WRITE saved=$n" >> $O; [ "$n" = 24 ] || { echo "S3B_FAILED stop write" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py sdb2 --assets $(cat $D/stop237_paths.txt) $V7/PSD_SHM237_JogStop | tail -1 | cut -c1-160 >> $O
"$PY" -c "
p=open('$D/stop237_paths.txt').read().split()
open('$D/req/sdb1.py','w').write('import builtins\nbuiltins.V237_SDB = {\'dry\': False, \'bias\': -3.0, \'clips\': %r}\nexec(open(r\'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/build237_stopdb.py\', encoding=\'utf8\').read())\n' % p)"
SHME_KIND=write SHME_MANIFEST=$MD/sdb2.json bash $R $D/req/sdb1.py sdb1 1200 > $D/last_sdb1.out 2>&1
grep -a -o 'SDB237_BIAS.*' $D/last_sdb1.out >> $O; grep -a -o '"entries": \[[^]]*\]' $D/last_sdb1.out | grep -o 'SHM237' | wc -l >> $O
grep -aq '"entries"' $D/last_sdb1.out || { echo "S3B_FAILED sdb" >> $O; exit 1; }
echo "S3B AB $(date +%T)" >> $O
export WARM=1
ab s3b "j36_stop:s8:0 j36_stop:o j36_stop:s7 j36_stop:s8 j36_stopb:s7 j36_stopb:s8 j36_stopr:s7 j36_stopr:s8 j36_wjs:s7 j36_wjs:s8 j36_rsm:s8 j36_rsl:s8 ter_drop_jog:s7 ter_drop_jog:s8 j36_stop:s8:2" $D/vars237.sh
echo "S3B_DONE $(date +%T)" >> $O
