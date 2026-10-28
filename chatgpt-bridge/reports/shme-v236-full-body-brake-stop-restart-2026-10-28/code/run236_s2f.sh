#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2F start $(date +%T)" >> $O
ab s2f "j34_chain1:s2st j34_chain1:st j36_stopr:s2st j36_wjs:s2st j36_wjsb:s2st jstart:s2st jstart:st jstart:o j36_rsl:s2st j36_rsm:s2st j36_rse:s2st j36_sside:s2st j36_stop:s2st j36_stopb:s2st wstart:s2st wstart:o c29_combo:s2st c29_combo:o" $D/vars236_cap.sh
echo "S2F_DONE $(date +%T)" >> $O
