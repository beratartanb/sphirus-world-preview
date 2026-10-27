#!/bin/bash
# run233_x.sh : V2.33 after FALL_DONE - fresh fixed-30 editor (reason: the FPS chain ends in a real-time editor): IS copies excluded from
# the active search (manifest), sprint-calm dry measure, K3 = o vs Q2 (Q + CamRecMaxErr 110) on the cases Q changed.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
until grep -aq "FALL_DONE" $O; do sleep 30; done
echo "X start $(date +%T) (reason: fixed-30 editor after the real-time FPS mode)" >> $O
relaunch x 30
out=$(SHME_KIND=measure bash $R $D/req/ex_dry.py ex_dry 600); echo "$out" | grep -a "EX233" | cut -c1-900 >> $O
pk=$(echo "$out" | grep -a -o '"copies": \[[^]]*\]' | grep -o "/Game/[^\"]*" | tr '\n' ' ')
[ -n "$pk" ] || { echo "X_FAILED no IS copies listed" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest233.py is_exclude --assets $pk >> $O 2>&1
SHME_KIND=write SHME_MANIFEST=$MD/is_exclude.json bash $R $D/req/ex_write.py ex_write 900 | grep -a "EX233\|GUARD\|REFUSED\|Traceback" | cut -c1-700 >> $O
SHME_KIND=measure bash $R $D/req/sc_dry.py sc_dry 900 | grep -a "SPRINTDB\|SC233\|Traceback" | cut -c1-2500 >> $O
export WARM=1 MEMPROBE=1
J="j30_slow:Q3:0"; for s in jback j30_rel_3200 cam33_wturn cam33_look cam33_back cam33_jturn cam33_sturn d_back j30_slow c30_calm cam32_wallturn; do J="$J $s:o $s:Q2 $s:Q3"; done
ab x "$J" $D/vars233.sh
echo "X_DONE $(date +%T)" >> $O
