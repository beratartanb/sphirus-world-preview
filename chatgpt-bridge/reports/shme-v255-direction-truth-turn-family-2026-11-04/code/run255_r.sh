#!/bin/bash
# run255_r.sh : V2.55 shorter cut brake (a0 / c_brake), rebuild the four cut clips + all DBs, then the full comparison run255_q
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_r.out; source $D/lib255.sh
export V219_EDARGS="-UseFixedTimeStep -FPS=60"; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; V21=Tools/SHME_V21_20261014
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|DB255|LEG_GUARD|write_error" | head -5 | cut -c1-320 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "R_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
until ! ps -ef | grep -q "[v]212_run"; do sleep 5; done
relaunch r1 60
step $V21/revert_noquit.py revert SHME_KIND=control
step $D/req/g4w_req.py g11b "SHME_KIND=write SHME_MANIFEST=$MD/v255_g11.json"
grep -aq "write_error\|\"error\"" $D/data/last_g11b.out && { echo "R_FAILED clip write" >> $O; exit 1; }
step $D/req/db5_req.py db11 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g11.json"
echo R_BUILD_OK >> $O
bash $D/run255_q.sh
echo TR255_DONE >> $O
