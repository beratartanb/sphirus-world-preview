#!/bin/bash
# gd17_final17.sh : GD17 final transfer + validation chain (ALL writes in GD17 folders / new names; GD15/GD16 assets read-only sources)
# 0 MHC_GD16_G16 duplicated to MHC_GD17_G16base  1 fit + 2 residual-feedback fits of data/head_G17S.npy -> MHC_GD17_G17  2 auto-rig -> SKM_GD17_Face_g17 + DNA
# 3 look: custom brow c4 bound to the rigged face, skin s1t6n (f6 texture + calmer nose normal layer), iris h6, lashes S_Thin, hair h75c
# 4 captures front + studio; GD16 G16 recaptured with its own GD16 look (before) for the same-session comparison
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD17_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010; G6=/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010
export LB_EYE=h6
bash $W/tools/gd17_memguard.sh 22 | tail -1
D=$G/MHC; Wn="$(cygpath -w "$(pwd)/$W/mhc")"
if [ ! -e Content/Sphirus/CharacterLab/GD17_IdentityMaster_20261010/MHC/MHC_GD17_G16base.uasset ]; then
 { echo "import builtins; builtins.GD17 = {'op': 'dup', 'src': '$G6/MHC/MHC_GD16_G16', 'dst': '$D/MHC_GD17_G16base', 'out': r'$Wn', 'tag': 'G16base'}"; cat $W/tools/ue_gd17_mhc.py; } > $W/mhc/job_dup_G16base.py
 MSYS_NO_PATHCONV=1 bash Tools/OutfitHome_20260929/run_of.sh $W/mhc/job_dup_G16base.py gd17-dup-g16base 600 | grep -oE "GD1[47]_MHC.{0,120}|Traceback.*"; fi
echo "== FIT G17"; bash $W/tools/gd17_fitfb.sh MHC_GD17_G16base MHC_GD17_G17 $W/data/head_G17S.npy G17
[ -f $W/data/head_G17_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd17_memguard.sh 22 | tail -1
echo "== RIG g17"; bash $W/tools/gd17_ue_cycle.sh MHC_GD17_G17 g17 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g17"; bash $W/tools/gd17_memguard.sh 26 | tail -1
LB_SKINP="$G/Looks/MI_GD17_Face_{lod}_s1t6n" bash $W/tools/gd17_browcap.sh c4 g17 refnh,ref,commonnh,common,close,closeclay,clay,expr,lod 0.0095 0.5 | grep -E "GD17_BROW|DONE|ERROR"
bash $W/tools/gd17_caps.sh cg17c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
echo "== GD16 G16 own look (before)"; LB_SKIN=s1t5 NOBIND=1 CUSTOMBROW=$G6/Grooms/GR_GD16_BrowCustom_c4 CUSTOMBROW_BIND=$G6/Face/Bindings/GB_GD16_EyebrowsCustom_c4_g16 bash $W/tools/gd17_lookB.sh $G6/Face/SKM_GD16_Face_g16 g16x 2>&1 | grep -E "COMP" | cut -c1-160
LIGHT=front bash $W/tools/gd17_caps.sh g16B ref,commonnh,common,clay | grep -E "DONE|ERROR"; bash $W/tools/gd17_caps.sh g16BS refnh,ref,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL17_DONE
