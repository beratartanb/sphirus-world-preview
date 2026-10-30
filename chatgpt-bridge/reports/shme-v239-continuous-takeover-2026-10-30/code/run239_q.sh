#!/bin/bash
# V2.39 Q: regenerate the 16 prefix takeovers with source-identical feet before t_K, rebuild entry (prefix windows) + play databases, test
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239
M9() { MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py "$@" | tail -c 160 >> $O; }
echo "Q start $(date +%T)" >> $O
TKS=$(for s in R_P21 R_P10; do for k in 1 2 3 4; do for t in Back Opp; do echo $V9/SHM239_Tk_${s}_K${k}_$t; done; done; done)
M9 tk3 --assets $TKS
SHME_KIND=write SHME_MANIFEST=$MD/tk3.json bash $R $D/req/tk2_w.py tk3_w 2400 > $D/last_tk3_w.out 2>&1
"$PY" -c "import json;J=json.load(open('$D/gen239_tk_write.json'))['clips'];bad=[n for n,c in J.items() if not c.get('saved')];print('TK3', len(J), 'unsaved', bad, [ (n[-12:], c.get('error','')[-200:]) for n,c in J.items() if 'error' in c][:2])" >> $O
tail -1 $O | grep -q "unsaved \[\]" || { echo "Q_FAILED tk3" >> $O; exit 1; }
M9 tkdb4 --assets $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp $V9/PSD_SHM239_TkP_Back $V9/PSD_SHM239_TkP_Opp $TKS
cat $D/req/tkdb3_w.py $D/req/tkp_w.py > $D/req/tkdb4_w.py
SHME_KIND=write SHME_MANIFEST=$MD/tkdb4.json bash $R $D/req/tkdb4_w.py tkdb4_w 1800 > $D/last_tkdb4_w.out 2>&1; grep -a -c "TDB239_BIAS" $D/last_tkdb4_w.out | sed 's/^/TDB_BIAS_N /' >> $O
[ "$(grep -a -c 'TDB239_BIAS' $D/last_tkdb4_w.out)" = 4 ] || { echo "Q_FAILED tkdb4" >> $O; exit 1; }
WARM=1 ab qw "j39_rl:tk j39_rw:tk"
ab q "j39_rl:tk j39_rw:tk j39_rl_e:tk j39_rl_l:tk j38_c90r:tk j38_cc90:tk"
echo "Q_DONE $(date +%T)" >> $O
