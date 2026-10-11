#!/bin/bash
# gd37_finalN.sh : GD37 lip / nose chain (ALL writes in GD37 folders / new names; GD31..GD36 assets read-only)
# 0 MHC_GD36_K36 (GD36 final, unrigged fit asset) duplicated to MHC_GD37_K36base   1 fit + 3 residual-feedback fits of data/head_N2.npy
# (gd37_edit3: border-ridge blunting, lateral upper-lip taper, mouth line +0.8 mm, upper-lip concavity, alae -6.5 %, lower nose -3.5 %) -> MHC_GD37_N37
# 2 auto-rig -> SKM_GD37_Face_n37 + DNA (+ cycle bindings)   3 GD35 brow ds7 (n4 colour) rebuilt on the new post-rig skin and bound
# 4 lashes (GD31 S_Thin) binding   5 GD35 look on the new face + captures (studio refnh / ref, calm-eye rest pose with hair, front light, common cams)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD37_Identity_20261011; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh
G=/Game/Sphirus/CharacterLab/GD37_IdentityMaster_20261011; G31=/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011; G35=/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011; CG=Content/Sphirus/CharacterLab/GD37_IdentityMaster_20261011
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }; Wp() { cygpath -w "$(pwd)/$1"; }
bash $T/gd37_memguard.sh 22 | tail -1; mkdir -p $N/mhc $N/jobs $N/rig
if [ ! -e $CG/MHC/MHC_GD37_K36base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '/Game/Sphirus/CharacterLab/GD36_IdentityMaster_20261011/MHC/MHC_GD36_K36', 'dst': '$G/MHC/MHC_GD37_K36base', 'out': r'$(Wp $N/mhc)', 'tag': 'K36base'}"; cat $T/ue_gd37_mhc.py; } > $N/mhc/job_dup.py
 MSYS_NO_PATHCONV=1 bash $R $N/mhc/job_dup.py gd37-dup 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
[ -e $CG/MHC/MHC_GD37_K36base.uasset ] || { echo DUP_GATE_STOP; exit 2; }
echo "== FIT N37"; bash $T/gd37_fitfb4.sh MHC_GD37_K36base MHC_GD37_N37 $N/data/head_N2.npy N37
[ -f $N/data/head_N37_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $T/gd37_memguard.sh 22 | tail -1
echo "== RIG n37"; bash $T/gd37_ue_cycle.sh MHC_GD37_N37 n37 || { echo RIG_STOP; exit 4; }
[ -f $N/data/head_n37_postrig.npy ] || { echo POSTRIG_GATE_STOP; exit 5; }
echo "== BROW ds7 on the new skin"; mkdir -p $N/brow/ds7n37
env BR_LEN=0.6 BR_HEAD_ANG=45 BR_HEADLEN=0.40 BR_HEAD_DENS=0.45 BR_BODY_UP=18 BR_BODY_DOWN=-16 BR_ROOT_HI=0.88 BR_ROOT_LO=-0.15 BR_SEED=13 BR_N=2990 BR_TAIL_U=0.50 BR_TAIL_MID=0.35 BR_TAIL_DENS=0.04 BR_TAIL_LEN=0.30 \
  "$BL" -b --factory-startup --python "$(cygpath -w $T/gd37_brow.py)" -- "$(m $N/data/head_n37_postrig.npy)" "$(m $N/data/brow3d_s5.json)" "$(m $N/brow/ds7n37)" 2>&1 | grep -oE "BROW_OK [0-9]+"
{ echo "import builtins; builtins.GD17_BROW = {'abc': r'$(Wp $N/brow/ds7n37/brow_main.abc)', 'tag': 'ds7n4k', 'face': '$G/Face/SKM_GD37_Face_n37', 'facetag': 'n37', 'width': 0.0095, 'tip': 0.5, 'shadow': 1.0, 'mi': '$G35/Looks/MI_GD35_BrowS_n4'}"; cat $T/ue_gd37_brow_import.py; } > $N/jobs/browimp_n37.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/browimp_n37.py)" gd37-browimp 900 | grep -oE '"binding": "[^"]*"|Traceback.*|AssertionError.*'
echo "== LASH binding"; { echo "import builtins; builtins.GD37_BIND = {'face': '$G/Face/SKM_GD37_Face_n37', 'items': [('$G31/Grooms/GR_GD31_Eyelashes_S_Thin', '$G/Face/Bindings/GB_GD37_EyelashesS_Thin31_n37', '/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy02')]}"; cat $T/ue_gd37_bind.py; } > $N/jobs/bind_lash_n37.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/bind_lash_n37.py)" gd37-bindlash 900 | grep -oE "GD37_BIND.*|Traceback.*|AssertionError.*"
echo "== LOOK + CAPTURES"; bash $T/gd37_memguard.sh 26 | tail -1
FACE=$G/Face/SKM_GD37_Face_n37 HAIRMAIN_B=$G/Face/Bindings/GB_GD37_HairMain_n37h75c HAIRLOOSE_B=$G/Face/Bindings/GB_GD37_HairLoose_n37h75c LASH_B=$G/Face/Bindings/GB_GD37_EyelashesS_Thin31_n37 \
  bash $T/gd37_comp.sh $G/Grooms/GR_GD37_BrowCustom_ds7n4k $G/Face/Bindings/GB_GD37_EyebrowsCustom_ds7n4k_n37 | grep -oE "GD37_COMP.*|LK_QA_SCENE_READY|Trace.*"
bash $T/gd37_caps.sh n37 refnh,ref,common | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
RESTF=rest_cases2.json REST=lid60 bash $T/gd37_caps.sh n37e rest,resth | grep -E "ERROR|TIMEOUT|REQ_FAIL|CAPS_DONE"
LIGHT=front bash $T/gd37_caps.sh n37f refnh | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
df -h /c | tail -1; echo FINALN37_CAPS_DONE
echo FINALN37_DONE
