#!/bin/bash
# run233_gates.sh : V2.33 gate proof in a fresh fixed-30 editor (reason: gated runner G1-G5 needs a new runner start)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V233_20261027/gatetest
M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/actref_current.json
echo "GATES2 start $(date +%T) (reason: first launch of the gated runner)" >> $O
relaunch gates2 30
r() { echo "-- $1" >> $O; shift; out=$("$@" 2>&1 | head -12); echo "$out" | grep -E "GATETEST|REFUSED|WRITE_GUARD|^OK|^ERROR|TIMEOUT" | head -4 | cut -c1-300 >> $O; }
r "T1 owner mismatch" env SHME_OWNER=other SHME_KIND=measure bash $R $T/t_save.py t_owner 60
r "T2 measure job saves" env SHME_KIND=measure bash $R $T/t_save.py t_measure 60
r "T3 write job without manifest" env SHME_KIND=write bash $R $T/t_save.py t_nomani 60
r "T4 write job with manifest (DA outside, A_CT_Ref inside)" env SHME_KIND=write SHME_MANIFEST=$M bash $R $T/t_save.py t_mani 60
# T5 = the V2.32 failure: a PIE run is going (qa_pie returns at once, PIE continues) and a DB write job is queued into it
( export WARM=0 MEMPROBE=0; cd Tools/SHME_V212_20261017 && bash v212_run.sh v233gate_c30_calm c30_calm '{}' ',"state_mode":"production"' > /dev/null 2>&1 ) &
for i in $(seq 1 60); do grep -aq "SHM_QA_SPAWNED v233gate_c30_calm" "Saved/Logs/$LR_LOG" 2>/dev/null && break; sleep 2; done
r "T5 DB write job queued during PIE" env SHME_KIND=write SHME_MANIFEST=$M bash $R $T/t_dbwrite.py t_pie 60
wait
r "T6 same DB write job after PIE ended" env SHME_KIND=write SHME_MANIFEST=$M bash $R $T/t_dbwrite.py t_after 60
M2=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/gt_create.json
r "T7 generator creates + bypass-saves an UNLISTED asset" env SHME_KIND=write SHME_MANIFEST=$M2 bash $R $T/t_create.py t_create 60
echo "-- cleanup manifest + delete scratch assets" >> $O; MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V233_20261027/manifest233.py gt_cleanup --assets /Game/_GateTest233/GT_Unlisted --new /Game/_GateTest233/GT_Listed /Game/_GateTest233 >> $O 2>&1
r "T8 cleanup (listed)" env SHME_KIND=write SHME_MANIFEST=Saved/Codex/SHME_V233_20261027/checkpoint/manifests/gt_cleanup.json bash $R $T/t_cleanup.py t_clean 60
echo "GATES2_DONE $(date +%T)" >> $O
