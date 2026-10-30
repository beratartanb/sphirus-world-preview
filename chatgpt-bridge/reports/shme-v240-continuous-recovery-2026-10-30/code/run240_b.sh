#!/bin/bash
# V2.40 B: source curve on the cuts, 96 per-(source,target) entry databases, deterministic entry select, test 30 + 120
source Saved/Codex/SHME_V240_20261030/lib240.sh; O=$D/chain.out; MD=$D/checkpoint/manifests
V8=/Game/GraceRanger/SHME/Animations/V238; V9=/Game/GraceRanger/SHME/Animations/V239; V0=/Game/GraceRanger/SHME/Animations/V240; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M0() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V240_20261030/manifest240.py "$@" | tail -c 120 >> $O; }
echo "B start $(date +%T)" >> $O
M0 src1 --assets $(for s in R L; do for p in $(seq -w 0 23); do echo $V8/SHM238_Cut_${s}_P$p; done; done)
SHME_KIND=write SHME_MANIFEST=$MD/src1.json bash $R $D/req/src_w.py src_w 1800 > $D/last_src_w.out 2>&1; grep -a -o "SRC240 .*" $D/last_src_w.out | cut -c1-200 >> $O
grep -a -q '"ok": true' $D/last_src_w.out || { echo "B_FAILED src" >> $O; exit 1; }
SAVED=$("$PY" -c "import json,glob;J={};[J.update({n:c for n,c in json.load(open(f))['clips'].items() if c.get('saved')}) for f in sorted(glob.glob('Saved/Codex/SHME_V239_20261030/gen239_tk_write_part*.json'))];print(' '.join('$V9/'+n for n in sorted(J)))")
M0 edb1 --assets $SAVED --new $(for e in $(seq -w 0 95); do echo $V0/PSD_SHM240_E$e; done)
SHME_KIND=write SHME_MANIFEST=$MD/edb1.json bash $R $D/req/edb_w.py edb_w 3000 > $D/last_edb_w.out 2>&1; echo "EDB_N $(grep -a -c EDB240_BIAS $D/last_edb_w.out) $(grep -a -o 'Traceback.*\|Error.\{0,160\}' $D/last_edb_w.out | head -2)" >> $O
[ "$(grep -a -c 'EDB240_BIAS' $D/last_edb_w.out)" = 96 ] || { echo "B_FAILED edb" >> $O; exit 1; }
M0 edbi1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/edbi1.json bash $R $D/req/edbi_w.py edbi_w 1800 > $D/last_edbi_w.out 2>&1; grep -a -o "EDB240 .*\|AssertionError.*\|Traceback.*" $D/last_edbi_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_edbi_w.out || { echo "B_FAILED edbi" >> $O; exit 1; }
WARM=1 ab b30 "j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk"
relaunch b120 120
WARM=1 ab b120 "j39_rw:tk j39_rl:tk j39_lr:tk j38_cc90:tk j39_rl_e:tk j39_rl_l:tk j39_lw:tk"
relaunch bend 30
echo "B_DONE $(date +%T)" >> $O
