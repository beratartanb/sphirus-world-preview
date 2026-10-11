#!/bin/bash
# gd38_postT.sh : post-rig checks of the GD38 face (head_t38_postrig.npy): gd13 checks vs the T38 target; post-rig vs target distance; the
# intended change (T38 - N2) retained after fit + rig; regions outside the edit zones unchanged vs GD37 n37 post-rig; eyeballs; regional
# left/right asymmetry (UV mirror + gd38_sym AMT 0) before (n37) and after (t38).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD38_Identity_20261011; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }
"$B" -b --factory-startup --python "$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools/gd13_checks.py)" -- "$(m $N/data/head_t38_postrig.npy)" "$(m $N/data/checks_t38_postrig.json)" "$(m $N/data/head_T38.npy)" "$(m $N/data/head_n37_postrig.npy)" 2>&1 | grep -oE '"folds": [0-9]+|"area_ratio_min": [0-9.]+|"area_ratio_max": [0-9.]+|"flipped_tris_vs_base": [0-9]+|"min_clear_mm": [-0-9.]+|"n_inside_0p3mm": [0-9]+' | tr '\n' ' '; echo
"$B" -b --factory-startup --python-expr "
import sys, numpy as np
sys.path.insert(0, r'$(cygpath -w Saved/Codex/GD13_Identity_20261009/tools)'); from gd13_common import NS, MX
A=np.load(r'$(m $N/data/head_t38_postrig.npy)'); T=np.load(r'$(m $N/data/head_T38.npy)'); K=np.load(r'$(m $N/data/head_N2.npy)'); A37=np.load(r'$(m $N/data/head_n37_postrig.npy)')
P, T_, K_, P37 = A[:NS], T[:NS], K[:NS], A37[:NS]
d=np.linalg.norm(P-T_,axis=1)*10; print('POST vs T38 target: mean %.3f p95 %.3f p99 %.3f max %.3f mm' % (d.mean(), np.percentile(d,95), np.percentile(d,99), d.max()))
want=T_-K_; got=P-P37; zone=np.linalg.norm(want,axis=1)*10>0.3
print('INTENDED change (T38-N2 > 0.3 mm, %d verts): wanted mean %.2f mm, got (t38-n37 post-rig) mean %.2f mm, retained %.0f %%, direction cos %.3f' % (zone.sum(), np.linalg.norm(want[zone],axis=1).mean()*10, np.linalg.norm(got[zone],axis=1).mean()*10, 100*np.sum(got[zone]*want[zone])/np.sum(want[zone]*want[zone]), np.sum(got[zone]*want[zone])/np.sqrt(np.sum(got[zone]**2)*np.sum(want[zone]**2))))
x=P37[:,0]-MX; y=P37[:,1]; z=P37[:,2]; face=(y>3)&(z>148.5)&(z<168); edit=np.linalg.norm(want,axis=1)*10>0.02; e=np.linalg.norm(P-P37,axis=1)*10
print('OUTSIDE the edit zones (face) vs GD37 post-rig: mean %.3f p99 %.3f max %.3f mm | outside face max %.3f mm' % (e[face&~edit].mean(), np.percentile(e[face&~edit],99), e[face&~edit].max(), e[~face].max()))
eL=slice(28955,29725); eR=slice(29725,30495); print('EYES vs GD37 post-rig: left (+x) max %.3f mm, right (-x) mean move %s mm | teeth max %.3f mm' % (np.linalg.norm(A[eL]-A37[eL],axis=1).max()*10, np.round((A[eR]-A37[eR]).mean(0)*10,2), np.linalg.norm(A[24049:28295]-A37[24049:28295],axis=1).max()*10))" 2>&1 | grep -E "POST|INTENDED|OUTSIDE|EYES"
for h in n37_postrig t38_postrig; do "$B" -b --factory-startup --python "$(cygpath -w $N/tools/gd38_uvmirror.py)" -- "$(m $N/data/head_$h.npy)" "$(m $N/data/mirror_uv_$h.npy)" >/dev/null 2>&1
MAFILE="$(m $N/data/mirror_uv_$h.npy)" "$B" -b --factory-startup --python "$(cygpath -w $N/tools/gd38_sym.py)" -- "$(m $N/data/head_$h.npy)" "$(m $N/data/_tmp.npy)" "$(m $N/data/asym_$h.json)" 0.0 0.6 2>&1 | grep -E "^SYM yaw" | sed 's/ | /\n   /g' | grep -E "forehead|brow_supra|glabella|upper_lid|lower_lid|malar|mid_cheek|upper_lip|lower_lip|jaw" | sed "s/^/$h /"; done; rm -f $N/data/_tmp.npy
echo POSTT38_DONE
