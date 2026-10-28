#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2D start $(date +%T)" >> $O
ab s2d "j36_stop:s2 j36_stop:s2:2 j36_stopb:s2 j36_wjs:s2 j36_wjsb:s2 j36_stopr:s2 j36_rse:s2 j36_rsm:s2 j36_rsl:s2" $D/vars236_cap.sh
echo "S2D_DONE $(date +%T)" >> $O
