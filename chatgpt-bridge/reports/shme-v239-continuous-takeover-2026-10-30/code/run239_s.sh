#!/bin/bash
# V2.39 S: full takeover family (364 clips, 4 jobs) -> entry + play databases -> exact heading map -> tests both sides
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239; A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "S start $(date +%T)" >> $O
ALL=$("$PY" -c "import json;print(' '.join('$V9/'+s['name'] for s in json.load(open('$D/tk_all_specs.json'))))")
EX=""; NW=""; for a in $ALL; do f="Content/GraceRanger/SHME/Animations/V239/$(basename $a).uasset"; if [ -f "$f" ]; then EX="$EX $a"; else NW="$NW $a"; fi; done
[ -f $MD/tkall.json ] || M9 tkall --assets $EX --new $NW
for k in ${PARTS:-0 1 2 3}; do
  SHME_KIND=write SHME_MANIFEST=$MD/tkall.json bash $R $D/req/tka_$k.py tka_$k 3000 > $D/last_tka_$k.out 2>&1; cp $D/gen239_tk_write.json $D/gen239_tk_write_part$k.json
  "$PY" -c "import json;J=json.load(open('$D/gen239_tk_write_part$k.json'))['clips'];bad=[n for n,c in J.items() if not c.get('saved') and not str(c.get('write_error','')).startswith('LEG_GUARD_FAIL')];rej=[n for n,c in J.items() if str(c.get('write_error','')).startswith('LEG_GUARD_FAIL')];print('TKA$k', len(J), 'unsaved', len(bad), bad[:3], 'guard_rejected', rej, [c.get('error','')[-160:] for n,c in J.items() if 'error' in c][:1])" >> $O
  tail -1 $O | grep -q "unsaved 0 " || { echo "S_FAILED tka$k" >> $O; exit 1; }
done
SAVED=$("$PY" -c "import json,glob;J={};[J.update({n:c for n,c in json.load(open(f))['clips'].items() if c.get('saved')}) for f in sorted(glob.glob('$D/gen239_tk_write_part*.json'))];print(' '.join('$V9/'+n for n in sorted(J)))")
echo "SAVED_N $(echo $SAVED | wc -w)" >> $O
M9 tkdball --assets $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp $V9/PSD_SHM239_TkP_Back $V9/PSD_SHM239_TkP_Opp $SAVED
SHME_KIND=write SHME_MANIFEST=$MD/tkdball.json bash $R $D/req/tkdb_all.py tkdb_all 3000 > $D/last_tkdb_all.out 2>&1; echo "TDB_BIAS_N $(grep -a -c TDB239_BIAS $D/last_tkdb_all.out)" >> $O; grep -a -o '"entries": \[[^]]\{0,60\}' $D/last_tkdb_all.out | head -2 >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb_all.out)" = 4 ] || { echo "S_FAILED tkdball" >> $O; exit 1; }
M9 cmd1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching
SHME_KIND=write SHME_MANIFEST=$MD/cmd1.json bash $R $D/req/cmd_w.py cmd_w 1800 > $D/last_cmd_w.out 2>&1; grep -a -o "CMD239 .*" $D/last_cmd_w.out | cut -c1-300 >> $O
grep -a -q '"saved": true' $D/last_cmd_w.out || { echo "S_FAILED cmd" >> $O; exit 1; }
WARM=1 ab sw "j39_rl:tk j39_lr:tk"
ab s "j39_rl:tk j39_rw:tk j39_rl_e:tk j39_rl_l:tk j39_lr:tk j39_lw:tk j38_cc90:tk j38_c90r:tk j38_c90l:tk mtf_jog:tk"
echo "S_DONE $(date +%T)" >> $O
