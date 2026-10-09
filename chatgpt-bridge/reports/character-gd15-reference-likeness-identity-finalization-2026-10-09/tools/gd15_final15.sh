#!/bin/bash
# gd15_final15.sh <final sculpt npy> <TAG e.g. G15> [src MHC = MHC_GD15_C8L] : GD15 final transfer + validation chain. ALL writes in GD15 folders / new names.
# 1 MetaHuman transfer: fit + 2 residual-feedback fits (gd15_fitfb.sh) -> MHC_GD15_<TAG>
# 2 auto-rig a duplicate (Epic service) -> DNA + face SKM_GD15_Face_<tag> + persistent DNA link (gd15_ue_cycle.sh; composes look A at its end)
# 3 final reference look B on the RIGGED face (h75c hair, FlatThick brows auburn-dark [optional brow source-proxy BROWSRC_D], S_Thin lashes,
#   iris h6, skin s1t5 = f5 texture) -> captures with the identity light ('front') and studio light: ref / refnh / common / commonnh /
#   close / clay / expr (23 rig cases) + LOD 0..3 front captures
# env: BROWSRC_D / BROWSRC_TAG (brow groom proxy shift), LB_EYE (h6), LB_SKIN (s1t5)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD15_Identity_20261009; G=/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009
T=$1; U=$2; t=$(echo $U | tr A-Z a-z); SRC=${3:-MHC_GD15_C8L}
export LB_EYE=${LB_EYE:-h6} LB_SKIN=${LB_SKIN:-s1t5}
echo "== FIT $U from $SRC"; bash $W/tools/gd15_fitfb.sh $SRC MHC_GD15_$U $T $U
[ -f $W/data/head_${U}_mhc.npy ] || { echo FIT_GATE_STOP; exit 3; }
bash $W/tools/gd15_memguard.sh 22 | tail -1
echo "== RIG $t"; bash $W/tools/gd15_ue_cycle.sh MHC_GD15_$U $t || { echo RIG_STOP; exit 4; }
echo "== LOOK B on rigged face"; bash $W/tools/gd15_memguard.sh 26 | tail -1
bash $W/tools/gd15_lookB.sh $G/Face/SKM_GD15_Face_$t ${t}lb | grep -E "ok|COMP|READY|Trace" | cut -c1-160
echo "== CAPTURES"; LIGHT=front bash $W/tools/gd15_caps.sh ${t}F refnh,ref,commonnh,common,close,clay,expr | grep -E "DONE|ERROR"
bash $W/tools/gd15_caps.sh ${t}S refnh,ref,commonnh,clay | grep -E "DONE|ERROR"
echo FINAL15_DONE $U
