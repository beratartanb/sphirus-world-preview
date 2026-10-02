#!/bin/bash
# gd9_cycle.sh <tag> <world-frame head npy> : GUARDIAN-3 full cycle: target json -> MetaHumanCharacter MHC_GD9_<TAG> (B2 whole-rig body = project frame)
# fit_state_to_target_vertices (alignment NONE) -> AUTO-RIG (joints + blend shapes, Epic service) -> DNA + geometry export -> project face asset
# SKM_GD9_Face_<tag> (plugin face skeleton / ABPs, P material slots) -> groom bindings + QA captures g3<tag>_{SETS|clay,real} -> frames
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; NPY=$2; T=Tools/CharacterLookdev_20260930; U=$(echo $TAG | tr a-z A-Z); G3=Saved/Codex/CharacterGuardian9_20261002
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"; R=Tools/OutfitHome_20260929/run_of.sh
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python-expr "
import json,numpy as np
X=np.load(r'$NPY'); r=lambda a: np.round(a,5).tolist()
json.dump({'head': r(X[:24049]), 'teeth': r(X[24049:28295]), 'eyeL': r(X[28955:29725]), 'eyeR': r(X[29725:30495])}, open('$G3/target_$TAG.json','w')); print('TGT ok')" 2>&1 | grep TGT
{ echo "import builtins; builtins.GD3_RIG = {'name': 'MHC_GD9_$U', 'b2': True, 'target_json': r'$(cygpath -w "$(pwd)/$G3/target_$TAG.json")', 'align': 'NONE', 'rig_type': 'JOINTS_AND_BLEND_SHAPES'}"; cat $T/ue_gd9_rig_build.py; } > "$SC/gd4_rig_$TAG.py"
bash $R "$SC/gd4_rig_$TAG.py" gd4-rig-$TAG 3000 | grep -oE '"request_auto_rigging", "[a-zA-Z]+", [0-9.]+|"has_face_dna_blendshapes": [a-z]+|"face_mesh_has_dna": [a-z]+|"err".{0,300}'
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" -b --factory-startup --python-expr "
import numpy as np
F=np.fromfile('$G3/MHC_GD9_${U}_postrig.f32',np.float32).reshape(-1,3).astype(float); T=np.load(r'$NPY'); np.save('$G3/${U}_postrig.npy',F); d=np.linalg.norm(F-T,axis=1); m=T[:24049,2]>149
print('RIGFIT face mean %.3f p95 %.3f max %.3f eyes %.3f' % (d[:24049][m].mean(), np.percentile(d[:24049][m],95), d[:24049][m].max(), d[28955:30495].mean()))" 2>&1 | grep RIGFIT
{ echo "import builtins; builtins.GD3_FS = {'src': '/Game/Sphirus/CharacterLab/CharacterGuardian9_20261002/MHC/Export/MHC_GD9_${U}_Head', 'dst': 'SKM_GD9_Face_$TAG'}"; cat $T/ue_gd9_face_setup.py; } > "$SC/gd4_fs_$TAG.py"
bash $R "$SC/gd4_fs_$TAG.py" gd4-fs-$TAG 900 | grep -oE '"pp_abp": "[^"]*"|"morphs": [0-9]+|Traceback'
{ echo "import builtins; builtins.GD3_DL = {'face': '/Game/Sphirus/CharacterLab/CharacterGuardian9_20261002/Face/SKM_GD9_Face_$TAG', 'dna_file': r'$(cygpath -w "$(pwd)/$G3/dna/MHC_GD9_$U/MHC_GD9_${U}_Head.dna")', 'dna_asset': '/Game/Sphirus/CharacterLab/CharacterGuardian9_20261002/MHC/DNA/MHC_GD9_${U}_Head'}"; cat $T/ue_gd3_dna_link.py; } > "$SC/gd4_dl_$TAG.py"
bash $R "$SC/gd4_dl_$TAG.py" gd4-dl-$TAG 900 | grep -oE '"face_dna": "[^"]*"|Traceback'
SETS=${SETS:-clay,real} bash $T/gd9_face_run.sh $TAG | grep -E "COMP3|DONE|ERROR"
bash $T/gd9_frames.sh g4$TAG "${FSETS:-clay real}" >/dev/null; echo GD9_CYCLE_DONE $TAG
