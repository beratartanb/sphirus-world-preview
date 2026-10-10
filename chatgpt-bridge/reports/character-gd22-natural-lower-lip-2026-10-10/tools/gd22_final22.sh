#!/bin/bash
# gd22_final22.sh : GD22 final transfer + validation chain (ALL writes in GD22 folders / new names; GD15..GD21 assets read-only)
# 0 MHC_GD21_G21 duplicated to MHC_GD22_G21base   1 fit + 2 residual-feedback fits of data/head_G22S.npy -> MHC_GD22_G22   2 auto-rig -> SKM_GD22_Face_g22 + DNA
# 3 look: custom brow c4, skin s1t6n (GD17 look, read-only), iris h6, lashes S_Thin, hair h75c   4 captures: front light sets + studio set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD22_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD22_IdentityMaster_20261010; G1=/Game/Sphirus/CharacterLab/GD21_IdentityMaster_20261010; G7=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd22_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD22_IdentityMaster_20261010/MHC/MHC_GD22_G21base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G1/MHC/MHC_GD21_G21', 'dst': '$D/MHC_GD22_G21base', 'out': r'$Wn', 'tag': 'G21base'}"; cat $W/tools/ue_gd22_mhc.py; } > $W/mhc/job_dup_G21base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G21base.py gd22-dup-g21base 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G22"; bash $W/tools/gd22_fitfb.sh MHC_GD22_G21base MHC_GD22_G22 $W/data/head_G22S.npy G22
[ -f $W/data/head_G22_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd22_memguard.sh 22 | tail -1
echo "== RIG g22"; bash $W/tools/gd22_ue_cycle.sh MHC_GD22_G22 g22 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g22"; bash $W/tools/gd22_memguard.sh 26 | tail -1
LB_SKINP="$G7/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd22_browcap.sh c4 g22 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD22_BROW|DONE|ERROR"
bash $W/tools/gd22_caps.sh cg22c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL22_DONE
