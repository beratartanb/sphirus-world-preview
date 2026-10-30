#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out
echo "C5B start $(date +%T)" >> $O
WARM=1 ab c5 "j38_c90r:cut2 j38_c90r:cut3 j38_c90l:cut3 j38_c90r:o mt_jog:o mt_jog:gz"
ab c5 "j38_c90r:cut3S j38_c90l:cut3S j38_c90r:cut3G" $D/vars238_cap.sh
echo "C5B_DONE $(date +%T)" >> $O
