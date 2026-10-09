#!/bin/bash
# gd14_ue_cycle.sh <sculpt MHC name in GD14/MHC, e.g. MHC_GD14_W1> <tag, e.g. w1> : GD14 real-material evaluation chain, ALL writes in the GD14 folders.
# 1 auto-rig a DUPLICATE MHC_GD14_<TAG>_Rig of the (unrigged) sculpt asset (Epic service) -> DNA + head export in GD14/MHC/{DNA,Export}
# 2 face asset GD14/Face/SKM_GD14_Face_<tag> (moved export; plugin face skeleton / post-process ABP / P material slots)  3 persistent DNA link
# 4 bindings (h75c hair from the P face source, library M_SlightArch brows + S_Thin lashes) into GD14/Face/Bindings  5 qa_config composition
# (x19a skin, e3n eyes, GC k10 body, Henley g17e, Chaos shorts m1; save_prefixes / studio_folder = GD14) + studio setup. Captures: gd14_caps.sh.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SRC=$1; TAG=$2; U=$(echo $TAG | tr a-z A-Z)
W=Saved/Codex/GD14_Identity_20261009; T=Tools/CharacterLookdev_20260930; R=Tools/OutfitHome_20260929/run_of.sh; J=$W/jobs; mkdir -p $J
G=/Game/Sphirus/CharacterLab/GD14_IdentityMaster_20261009; RIG=MHC_GD14_${U}_Rig; FACE=$G/Face/SKM_GD14_Face_$TAG; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
for f in Content/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/MHC/$RIG.uasset Content/Sphirus/CharacterLab/GD14_IdentityMaster_20261009/Face/SKM_GD14_Face_$TAG.uasset; do [ -e "$f" ] && { echo "TAG_EXISTS_STOP $TAG ($f)"; exit 5; }; done
[ -f $W/qa_config_before_gd14.json ] || cp Saved/Codex/CharacterLookdev_20260930/qa_config.json $W/qa_config_before_gd14.json
{ echo "import builtins; builtins.GD14R = {'src': '$G/MHC/$SRC', 'dst': '$RIG', 'rig_type': 'JOINTS_AND_BLEND_SHAPES'}"; cat $W/tools/ue_gd14_rig.py; } > $J/rig_$TAG.py
RIGOUT=$(bash $R $J/rig_$TAG.py gd14-rig-$TAG 3000 | grep -oE '"request_auto_rigging", "[a-zA-Z]+", [0-9.]+|"has_face_dna_blendshapes": [a-z]+|"face_mesh_has_dna": [a-z]+|"err".{0,300}|TIMEOUT.*|Traceback.*|AssertionError.*'); echo "$RIGOUT"
echo "$RIGOUT" | grep -q '"request_auto_rigging", "ok"' && echo "$RIGOUT" | grep -q '"face_mesh_has_dna": true' && [ -f $W/rig/${RIG}_postrig.f32 ] || { echo RIG_GATE_STOP $TAG; exit 4; }
"$B" -b --factory-startup --python-expr "
import numpy as np
F=np.fromfile(r'$W/rig/${RIG}_postrig.f32',np.float32).reshape(-1,3).astype(float); P=np.fromfile(r'$W/rig/${RIG}_prerig.f32',np.float32).reshape(-1,3).astype(float); np.save(r'$W/data/head_${TAG}_postrig.npy',F); d=np.linalg.norm(F-P,axis=1)
print('RIGFIT postrig-vs-prerig skin mean %.3f p95 %.3f max %.3f eyes %.3f mm' % (10*d[:24049].mean(), 10*np.percentile(d[:24049],95), 10*d[:24049].max(), 10*d[28955:30495].mean()))" 2>&1 | grep RIGFIT
{ echo "import builtins; builtins.GD3_FS = {'src': '$G/MHC/Export/${RIG}_Head', 'dst': 'SKM_GD14_Face_$TAG'}"; sed "s#/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Face#$G/Face#" $T/ue_g11rr_face_setup.py; } > $J/fs_$TAG.py
grep -q "GD11_FaceR" $J/fs_$TAG.py && { echo "FS_PATH_STOP"; exit 6; }
bash $R $J/fs_$TAG.py gd14-fs-$TAG 900 | grep -oE '"pp_abp": "[^"]*"|"morphs": [0-9]+|Traceback.*|AssertionError.*'
{ echo "import builtins; builtins.GD3_DL = {'face': '$FACE', 'dna_file': r'$(cygpath -w "$(pwd)/$W/rig/dna/$RIG/${RIG}_Head.dna")', 'dna_asset': '$G/MHC/DNA/${RIG}_Head'}"; cat $T/ue_gd3_dna_link.py; } > $J/dl_$TAG.py
bash $R $J/dl_$TAG.py gd14-dl-$TAG 900 | grep -oE '"face_dna": "[^"]*"|Traceback.*'
bash $W/tools/gd14_bind_comp.sh $TAG
echo GD14_UE_CYCLE_DONE $TAG
