#!/bin/bash
# gd4_hair_cycle.sh <tag> : GUARDIAN-4 hair (assets in CharacterGuardian8_20261002/Hair): build (unless SKIP_BUILD), import, sim, helmet + LODs, DEFAULT LOD mode. Face bindings are made by gd7_face_run.sh (source mesh = P face).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; FS=$2; T=Tools/CharacterLookdev_20260930; HD=Saved/Codex/CharacterGuardian8_20261002/hair/$TAG; R=Tools/OutfitHome_20260929/run_of.sh
G=/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002; E=Saved/Codex/CharacterLookdev_20260930; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
[ -n "${SKIP_BUILD:-}" ] || env $(grep -v '^$' $HD/build_env.txt | tr '\n' ' ') "$B" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_gd8_hair.py")" -- "$(cygpath -w "$(pwd)/Saved/Codex/CharacterFinal_20260929/sculpt_package_v6.json.gz")" "$(cygpath -w "$(pwd)/$HD")" > $HD/build_log.txt 2>&1; ls $HD/hair_main.abc
MAT="{'hairMelanin': 0.50, 'hairRedness': 0.50, 'RedVariation': 0.18, 'MelaninVariationFine': 0.8, 'MelaninVariationRough': 0.6, 'Desat': 0.08, 'Ombre': 0.0, 'OmbreShift': 0.5, 'OmbreContrast': 0.2, 'OmbreIntensity': 0.0, 'OmbreMelanin': 0.50, 'OmbreRedness': 0.50, 'Highlights': 1.0, 'HighlightsMelanin': 0.44, 'HighlightsRedness': 0.52, 'HighlightsIntensity': 0.02, 'HighlightsBlending': 0.6, 'HighlightsRootDistance': 0.3, 'RoughnessOverall': 0.78, 'HairRoughness': 0.64, 'Roughness': 0.78, 'Spec0': 0.20, 'Spec1': 0.30, 'Scraggle': 0.30, 'LightAmount': 0.3}"
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR = {'dir': r'$(cygpath -w "$(pwd)/$HD")', 'tag': '$TAG', 'mi': 'MI_GD_Hair_$TAG', 'mat': $MAT, 'width_main': 0.0075, 'width_loose': 0.006, 'mi_loose': 'MI_GD_HairLoose_$TAG', 'mat_loose': {'OmbreIntensity': 0.0, 'OmbreMelanin': 0.52, 'OmbreRedness': 0.50, 'HighlightsIntensity': 0.0, 'hairMelanin': 0.56}}"; cat $T/ue_lk_hair.py; } > "$SC/gd4_hair_$TAG.py"
bash $R "$SC/gd4_hair_$TAG.py" gdhair-$TAG 1800 | grep -E "^(OK|ERROR)|Traceback" | head -3
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR_TAG = '$TAG'; builtins.LK_SIM = {'BendStiffness': '0.450000', 'BendDamping': '0.150000', 'AirDrag': '0.300000'}"; cat $T/ue_lk_hair_sim.py; } > "$SC/gd4_sim_$TAG.py"; bash $R "$SC/gd4_sim_$TAG.py" gdsim-$TAG 900 | grep -E "^(OK|ERROR)|Traceback" | head -2
{ echo "import builtins; builtins.SPH_HAIR_DIR = '$G/Hair'; builtins.RV_HAIR_TAG = '$TAG'"; cat $T/ue_lk_hair_save.py; } > "$SC/gd4_simsave_$TAG.py"; bash $R "$SC/gd4_simsave_$TAG.py" gdsimsave-$TAG 900 | grep -E "SAVED|ERROR" | head -2
"$B" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_lk_hair_helmet.py")" -- "$(cygpath -w "$(pwd)/$HD/hair_main.abc")" "$(cygpath -w "$(pwd)/$HD/hair_loose.abc")" "$(cygpath -w "$(pwd)/$HD/helmet.json")" 2500 > /dev/null 2>&1; ls $HD/helmet.json
{ echo "import builtins; builtins.LK_HAIR_LOD = {'tag': '$TAG', 'dir': '$G/Hair', 'helmet_json': r'$(cygpath -w "$(pwd)/$HD/helmet.json")'}"; cat $T/ue_lk_hair_lods.py; } > "$SC/gd4_lods_$TAG.py"; bash $R "$SC/gd4_lods_$TAG.py" gdlods-$TAG 1200 | grep -E "^(OK|ERROR)|Traceback" | head -2
cat > "$SC/gd4_lmd_$TAG.py" <<PYE
import unreal as u, json
out = {}
for part in ('Main', 'Loose'):
    g = u.load_asset('$G/Hair/GR_LK_Hair_'+part+'_$TAG'); g.set_editor_property('lod_mode', u.GroomLODMode.DEFAULT); out[part] = [str(g.get_editor_property('lod_mode')), u.EditorAssetLibrary.save_loaded_asset(g, False)]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('LMD', json.dumps(out))
PYE
bash $R "$SC/gd4_lmd_$TAG.py" gdlmd-$TAG 600 | grep -E "LMD|Traceback" | cut -c1-200
echo "{\"main\": \"$G/Hair/GR_LK_Hair_Main_$TAG\", \"loose\": \"$G/Hair/GR_LK_Hair_Loose_$TAG\", \"tag\": \"$TAG\"}" > Saved/Codex/CharacterGuardian8_20261002/hair_grooms.json
echo GD8_HAIR_DONE $TAG
