#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "C start $(date +%T)" >> $O
WARM=1 ab c "j39_rl:o j39_rl:tk j39_rw:o j39_rw:tk j38_cc90:tk j38_c90r:tk"
echo "C_DONE $(date +%T)" >> $O
