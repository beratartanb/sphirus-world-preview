#!/bin/bash
# chainL_hc.sh <hair tag> <label> : import the L hair candidate, bind it to the UNCHANGED F4ab (L bindings f4ab<tag>), capture whole/cu/fx with provenance
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; t=${1:?hair tag}; LB=${2:?label}; T=Tools/CharacterLookdev_20260930; L=/Game/Sphirus/CharacterLab/GD11_HeadRefinementL_20261005
F4=/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab; BP=$L/Face/Bindings/GB_G11RL
SKIP_BUILD=1 bash $T/gd11rl_hair_cycle.sh $t x | grep -E "HAIR_DONE|LMD|Traceback"
FACE=$F4 HAIR=gl:$t BSUF=f4ab$t SKIN=gck10 GD3_EYES_TAG=e2 SETS=none CAPP=x bash $T/gd11rl_face_run.sh f4ab | grep -E "GD_LB|dirty|REFUSE|Traceback"
CAND_ID="$LB: F4ab + $t (L bindings f4ab$t, target F4ab) + k10" bash $T/gd11rl_caps.sh $LB $F4 $BP f4ab$t gl:$t whole,cu,fx | grep -E "COMP4|BINDINGS|G11RL_PROV|DONE|REFUSE|ERROR"
echo CHAINL_HC_END $t
