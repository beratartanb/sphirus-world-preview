#!/bin/bash
# run234_b12.sh : V2.34 B12 camera function build (walk / jog exploration gate by RedirectGait) + walk stop toe clearance (dry -> manifest -> write) + shuffle probe + candidate G suite.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B12_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B12_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B12_FAILED manifest $1" >> $O; exit 1; }; }
echo "B12 start $(date +%T) (reason: camera function change -> fresh editor, V2.30 memory rule)" >> $O
relaunch b12 30
step $V21/revert_noquit.py revert SHME_KIND=control
mani locoG --assets /Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent /Game/GraceRanger/BP_GR_Player /Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player
step $T3/only_v233cam.py only SHME_KIND=control
step $V1/build_funcs.py funcs "SHME_KIND=write SHME_MANIFEST=$MD/locoG.json"
step $T/probe234_route.py census SHME_KIND=measure
grep -a "ROUTE234" $D/last_census.out | tail -1 | grep -q '"ok": true' || { echo "B12_FAILED census (functions incomplete - nothing saved)" >> $O; exit 1; }
step $V2/save_comp.py save_comp2 "SHME_KIND=write SHME_MANIFEST=$MD/locoG.json"
step $V2/only_all.py only_all SHME_KIND=control
step $T3/save_manifest_dirty.py smd2 "SHME_KIND=write SHME_MANIFEST=$MD/locoG.json"
echo "B12_BUILT $(date +%T)" >> $O
step $D/req/shuffle.py shuffle SHME_KIND=measure
grep -a -o "SHUF234 {.*" $D/last_shuffle.out > $D/shuffle234.json
step $D/req/sc_dry4.py sc_dry4 SHME_KIND=measure
cp $D/sc234_dry.json $D/sc234_dry4.json
"$PY" -c "
import json; d = json.load(open('$D/sc234_dry4.json'))
w = [r['path'].split('.')[0] for r in d if r.get('touched') and r.get('foot_xy_err_cm', 9) < 0.5 and 'Jog_Fwd_Stop' not in r['path']]
json.dump(w, open('$D/sc234_writelist4.json', 'w')); print('SC234_WRITE4', len(w), w)" >> $O 2>&1
MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py stopclear4 --from $D/sc234_writelist4.json >> $O 2>&1 || { echo "B12_FAILED manifest" >> $O; exit 1; }
"$PY" -c "
import json; w = json.load(open('$D/sc234_writelist4.json')); s = open('$D/req/sc_dry4.py').read().replace('\"dry_run\": True', '\"dry_run\": False').replace('[\"folder:/Game/GraceRanger/SHME/Animations/Stops\"]', repr([x + '.' + x.rsplit('/', 1)[1] for x in w]))
open('$D/req/sc_write4.py', 'w').write(s)"
step $D/req/sc_write4.py sc_write4 "SHME_KIND=write SHME_MANIFEST=$MD/stopclear4.json"
export WARM=1 MEMPROBE=1
J="j30_rel_3200:G:1 j30_rel_3450:G:1 j30_slow:G:1 j34_chain1:G:1 jstart:G:1 jstart:o:1 wstart:G:1 wstart:o:1 c29_combo:G:1 c29_combo:o:1 e29_chain:G:1 e29_load:G:1 jback:G:1 jback:o:1 wdiag:G:1 wdiag:o:1 s29_swl12:G:1"
J="$J cam33_sturn:Gp:1 cam33_sturn:Goffp:1 cam33_wturn:Gp:1 cam33_wturn:Goffp:1 cam33_wturn:op:1 cam33_jturnj:Gp:1 cam33_jturnj:G:1 cam34_wflow:Gp:1 cam34_jlook:Gp:1 cam34_jlook:op:1 cam34_jcor:Gp:1 cam32_chain:Gp:1 cam32_chain:op:1 cam32_wallturn:Gp:1 cam_corr:Gp:1 ins_ws:Gp:1 cam33_back:Gp:1 cam33_idlelook:Gp:1 map_r1:Gp:1"
ab b12 "$J" $D/vars234.sh
echo "B12_DONE $(date +%T)" >> $O
