#!/bin/bash
# gd18_final18.sh : GD18 final transfer + validation chain (ALL writes in GD18 folders / new names; GD15/GD16/GD17 assets are read-only sources)
# 0 MHC_GD17_G17 duplicated to MHC_GD18_G17base (fit guard: the source MHC must be inside the pass folder)
# 1 fit + 2 residual-feedback fits of data/head_G18S.npy -> MHC_GD18_G18   2 auto-rig -> SKM_GD18_Face_g18 + DNA
# 3 look: custom brow c4 (GD16/17 reference brow, re-bound to the GD18 face), skin s1t6n (GD17 look, read-only), iris h6, lashes S_Thin, hair h75c
# 4 captures: front light (ref / refnh / common / close / closeclay / clay / expr / lod) + studio set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD18_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD18_IdentityMaster_20261010; G7=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd18_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD18_IdentityMaster_20261010/MHC/MHC_GD18_G17base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G7/MHC/MHC_GD17_G17', 'dst': '$D/MHC_GD18_G17base', 'out': r'$Wn', 'tag': 'G17base'}"; cat $W/tools/ue_gd18_mhc.py; } > $W/mhc/job_dup_G17base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G17base.py gd18-dup-g17base 600 | grep -oE "GD1[478]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G18"; bash $W/tools/gd18_fitfb.sh MHC_GD18_G17base MHC_GD18_G18 $W/data/head_G18S.npy G18
[ -f $W/data/head_G18_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd18_memguard.sh 22 | tail -1
echo "== RIG g18"; bash $W/tools/gd18_ue_cycle.sh MHC_GD18_G18 g18 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g18"; bash $W/tools/gd18_memguard.sh 26 | tail -1
LB_SKINP="$G7/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd18_browcap.sh c4 g18 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD18_BROW|DONE|ERROR"
bash $W/tools/gd18_caps.sh cg18c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL18_DONE
