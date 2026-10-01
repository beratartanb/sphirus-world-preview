#!/bin/bash
# gd_final_caps.sh <prefix-stem> : full GUARDIAN evidence capture batch on the final composition (face gate sets + rig, garments, seam, LOD)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; S=$1; T=Tools/CharacterLookdev_20260930; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
MSYS_NO_PATHCONV=1 "$PY" $T/gd_final_comp.py h c14s
bash $T/gd_captures.sh ${S}f clay,real,hair,rig; bash $T/gd_frames.sh ${S}f "clay real hair"
for set in henley shorts waist neck sleeve full seam lod; do bash $T/cr_run_tests.sh ${S}_$set $set setup; done
echo FINAL_CAPS_DONE $S
