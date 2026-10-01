#!/bin/bash
# gd_henley_full.sh <tag> : GUARDIAN garment chain for an already-built pattern tag (garments/<tag>): weights + corrective solve (same
# flags as cr_garment_full.sh) -> body soft-tissue transfer onto the Henley correctives -> morph LODs -> UE meshes in the Guardian Outfit
# folder with the corrective m1 materials (referenced read-only)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; T=Tools/CharacterLookdev_20260930; TR=Tools/CharacterRevision_20260930; GA=Saved/Codex/CharacterLookdev_20260930/garments/$TAG
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; W() { cygpath -w "$(pwd)/$1"; }
export LK_DEST=/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Outfit
NO_UE=1 SPH_W_UA_SMOOTH=24 SPH_GC_HK=1 SPH_GC_ELBOW=1 SPH_GC_ELB_SIDE=1 SPH_GC_ARM_R=15 SPH_GC_HIP_Z=104 SPH_GC_GRAV="pl_bend30:0.35,pl_bend60:0.7,pl_bend90:0.9" bash $T/lk_garment_chain.sh $TAG g13s 2>&1 | tail -2
cp $GA/morph_lk_garments_cur.json $GA/morph_lk_garments_cur_src.json
"$B" -b --factory-startup --python "$(W $T/blender_cr_softtissue_transfer.py)" -- "$(W Saved/Codex/CharacterCorrective_20261001/body_LK_rv_morphs.npz)" "$(W $GA/outfit_geometry.json.gz)" "$(W $GA/morph_lk_garments_cur_src.json)" "$(W $GA/morph_lk_garments_cur.json)" 2>&1 | grep -oE "STT_OK|Error.*" | head -2
"$B" -b --factory-startup --python "$(W $TR/blender_garment_morph_lods.py)" -- "$(W $GA/outfit_geometry.json.gz)" "$(W $GA)" "$(W $GA/morph_lk_garments_cur.json)" 2>&1 | grep -E "GMORPH" | cut -c1-80
MD=/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit/Materials
FROM_MESHES=1 bash $T/lk_garment_chain.sh $TAG g13s "{'henley': ['$MD/MI_LK_Henley_m1', '$MD/MI_LK_Henley_Trim_m1', '$MD/MI_LK_Buttons_m1'], 'trousers': ['$MD/MI_LK_Shorts_m1', '$MD/MI_LK_Shorts_Trim_m1', '$MD/MI_LK_Drawstring_m1']}" 2>&1 | tail -5
echo GD_HENLEY_DONE $TAG
