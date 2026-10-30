#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "A start $(date +%T)" >> $O
relaunch a 30
SHME_KIND=measure bash $R $D/req/tk_dry.py tk_dry 1800 > $D/last_tk_dry.out 2>&1; grep -a -E "G239TK|Error|Traceback" $D/last_tk_dry.out | cut -c1-1500 >> $O
echo "A_DONE $(date +%T)" >> $O
