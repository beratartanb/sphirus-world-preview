#!/bin/bash
# run232_b8.sh : V2.32 SW + B8 (same editor, after B7_DONE): D closing-step clearance written IN PLACE on the owned stop clips (minclear:
# ball >= planted + 2.5 cm from 3 cm after lift-off to 3 cm before landing; checkpoint pre_v232/.../Stops), then the walk-stop set again
# (the before = the same scenarios earlier in this session: S1 / B2 / B4 o runs).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B7_DONE" $O; do sleep 30; done
bash $R $D/req/sf_write.py sfw 1500 > $D/sf_write.out 2>&1; echo "SW $(grep -a -o 'SF232 {.\{0,400\}' $D/sf_write.out | head -1)" >> $O
grep -aq "LEG_GUARD_FAIL\|Traceback" $D/sf_write.out && echo "SW_WARN guard/traceback in sf_write.out" >> $O
export WARM=1 MEMPROBE=1
J=""; for s in c30_calm wstart wdiag c29_combo a29_angb cam32_w45 cam32_look stopphase taps; do J="$J $s:o"; done
ab b8 "$J" $D/vars232.sh
echo "B8_DONE $(date +%T)" >> $O
