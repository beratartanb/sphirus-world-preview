#!/bin/bash
# chainL_tech.sh <hair tag> : technical integration of F4ab + <hair> (L bindings): rig expression set, motion, pitch, RL lights, clean-restart LOD tune, reopen check, after-restart captures, LOD distance set, checkpoint verify
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; t=${1:?hair tag}; T=Tools/CharacterLookdev_20260930; L=/Game/Sphirus/CharacterLab/GD11_HeadRefinementL_20261005; LD=Saved/Codex/GD11_HeadRefinementL_20261005
F4=/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab; BP=$L/Face/Bindings/GB_G11RL; SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
comp() { FACE=$F4 NOBIND=1 BINDPFX=$BP BSUF=f4ab$t HAIR=gl:$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rl_face_run.sh x | grep COMP4; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
  { echo "import builtins; builtins.G11RL_PROV = {'label': '$1', 'candidate': 'F4ab + $t (L bindings f4ab$t) + k10', 'out': r'$(cygpath -w "$(pwd)/$LD/prov/$1.json")'}"; cat $T/ue_g11rl_provenance.py; } > "$SC/prov_$1.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$1.py" prov 300 | grep -o "G11RL_PROV" ; }
bash $T/gd11rl_caps.sh g11rlRL $F4 $BP f4ab$t gl:$t rl | grep -E "DONE|ERROR|REFUSE"
bash $T/gd11rl_caps.sh g11rlP $F4 $BP f4ab$t gl:$t pitch | grep -E "DONE|ERROR|REFUSE"
comp g11rlrig; bash $T/gd11r_capcases.sh g11rlrig "json.load(open('$LD/data/tech_cases.json'))['g11rlrig']"
comp g11rlmot; bash $T/gd11r_capcases.sh g11rlmot "json.load(open('$LD/data/tech_cases.json'))['g11rlmot']"
bash $T/lk_editor_restart.sh g11rl_lod | tail -1
{ echo "import builtins; builtins.G11RL_LOD = {'grooms': {'Main': '$L/Hair/GR_LK_Hair_Main_${t}', 'Loose': '$L/Hair/GR_LK_Hair_Loose_${t}'}, 'thickness': [1.0, 1.25, 1.7, 1.0]}"; cat $T/ue_g11rl_hairlod_tune.py; } > "$SC/lodtune_l.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/lodtune_l.py" lodtune 900 | grep G11RL_LOD | cut -c1-300
bash $T/lk_editor_restart.sh g11rl_reopen | tail -1
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11rl_reopen.py")" reopen 900 | grep -o "G11RL_REOPEN2.*\|\"dirty_before\": \[[^]]*\]\|\"dirty_after\": \[[^]]*\]\|\"morph_total\": [0-9]*\|\"dna\": \"[^\"]*\"\|Traceback.*"
bash $T/gd11rl_caps.sh g11rlafter $F4 $BP f4ab$t gl:$t whole,fx | grep -E "DONE|ERROR|REFUSE"
comp g11rllod; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_g11rf_dome20.py" dome20 300 | grep -c DOME20
bash $T/gd11r_capcases.sh g11rllod "[dict(name='g11rllod_%s_%d' % (k, d), view='custom', cam=([0, d, 160, -90, 0] if k == 'f' else [d*0.7071, d*0.7071, 160, -135, 0] if k == 'd' else [-d*0.7071, -d*0.7071, 160, 45, 0]), fov=15, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160) for d in (125, 300, 600, 900, 1200, 1600, 2000, 2500) for k in ('f', 'd', 'b')]"
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" $T/gd11rl_checkpoint.py --verify
echo CHAINL_TECH_END
