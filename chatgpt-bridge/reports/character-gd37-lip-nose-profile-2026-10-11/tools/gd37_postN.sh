#!/bin/bash
# gd37_postN.sh : post-rig checks of the GD37 face (head_n37_postrig.npy): gd13 checks vs the N2 target and vs the GD36 post-rig face; post-rig vs
# target distance; regions OUTSIDE the lip / nose zone unchanged vs GD36 k36 post-rig; the intended change (N2 - K100) retained after fit + rig.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD37_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_checks.py)" -- "$(m $N/data/head_n37_postrig.npy)" "$(m $N/data/checks_n37_postrig.json)" "$(m $N/data/head_N2.npy)" "$(m $N/data/head_k36_postrig.npy)" 2>&1 | grep -oE '"folds": [0-9]+|"area_ratio_min": [0-9.]+|"area_ratio_max": [0-9.]+|"flipped_tris_vs_base": [0-9]+' | tr '\n' ' '; echo
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_checks.py)" -- "$(m $N/data/head_k36_postrig.npy)" "$(m $N/data/checks_k36_postrig_ref.json)" "$(m $N/data/head_K100.npy)" 2>&1 | grep -oE '"folds": [0-9]+|"area_ratio_min": [0-9.]+' | tr '\n' ' ' | sed 's/^/GD36 k36 post-rig reference: /'; echo
"$B" -b --factory-startup --python-expr "
import sys, numpy as np
sys.path.insert(0, r'$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools)'); from gd13_common import NS, MX
P=np.load(r'$(m $N/data/head_n37_postrig.npy)')[:NS]; T=np.load(r'$(m $N/data/head_N2.npy)')[:NS]; K=np.load(r'$(m $N/data/head_K100.npy)')[:NS]; P36=np.load(r'$(m $N/data/head_k36_postrig.npy)')[:NS]
d=np.linalg.norm(P-T,axis=1)*10; print('POST vs N2 target: mean %.3f p95 %.3f p99 %.3f max %.3f mm' % (d.mean(), np.percentile(d,95), np.percentile(d,99), d.max()))
want=(T-K); got=(P-P36); zone=np.linalg.norm(want,axis=1)*10>0.3
print('INTENDED change (N2-K100 > 0.3 mm, %d verts): wanted mean %.2f mm, got (n37-k36 post-rig) mean %.2f mm, retained %.0f %%, direction cos %.3f' % (zone.sum(), np.linalg.norm(want[zone],axis=1).mean()*10, np.linalg.norm(got[zone],axis=1).mean()*10, 100*np.sum(got[zone]*want[zone])/np.sum(want[zone]*want[zone]), np.sum(got[zone]*want[zone])/np.sqrt(np.sum(got[zone]**2)*np.sum(want[zone]**2))))
x=P36[:,0]-MX; y=P36[:,1]; z=P36[:,2]; lipnose=(z>153.6)&(z<160.6)&(np.abs(x)<3.4)&(y>10.5); face=(y>3)&(z>148.5)&(z<168); e=np.linalg.norm(P-P36,axis=1)*10
print('OUTSIDE the lip/nose zone (face) vs GD36 post-rig: mean %.3f p99 %.3f max %.3f mm | whole head outside face max %.3f mm' % (e[face&~lipnose].mean(), np.percentile(e[face&~lipnose],99), e[face&~lipnose].max(), e[~face].max()))
eyes=slice(28955,30495); A=np.load(r'$(m $N/data/head_n37_postrig.npy)'); A36=np.load(r'$(m $N/data/head_k36_postrig.npy)'); print('EYES vs GD36 post-rig max %.3f mm | teeth max %.3f mm' % (np.linalg.norm(A[eyes]-A36[eyes],axis=1).max()*10, np.linalg.norm(A[24049:28295]-A36[24049:28295],axis=1).max()*10))" 2>&1 | grep -E "POST|INTENDED|OUTSIDE|EYES"
echo POSTN37_DONE
