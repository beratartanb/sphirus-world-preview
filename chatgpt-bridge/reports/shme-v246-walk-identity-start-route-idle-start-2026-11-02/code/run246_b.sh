#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V246_20261101; M=Saved/Codex/SHME_V233_20261027/checkpoint/manifests; RUN=Tools/SHME_V2_20261014/run_v2.sh
PY="C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
for i in $(seq 1 360); do grep -q RC246_DONE $D/chain.out && break; sleep 20; done
source $D/lib246.sh
"$PY" Tools/SHME_V233_20261027/manifest233.py v246_abpbk --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching | tail -1 | cut -c1-160 >> $O
export SHME_MANIFEST=$M/v246_abpbk.json
WARM=1 ab in "taps:inrt jstart:inrt j40_rlw:inrt w43_idle:inrt w42_id:inrt taps:inrto jstart:inrto taps:idl4 jstart:idl4"
echo IN246_DONE >> $O
