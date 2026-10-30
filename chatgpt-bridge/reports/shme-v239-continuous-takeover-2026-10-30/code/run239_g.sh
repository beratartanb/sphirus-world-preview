#!/bin/bash
source Saved/Codex/SHME_V239_20261030/lib239.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; V9=/Game/GraceRanger/SHME/Animations/V239
echo "G start $(date +%T)" >> $O
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V239_20261030/manifest239.py pss1 --assets $V9/PSD_SHM239_Tk_Back $V9/PSD_SHM239_Tk_Opp --new $V9/PSS_SHM239_Takeover | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/pss1.json bash $R $D/req/pss_w.py pss_w 1800 > $D/last_pss_w.out 2>&1; grep -a -o "PSS239 .*" $D/last_pss_w.out | cut -c1-500 >> $O
grep -a -q '"schema_traj_w": 0.15' $D/last_pss_w.out || { echo "G_FAILED pss" >> $O; exit 1; }
WARM=1 ab g "j39_rl:tk j39_rw:tk"
echo "G_DONE $(date +%T)" >> $O
