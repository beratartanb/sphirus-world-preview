#!/bin/bash
# run237_cb.sh : stop-entry continuing-bias candidates (cb10 / cb25) vs production o at 120 FPS (worst case) then 30 FPS (same scenarios)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh
export WARM=1
J="j36_stop:cb10:0 j36_stop:cb25:0 j36_stop:o j36_stop:cb10 j36_stop:cb25 j36_stopr:o j36_stopr:cb10 j36_stopr:cb25 j36_rse:o j36_rse:cb10 j36_rse:cb25 j36_rsl:o j36_rsl:cb10 j36_rsl:cb25 j36_stopb:o j36_stopb:cb10 j36_stopb:cb25 j36_wjs:o j36_wjs:cb10 j36_wjs:cb25 j36_rsm:o j36_rsm:cb10 j36_rsm:cb25"
for m in 120 30; do
  echo "CB start $m $(date +%T) (reason: stop-entry bin re-selection, bias candidates)" >> $O
  relaunch cb$m $m
  ab cb$m "$J" $D/vars237.sh
  echo "CB_DONE $m $(date +%T)" >> $O
done
