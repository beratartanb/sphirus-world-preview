#!/bin/bash
# chainO.sh <face tag o1> <hair tag h50a> <brow tag b1> : after gd11ro_cycle.sh (o1 rigged, bound to h49a with brow M_Fine) and the brow import:
# bindings: n1+h50a (hair only), o1+h50a (combined) with the custom brow; captures with provenance: S (N: n1+h49a+M_Fine), NO (o1+h49a+M_Fine), BO (n1+h49a+custom brow),
# HO (n1+h50a+M_Fine), C (o1+h50a+custom brow); main-only sets (HairLoose hidden); facecu for S/NO/C; gameplay light for S and C; technical set for C; LOD probe; reopen; checkpoint.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; f=${1:?face}; t=${2:?hair}; bt=${3:?brow}; T=Tools/CharacterLookdev_20260930; O=/Game/Sphirus/CharacterLab/GD11_HeadRefinementO_20261005; OD=Saved/Codex/GD11_HeadRefinementO_20261005
FN=/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/Face/SKM_G11RN_Face_n1; FO=$O/Face/SKM_G11RO_Face_$f; BP=$O/Face/Bindings/GB_G11RO; NB=/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/Face/Bindings/GB_G11RN; BROWP=$O/Hair/GR_O_Brow_$bt
SC="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/b05832b1-23f7-44dd-a92f-e1907201ea47/scratchpad"
SKIP_BUILD=1 bash $T/gd11ro_hair_cycle.sh $t x | grep -E "HAIR_DONE|LMD|Traceback"
BROW=M_Fine FACE=$FN HAIR=go:$t BSUF=n1$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11ro_face_run.sh n1 | grep -E "GD_LB|REFUSE|Traceback" | cut -c1-100
BROW=$BROWP FACE=$FO HAIR=go:$t BSUF=$f$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11ro_face_run.sh $f | grep -E "GD_LB|REFUSE|Traceback" | cut -c1-100
{ echo "import builtins; builtins.G11RO_BROW = {'abc': r'$(cygpath -w "$(pwd)/$OD/brow/$bt/brow_main.abc")', 'tag': '$bt', 'faces': {'$f$t': '$FO', 'n1h49a': '$FN'}, 'width': 0.0045, 'shadow': 0.6}"; cat $T/ue_g11ro_brow_import.py; } > "$SC/brow_${bt}_bind.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/brow_${bt}_bind.py" browbind 1800 | grep -o "G11RO_BROW.*" | cut -c1-300
cap() { CAND_ID="$2" BROW=${8:-M_Fine} bash $T/gd11ro_caps.sh $1 $3 $4 $5 $6 $7 | grep -E "G11RO_PROV|DONE|REFUSE|ERROR"; }
MAIN="('mo_front', [0, 125, 159, -90, 0], 15, 'studio', ['HairLoose']), ('mo_q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15, 'studio', ['HairLoose']), ('mo_q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15, 'studio', ['HairLoose']), ('mo_profR', [-125, 3, 160, 0, 0], 15, 'studio', ['HairLoose']), ('mo_profL', [125, 3, 160, 180, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qR', [-88, -88, 161, 45, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qL', [88, -88, 161, 135, 0], 15, 'studio', ['HairLoose']), ('mo_back', [0, -125, 159, 90, 0], 15, 'studio', ['HairLoose']), ('mo_rear3qR_lit', [-88, -88, 161, 45, 0], 15, 'rearR', ['HairLoose']), ('mo_profR_lit', [-125, -2, 161, 0, 0], 17, 'rearR', ['HairLoose'])"
mainonly() { bash $T/gd11r_capcases.sh $1 "[dict(name='$1'+'_'+n, view='custom', cam=c, fov=fv, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=163, hide=h) for n, c, fv, li, h in ($MAIN)]" | grep -E "DONE|ERROR"; }
GP="('gp_front', [0, 125, 159, -90, 0], 15), ('gp_q3R', [-64.468, 113.297, 160.141, -58.0, 1.0], 15), ('gp_q3L', [64.468, 113.297, 160.141, -122.0, 1.0], 15), ('gp_profR', [-125, 3, 160, 0, 0], 15), ('gp_rear3qR', [-88, -88, 161, 45, 0], 15), ('gp_back', [0, -125, 159, 90, 0], 15), ('gp_fcq3', [-25.4, 50.8, 160.5, -58.0, 1.0], 24.0), ('gp_fcfront', [0, 62, 160.0, -90, 0], 22.0)"
gameplay() { bash $T/gd11r_capcases.sh $1 "[dict(name='$1'+'_'+n, view='custom', cam=c, fov=fv, garments=True, materials='real', light='gameplay', animation=None, time=0, light_target_z=163) for n, c, fv in ($GP)]" | grep -E "DONE|ERROR"; }
cap g11roS  "S (N record): n1 + h49a + brow M_Fine (N bindings n1h49a) + k10" $FN $NB n1h49a gn:h49a whole,cu,fx M_Fine; mainonly g11roSmo
cap g11roNO "NO: $f + h49a + brow M_Fine (O bindings ${f}h49a) + k10" $FO $BP ${f}h49a gn:h49a whole,cu M_Fine
cap g11roBO "BO: n1 + h49a + custom brow $bt (O binding EyebrowsCustom_n1h49a) + k10" $FN $NB n1h49a gn:h49a whole,cu $BROWP
cap g11roHO "HO: n1 + $t + brow M_Fine (O bindings n1$t) + k10" $FN $BP n1$t go:$t whole,cu,fx M_Fine; mainonly g11roHOmo
cap g11roC  "C: $f + $t + custom brow $bt (O bindings $f$t) + k10" $FO $BP $f$t go:$t whole,layers,cu,fx $BROWP; mainonly g11roCmo
SKIN_C=gck10 BROW=M_Fine bash $T/gd11ro_combo.sh g11roSfc $FN gn:h49a $NB n1h49a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 BROW=M_Fine bash $T/gd11ro_combo.sh g11roNOfc $FO gn:h49a $BP ${f}h49a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 BROW=$BROWP bash $T/gd11ro_combo.sh g11roCfc $FO go:$t $BP $f$t facecu | grep -E "DONE|ERROR"
comp() { BROW=${2:-M_Fine} FACE=$3 NOBIND=1 BINDPFX=$4 BSUF=$5 HAIR=$6 SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11ro_face_run.sh x | grep COMP4; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_lk_qa_setup.py" lk-setup 300 | tail -1 >/dev/null
  { echo "import builtins; builtins.G11RO_PROV = {'label': '$1', 'candidate': '$7', 'out': r'$(cygpath -w "$(pwd)/$OD/prov/$1.json")'}"; cat $T/ue_g11ro_provenance.py; } > "$SC/prov_$1.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/prov_$1.py" prov 300 | grep -o "G11RO_PROV"; }
