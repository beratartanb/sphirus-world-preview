#!/bin/bash
# run232_b10.sh : V2.32 B10 (same editor, after B9_DONE): B_F exit-loop databases (build_v232_bfx), warm-up, A/B bfx / bfxl vs o.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B9_DONE" $O; do sleep 30; done
bash $R $D/req/bfx_dry.py bfxd 900 > $D/bfx_dry.out 2>&1; echo "BFX_DRY $(grep -a -o 'RDB226 {.\{0,300\}' $D/bfx_dry.out)" >> $O
grep -aq '"missing": \[\]' $D/bfx_dry.out || { echo "B10_FAILED bfx missing" >> $O; exit 1; }
bash $R $D/req/bfx_write.py bfxw 1500 > $D/bfx_write.out 2>&1; echo "BFX_WRITE $(grep -a -o 'RDB226 {.\{0,600\}' $D/bfx_write.out | cut -c1-600)" >> $O
export WARM=1 MEMPROBE=1
J=""; for v in o bfx bfxl; do for s in e29_load e29_chain e31_s2_4750 e31_s2_4900 s29_swl12 j30_slow j24_ph0 j24_dbl w30_rev k_ws_clean; do J="$J $s:$v"; done; done
ab b10 "$J" $D/vars232.sh
echo "B10_DONE $(date +%T)" >> $O
