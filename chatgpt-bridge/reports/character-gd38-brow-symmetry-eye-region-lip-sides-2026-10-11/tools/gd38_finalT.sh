#!/bin/bash
# gd38_finalT.sh : GD38 chain (ALL writes in GD38 folders / new names; GD31..GD37 assets read-only)
# 0 MHC_GD37_N37 (GD37 final, unrigged fit asset) duplicated to MHC_GD38_N37base   1 fit + 3 residual-feedback fits of data/head_T38.npy
# (gd38_edit: perioral sides 2.5 mm back with the mouth-corner pockets kept; right eye region = eyeball onto the aligned mirror of the left
# (-0.74/-1.49/-0.10 mm), lids rigid with it, under-eye bag + brow ridge from the aligned mirror of the left) -> MHC_GD38_T38
# 2 auto-rig -> SKM_GD38_Face_t38 + DNA   3 brow: SYMMETRIC stations brow3d_s8.json (right brow = aligned mirror of the left, heads 2.5 mm
# medial), ds7 parameters + n4 colour, rebuilt on the new post-rig skin   4 lashes   5 GD35 look + captures
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; N=Saved/Codex/GD38_Identity_20261011; T=$N/tools; R=Tools/OutfitHome_20260929/run_of.sh
G=/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011; G31=/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011; G35=/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011; CG=Content/Sphirus/CharacterLab/GD38_IdentityMaster_20261011
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; m() { cygpath -m "$(pwd)/$1"; }; Wp() { cygpath -w "$(pwd)/$1"; }
bash $T/gd38_memguard.sh 22 | tail -1; mkdir -p $N/mhc $N/jobs $N/rig
if [ ! -e $CG/MHC/MHC_GD38_N37base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '/Game/Sphirus/CharacterLab/GD37_IdentityMaster_20261011/MHC/MHC_GD37_N37', 'dst': '$G/MHC/MHC_GD38_N37base', 'out': r'$(Wp $N/mhc)', 'tag': 'N37base'}"; cat $T/ue_gd38_mhc.py; } > $N/mhc/job_dup.py
 MSYS_NO_PATHCONV=1 bash $R $N/mhc/job_dup.py gd38-dup 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
[ -e $CG/MHC/MHC_GD38_N37base.uasset ] || { echo DUP_GATE_STOP; exit 2; }
echo "== FIT T38"; bash $T/gd38_fitfb4.sh MHC_GD38_N37base MHC_GD38_T38 $N/data/head_T38.npy T38
[ -f $N/data/head_T38_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $T/gd38_memguard.sh 22 | tail -1
echo "== RIG t38"; bash $T/gd38_ue_cycle.sh MHC_GD38_T38 t38 || { echo RIG_STOP; exit 4; }
[ -f $N/data/head_t38_postrig.npy ] || { echo POSTRIG_GATE_STOP; exit 5; }
echo "== BROW ds8s (symmetric stations) on the new skin"; mkdir -p $N/brow/ds8t38
env BR_LEN=0.6 BR_HEAD_ANG=45 BR_HEADLEN=0.40 BR_HEAD_DENS=0.45 BR_BODY_UP=18 BR_BODY_DOWN=-16 BR_ROOT_HI=0.88 BR_ROOT_LO=-0.15 BR_SEED=13 BR_N=2990 BR_TAIL_U=0.50 BR_TAIL_MID=0.35 BR_TAIL_DENS=0.04 BR_TAIL_LEN=0.30 \
  "$BL" -b --factory-startup --python "$(cygpath -w $T/gd38_brow.py)" -- "$(m $N/data/head_t38_postrig.npy)" "$(m $N/data/brow3d_s8.json)" "$(m $N/brow/ds8t38)" 2>&1 | grep -oE "BROW_OK [0-9]+"
{ echo "import builtins; builtins.GD17_BROW = {'abc': r'$(Wp $N/brow/ds8t38/brow_main.abc)', 'tag': 'ds8s', 'face': '$G/Face/SKM_GD38_Face_t38', 'facetag': 't38', 'width': 0.0095, 'tip': 0.5, 'shadow': 1.0, 'mi': '$G35/Looks/MI_GD35_BrowS_n4'}"; cat $T/ue_gd38_brow_import.py; } > $N/jobs/browimp_t38.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/browimp_t38.py)" gd38-browimp 900 | grep -oE '"binding": "[^"]*"|Traceback.*|AssertionError.*'
echo "== LASH binding"; { echo "import builtins; builtins.GD38_BIND = {'face': '$G/Face/SKM_GD38_Face_t38', 'items': [('$G31/Grooms/GR_GD31_Eyelashes_S_Thin', '$G/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38', '/MetaHumanCharacter/Optional/Grooms/GroomMesh/SKM_Groom_Head_Legacy02')]}"; cat $T/ue_gd38_bind.py; } > $N/jobs/bind_lash_t38.py
MSYS_NO_PATHCONV=1 bash $R "$(Wp $N/jobs/bind_lash_t38.py)" gd38-bindlash 900 | grep -oE "GD38_BIND.*|Traceback.*|AssertionError.*"
echo "== LOOK + CAPTURES"; bash $T/gd38_memguard.sh 26 | tail -1
FACE=$G/Face/SKM_GD38_Face_t38 HAIRMAIN_B=$G/Face/Bindings/GB_GD38_HairMain_t38h75c HAIRLOOSE_B=$G/Face/Bindings/GB_GD38_HairLoose_t38h75c LASH_B=$G/Face/Bindings/GB_GD38_EyelashesS_Thin31_t38 \
  bash $T/gd38_comp.sh $G/Grooms/GR_GD38_BrowCustom_ds8s $G/Face/Bindings/GB_GD38_EyebrowsCustom_ds8s_t38 | grep -oE "GD38_COMP.*|LK_QA_SCENE_READY|Trace.*"
bash $T/gd38_caps.sh t38 refnh,ref,common | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
RESTF=rest_cases2.json REST=lid60 bash $T/gd38_caps.sh t38e rest,resth | grep -E "ERROR|TIMEOUT|REQ_FAIL|CAPS_DONE"
LIGHT=front bash $T/gd38_caps.sh t38f refnh | grep -E "DONE|ERROR|TIMEOUT|REQ_FAIL"
df -h /c | tail -1; echo FINALT38_CAPS_DONE
echo FINALT38_DONE