SKIN_C=gck10 BROW=$BROWP bash $T/gd11ro_combo.sh g11roBOfc $FN gn:h49a $NB n1h49a facecu | grep -E "DONE|ERROR"
SKIN_C=gck10 BROW=M_Fine bash $T/gd11ro_combo.sh g11roHOfc $FN go:$t $BP n1$t facecu | grep -E "DONE|ERROR"
NOSE="('nosefront', [0, 52, 158.5, -90, 0], 11.0), ('noselow', [0, 52, 149.5, -90, 17], 11.0), ('noselow3q', [-20, 46, 148.5, -66, 16], 12.0), ('fcq3L', [25.4, 50.8, 160.5, -122.0, 1.0], 24.0), ('fcprofL', [52, 2, 159.5, 180, 0], 14.0), ('fcprofR', [-52, 2, 159.5, 0, 0], 14.0)"
nose() { bash $T/gd11r_capcases.sh $1 "[dict(name='$1'+'_studio_'+n, view='custom', cam=c, fov=fv, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=158) for n, c, fv in ($NOSE)]" | grep -E "DONE|ERROR"; }
comp g11roSn M_Fine $FN $NB n1h49a gn:h49a "S nose set"; nose g11roSn
comp g11roNOn M_Fine $FO $BP ${f}h49a gn:h49a "NO nose set"; nose g11roNOn
comp g11roCn $BROWP $FO $BP $f$t go:$t "C nose set"; nose g11roCn
comp g11roSgp M_Fine $FN $NB n1h49a gn:h49a "S gameplay light (sun+sky)"; gameplay g11roSgp
comp g11roCgp $BROWP $FO $BP $f$t go:$t "C gameplay light (sun+sky)"; gameplay g11roCgp
cap g11roRL "C" $FO $BP $f$t go:$t rl $BROWP
cap g11roP "C" $FO $BP $f$t go:$t pitch $BROWP
comp g11rorig $BROWP $FO $BP $f$t go:$t "C rig"; bash $T/gd11r_capcases.sh g11rorig "json.load(open('$OD/data/tech_cases.json'))['g11rorig']"
comp g11romot $BROWP $FO $BP $f$t go:$t "C motion"; bash $T/gd11r_capcases.sh g11romot "json.load(open('$OD/data/tech_cases.json'))['g11romot']"
bash $T/lk_editor_restart.sh g11ro_lod | tail -1
{ echo "import builtins; builtins.G11RO_LOD = {'grooms': {'Main': '$O/Hair/GR_LK_Hair_Main_${t}', 'Loose': '$O/Hair/GR_LK_Hair_Loose_${t}'}, 'thickness': [1.0, 1.25, 1.7, 1.0]}"; cat $T/ue_g11ro_hairlod_tune.py; } > "$SC/lodtune_o.py"; bash Tools/OutfitHome_20260929/run_of.sh "$SC/lodtune_o.py" lodtune 900 | grep G11RO_LOD | cut -c1-300
bash $T/lk_editor_restart.sh g11ro_reopen | tail -1
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11ro_reopen.py")" reopen 900 | grep -o "G11RO_REOPEN2.*\|\"dirty_before\": \[[^]]*\]\|\"dirty_after\": \[[^]]*\]\|\"morph_total\": [0-9]*\|\"dna\": \"[^\"]*\"\|Traceback.*"
cap g11roafter "C" $FO $BP $f$t go:$t whole,fx $BROWP
comp g11rolod $BROWP $FO $BP $f$t go:$t "C lod"; bash Tools/OutfitHome_20260929/run_of.sh "$T/ue_g11rf_dome20.py" dome20 300 | grep -c DOME20
bash $T/gd11r_capcases.sh g11rolod "[dict(name='g11rolod_%s_%d' % (k, d), view='custom', cam=([0, d, 160, -90, 0] if k == 'f' else [d*0.7071, d*0.7071, 160, -135, 0] if k == 'd' else [-d*0.7071, -d*0.7071, 160, 45, 0]), fov=15, garments=True, materials='real', light='studio', animation=None, time=0, light_target_z=160) for d in (125, 300, 600, 900, 1200, 1600, 2000, 2500) for k in ('f', 'd', 'b')]"
bash Tools/OutfitHome_20260929/run_of.sh "$(cygpath -w "$(pwd)/$T/ue_g11ro_lodprobe.py")" lodprobe 300 | grep -o "G11RO_LODPROBE.*" | cut -c1-400
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" $T/gd11ro_checkpoint.py --verify
echo CHAINO_END
