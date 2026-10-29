#!/bin/bash
# run237_s2.sh : V2.37 FootPlacement probe (read-only) + re-push family (96 links: 24 stop bins x re-press 0.10/0.26/0.42/0.58 s) into the
# candidate resume DB, then the re-press family A/B (early / mid / late / opposite / side, both brake feet) in the same editor
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
V7=/Game/GraceRanger/SHME/Animations/V237
echo "S2 start $(date +%T)" >> $O
SHME_KIND=measure bash $R $D/req/fp.py fp 600 > $D/last_fp.out 2>&1; grep -a -c 'FP237' $D/last_fp.out >> $O
SHME_KIND=measure bash $R $D/req/grp_dry.py grpd 1800 > $D/last_grpd.out 2>&1; cp $D/gen237_start_dry.json $D/gen237_repush_dry.json
"$PY" -c "
import json; d=json.load(open('$D/gen237_repush_dry.json'))
bad=[(n,c['foot_err'],c['ball_z_jump_max'],c['pelvis_drop_max']) for n,c in d['clips'].items() if c['foot_err']>6 or c['pelvis_drop_max']>3 or c['entry_err']>0.5]
print('REPUSH_DRY n=%d bad=%d %s' % (len(d['clips']), len(bad), bad[:6]))" >> $O
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py rp1 --new $(cat $D/repush_paths.txt) | tail -1 | cut -c1-160 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/rp1.json bash $R $D/req/grp_w.py grpw 1800 > $D/last_grpw.out 2>&1; cp $D/gen237_start_write.json $D/gen237_repush_write.json
n=$(grep -a -o '"saved": true' $D/last_grpw.out | wc -l); echo "REPUSH_WRITE saved=$n" >> $O
[ "$n" = 96 ] || { echo "S2_FAILED repush write" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py db2 --assets $V7/PSD_SHM237_JogResume $V7/SHM237_JogStart_F_Lfoot $V7/SHM237_JogStart_F_Rfoot $V7/SHM237_RePush_Br_P00_T038 $(cat $D/repush_paths.txt) | tail -1 | cut -c1-160 >> $O
"$PY" -c "
import json; p=open('$D/repush_paths.txt').read().split()
open('$D/req/db2.py','w').write('import builtins\nbuiltins.V237_DB = {\'dry\': False, \'groups\': [\'resume\'], \'repush\': %r}\nexec(open(r\'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/build237_dbs.py\', encoding=\'utf8\').read())\n' % (['$V7/SHM237_RePush_Br_P00_T038'] + p))"
SHME_KIND=write SHME_MANIFEST=$MD/db2.json bash $R $D/req/db2.py db2 1800 > $D/last_db2.out 2>&1
grep -a -o 'DB237 {.*' $D/last_db2.out | grep -o '"src_n": [0-9]*\|"bias": [-0-9.]*' | tr '\n' ' ' >> $O; grep -a -o '"entries": \[[^]]*\]' $D/last_db2.out | grep -o 'SHM237' | wc -l >> $O
grep -aq '"entries"' $D/last_db2.out || { echo "S2_FAILED db2" >> $O; exit 1; }
echo "S2 AB $(date +%T)" >> $O
export WARM=1
ab s2 "j36_rsm:s7:0 j36_rse:o j36_rse:s7 j36_rsm:o j36_rsm:s7 j36_rsl:o j36_rsl:s7 j36_rsx:o j36_rsx:s7 j36_sside:o j36_sside:s7 j36_stopb:o j36_stopb:s7 j36_wjsb:o j36_wjsb:s7 j36_rsm:s7:2 j36_rse:s7:2" $D/vars237.sh
echo "S2_DONE $(date +%T)" >> $O
