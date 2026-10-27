#!/bin/bash
# run233_s.sh : V2.33 5E sprint attitude candidate (after X_DONE, same fixed-30 editor): dry -> exact write manifest (new copies + DB) ->
# write -> o vs sc (ABP SHM211_DB_Sprint -> the calm DB) on sprint cases, 2 repeats; upper232 posture audit after.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
until grep -aq "X_DONE" $O; do sleep 30; done
echo "S start $(date +%T)" >> $O
out=$(SHME_KIND=measure bash $R $D/req/sc_dry.py sc_dry2 900); echo "$out" | grep -a "SC233" | cut -c1-1500 >> $O
names=$(echo "$out" | grep -a "SC233" | "$PY" -c "import sys,json; d=json.loads(sys.stdin.read().split('SC233 ',1)[1]); print(' '.join('/Game/GraceRanger/SHME/Animations/V233/SprintCalm/SHM233_Calm_'+n for n in d['clips']))")
[ -n "$names" ] || { echo "S_FAILED no clips" >> $O; exit 1; }
MSYS_NO_PATHCONV=1 "$PY" $T/manifest233.py sprintcalm --new $names /Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm >> $O 2>&1
SHME_KIND=write SHME_MANIFEST=$MD/sprintcalm.json bash $R $D/req/sc_write.py sc_write 1500 | grep -a "SC233\|GUARD\|REFUSED\|Traceback" | cut -c1-2500 >> $O
grep -a "^SC233" $O | tail -1 | grep -q '"saved_db": true' || { echo "S_FAILED write" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J="d_sprint:sc:0"; for s in d_sprint cam33_sturn cam32_chain legs_slope_sprint cam32_s90 s29_swl12; do for rp in 1 2; do J="$J $s:o:$rp $s:sc:$rp"; done; done
ab s "$J" $D/vars233.sh
echo "S_DONE $(date +%T)" >> $O
