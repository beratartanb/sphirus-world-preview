#!/bin/bash
# run237_s1.sh : V2.37 stage A/B: write the starts + representative re-push, build the candidate DBs, smoke, broken + sound A/B (same editor)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
V7=/Game/GraceRanger/SHME/Animations/V237; V6=/Game/GraceRanger/SHME/Animations/V236
CL="$V7/SHM237_JogStart_F_Lfoot $V7/SHM237_JogStart_F_Rfoot $V7/SHM237_RePush_Br_P00_T038"
echo "S1 start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py st1 --new $CL | tail -1 | cut -c1-200 >> $O
sed 's/'"'"'dry_run'"'"': True/'"'"'dry_run'"'"': False/' $D/req/gst_dry.py > $D/req/gst_w1.py
SHME_KIND=write SHME_MANIFEST=$MD/st1.json bash $R $D/req/gst_w1.py gstw1 900 > $D/last_gstw1.out 2>&1
grep -a -o 'G237ST {.*' $D/last_gstw1.out | grep -o '"saved": [a-z]*' | tr '\n' ' ' >> $O; echo >> $O
[ "$(grep -a -o '"saved": true' $D/last_gstw1.out | wc -l)" = 3 ] || { echo "S1_FAILED write" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py db1 --assets $CL --new $V7/PSD_SHM237_JogStartS_L $V7/PSD_SHM237_JogStartS_R $V7/PSD_SHM237_JogResume | tail -1 | cut -c1-200 >> $O
printf "import builtins\nbuiltins.V237_DB = {'dry': False, 'repush': ['$V7/SHM237_RePush_Br_P00_T038']}\nexec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V237_20261029/build237_dbs.py', encoding='utf8').read())\n" > $D/req/db1.py
SHME_KIND=write SHME_MANIFEST=$MD/db1.json bash $R $D/req/db1.py db1 900 > $D/last_db1.out 2>&1
grep -a -o 'DB237 {.*' $D/last_db1.out | cut -c1-900 >> $O
grep -aq '"entries"' $D/last_db1.out || { echo "S1_FAILED db" >> $O; exit 1; }
echo "S1 AB $(date +%T) (first candidate run = DB warm-up, discarded)" >> $O
export WARM=1
ab s1 "j36_wjs:s7:0 j36_wjs:o j36_wjs:s7 j34_chain1:o j34_chain1:s7 j36_rsm:o j36_rsm:s7 j36_stop:o j36_stop:s7 jstart:o jstart:s7 j36_wjs:s7:2 j34_chain1:s7:2" $D/vars237.sh
echo "S1_DONE $(date +%T)" >> $O
