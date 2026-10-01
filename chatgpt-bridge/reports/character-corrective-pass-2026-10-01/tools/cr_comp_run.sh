#!/bin/bash
# cr_comp_run.sh <henley tag> <shorts tag> <cloth: none|both|shorts> <prefix> <set> : set the corrective QA composition, rebuild the QA scene, run one garment test set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Tools/CharacterLookdev_20260930; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
O=/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Outfit; CL=/Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Cloth
case $3 in m1both) CG="{\"Shorts\": \"$CL/CA_CR_Shorts_m1\", \"HenleyLower\": \"$CL/CA_CR_HenleyLower_m1f\"}";; m1shorts) CG="{\"Shorts\": \"$CL/CA_CR_Shorts_m1\"}";; both) CG="{\"Shorts\": \"$CL/CA_CR_Shorts_g16a\", \"HenleyLower\": \"$CL/CA_CR_HenleyLower_g16b\"}";; shorts) CG="{\"Shorts\": \"$CL/CA_CR_Shorts_g16a\"}";; *) CG="{}";; esac
MSYS_NO_PATHCONV=1 "$PY" $T/cr_set_comp.py ${FACE:-cr_i} cr:id17 $O/SKM_LK_Henley_$1 $O/SKM_LK_Shorts_$2 /Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Skin/MI_LK_Body_Baked_G ${SKIN:-c11} /Game/Sphirus/CharacterLab/CharacterCorrective_20261001/Skin "$CG"
bash $T/cr_run_tests.sh $4 $5 setup
