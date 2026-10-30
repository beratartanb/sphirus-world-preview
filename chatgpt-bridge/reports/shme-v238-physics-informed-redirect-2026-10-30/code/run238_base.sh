#!/bin/bash
# V2.38 baseline: production (V2.37) on the new hard-turn scenarios, fixed 30, + side / game captures of the jog and sprint 90 cut
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out
echo "BASE start $(date +%T)" >> $O
relaunch base 30
WARM=1 ab base "w38_c90r:o j38_c90r:o j38_c90l:o s38_c90r:o s38_c90l:o j38_c45r:o j38_c135r:o j38_cc90:o"
ab base "j38_c90r:oS j38_c90r:oG s38_c90r:oS j38_c90l:oS" $D/vars238_cap.sh
echo "BASE_DONE $(date +%T)" >> $O
