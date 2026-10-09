#!/bin/bash
# gd16_final16.sh : GD16 final transfer + validation chain (ALL writes in GD16 folders / new names; GD15 assets are read-only sources)
# 1 MetaHuman transfer of the GD16 sculpt (data/head_G16S.npy): fit + 2 residual-feedback fits from the GD15 G15 MHC state -> MHC_GD16_G16
# 2 auto-rig a duplicate (Epic service) -> DNA + face SKM_GD16_Face_g16 + persistent DNA link
# 3 GD16 look: custom reference-curve brow c4 (GR_GD16_BrowCustom_c4) bound to the rigged face, iris h6, skin s1t5, S_Thin lashes, h75c hair
# 4 captures: front light ref/refnh/common/commonnh/close/clay/expr/lod + studio ref/refnh/commonnh/clay; GD15 G15 recaptured with the SAME look
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD16_Identity_20261010; G=/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010
export LB_EYE=h6 LB_SKIN=s1t5
echo "== FIT G16"; bash $W/tools/gd16_fitfb.sh MHC_GD16_G15base MHC_GD16_G16 $W/data/head_G16S.npy G16
[ -f $W/data/head_G16_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd16_memguard.sh 22 | tail -1
echo "== RIG g16"; bash $W/tools/gd16_ue_cycle.sh MHC_GD16_G16 g16 || { echo RIG_STOP; exit 4; }
echo "== LOOK + CAPTURES g16"; bash $W/tools/gd16_memguard.sh 26 | tail -1
bash $W/tools/gd16_browcap.sh c4 g16 refnh,ref,commonnh,common,close,clay,expr,lod 0.0095 0.5 | grep -E "GD16_BROW|DONE|ERROR"
bash $W/tools/gd16_caps.sh cg16c4S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
echo "== GD15 G15 same look (comparison)"; BROWSRC_D=-0.07 BROWSRC_TAG=u07 bash $W/tools/gd16_lookB.sh /Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Face/SKM_GD15_Face_g15 g15r 2>&1 | grep -E "COMP|READY" | cut -c1-160
LIGHT=front bash $W/tools/gd16_caps.sh g15B refnh,ref,commonnh,common,close,clay | grep -E "DONE|ERROR"; bash $W/tools/gd16_caps.sh g15BS refnh,ref,clay | grep -E "DONE|ERROR"
df -h /c | tail -1; echo FINAL16_DONE
