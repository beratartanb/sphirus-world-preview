#!/bin/bash
# gd_cycle.sh <tag> <head npy> <hair tag> : GUARDIAN face cycle (outputs in CharacterGuardian_20261001): MHC_GD_<TAG> fit + export -> per-LOD BR_Neutral deploy -> SKM_GD_FaceMesh_<tag> -> bindings GB_GD_*_<tag>
# MetaHuman state fit MHC_GD_<TAG> + export -> per-LOD BR_Neutral deploy (+ seam normals) -> SKM_GD_FaceMesh_<tag> -> bindings GB_CR_*_<tag> -> captures c<tag>
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; NPY=$2; HT=$3; C2=Saved/Codex/CharacterGuardian_20261001; T=Tools/CharacterLookdev_20260930
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"; U=$(echo $TAG | tr a-z A-Z); G=/Game/Sphirus/CharacterLab/CharacterGuardian_20261001
cat > "$SC/gdtgt_$TAG.py" <<PYE
import sys, json; sys.path.insert(0, 'Tools/CharacterLookdev_20260930'); from id_common import *
X = np.load(r'$NPY'); X0 = np.load('Saved/Codex/CharacterIdentity_20260930/head_face_c.npy')
json.dump({'head': X[:24049].round(5).tolist(), 'teeth': X[24049:28295].round(5).tolist(), 'eyeL': X[28955:29725].round(5).tolist(), 'eyeR': X[29725:30495].round(5).tolist()}, open('$C2/face/target_$TAG.json', 'w')); print('TGT ok')
PYE
"$B" -b --factory-startup --python "$SC/gdtgt_$TAG.py" 2>&1 | grep TGT
for nm in Base $U; do
  if [ $nm = Base ] && [ -f $C2/face/export_MHC_GD_Base.json ]; then continue; fi
  J=""; [ $nm != Base ] && J=", 'npz_json': r'$(cygpath -w "$(pwd)/$C2/face/target_$TAG.json")'"
  { echo "import builtins; builtins.ID_FIT = {'name': 'MHC_GD_$nm', 'folder': '$G/MHC', 'outdir': '$C2/face'$J}"; cat $T/ue_id_mhc_fit.py; } > "$SC/gdfit_$nm.py"
  bash Tools/OutfitHome_20260929/run_of.sh "$SC/gdfit_$nm.py" gdfit-$nm 1500 | grep -o '"export": "[^"]*"'
done
ID_EXPORT_DIR=$C2/face "$B" -b --factory-startup --python $T/blender_id_deploy.py -- MHC_GD_$U $C2/face/deploy_$TAG MHC_GD_Base 2>&1 | grep DEPLOY | cut -c1-160
{ echo "import builtins; builtins.FM_FACE = {'dir': r'$(cygpath -w "$(pwd)/$C2/face/deploy_$TAG")', 'name': 'SKM_GD_FaceMesh_$TAG', 'folder': '$G/Face'}"; cat $T/ue_fm_face_setup_bake.py; } > "$SC/gdbake_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/gdbake_$TAG.py" gdbake-$TAG 1500 | grep -o '"seam_normal_override": true\|"morphs_after": [0-9]*\|"dirty_after": \[[^]]*\]'
GM=$(cat $C2/hair_grooms.json 2>/dev/null); H=/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Hair
HM=$H/GR_LK_Hair_Main_$HT; HL=$H/GR_LK_Hair_Loose_$HT; case $HT in cr:*) HM=/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Hair/GR_LK_Hair_Main_${HT#cr:}; HL=/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Hair/GR_LK_Hair_Loose_${HT#cr:};; esac
{ echo "import builtins; builtins.FM_BIND = {'face': '$G/Face/SKM_GD_FaceMesh_$TAG', 'suffix': '$TAG', 'prefix': 'GB_GD', 'folder': '$G/Face/Bindings', 'grooms': {'HairMain': '$HM', 'HairLoose': '$HL', 'Eyebrows': '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyebrows_Soft', 'Eyelashes': '/Game/MetaHumans/MH_MainCharacter/Grooms/Eyelashes_L_Curl'}}"; cat $T/ue_fm_bind.py; } > "$SC/gdbind_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/gdbind_$TAG.py" gdbind-$TAG 900 | tail -1 | grep -o '"dirty": \[[^]]*\]'
echo GD_CYCLE_DONE $TAG
