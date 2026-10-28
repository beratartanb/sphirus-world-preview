#!/bin/bash
# run234_b11.sh : V2.34 B11 (same editor as B10): jog stop closing step - toe mid-segment clearance (dry -> manifest -> write) with a same-session before / after.
#   editor A (fresh; reason: new DA fields + new component variables must be compiled into fresh classes): profiles + comp vars + save
#   editor B (fresh; reason: V2.30 rule - a function build after a vars build in the same editor ballooned to 94 GB): SHM_UpdateCameraV21
#   only, census (probe234_camfn: setters present, nodes > 1000) BEFORE any save, BP_GR_Player locomotion readers, smoke + behaviour check,
#   then the first broken case + sound counter-case (sprint hard right / walk right, gamepad profile).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; R=Tools/SHME_V2_20261014/run_v2.sh
V1=Tools/SHME_V1_20260925; V2=Tools/SHME_V2_20261014; V21=Tools/SHME_V21_20261014; T=Tools/SHME_V234_20261028; T3=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
step() { echo "== $2 $(date +%T)" >> $O; out=$(env $3 bash $R "$1" "$2" 1500); echo "$out" > $D/last_$2.out; echo "$out" | head -1 >> $O; echo "$out" | grep -aE "GUARD|REFUSED|Traceback|FAIL|CAMFN234|LOCO234|SMD233|_lasthitby_patched" | head -5 | cut -c1-600 >> $O
  echo "$out" | head -1 | grep -qE "^OK" || { echo "B11_FAILED $2 $(date +%T)" >> $O; exit 1; }
  echo "$out" | grep -q "FAIL DSL\|BUILD_FUNCS_FAILED" && { echo "B11_FAILED $2 (build fail)" >> $O; exit 1; }; }
mani() { MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py "$@" >> $O 2>&1 || { echo "B11_FAILED manifest $1" >> $O; exit 1; }; }
until grep -aq "^B10_DONE\|^B10_FAILED" $O; do sleep 20; done
echo "B11 start $(date +%T)" >> $O
export WARM=0 MEMPROBE=1
S="j30_slow j34_chain1 j30_rel_3450 j30_rel_3200 cam_corr cam34_jcor"
J=""; for s in $S; do J="$J $s:o:1"; done
ab b11pre "$J" $D/vars234.sh
step $D/req/sc_dry3.py sc_dry3 SHME_KIND=measure
cp $D/sc234_dry.json $D/sc234_dry3.json
MSYS_NO_PATHCONV=1 "$PY" $T/manifest234.py stopclear3 --assets /Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop >> $O 2>&1 || { echo "B11_FAILED manifest" >> $O; exit 1; }
sed -e 's/"dry_run": True/"dry_run": False/' $D/req/sc_dry3.py > $D/req/sc_write3.py
step $D/req/sc_write3.py sc_write3 "SHME_KIND=write SHME_MANIFEST=$MD/stopclear3.json"
grep -a -o "SC234 .*" $D/last_sc_write3.out | cut -c1-600 >> $O
ab b11post "$J" $D/vars234.sh
echo "B11_DONE $(date +%T)" >> $O
