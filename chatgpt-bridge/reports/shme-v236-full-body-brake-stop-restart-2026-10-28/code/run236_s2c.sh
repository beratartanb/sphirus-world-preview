#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2C start $(date +%T)" >> $O
ab s2c "j36_stop:s2 j36_stop:s2:2 j36_stopb:s2 j36_stopb:s2:2 j36_stopr:s2 j36_rse:s2 j36_rse:o j36_rsm:s2 j36_rsl:s2 j36_rsl:o j36_rsx:s2 j36_rsx:o j36_wjs:s2 j36_wjs:o j36_wjsb:s2 j36_wjsb:o j36_sside:s2 j36_sside:o jstart:s2 jstart:o j34_chain1:s2 j34_chain1:o j36_stop:s2S j36_stopb:s2S j36_stopr:s2S j36_stop:s2G" $D/vars236_cap.sh
echo "S2C_DONE $(date +%T)" >> $O
