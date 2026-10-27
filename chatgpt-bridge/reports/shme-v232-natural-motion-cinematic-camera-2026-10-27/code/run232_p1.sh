#!/bin/bash
# run232_p1.sh : V2.32 P1 (same editor as C1b, after C1_DONE and the P definition in vars232.sh): slow B_F X DB rebuilt with the jog loop,
# warm-up, then the combined candidate P vs production o INTERLEAVED per scenario, 2 repeats each (fixed 30) on the mandatory set.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "C1_DONE" $O && grep -aq "^cand P " $D/vars232.sh; do sleep 30; done
bash $R $D/req/up_write.py upw 1200 > $D/up_write.out 2>&1; echo "UPW $(grep -a -o 'UP232 {.\{0,600\}' $D/up_write.out | head -1)" >> $O
bash $R $D/req/bfx_write2.py bfxw2 1500 > $D/bfx_write2.out 2>&1; echo "BFX_WRITE2 $(grep -a -o 'RDB226 {.\{0,200\}' $D/bfx_write2.out | cut -c1-200)" >> $O
export WARM=1 MEMPROBE=1
J=""; for s in c30_calm cam32_chain cam32_s90 cam32_brk2 cam32_wallturn cam32_look cam32_w45 e29_load e29_chain e29_recov e31_s2_4750 e31_s2_4900 s29_swl12 j30_slow j30_rel_3200 j30_rel_3450 jback jstart c29_combo a29_angb ter_drop_walk ter_step2 legs_slope_sprint ins_ws map_r1 d_sprint; do for rp in 1 2; do J="$J $s:o:$rp $s:P:$rp"; done; done
ab p1 "$J" $D/vars232.sh
echo "P1_DONE $(date +%T)" >> $O
