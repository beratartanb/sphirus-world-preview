#!/bin/bash
# run255_o.sh : V2.55 stage 1 of the final candidate: run-frame threshold 150 (component function), speed framing (pawn), knee over toes + swing floor + calmer sprint arms (clips), then a short look: 4 turns + side and game camera captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_o.out; source $D/lib255.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|FRAME255|CAMFN234|DB255|LEG_GUARD|write_error" | head -5 | cut -c1-360 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "O_FAILED $2 $(date +%T)" >> $O; exit 1; }; echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "O_FAILED $2 (build fail)" >> $O; exit 1; }; }
echo "O start $(date +%T)" >> $O
relaunch o1 60
step $V21/revert_noquit.py revert SHME_KIND=control
step $D/req/only255.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/v255_o.json"
step Tools/SHME_V234_20261028/probe234_camfn.py census SHME_KIND=measure
grep -a '"ok": true' $D/data/last_census.out | grep -q CAMFN234 || { echo "O_FAILED census" >> $O; exit 1; }
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/v255_o.json"
step $V2/only_all.py only_all SHME_KIND=control
step $D/req/frame_req.py frame "SHME_KIND=write SHME_MANIFEST=$MD/v255_o.json"
grep -a "FRAME255" $D/data/last_frame.out | grep -q '"ok": true' || { echo "O_FAILED frame" >> $O; exit 1; }
step $D/req/g3w_req.py g10a "SHME_KIND=write SHME_MANIFEST=$MD/v255_g10.json"
step $D/req/g4w_req.py g10b "SHME_KIND=write SHME_MANIFEST=$MD/v255_g10.json"
grep -aq "write_error\|\"error\"" $D/data/last_g10a.out $D/data/last_g10b.out && { echo "O_FAILED clip write" >> $O; exit 1; }
step $D/req/db5_req.py db10 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g10.json"
echo O_BUILD_OK >> $O
WARM=1 ab o60w "s54_revR:c7 s54_revL:c7 s54_r90:c7 s54_l90:c7 j54_rev:c7 j54_r90:c7 j38_c90l:c7" $D/vars255.sh
ab o60 "s54_revR:c7 s54_revL:c7 s54_r90:c7 j54_rev:c7 j54_r90:c7 fz_jog_m:c7 fz_sprint_m:c7" $D/vars255.sh
CAP_START=4.6 CAP_SECS=3.2 ab ocap "s54_revR:c7S s54_revR:c7G j54_rev:c7S j54_rev:c7G s54_r90:c7S j54_r90:c7S" $D/vars255.sh
echo TO255_DONE >> $O
