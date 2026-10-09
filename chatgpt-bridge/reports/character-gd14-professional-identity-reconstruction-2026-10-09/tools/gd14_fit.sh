#!/bin/bash
# gd14_fit.sh <src MHC name> <dst MHC name> <head npy (DNA order, project frame)> <tag> : transfer a Blender-sculpted head into a new MHC asset
# (fit_state_to_target_vertices, alignment NONE, HF delta kept) and measure the fit fidelity vs the sculpt (data/head_<tag>_mhc.npy)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009; D=/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
[ -e Content/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC/$2.uasset ] && { echo "EXISTS_STOP $2"; exit 5; }
"$B" -b --factory-startup --python-expr "
import json,numpy as np
X=np.load(r'$3'); r=lambda a: np.round(a,5).tolist()
json.dump({'head': r(X[:24049]), 'teeth': r(X[24049:28295]), 'eyeL': r(X[28955:29725]), 'eyeR': r(X[29725:30495])}, open(r'$W/mhc/target_$4.json','w')); print('TGT ok')" 2>&1 | grep TGT
{ echo "import builtins; builtins.GD14F = {'src': '$D/$1', 'dst': '$D/$2', 'target_json': r'$(Wp $W/mhc/target_$4.json)', 'out': r'$(Wp $W/mhc)', 'tag': '$4'}"; cat $W/tools/ue_gd14_fit.py; } > $W/jobs/fit_$4.py
bash Tools/OutfitHome_20260929/run_of.sh $W/jobs/fit_$4.py gd14-fit-$4 1500 | grep -oE "GD14_FIT.*|Traceback.*|AssertionError.*" | cut -c1-400
"$B" -b --factory-startup --python-expr "
import numpy as np
F=np.fromfile(r'$W/mhc/$4_verts.f32',np.float32).reshape(-1,3).astype(float); T=np.load(r'$3'); np.save(r'$W/data/head_$4_mhc.npy',F); d=np.linalg.norm(F-T,axis=1)*10
print('FITFID skin mean %.3f p95 %.3f p99 %.3f max %.3f mm | eyes max %.3f | teeth max %.3f' % (d[:24049].mean(), np.percentile(d[:24049],95), np.percentile(d[:24049],99), d[:24049].max(), d[28955:30495].max(), d[24049:28295].max()))" 2>&1 | grep FITFID
