#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out
echo "REG start $(date +%T)" >> $O
WARM=1 ab reg " j38_c90r:o j38_c90r:cut3 j38_c90l:o j38_c90l:cut3 j38_c45r:o j38_c45r:cut3 j38_c135r:o j38_c135r:cut3 j38_cc90:o j38_cc90:cut3 w38_c90r:o w38_c90r:cut3 s38_c90r:o s38_c90r:cut3 s38_c90l:o s38_c90l:cut3 jdiag:o jdiag:cut3 jswap:o jswap:cut3 jlean:o jlean:cut3 ad_jog:o ad_jog:cut3 chain_jogcut:o chain_jogcut:cut3 mt_jog:o mt_jog:cut3 mtf_jog:o mtf_jog:cut3 cam32_j90:o cam32_j90:cut3 j36_stop:o j36_stop:cut3 j36_rsm:o j36_rsm:cut3 j36_wjs:o j36_wjs:cut3 j36_sside:o j36_sside:cut3 j35_rev:o j35_rev:cut3 j30_rel_3450:o j30_rel_3450:cut3 j34_chain1:o j34_chain1:cut3 jstart:o jstart:cut3 e29_chain:o e29_chain:cut3 c29_combo:o c29_combo:cut3 j36_stopr:o j36_stopr:cut3 ter_drop_jog:o ter_drop_jog:cut3"
echo "REG_DONE $(date +%T)" >> $O
