#!/bin/bash
# gd19_final19.sh : GD19 final transfer + validation chain (ALL writes in GD19 folders / new names; GD15..GD18 assets are read-only sources)
# 0 MHC_GD18_G18E duplicated to MHC_GD19_G18base   1 fit + 2 residual-feedback fits of data/head_G19S.npy -> MHC_GD19_G19   2 auto-rig -> SKM_GD19_Face_g19 + DNA
# 3 look: custom brow c4, skin s1t6n (GD17 look, read-only), iris h6, lashes S_Thin, hair h75c   4 captures: front light sets + studio set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD19_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD19_IdentityMaster_20261010; G8=/Game/Sphirus/CharacterLab/GD18_IdentityMaster_20261010; G7=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd19_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD19_IdentityMaster_20261010/MHC/MHC_GD19_G18base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G8/MHC/MHC_GD18_G18E', 'dst': '$D/MHC_GD19_G18base', 'out': r'$Wn', 'tag': 'G18base'}"; cat $W/tools/ue_gd19_mhc.py; } > $W/mhc/job_dup_G18base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G18base.py gd19-dup-g18base 600 | grep -oE "GD1[4-9]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G19"; bash $W/tools/gd19_fitfb.sh MHC_GD19_G18base MHC_GD19_G19 $W/data/head_G19S.npy G19
[ -f $W/data/head_G19_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd19_memguard.sh 22 | tail -1
echo "== RIG g19"; bash $W/tools/gd19_ue_cycle.sh MHC_GD19_G19 g19 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g19"; bash $W/tools/gd19_memguard.sh 26 | tail -1
LB_SKINP="$G7/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd19_browcap.sh c4 g19 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD19_BROW|DONE|ERROR"
bash $W/tools/gd19_caps.sh cg19c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL19_DONE
