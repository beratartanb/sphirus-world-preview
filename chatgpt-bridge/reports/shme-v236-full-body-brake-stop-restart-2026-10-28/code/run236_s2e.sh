#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2E start $(date +%T)" >> $O
ab s2e "j36_stop:s2 j36_stop:s2:2 j36_stopb:s2 j36_stopr:s2 j34_chain1:s2 j36_wjs:s2 j36_wjsb:s2 jstart:s2 j36_rse:s2 j36_rsm:s2 j36_rsl:s2 j36_rsx:s2 j36_sside:s2 j30_slow:s2 j30_slow:o j35_rev:s2 j35_rev:o" $D/vars236_cap.sh
echo "S2E_DONE $(date +%T)" >> $O
