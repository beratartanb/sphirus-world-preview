#!/bin/bash
# run232_soak.sh : V2.32 IsUnique study (same editor as C1, after C1_DONE): 100 bare PIE cycles (no harness work at all), then 100 cycles
# with only the harness end-path calls; counts completed cycles from the log; an engine crash ends the editor (counted, then relaunched).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "C1_DONE\|C1_FAILED" $O; do sleep 30; done
for m in bare harness_end; do
  LOG="Saved/Logs/$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)")"; export LR_LOG=$(basename $LOG)
  c0=$(grep -a -c "SOAK232_DONE" $LOG); echo "SOAK_START $m $(date +%T) log $LR_LOG" >> $O
  bash $R $D/req/soak_$m.py soak_$m 120 > $D/soak_$m.out 2>&1
  for i in $(seq 1 720); do
    tasklist 2>/dev/null | grep -qi UnrealEditor.exe || { echo "SOAK_EDITOR_GONE $m after $(grep -a -c "SOAK232 n=.*mode=$m" $LOG) cycles; crash: $(grep -a -c 'GameViewport.IsUnique' $LOG) $(date +%T)" >> $O; relaunch soak_r 30; break; }
    [ $(grep -a -c "SOAK232_DONE" $LOG) -gt $c0 ] && { echo "SOAK_DONE $m cycles $(grep -a -c "SOAK232 n=.*mode=$m" $LOG) crash 0 $(date +%T)" >> $O; break; }
    sleep 5
  done
done
echo "SOAK_FIN $(date +%T)" >> $O
