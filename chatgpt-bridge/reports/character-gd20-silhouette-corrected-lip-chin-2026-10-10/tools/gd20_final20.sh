#!/bin/bash
# gd20_final20.sh : GD20 final transfer + validation chain (ALL writes in GD20 folders / new names; GD15..GD19 assets read-only)
# 0 MHC_GD19_G19 duplicated to MHC_GD20_G19base   1 fit + 2 residual-feedback fits of data/head_G20S.npy -> MHC_GD20_G20   2 auto-rig -> SKM_GD20_Face_g20 + DNA
# 3 look: custom brow c4, skin s1t6n (GD17 look, read-only), iris h6, lashes S_Thin, hair h75c   4 captures: front light sets + studio set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD20_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD20_IdentityMaster_20261010; G9=/Game/Sphirus/CharacterLab/GD19_IdentityMaster_20261010; G7=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd20_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD20_IdentityMaster_20261010/MHC/MHC_GD20_G19base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G9/MHC/MHC_GD19_G19', 'dst': '$D/MHC_GD20_G19base', 'out': r'$Wn', 'tag': 'G19base'}"; cat $W/tools/ue_gd20_mhc.py; } > $W/mhc/job_dup_G19base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G19base.py gd20-dup-g19base 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G20"; bash $W/tools/gd20_fitfb.sh MHC_GD20_G19base MHC_GD20_G20 $W/data/head_G20S.npy G20
[ -f $W/data/head_G20_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd20_memguard.sh 22 | tail -1
echo "== RIG g20"; bash $W/tools/gd20_ue_cycle.sh MHC_GD20_G20 g20 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g20"; bash $W/tools/gd20_memguard.sh 26 | tail -1
LB_SKINP="$G7/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd20_browcap.sh c4 g20 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD20_BROW|DONE|ERROR"
bash $W/tools/gd20_caps.sh cg20c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL20_DONE
