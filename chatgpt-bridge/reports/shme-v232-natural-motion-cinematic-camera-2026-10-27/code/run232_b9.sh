#!/bin/bash
# run232_b9.sh : V2.32 B9 (same editor, after B8_DONE): tick order through the existing flag IntentTickPrePhysics (itp) vs production o,
# incl. the stop stages that regressed in V2.0 (stopphase / jstopphase: +4-13 cm then).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B8_DONE" $O; do sleep 30; done
export WARM=0 MEMPROBE=1
J=""; for v in o itp; do for s in stopphase jstopphase e29_load e31_s2_4750 j30_slow c29_combo; do J="$J $s:$v"; done; done
ab b9 "$J" $D/vars232.sh
echo "B9_DONE $(date +%T)" >> $O
