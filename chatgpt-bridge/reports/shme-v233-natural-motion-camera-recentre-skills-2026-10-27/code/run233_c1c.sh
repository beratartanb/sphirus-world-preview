#!/bin/bash
# run233_c1b.sh : V2.33 chain 1 stage 1 (same editor): o vs sbk2 (family-4 branch) vs sb22 (entry override), interleaved, 2 repeats.
# Broken: true-stand jog backward starts (j30_slow, jback, d_back, k_jogback). Sound counter-cases that must NOT change / must not pick
# the stand-back start: release-repress (j30_rel_3200 / 3450), walk backward (d_backw, k_walkback), turn / walk starts (jstart, wstart),
# calm walk (c30_calm).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
echo "C1C start $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J=""; for s in j30_slow jback d_back k_jogback jstart j30_rel_3200 j30_rel_3450; do for rp in 1 2; do J="$J $s:o:$rp $s:sb22:$rp"; done; done
ab c1c "$J" $D/vars233.sh
echo "C1C_DONE $(date +%T)" >> $O
