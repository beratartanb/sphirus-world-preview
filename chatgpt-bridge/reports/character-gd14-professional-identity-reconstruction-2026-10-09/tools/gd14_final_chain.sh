#!/bin/bash
# GD14 final chain: W8 (final lip pass) + GD12 / GD13 comparison transfers (test copies in the GD14 folder only)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD14_Identity_20261009
bash $W/tools/gd14_fitfb.sh MHC_GD14_W7 MHC_GD14_W8 $W/data/head_W8S.npy W8
bash $W/tools/gd14_memguard.sh 22; bash $W/tools/gd14_ue_cycle.sh MHC_GD14_W8 w8
LIGHT=front bash $W/tools/gd14_caps.sh w8F refnh,ref,commonnh,common,close,clay,expr; bash $W/tools/gd14_caps.sh w8S refnh,ref,clay; bash $W/tools/gd14_track.sh w8F refnh
for C in GD12 GD13; do t=$(echo $C | tr A-Z a-z); bash $W/tools/gd14_fitfb.sh MHC_GD14_W0 MHC_GD14_CMP_$C $W/data/head_$C.npy CMP$C
  bash $W/tools/gd14_memguard.sh 22; bash $W/tools/gd14_ue_cycle.sh MHC_GD14_CMP_$C c$t; LIGHT=front bash $W/tools/gd14_caps.sh c${t}F refnh,ref,commonnh; bash $W/tools/gd14_caps.sh c${t}S refnh; done
echo FINAL_CHAIN_DONE
