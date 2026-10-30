#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "W start $(date +%T)" >> $O
WARM=1 ab reg "$(cat $D/reg_jobs.txt)"
echo "W_DONE $(date +%T)" >> $O
