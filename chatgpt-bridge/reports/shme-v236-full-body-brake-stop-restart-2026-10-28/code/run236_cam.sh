#!/bin/bash
# run236_cam.sh : camera on / off with the same V2.36 production body (camoff = CamRecEnabled false only) + mouse / gamepad recentre,
# after the final captures (same cap editor, fixed 30). Waits only on markers written after the FINV2 line of chain.out.
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
fin2() { sed -n '/FINV2 start/,$p' $O; }
until fin2 | grep -qE "CAP_DONE|RELAUNCH_FAILED"; do sleep 20; done
fin2 | grep -q "CAP_DONE" || exit 1
echo "CAMAB start $(date +%T) (same cap editor, fixed 30)" >> $O
export WARM=1
ab camab "cam33_sturn:o cam33_sturn:camoff j36_stopr:o j36_stopr:camoff j35_rev:o j35_rev:camoff cam33_wturn:o cam33_wturn:pad235" $D/vars236.sh
echo "CAMAB_DONE $(date +%T)" >> $O
