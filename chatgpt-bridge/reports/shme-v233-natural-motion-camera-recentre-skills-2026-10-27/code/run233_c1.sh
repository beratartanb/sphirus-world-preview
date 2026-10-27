#!/bin/bash
# run233_c1.sh : V2.33 chain 1 stage 1 (same editor telB; no relaunch: nothing to rebuild) - stand-back start sbk vs production o,
# broken cases (true-stand backward starts) + sound counter-cases (release-repress, turn / walk starts, calm walk), interleaved, 2 repeats.
# r0 = DB index warm-up of the new database (V2.30: an edited / new DB builds its index on first use) - not evaluated.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
echo "C1 start $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
J="j30_slow:sbk:0"; for s in j30_slow jback d_back j30_rel_3200 j30_rel_3450 jstart wstart c30_calm; do for rp in 1 2; do J="$J $s:o:$rp $s:sbk:$rp"; done; done
ab c1 "$J" $D/vars233.sh
echo "C1_DONE $(date +%T)" >> $O
