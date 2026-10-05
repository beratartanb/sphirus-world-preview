#!/bin/bash
# chainN.sh <face tag n1> <hair tag h49a> <BROW name> : after gd11rn_cycle.sh (face n1 rigged + bound to h48a with the current brow):
# bind hair-only (m2+h49a), combined (n1+h49a) with BROW; capture with provenance: S (m2+h48a, M bindings), BO (m2+h48a, BROW), NO (n1+h48a), HO (m2+h49a), C (n1+h49a+BROW);
# main-only hair sets (HairLoose hidden), facecu for S/NO/C, sky (gameplay-like) light for S and C; technical set for C; LOD property listing; reopen; checkpoint.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; f=${1:?face tag}; t=${2:?hair tag}; BR=${3:?brow}; T=Tools/CharacterLookdev_20260930; N=/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005; ND=Saved/Codex/GD11_HeadRefinementN_20261005
FM=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2; FN=$N/Face/SKM_G11RN_Face_$f; BP=$N/Face/Bindings/GB_G11RN; MB=/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/Bindings/GB_G11RM
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
SKIP_BUILD=1 bash $T/gd11rn_hair_cycle.sh $t x | grep -E "HAIR_DONE|LMD|Traceback"
FACE=$FM HAIR=gn:$t BSUF=m2$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rn_face_run.sh m2 | grep -E "GD_LB|REFUSE|Traceback" | cut -c1-100
BROW=$BR FACE=$FN HAIR=gn:$t BSUF=$f$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rn_face_run.sh $f | grep -E "GD_LB|REFUSE|Traceback" | cut -c1-100
cap() { CAND_ID="$2" BROW=${8:-M_SlightArch} bash $T/gd11rn_caps.sh $1 $3 $4 $5 $6 $7 | grep -E "G11RN_PROV|DONE|REFUSE|ERROR"; }
MAIN="('mo_front', [0, 125, 159, -90, 0], 15, 'studio', ['HairLoose']), ('mo_q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15, 'studio', ['HairLoose']), ('mo_q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15, 'studio', ['HairLoose']), ('mo_profR', [-125, 3, 160, 0, 0], 15, 'studio', ['HairLoose']), ('mo_profL', [125, 3, 160, 180, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qR', [-88, -88, 161, 45, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qL', [88, -88, 161, 135, 0], 15, 'studio', ['HairLoose']), ('mo_back', [0, -125, 159, 90, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qR_lit', [-88, -88, 161, 45, 0], 15, 'rearR', ['HairLoose']), ('mo_profR_lit', [-125, -2, 161, 0, 0], 17, 'rearR', ['HairLoose'])"
mainonly() { bash $T/gd11r_capcases.sh $1 "[dict(name='$1'+'_'+n, view='custom', cam=c, fov=fv, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163, hide=h) for n, c, fv, li, h in ($MAIN)]" | grep -E "DONE|ERROR"; }
SKY="('sky_front', [0, 125, 159, -90, 0], 15), ('sky_q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15), ('sky_q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15), ('sky_profR', [-125, 3, 160, 0, 0], 15), ('sky_rear3qR', [-88, -88, 161, 45, 0], 15), ('sky_back', [0, -125, 159, 90, 0], 15), ('sky_fcq3', [-25.4, 50.8, 160.5, -58.0, 1.0], 24.0)"
sky() { bash $T/gd11r_capcases.sh $1 "[dict(name='$1'+'_'+n, view='custom', cam=c, fov=fv, garments=True, materials='real', light='sky', animation=None, time=0, light_target_z=163) for n, c, fv in ($SKY)]" | grep -E "DONE|ERROR"; }
cap g11rnS  "S: m2 + h48a (M bindings m2h48a) + brow M_SlightArch + k10" $FM $MB m2h48a gm:h48a whole,cu,fx M_SlightArch; mainonly g11rnSmo
cap g11rnBO "BO: m2 + h48a + brow $BR (N bindings m2h48a) + k10" $FM $BP m2h48a gm:h48a whole,cu $BR
cap g11rnNO "NO: $f + h48a (N bindings ${f}h48a) + brow M_SlightArch + k10" $FN $BP ${f}h48a gm:h48a whole,cu M_SlightArch
cap g11rnHO "HO: m2 + $t (N bindings m2$t) + brow M_SlightArch + k10" $FM $BP m2$t gn:$t whole,cu,fx M_SlightArch; mainonly g11rnHOmo
cap g11rnC  "C: $f + $t + brow $BR (N bindings $f$t) + k10" $FN $BP $f$t gn:$t whole,layers,cu,fx $BR; mainonly g11rnCmo
SKIN_C=gck10 bash $T/gd11rn_combo.sh g11rnSfc $FM gm:h48a $MB m2h48a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 bash $T/gd11rn_combo.sh g11rnNOfc $FN gm:h48a $BP ${f}h48a facecu | grep -E "DONE|ERROR"
BROW=$BR SKIN_C=gck10 bash $T/gd11rn_combo.sh g11rnCfc $FN gn:$t $BP $f$t facecu | grep -E "DONE|ERROR"
comp() { BROW=${2:-M_SlightArch} FACE=$3 NOBIND=1 BINDPFX=$4 BSUF=$5 HAIR=$6 SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rn_face_run.sh x | grep COMP4; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
  { echo "import builtins; builtins.G11RN_PROV = {'label': '$1', 'candidate': '$7', 'out': r'$(cygpath -w "$(pwd)/$ND/prov/$1.json")'}"; cat $T/ue_g11rn_provenance.py; } > "$SC/prov_$1.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$1.py" prov 300 | grep -o "G11RN_PROV"; }
