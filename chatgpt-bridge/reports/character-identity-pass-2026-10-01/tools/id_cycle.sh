#!/bin/bash
# id_cycle.sh <tag> <head npy> : IDENTITY cycle for one candidate head shape: MetaHuman state fit (MHC_ID_<TAG>) -> per-LOD
# BR_Neutral deploy -> bake SKM_ID_FaceMesh_<tag> (isolated folder) -> brow / lash / hair bindings GB_ID_*_<tag> -> clay + real gate captures i<tag>
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; NPY=$2; HT=${3:-v15c}; I=Saved/Codex/CharacterIdentity_20260930; T=Tools/CharacterLookdev_20260930
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"; U=$(echo $TAG | tr a-z A-Z)
cat > "$SC/tgt_$TAG.py" <<PYE
import sys, json; sys.path.insert(0, 'Tools/CharacterLookdev_20260930'); from id_common import *
X = np.load(r'$NPY'); X0 = np.load(I+'/head_face_c.npy')
json.dump({'head': X[:24049].round(5).tolist(), 'teeth': X0[24049:28295].round(5).tolist(), 'eyeL': X0[28955:29725].round(5).tolist(), 'eyeR': X0[29725:30495].round(5).tolist()}, open(I+'/target_$TAG.json', 'w')); print('TGT ok')
PYE
"$B" -b --factory-startup --python "$SC/tgt_$TAG.py" 2>&1 | grep TGT
{ echo "import builtins; builtins.ID_FIT = {'name': 'MHC_ID_$U', 'npz_json': r'$(cygpath -w "$(pwd)/$I/target_$TAG.json")'}"; cat $T/ue_id_mhc_fit.py; } > "$SC/idfit_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/idfit_$TAG.py" idfit-$TAG 1500 | grep -o '"export": "[^"]*"' 
"$B" -b --factory-startup --python $T/blender_id_deploy.py -- MHC_ID_$U $I/deploy_$TAG 2>&1 | grep DEPLOY | cut -c1-160
{ echo "import builtins; builtins.FM_FACE = {'dir': r'$(cygpath -w "$(pwd)/$I/deploy_$TAG")', 'name': 'SKM_ID_FaceMesh_$TAG', 'folder': '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face'}"; cat $T/ue_fm_face_setup_bake.py; } > "$SC/id_bake_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/id_bake_$TAG.py" id-bake-$TAG 1500 | grep -o 'FM_FACE_BAKE.\{0,60\}\|"morphs_after": [0-9]*\|"dirty_after": \[[^]]*\]'
H=/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Hair
if [[ $HT == id* ]]; then GM=$(python_get() { :; }; "/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" -c "import json; d=json.load(open('$I/hair_grooms.json')); print(d['main']+'|'+d['loose'])"); HM=${GM%%|*}; HL=${GM#*|}; else HM=$H/GR_LK_Hair_Main_$HT; HL=$H/GR_LK_Hair_Loose_$HT; fi
{ echo "import builtins; builtins.FM_BIND = {'face': '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/SKM_ID_FaceMesh_$TAG', 'suffix': '$TAG', 'prefix': 'GB_ID', 'folder': '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/Bindings', 'grooms': {'HairMain': '$HM', 'HairLoose': '$HL', 'Eyebrows': '/Game/MetaHumans/MH_MainCharacter/Grooms/Eyebrows_M_Slit', 'Eyelashes': '/Game/MetaHumans/MH_MainCharacter/Grooms/Eyelashes_L_Curl'}}"; cat $T/ue_fm_bind.py; } > "$SC/id_bind_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/id_bind_$TAG.py" id-bind-$TAG 900 | tail -1 | grep -o '"dirty": \[[^]]*\]'
bash $T/id_face_captures.sh i$TAG $TAG $HT ${4:-clay,real} 2>&1 | grep -E "DONE|ERROR"
