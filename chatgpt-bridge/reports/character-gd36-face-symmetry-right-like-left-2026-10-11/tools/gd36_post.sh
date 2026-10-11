#!/bin/bash
# gd36_post.sh : post-rig checks of the GD36 face (head_g36_postrig.npy): gd13 checks vs the H100 target and vs G31S; post-rig vs target distance;
# LEFT half (+x, the good side) unchanged vs the GD31 post-rig face; remaining left/right asymmetry per region (UV mirror, gd36_sym AMT 0).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD36_Identity_20261011; T=$N/tools; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_checks.py)" -- "$(m $N/data/head_g36_postrig.npy)" "$(m $N/data/checks_g36_postrig.json)" "$(m $N/data/head_H100.npy)" "$(m $N/data/head_G31S.npy)" 2>&1 | grep -E "^CHECKS|^DISP" | cut -c1-400
"$B" -b --factory-startup --python-expr "
import sys, numpy as np
sys.path.insert(0, r'$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools)'); from gd13_common import NS, MX
P=np.load(r'$(m $N/data/head_g36_postrig.npy)')[:NS]; H=np.load(r'$(m $N/data/head_H100.npy)')[:NS]; P31=np.load(r'$(m $N/data/head_g31_postrig.npy)')[:NS]; S=np.load(r'$(m $N/data/head_G31S.npy)')[:NS]
d=np.linalg.norm(P-H,axis=1)*10; print('POST vs H100 target: mean %.3f p95 %.3f p99 %.3f max %.3f mm' % (d.mean(), np.percentile(d,95), np.percentile(d,99), d.max()))
L=(S[:,0]-MX)>0.6; face=(S[:,1]>3)&(S[:,2]>148.5)&(S[:,2]<168); e=np.linalg.norm(P-P31,axis=1)*10
print('LEFT half (+x, good side) post-rig GD36 vs GD31: mean %.3f p95 %.3f max %.3f mm (face)' % (e[L&face].mean(), np.percentile(e[L&face],95), e[L&face].max()))
print('RIGHT half moved vs GD31 post-rig: mean %.2f max %.2f mm (face)' % (e[(~L)&face&((S[:,0]-MX)<-0.6)].mean(), e[(~L)&face&((S[:,0]-MX)<-0.6)].max()))" 2>&1 | grep -E "POST|LEFT|RIGHT"
"$B" -b --factory-startup --python "$(cygpath -w $T/gd36_uvmirror.py)" -- "$(m $N/data/head_g36_postrig.npy)" "$(m $N/data/mirror_uv_g36post.npy)" 2>&1 | grep -oE "face \|X - aligned mirror\|.*"
MAFILE="$(m $N/data/mirror_uv_g36post.npy)" "$B" -b --factory-startup --python "$(cygpath -w $T/gd36_sym.py)" -- "$(m $N/data/head_g36_postrig.npy)" "$(m $N/data/_tmp_post.npy)" "$(m $N/data/asym_g36_postrig.json)" 0.0 0.6 2>&1 | grep -E "^SYM yaw" | sed 's/ | /\n   /g'; rm -f $N/data/_tmp_post.npy
"$B" -b --factory-startup --python "$(cygpath -w $T/gd36_uvmirror.py)" -- "$(m $N/data/head_g31_postrig.npy)" "$(m $N/data/mirror_uv_g31post.npy)" 2>&1 | grep -oE "face \|X - aligned mirror\|.*" | sed 's/^/G31 post: /'
echo POST36_DONE
