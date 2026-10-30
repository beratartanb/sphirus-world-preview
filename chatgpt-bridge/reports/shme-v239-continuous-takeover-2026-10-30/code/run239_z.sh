#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "Z start $(date +%T)" >> $O
relaunch z 30
SHME_KIND=measure bash $R $D/req/verify239.py verify239 1800 > $D/verify239_z.out 2>&1; grep -a -o "VERIFY239 .*" $D/verify239_z.out | cut -c1-1200 >> $O
echo "Z_DONE $(date +%T)" >> $O
