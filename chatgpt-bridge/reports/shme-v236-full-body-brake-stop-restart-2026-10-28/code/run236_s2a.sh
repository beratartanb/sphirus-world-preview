#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2A start $(date +%T)" >> $O
ab s2a "j36_stop:s1 j36_stop:o j36_stopb:s1 j36_stopb:o j36_stop:s1:2 j36_stopb:o:2 j36_stopr:s1 j36_stopr:o j36_rsm:s1 j36_rsm:o j36_stop:s1S j36_stopb:s1S j36_stop:oS j36_stopb:oS" $D/vars236_cap.sh
echo "S2A_DONE $(date +%T)" >> $O
