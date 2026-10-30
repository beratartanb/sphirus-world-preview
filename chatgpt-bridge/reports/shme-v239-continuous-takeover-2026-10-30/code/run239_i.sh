#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239
echo "I start $(date +%T)" >> $O
TKS=$(for s in R_P21 R_P10; do for k in 1 2 3 4; do for t in Back Opp; do echo $V9/SHM239_Tk_${s}_K${k}_$t; done; done; done)
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py jctk1 --assets $TKS --new $V9/PSD_SHM239_JogCutTk | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/jctk1.json bash $R $D/req/jctk_w.py jctk_w 1800 > $D/last_jctk_w.out 2>&1; grep -a -o "JCTK239 .*" $D/last_jctk_w.out | cut -c1-400 >> $O
grep -a -q '"tk": 16' $D/last_jctk_w.out || { echo "I_FAILED jctk" >> $O; exit 1; }
WARM=1 ab iw "j39_rl:tk2"
ab i "j39_rl:tk2 j39_rw:tk2 j38_c90r:tk2 j38_cc90:tk2"
echo "I_DONE $(date +%T)" >> $O
