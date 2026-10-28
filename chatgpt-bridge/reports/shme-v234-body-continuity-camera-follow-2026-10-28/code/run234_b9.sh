#!/bin/bash
# run234_b9.sh : V2.34 B9 (same editor): stop closing-step clearance - production BEFORE runs, dry run 2, manifest = the dry-run write list, write, AFTER runs; terrain diagnosis runs.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B9_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B9_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B9_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aq "^B8_DONE" $O; do sleep 20; done
echo "B9 start $(date +%T) (same editor; content write with a same-session before / after)" >> $O
export WARM=1 MEMPROBE=1
S="j30_slow j34_chain1 wstart jback c29_combo j30_rel_3450 s34_straight"
J=""; for s in $S; do J="$J $s:o:1"; done
ab b9pre "$J ter_drop_walk:o:1 ter_step2:o:1 ter_drop_jog:o:1" $D/vars234.sh
step $D/req/sc_dry2.py sc_dry2 SHME_KIND=measure
"$PY" -c "
import json; d = json.load(open('$D/sc234_dry.json'))
w = [r['path'].split('.')[0] for r in d if r.get('touched') and r.get('foot_xy_err_cm', 9) < 0.5]
json.dump(w, open('$D/sc234_writelist.json', 'w')); print('SC234_WRITE', len(w), w)" >> $O 2>&1
MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py stopclear --from $D/sc234_writelist.json >> $O 2>&1 || { echo "B9_FAILED manifest" >> $O; exit 1; }
sed -e 's/"dry_run": True/"dry_run": False/' -e 's#"clips": \["folder:/Game/GraceRanger/SHME/Animations/Stops"\]#"clips": CLIPS#' $D/req/sc_dry2.py > $D/req/sc_write.py
"$PY" -c "
import json; w = json.load(open('$D/sc234_writelist.json')); p = '$D/req/sc_write.py'; s = open(p).read().replace('CLIPS', repr([x + '.' + x.rsplit('/', 1)[1] for x in w])); open(p, 'w').write(s)"
step $D/req/sc_write.py sc_write "SHME_KIND=write SHME_MANIFEST=$MD/stopclear.json"
grep -a -o "SC234 .*" $D/last_sc_write.out | cut -c1-300 >> $O
J=""; for s in $S; do J="$J $s:o:1"; done
ab b9post "$J" $D/vars234.sh
echo "B9_DONE $(date +%T)" >> $O
