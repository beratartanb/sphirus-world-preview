#!/bin/bash
# chainM.sh <face tag e.g. m2> <hair tag e.g. h48a> : after gd11rm_cycle.sh (face rigged, bound to h47a as face-only state) -
# import the M hair, bind: F4ab+<hair> (hair only), <face>+<hair> (combined); capture 7-view sets with provenance for S (F4ab+h47a, L bindings), FO (<face>+h47a), HO (F4ab+<hair>), C (<face>+<hair>);
# facecu for S/FO/C; then technical for C: RL, pitch, rig, motion, clean-restart LOD tune, reopen, after, LOD distance, checkpoint verify.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; f=${1:?face tag}; t=${2:?hair tag}; T=Tools/CharacterLookdev_20260930; M=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005; MD=Saved/Codex/GD11_HeadRefinementM_20261005
F4=/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab; FM=$M/Face/SKM_G11RM_Face_$f; BP=$M/Face/Bindings/GB_G11RM; LB=/Game/Sphirus/CharacterLab/GD11_HeadRefinementL_20261005/Face/Bindings/GB_G11RL
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
SKIP_BUILD=1 bash $T/gd11rm_hair_cycle.sh $t x | grep -E "HAIR_DONE|LMD|Traceback"
FACE=$F4 HAIR=gm:$t BSUF=f4ab$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rm_face_run.sh f4ab | grep -E "GD_LB|dirty|REFUSE|Traceback"
FACE=$FM HAIR=gm:$t BSUF=$f$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rm_face_run.sh $f | grep -E "GD_LB|dirty|REFUSE|Traceback"
cap() { CAND_ID="$2" bash $T/gd11rm_caps.sh $1 $3 $4 $5 $6 $7 | grep -E "G11RM_PROV|DONE|REFUSE|ERROR"; }
cap g11rmS  "S: F4ab + h47a (L bindings f4abh47a) + k10" $F4 $LB f4abh47a gl:h47a whole,cu,fx
cap g11rmFO "FO: $f + h47a (M bindings ${f}h47a) + k10" $FM $BP ${f}h47a gl:h47a whole,cu,fx
cap g11rmHO "HO: F4ab + $t (M bindings f4ab$t) + k10" $F4 $BP f4ab$t gm:$t whole,cu,fx
cap g11rmC  "C: $f + $t (M bindings $f$t) + k10" $FM $BP $f$t gm:$t whole,layers,cu,fx
SKIN_C=gck10 bash $T/gd11rm_combo.sh g11rmSfc $F4 gl:h47a $LB f4abh47a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 bash $T/gd11rm_combo.sh g11rmFOfc $FM gl:h47a $BP ${f}h47a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 bash $T/gd11rm_combo.sh g11rmCfc $FM gm:$t $BP $f$t facecu | grep -E "DONE|ERROR"
comp() { FACE=$FM NOBIND=1 BINDPFX=$BP BSUF=$f$t HAIR=gm:$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rm_face_run.sh x | grep COMP4; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
  { echo "import builtins; builtins.G11RM_PROV = {'label': '$1', 'candidate': 'C: $f + $t (M bindings $f$t) + k10', 'out': r'$(cygpath -w "$(pwd)/$MD/prov/$1.json")'}"; cat $T/ue_g11rm_provenance.py; } > "$SC/prov_$1.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$1.py" prov 300 | grep -o "G11RM_PROV"; }
cap g11rmRL "C" $FM $BP $f$t gm:$t rl
cap g11rmP "C" $FM $BP $f$t gm:$t pitch
comp g11rmrig; bash $T/gd11r_capcases.sh g11rmrig "json.load(open('$MD/data/tech_cases.json'))['g11rmrig']"
comp g11rmmot; bash $T/gd11r_capcases.sh g11rmmot "json.load(open('$MD/data/tech_cases.json'))['g11rmmot']"
bash $T/lk_editor_restart.sh g11rm_lod | tail -1
{ echo "import builtins; builtins.G11RM_LOD = {'grooms': {'Main': '$M/Hair/GR_LK_Hair_Main_${t}', 'Loose': '$M/Hair/GR_LK_Hair_Loose_${t}'}, 'thickness': [1.0, 1.25, 1.7, 1.0]}"; cat $T/ue_g11rm_hairlod_tune.py; } > "$SC/lodtune_m.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/lodtune_m.py" lodtune 900 | grep G11RM_LOD | cut -c1-300
bash $T/lk_editor_restart.sh g11rm_reopen | tail -1
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11rm_reopen.py")" reopen 900 | grep -o "G11RM_REOPEN2.*\|\"dirty_before\": \[[^]]*\]\|\"dirty_after\": \[[^]]*\]\|\"morph_total\": [0-9]*\|\"dna\": \"[^\"]*\"\|Traceback.*"
cap g11rmafter "C" $FM $BP $f$t gm:$t whole,fx
comp g11rmlod; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_g11rf_dome20.py" dome20 300 | grep -c DOME20
bash $T/gd11r_capcases.sh g11rmlod "[dict(name='g11rmlod_%s_%d' % (k, d), view='custom', cam=([0, d, 160, -90, 0] if k == 'f' else [d*0.7071, d*0.7071, 160, -135, 0] if k == 'd' else [-d*0.7071, -d*0.7071, 160, 45, 0]), fov=15, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160) for d in (125, 300, 600, 900, 1200, 1600, 2000, 2500) for k in ('f', 'd', 'b')]"
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" $T/gd11rm_checkpoint.py --verify
echo CHAINM_END
