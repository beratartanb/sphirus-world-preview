#!/bin/bash
# gd14_step.sh <src asset name> <dst asset name> <targets json basename in mhc/> <tag> [iters=10] : duplicate an MHC work asset and run the iterative landmark sculpt on it (saved)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD14_Identity_20261009; D=/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC; Wn="$(cygpath -w "$(pwd)/$N/mhc")"
if [ -e Content/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC/$2.uasset ]; then [ "${RESUME:-0}" = 1 ] || { echo "EXISTS_STOP $2"; exit 5; }; SKIPDUP=1; fi
{ echo "import builtins; builtins.GD14 = {'op': 'dup', 'src': '$D/$1', 'dst': '$D/$2', 'out': r'$Wn', 'tag': '${4}_start'}"; cat $N/tools/ue_gd14_mhc.py; } > $N/mhc/job_dup_$4.py
[ "${SKIPDUP:-0}" = 1 ] || bash Tools/OutfitHome_20260929/run_of.sh $N/mhc/job_dup_$4.py gd14-dup-$4 600 | grep -oE "GD14_MHC.*" | cut -c1-200
{ echo "import builtins, json; builtins.GD14T = {'dst': '$D/$2', 'out': r'$Wn', 'tag': '$4', 'targets': json.load(open(r'$Wn/$3')), 'iters': ${5:-10}, 'gain': 1.0, 'save': True}"; cat $N/tools/ue_gd14_target.py; } > $N/mhc/job_step_$4.py
bash Tools/OutfitHome_20260929/run_of.sh $N/mhc/job_step_$4.py gd14-step-$4 1500 | grep -oE "GD14_TGT.*" | cut -c1-400
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python-expr "
import numpy as np; X=np.fromfile(r'$Wn/${4}_verts.f32',np.float32).reshape(-1,3).astype(float); np.save(r'$(cygpath -w "$(pwd)/$N/data/head_$4.npy")', X); print('NPY_OK', X.shape)" 2>&1 | grep NPY_OK
