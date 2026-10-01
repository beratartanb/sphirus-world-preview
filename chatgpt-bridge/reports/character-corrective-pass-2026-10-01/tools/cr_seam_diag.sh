#!/bin/bash
# cr_seam_diag.sh <prefix> <body MI path> <head LOD0 MI path> : swap only the seam-relevant skin MIs in the QA composition, rebuild, capture the seam set
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; T=Tools/CharacterLookdev_20260930; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
MSYS_NO_PATHCONV=1 "$PY" -c "
import json, sys; p='Saved/Codex/CharacterLookdev_20260930/qa_config.json'; d=json.load(open(p)); d['material_overrides']['Body']['0']=sys.argv[1]; d['material_overrides']['Head']['0']=sys.argv[2]; json.dump(d, open(p,'w'), indent=1); print('SEAMCOMP', sys.argv[1].split('/')[-1], sys.argv[2].split('/')[-1])" "$2" "$3"
bash $T/cr_run_tests.sh $1 seam setup