comp g11rnSsky M_SlightArch $FM $MB m2h48a gm:h48a "S sky light"; sky g11rnSsky
comp g11rnCsky $BR $FN $BP $f$t gn:$t "C sky light"; sky g11rnCsky
cap g11rnRL "C" $FN $BP $f$t gn:$t rl $BR
cap g11rnP "C" $FN $BP $f$t gn:$t pitch $BR
comp g11rnrig $BR $FN $BP $f$t gn:$t "C rig"; bash $T/gd11r_capcases.sh g11rnrig "json.load(open('$ND/data/tech_cases.json'))['g11rnrig']"
comp g11rnmot $BR $FN $BP $f$t gn:$t "C motion"; bash $T/gd11r_capcases.sh g11rnmot "json.load(open('$ND/data/tech_cases.json'))['g11rnmot']"
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11rn_lodprobe.py")" lodprobe 300 | grep -o "G11RN_LODPROBE.*" | cut -c1-900
bash $T/lk_editor_restart.sh g11rn_lod | tail -1
{ echo "import builtins; builtins.G11RN_LOD = {'grooms': {'Main': '$N/Hair/GR_LK_Hair_Main_${t}', 'Loose': '$N/Hair/GR_LK_Hair_Loose_${t}'}, 'thickness': [1.0, 1.25, 1.7, 1.0]}"; cat $T/ue_g11rn_hairlod_tune.py; } > "$SC/lodtune_n.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/lodtune_n.py" lodtune 900 | grep G11RN_LOD | cut -c1-300
bash $T/lk_editor_restart.sh g11rn_reopen | tail -1
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11rn_reopen.py")" reopen 900 | grep -o "G11RN_REOPEN2.*\|\"dirty_before\": \[[^]]*\]\|\"dirty_after\": \[[^]]*\]\|\"morph_total\": [0-9]*\|\"dna\": \"[^\"]*\"\|Traceback.*"
cap g11rnafter "C" $FN $BP $f$t gn:$t whole,fx $BR
comp g11rnlod $BR $FN $BP $f$t gn:$t "C lod"; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_g11rf_dome20.py" dome20 300 | grep -c DOME20
bash $T/gd11r_capcases.sh g11rnlod "[dict(name='g11rnlod_%s_%d' % (k, d), view='custom', cam=([0, d, 160, -90, 0] if k == 'f' else [d*0.7071, d*0.7071, 160, -135, 0] if k == 'd' else [-d*0.7071, -d*0.7071, 160, 45, 0]), fov=15, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160) for d in (125, 300, 600, 900, 1200, 1600, 2000, 2500) for k in ('f', 'd', 'b')]"
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11rn_lodprobe.py")" lodprobe2 300 | grep -o "G11RN_LODPROBE.*" | cut -c1-900
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" $T/gd11rn_checkpoint.py --verify
echo CHAINN_END
