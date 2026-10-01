#!/bin/bash
# gd_hair_cycle.sh <tag> <face tag> : GUARDIAN hair: import strands (Saved/Codex/CharacterGuardian_20261001/hair/<tag>) into the Guardian Hair
# folder (colour adjusted: brown-first auburn, softer ombre / highlights), loose-groom sim + save, helmet + LOD chain, DEFAULT groom LOD mode,
# bindings GB_GD_Hair{Main,Loose}_<face tag>
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; FS=$2; T=Tools/CharacterLookdev_20260930; HD=Saved/Codex/CharacterGuardian_20261001/hair/$TAG; R=Tools/OutfitHome_20260929/run_of.sh
G=/Game/Sphirus/CharacterLab/CharacterGuardian_20261001; E=Saved/Codex/CharacterLookdev_20260930; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
MAT="{'hairMelanin': 0.50, 'hairRedness': 0.50, 'RedVariation': 0.25, 'MelaninVariationFine': 0.8, 'MelaninVariationRough': 0.55, 'Desat': 0.05, 'Ombre': 1.0, 'OmbreShift': 0.5, 'OmbreContrast': 0.2, 'OmbreIntensity': 0.25, 'OmbreMelanin': 0.44, 'OmbreRedness': 0.5, 'Highlights': 1.0, 'HighlightsMelanin': 0.38, 'HighlightsRedness': 0.55, 'HighlightsIntensity': 0.25, 'HighlightsBlending': 0.6, 'HighlightsRootDistance': 0.2, 'RoughnessOverall': 0.70, 'HairRoughness': 0.55, 'Roughness': 0.72, 'Spec0': 0.30, 'Spec1': 0.45, 'Scraggle': 0.30, 'LightAmount': 0.3}"
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR = {'dir': r'$(cygpath -w "$(pwd)/$HD")', 'tag': '$TAG', 'mi': 'MI_GD_Hair_$TAG', 'mat': $MAT, 'width_main': 0.0075, 'width_loose': 0.006, 'mi_loose': 'MI_GD_HairLoose_$TAG', 'mat_loose': {'OmbreIntensity': 0.15, 'OmbreMelanin': 0.5, 'OmbreRedness': 0.46, 'HighlightsIntensity': 0.15, 'hairMelanin': 0.52}}"; cat $T/ue_lk_hair.py; } > "$SC/gd_hair_$TAG.py"
bash $R "$SC/gd_hair_$TAG.py" gdhair-$TAG 1800 | grep -E "^(OK|ERROR)|Traceback" | head -3
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR_TAG = '$TAG'; builtins.LK_SIM = {'BendStiffness': '0.450000', 'BendDamping': '0.150000', 'AirDrag': '0.300000'}"; cat $T/ue_lk_hair_sim.py; } > "$SC/gd_sim_$TAG.py"; bash $R "$SC/gd_sim_$TAG.py" gdsim-$TAG 900 | grep -E "^(OK|ERROR)|Traceback" | head -2
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR_TAG = '$TAG'"; cat $T/ue_lk_hair_save.py; } > "$SC/gd_simsave_$TAG.py"; bash $R "$SC/gd_simsave_$TAG.py" gdsimsave-$TAG 900 | grep -E "SAVED|ERROR" | head -2
"$B" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_lk_hair_helmet.py")" -- "$(cygpath -w "$(pwd)/$HD/hair_main.abc")" "$(cygpath -w "$(pwd)/$HD/hair_loose.abc")" "$(cygpath -w "$(pwd)/$HD/helmet.json")" 2500 > /dev/null 2>&1; ls $HD/helmet.json
{ echo "import builtins; builtins.LK_HAIR_LOD = {'tag': '$TAG', 'dir': '$G/Hair', 'helmet_json': r'$(cygpath -w "$(pwd)/$HD/helmet.json")'}"; cat $T/ue_lk_hair_lods.py; } > "$SC/gd_lods_$TAG.py"; bash $R "$SC/gd_lods_$TAG.py" gdlods-$TAG 1200 | grep -E "^(OK|ERROR)|Traceback" | head -2
cat > "$SC/gd_lmd_$TAG.py" <<PYE
import unreal as u, json
out = {}
for part in ('Main', 'Loose'):
    g = u.load_asset('$G/Hair/GR_LK_Hair_'+part+'_$TAG'); g.set_editor_property('lod_mode', u.GroomLODMode.DEFAULT); out[part] = [str(g.get_editor_property('lod_mode')), u.EditorAssetLibrary.save_loaded_asset(g, False)]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('LMD', json.dumps(out))
PYE
bash $R "$SC/gd_lmd_$TAG.py" gdlmd-$TAG 600 | grep -E "LMD|Traceback" | cut -c1-200
{ echo "import builtins; builtins.FM_BIND = {'face': '$G/Face/SKM_GD_FaceMesh_$FS', 'suffix': '$FS', 'prefix': 'GB_GD', 'folder': '$G/Face/Bindings', 'grooms': {'HairMain': '$G/Hair/GR_LK_Hair_Main_$TAG', 'HairLoose': '$G/Hair/GR_LK_Hair_Loose_$TAG'}}"; cat $T/ue_fm_bind.py; } > "$SC/gd_hbind_$TAG.py"
bash $R "$SC/gd_hbind_$TAG.py" gdhbind-$TAG 900 | tail -1 | grep -o '"dirty": \[[^]]*\]'
echo "{\"main\": \"$G/Hair/GR_LK_Hair_Main_$TAG\", \"loose\": \"$G/Hair/GR_LK_Hair_Loose_$TAG\", \"tag\": \"$TAG\"}" > Saved/Codex/CharacterGuardian_20261001/hair_grooms.json
echo GD_HAIR_DONE $TAG
