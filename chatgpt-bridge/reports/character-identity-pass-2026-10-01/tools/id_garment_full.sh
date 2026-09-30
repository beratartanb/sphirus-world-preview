#!/bin/bash
# id_garment_full.sh <tag> <shorts print json> [builder VAR=value ...] : IDENTITY-pass garment candidate end to end: pattern build (g14h
# construction args + given overrides) -> chain (g14h corrective settings) -> UE meshes (v2 MIs) -> textile textures in the new pattern
# space -> duplicated _<tag> MIs with swapped textures -> mesh slots
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; PRINT=$2; shift 2; T=Tools/CharacterLookdev_20260930; G=Saved/Codex/CharacterLookdev_20260930/garments/$TAG
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
bash $T/lk_garment_cycle.sh $TAG $(cat Saved/Codex/CharacterIdentity_20260930/g14h_args.txt) "$@" 2>&1 | grep -E "BUILD_OK|hem angle|band_top" | cut -c1-120
NO_UE=1 SPH_W_UA_SMOOTH=24 SPH_GC_HK=1 SPH_GC_ELBOW=1 SPH_GC_ELB_SIDE=1 SPH_GC_ARM_R=15 SPH_GC_HIP_Z=104 SPH_GC_GRAV="pl_bend30:0.35,pl_bend60:0.7,pl_bend90:0.9" bash $T/lk_garment_chain.sh $TAG g13s 2>&1 | tail -2
FROM_MESHES=1 bash $T/lk_garment_chain.sh $TAG g13s "{'henley': ['MI_LK_Henley_v2', 'MI_LK_Henley_Trim_v2', 'MI_LK_Buttons_v2'], 'trousers': ['MI_LK_Shorts_v2', 'MI_LK_Shorts_Trim_v2', 'MI_LK_Drawstring_v2']}" 2>&1 | tail -2
mkdir -p $G/tex; SPH_TEX_V2=1 SPH_TEX_SHORTS="$PRINT" "$B" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_lk_textile_tex.py")" -- "$(cygpath -w "$(pwd)/$G/outfit_geometry.json.gz")" "$(cygpath -w "$(pwd)/$G/tex")" 2>&1 | grep -c "saved T_LK"
O=/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Outfit; { echo "import builtins; builtins.ID_TEX = {'tex_dir': r'$(cygpath -w "$(pwd)/$G/tex")', 'suffix': '_$TAG', 'meshes': {}}"; cat $T/ue_id_textile_swap.py; } > "$SC/id_tex_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/id_tex_$TAG.py" id-tex-$TAG 1500 | grep -o '"dirty": \[[^]]*\]'
sed "s/_g15a/_$TAG/g" "$SC/id_slots_g15a.py" > "$SC/id_slots_$TAG.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/id_slots_$TAG.py" id-slots-$TAG 600 | grep -E "SLOTS" | cut -c1-200
echo GARMENT_DONE $TAG
