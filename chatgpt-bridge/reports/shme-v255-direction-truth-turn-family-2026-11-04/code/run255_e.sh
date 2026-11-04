#!/bin/bash
# run255_e.sh : V2.55 build: editor A component vars; editor B camera function (raw frame hand-over) + census + pawn + ABP patches; regenerate the sprint turn; smoke
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V255_20261104; export O=$D/run255_e.out; source $D/lib255.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V255_20261104; T3=Tools/SHME_V233_20261027; MD=Saved/Codex/SHME_V233_20261027/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/data/last_$2.out; echo "$out" | head -1 | cut -c1-200 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|PAWN255|ABP255|CAMFN234|G255|DB255" | head -5 | cut -c1-900 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "E_FAILED $2 $(date +%T)" >> $O; exit 1; }; echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "E_FAILED $2 (build fail)" >> $O; exit 1; }; }
echo "E start $(date +%T)" >> $O
relaunch e1 60
step $V21/revert_noquit.py revert SHME_KIND=control
step $V1/build_comp_vars.py comp_vars "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
step $V2/save_comp.py save_comp "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
step $T3/save_manifest_dirty.py smd "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
relaunch e2 60
step $V21/revert_noquit.py revert2 SHME_KIND=control
step $D/req/only255.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
step Tools/SHME_V234_20261028/probe234_camfn.py census SHME_KIND=measure
grep -a '"ok": true' $D/data/last_census.out | grep -q CAMFN234 || { echo "E_FAILED census" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
step $V2/only_all.py only_all SHME_KIND=control
step $D/req/pawn_req.py pawn "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
grep -a "PAWN255" $D/data/last_pawn.out | grep -q '"ok": true' || { echo "E_FAILED pawn" >> $O; exit 1; }
step $D/req/abp_req.py abp "SHME_KIND=write SHME_MANIFEST=$MD/v255_ctl.json"
grep -a "ABP255" $D/data/last_abp.out | grep -q '"ok": true' || { echo "E_FAILED abp" >> $O; exit 1; }
step $D/req/g2w_req.py g2w "SHME_KIND=write SHME_MANIFEST=$MD/v255_g2.json"
step $D/req/db2_req.py db2 "SHME_KIND=write SHME_MANIFEST=$MD/v255_g2.json"
WARM=1 ab e60 "s54_revR:c1 s54_revR:c1 s54_revL:c1 s54_r135:c1 fz_sprint_a:c1 fz_sprint_m:c1" $D/vars255.sh
echo TE255_DONE >> $O
