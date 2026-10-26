#!/bin/bash
# run230_p0.sh : V2.30 phase 0 - post-cleanup safety + memory study. One fresh editor: production verify (V2.29 expectations),
# dependency integrity of the live locomotion owners, memory samples fresh / after GC, then the SAME short scenario (j24_ph0, production)
# 8x with a sample after every run (no GC), a GC sample, 8x more with GC samples, a final GC sample. Memory guard raised to 50 GB for the study.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; T=Tools/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh
step() { echo "== $2 $(date +%T)" >> $O; bash $R "$1" "$2" "${3:-900}" > $D/$2.out 2>&1; grep -a "$4" $D/$2.out | cut -c1-1500 >> $O; }
echo "P0 start $(date +%T)" >> $O
relaunch p0 30
step $D/req/mp_fresh.py mp_fresh 300 MEM230
step $D/req/verify_p0.py verify_p0 900 VERIFY229
step $T/integrity230.py integrity 900 INTEGRITY230
step $D/req/mp_fresh_gc.py mp_fresh_gc 300 MEM230
export WARM=0 MEMCAP_GB=50 MEMPROBE=1 MEMPROBE_GC=False
J=""; for i in 1 2 3 4 5 6 7 8; do J="$J j24_ph0:o:$i"; done
ab mem "$J" $D/vars230.sh
step $D/req/mp_after8_gc.py mp_after8_gc 300 MEM230
export MEMPROBE_GC=True
J=""; for i in 9 10 11 12 13 14 15 16; do J="$J j24_ph0:o:$i"; done
ab mem "$J" $D/vars230.sh
step $D/req/mp_after16_gc.py mp_after16_gc 300 MEM230
echo "P0_DONE $(date +%T)" >> $O
