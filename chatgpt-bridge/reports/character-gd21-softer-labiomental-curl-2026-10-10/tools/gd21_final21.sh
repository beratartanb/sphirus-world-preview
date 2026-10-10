#!/bin/bash
# gd21_final21.sh : GD21 final transfer + validation chain (ALL writes in GD21 folders / new names; GD15..GD20 assets read-only)
# 0 MHC_GD20_G20 duplicated to MHC_GD21_G20base   1 fit + 2 residual-feedback fits of data/head_G21S.npy -> MHC_GD21_G21   2 auto-rig -> SKM_GD21_Face_g21 + DNA
# 3 look: custom brow c4, skin s1t6n (GD17 look, read-only), iris h6, lashes S_Thin, hair h75c   4 captures: front light sets + studio set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD21_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD21_IdentityMaster_20261010; G0=/Game/Sphirus/CharacterLab/GD20_IdentityMaster_20261010; G7=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd21_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD21_IdentityMaster_20261010/MHC/MHC_GD21_G20base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G0/MHC/MHC_GD20_G20', 'dst': '$D/MHC_GD21_G20base', 'out': r'$Wn', 'tag': 'G20base'}"; cat $W/tools/ue_gd21_mhc.py; } > $W/mhc/job_dup_G20base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G20base.py gd21-dup-g20base 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G21"; bash $W/tools/gd21_fitfb.sh MHC_GD21_G20base MHC_GD21_G21 $W/data/head_G21S.npy G21
[ -f $W/data/head_G21_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd21_memguard.sh 22 | tail -1
echo "== RIG g21"; bash $W/tools/gd21_ue_cycle.sh MHC_GD21_G21 g21 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g21"; bash $W/tools/gd21_memguard.sh 26 | tail -1
LB_SKINP="$G7/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd21_browcap.sh c4 g21 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD21_BROW|DONE|ERROR"
bash $W/tools/gd21_caps.sh cg21c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL21_DONE
