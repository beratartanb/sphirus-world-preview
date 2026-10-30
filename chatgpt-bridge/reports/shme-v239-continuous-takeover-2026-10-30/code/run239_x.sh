#!/bin/bash
# V2.39 X: frame-rate modes for the candidate (o vs tk), then back to fixed 30
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out
echo "X start $(date +%T)" >> $O
J=""; for s in j39_rl j39_rw j39_lr j38_cc90 mtf_jog jlean j38_c90r j38_c90l j39_push_plan; do J="$J $s:o $s:tk"; done
for m in 60 120 20 real; do relaunch x$m $m; WARM=1 ab x$m "j39_rl:tk $J"; echo "X_DONE_MODE $m $(date +%T)" >> $O; done
relaunch xend 30
echo "X_DONE $(date +%T)" >> $O
