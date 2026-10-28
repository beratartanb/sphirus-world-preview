#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2B start $(date +%T)" >> $O
ab s2b "j36_stop:s1 j36_stop:s1:2 j36_stopb:s1 j36_stopr:s1 j36_rsm:s1 j36_rse:s1 j36_rsl:s1 j36_rsx:s1 j36_stop:s1S j36_stopb:s1S j36_stopr:s1S j36_stop:s1G" $D/vars236_cap.sh
echo "S2B_DONE $(date +%T)" >> $O
