#!/bin/bash
# run231_a3.sh : same editor: TIP-end install (fixed name match), A3 short tests (te, P in the fixed-30 editor)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; R="bash Tools/SHME_V2_20261014/run_v2.sh"; export O=$D/chain.out; source $D/lib231.sh
until grep -aq "B2_DONE" $O; do sleep 20; done
echo "A3 start $(date +%T)" >> $O
$R $D/req/tipend_save.py tipend 900 > $D/tipend.out 2>&1; grep -a -o "TIPEND231.*\|Traceback.*\|Error:.*" $D/tipend.out | cut -c1-600 >> $O
export WARM=0 MEMPROBE=1
J="legs_slope_sprint:te legs_slope_sprint:te:2 s29_cam:te c30_calm:te w30_rev:te"
for v in o P; do for s in s29_swl12 j30_rel_3100 e29_load c30_calm c29_combo s29_ws a29_angb ins_ws; do J="$J $s:$v"; done; done
ab a3 "$J" $D/vars231.sh
echo "A3_DONE $(date +%T)" >> $O
