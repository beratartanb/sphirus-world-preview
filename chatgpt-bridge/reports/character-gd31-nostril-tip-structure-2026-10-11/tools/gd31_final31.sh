#!/bin/bash
# gd31_final31.sh : GD31 final transfer + validation chain (ALL writes in GD31 folders / new names; GD15..GD30 assets read-only)
# 0 MHC_GD30_G30W (GD30 final W4) duplicated to MHC_GD31_G30Wbase   1 fit + 2 residual-feedback fits of data/head_G31S.npy -> MHC_GD31_G31
# 2 auto-rig -> SKM_GD31_Face_g31 + DNA   3 lookdev: texture T_GD31_Head_BC_n3 (GD17 baked base colour with the nostril interior darkened) imported,
# MI_GD31_Face_{lod}_s1t6n_n3 = children of the read-only GD17 s1t6n MIs with only the base colour swapped   4 look: custom brow c4, iris h6,
# lashes S_Thin, hair h75c   5 captures: front light sets + studio set (studio = soft light, closer to the reference photos)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD31_Identity_20261011; G=/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011; G2=/Game/Sphirus/CharacterLab/GD30_IdentityMaster_20261011
export LB_EYE=h6
bash $W/tools/gd31_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"; mkdir -p $W/mhc $W/jobs $W/rig
if [ ! -e Content/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/MHC/MHC_GD31_G30Wbase.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G2/MHC/MHC_GD30_G30W', 'dst': '$D/MHC_GD31_G30Wbase', 'out': r'$Wn', 'tag': 'G30Wbase'}"; cat $W/tools/ue_gd31_mhc.py; } > $W/mhc/job_dup_G30Wbase.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G30Wbase.py gd31-dup-g30wbase 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
[ -e Content/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/MHC/MHC_GD31_G30Wbase.uasset ] || { echo DUP_GATE_STOP; exit 2; }
echo "== FIT G31"; bash $W/tools/gd31_fitfb.sh MHC_GD31_G30Wbase MHC_GD31_G31 $W/data/head_G31S.npy G31
[ -f $W/data/head_G31_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd31_memguard.sh 22 | tail -1
echo "== RIG g31"; bash $W/tools/gd31_ue_cycle.sh MHC_GD31_G31 g31 || { echo RIG_STOP; exit 4; }
echo "== LOOKDEV texture n3 + MIs"
[ -e Content/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/Textures/T_GD31_Head_BC_n3.uasset ] || MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/tools/job_teximp_n3.py gd31-teximp-n3 900 | grep -oE "IMPORTED.{0,200}|Traceback.*|Error.*"
[ -e Content/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/Textures/T_GD31_Head_BC_n3.uasset ] || { echo TEX_GATE_STOP; exit 5; }
MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/tools/job_mk_n3.py gd31-mk-n3 600 | grep -oE "GD31_MK.{0,300}|Traceback.*|AssertionError.*"
[ -e Content/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD0_s1t6n_n3.uasset ] || { echo MI_GATE_STOP; exit 6; }
echo "== LOOK + CAPTURES g31"; bash $W/tools/gd31_memguard.sh 26 | tail -1
LB_SKINP="$G/Looks/MI_GD31_Face_{lod}_s1t6n_n3" bash $W/tools/gd31_browcap.sh c4 g31 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD31_BROW|DONE|ERROR"
bash $W/tools/gd31_caps.sh cg31c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL31_DONE
