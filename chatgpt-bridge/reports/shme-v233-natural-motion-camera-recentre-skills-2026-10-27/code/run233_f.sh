#!/bin/bash
# run233_f.sh : V2.33 combined candidate Q (stand-back start + auto recentre) vs production o: fixed 30 (2 rep) and the FPS modes
# 60 / 120 / 20 / real time (1 rep each; the FPS mode is an editor launch argument -> one relaunch per mode, reason logged).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
S="j30_slow jback d_back k_jogback j30_rel_3200 jstart wstart c30_calm cam33_wturn cam33_jturn cam33_sturn cam33_look cam33_back cam33_idlelook cam32_wallturn ins_ws"
for m in 30 60 120 20 real; do
  echo "F start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch f$m $m
  export WARM=1 MEMPROBE=1
  J="j30_slow:Q:0"; for s in $S; do if [ $m = 30 ]; then J="$J $s:o:1 $s:Q:1 $s:o:2 $s:Q:2"; else J="$J $s:o $s:Q"; fi; case $s in cam33_*) J="$J $s:Qp:1";; esac; done
  ab f$m "$J" $D/vars233.sh
  echo "F_DONE $m $(date +%T)" >> $O
done
echo "FALL_DONE $(date +%T)" >> $O
