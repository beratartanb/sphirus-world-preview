#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V243_20261101; source $D/lib243.sh
WARM=1 ab prod3 "j41_rl_p10:o:2 j42_lr_p10:o:2 j41_rl_p10:o:3"
echo PROD3_DONE >> $O
