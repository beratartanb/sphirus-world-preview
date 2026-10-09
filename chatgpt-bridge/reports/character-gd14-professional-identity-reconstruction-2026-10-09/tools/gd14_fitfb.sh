#!/bin/bash
# gd14_fitfb.sh <src MHC> <final MHC name> <sculpt npy> <TAG> : Blender sculpt -> MHC transfer with residual feedback: fit(T) -> <TAG>f1,
# fit(T + (T-F1)) -> <TAG>f2, fit(T2 + (T-F2)) -> final <TAG> (fit_state_to_target_vertices alone loses broad smooth changes: submalar 18 % retained)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; S=$1; FN=$2; T=$3; G=$4
bash $W/tools/gd14_memguard.sh 22
fb() { "$B" -b --factory-startup --python-expr "
import numpy as np
T=np.load(r'$T'); P=np.load(r'$1'); F=np.load(r'$2'); Q=P.copy(); Q[:24049]=P[:24049]+(T[:24049]-F[:24049]); np.save(r'$3', Q); print('FB ok')" 2>&1 | grep -q "FB ok"; }
bash $W/tools/gd14_fit.sh $S ${FN}_f1 $T ${G}f1 | grep -E "FITFID|STOP|Traceback"
fb $T $W/data/head_${G}f1_mhc.npy $W/data/head_${G}S_fb1.npy
bash $W/tools/gd14_fit.sh $S ${FN}_f2 $W/data/head_${G}S_fb1.npy ${G}f2 | grep -E "STOP|Traceback"
fb $W/data/head_${G}S_fb1.npy $W/data/head_${G}f2_mhc.npy $W/data/head_${G}S_fb2.npy
bash $W/tools/gd14_fit.sh $S $FN $W/data/head_${G}S_fb2.npy $G | grep -E "STOP|Traceback"
"$B" -b --factory-startup --python-expr "
import numpy as np
T=np.load(r'$T'); F=np.load(r'$W/data/head_${G}_mhc.npy'); d=np.linalg.norm(F-T,axis=1)[:24049]*10
print('FINAL $G vs sculpt: mean %.3f p95 %.3f p99 %.3f max %.3f mm' % (d.mean(), np.percentile(d,95), np.percentile(d,99), d.max()))" 2>&1 | grep FINAL
