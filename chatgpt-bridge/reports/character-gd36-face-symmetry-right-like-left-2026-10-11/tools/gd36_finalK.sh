#!/bin/bash
# gd36_finalK.sh (= gd36_final.sh with the corrected target K100: cranium / back of head, neck and ears exactly unmoved; 4-fit feedback) : GD36 face symmetry chain (ALL writes in GD36 folders / new names; GD31..GD35 assets read-only)
# 0 MHC_GD31_G31 (GD31 final) duplicated to MHC_GD36_G31base   1 fit + 2 residual-feedback fits of data/head_H100.npy -> MHC_GD36_G36
# 2 auto-rig -> SKM_GD36_Face_k36 + DNA (+ cycle bindings / studio)   3 GD35 brow ds7 (tail fade, n4 colour) rebuilt on the NEW post-rig skin
# (right brow ridge moved) and bound   4 lashes (GD31 S_Thin) binding   5 GD35 look on the new face + captures (studio refnh / ref, calm-eye rest
# pose with hair, symmetric front light, fixed common cameras incl. the right profile)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD36_Identity_20261011; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh
G=/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011; G31=/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011; G35=/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011; CG=Content/Sphirus/CharacterLab/GD36_IdentityMaster_20261011
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }; Wp() { cygpath -w "$(pwd)/$1"; }
bash $T/gd36_memguard.sh 22 | tail -1; mkdir -p $N/mhc $N/jobs $N/rig
if [ ! -e $CG/MHC/MHC_GD36_G31base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G31/MHC/MHC_GD31_G31', 'dst': '$G/MHC/MHC_GD36_G31base', 'out': r'$(Wp $N/mhc)', 'tag': 'G31base'}"; cat $T/ue_gd36_mhc.py; } > $N/mhc/job_dup.py
 MSYS_NO_PATHCONV=1 bash $R $N/mhc/job_dup.py gd36-dup 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
[ -e $CG/MHC/MHC_GD36_G31base.uasset ] || { echo DUP_GATE_STOP; exit 2; }
echo "== FIT G36"; bash $T/gd36_fitfb4.sh MHC_GD36_G31base MHC_GD36_K36 $N/data/head_K100.npy K36
[ -f $N/data/head_K36_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $T/gd36_memguard.sh 22 | tail -1
echo "== RIG g36"; bash $T/gd36_ue_cycle.sh MHC_GD36_K36 k36 || { echo RIG_STOP; exit 4; }
[ -f $N/data/head_k36_postrig.npy ] || { echo POSTRIG_GATE_STOP; exit 5; }
echo "== BROW ds7 on the new skin"; mkdir -p $N/brow/ds7k36
env BR_LEN=0.6 BR_HEAD_ANG=45 BR_HEADLEN=0.40 BR_HEAD_DENS=0.45 BR_BODY_UP=18 BR_BODY_DOWN=-16 BR_ROOT_HI=0.88 BR_ROOT_LO=-0.15 BR_SEED=13 BR_N=2990 BR_TAIL_U=0.50 BR_TAIL_MID=0.35 BR_TAIL_DENS=0.04 BR_TAIL_LEN=0.30 \
  "$BL" -b --factory-startup --python "$(cygpath -w $T/gd36_brow.py)" -- "$(m $N/data/head_k36_postrig.npy)" "$(m $N/data/brow3d_s5.json)" "$(m $N/brow/ds7k36)" 2>&1 | grep -oE "BROW_OK [0-9]+"
{ echo "import builtins; builtins.GD17_BROW = {'abc': r'$(Wp $N/brow/ds7k36/brow_main.abc)', 'tag': 'ds7n4k', 'face': '$G/Face/SKM_GD36_Face_k36', 'facetag': 'k36', 'width': 0.0095, 'tip': 0.5, 'shadow': 1.0, 'mi': '$G35/Looks/MI_GD35_BrowS_n4'}"; cat $T/ue_gd36_brow_import.py; } > $N/jobs/browimp_k36.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/browimp_k36.py)" gd36-browimp 900 | grep -oE '"binding": "[^"]*"|Traceback.*|AssertionError.*'
echo "== LASH binding"; { echo "import builtins; builtins.GD36_BIND = {'face': '$G/Face/SKM_GD36_Face_k36', 'items': [('$G31/Grooms/GR_GD31_Eyelashes_S_Thin', '$G/Face/Bindings/GB_GD36_EyelashesS_Thin31_k36', '/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy02')]}"; cat $T/ue_gd36_bind.py; } > $N/jobs/bind_lash_k36.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/bind_lash_k36.py)" gd36-bindlash 900 | grep -oE "GD36_BIND.*|Traceback.*|AssertionError.*"
echo "== LOOK + CAPTURES"; bash $T/gd36_memguard.sh 26 | tail -1
FACE=$G/Face/SKM_GD36_Face_k36 HAIRMAIN_B=$G/Face/Bindings/GB_GD36_HairMain_k36h75c HAIRLOOSE_B=$G/Face/Bindings/GB_GD36_HairLoose_k36h75c LASH_B=$G/Face/Bindings/GB_GD36_EyelashesS_Thin31_k36 \
  bash $T/gd36_comp.sh $G/Grooms/GR_GD36_BrowCustom_ds7n4k $G/Face/Bindings/GB_GD36_EyebrowsCustom_ds7n4k_k36 | grep -oE "GD36_COMP.*|LK_QA_SCENE_READY|Trace.*"
bash $T/gd36_caps.sh k36 refnh,ref,common | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
RESTF=rest_cases2.json REST=lid60 bash $T/gd36_caps.sh k36e rest,resth | grep -E "ERROR|TIMEOUT|REQ_FAIL|CAPS_DONE"
LIGHT=front bash $T/gd36_caps.sh k36f refnh | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
df -h /c | tail -1; echo FINALK36_CAPS_DONE
echo FINALK36_DONE
