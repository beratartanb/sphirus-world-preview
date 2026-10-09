#!/bin/bash
# GD14 W9 = corrected-winding brush program C1 on W2 + lid-margin fold repair -> MHC (feedback fits) -> rig -> captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009
bash $W/tools/gd14_memguard.sh 22; bash $W/tools/gd14_fitfb.sh MHC_GD14_W2 MHC_GD14_W9 $W/data/head_W9S.npy W9
bash $W/tools/gd14_memguard.sh 22; bash $W/tools/gd14_ue_cycle.sh MHC_GD14_W9 w9
LIGHT=front bash $W/tools/gd14_caps.sh w9F refnh,ref,commonnh,common,close,clay,expr; bash $W/tools/gd14_caps.sh w9S refnh,ref; bash $W/tools/gd14_track.sh w9F refnh
echo W9_CHAIN_DONE
