#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_g.out; source $D/lib255.sh
MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|ROUTE255|DB255" | head -5 | cut -c1-900 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "G_FAILED $2 $(date +%T)" >> $O; exit 1; }; }
step Tools/SHME_V21_20261014/revert_noquit.py revert SHME_KIND=control
step $D/req/route_req.py route "SHME_KIND=write SHME_MANIFEST=$MD/v255_route.json"
grep -a "ROUTE255" $D/data/last_route.out | grep -q '"ok": true' || { echo "G_FAILED route" >> $O; exit 1; }
step $D/req/g3w_req.py g3w "SHME_KIND=write SHME_MANIFEST=$MD/v255_g3.json"
step $D/req/db3_req.py db3 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g3.json"
WARM=1 ab g60 "s54_revR:c2 s54_revL:c2 j54_rev:c2 s54_revR:c2 s54_revL:c2 j54_rev:c2 j54_r135:c2 s54_r135:c2 fz_sprint_a:c2 fz_sprint_m:c2 fz_jog_a:c2 fz_jog_m:c2" $D/vars255.sh
echo TG255_DONE >> $O
