#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "C7 start $(date +%T)" >> $O
A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V238_20261030/manifest238.py walk1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/walk1.json bash $R $D/req/walk1.py walk1 1800 > $D/last_walk1.out 2>&1; grep -a -o "WALK238 .*" $D/last_walk1.out | cut -c1-500 >> $O
grep -a -q '"ok": true' $D/last_walk1.out && grep -a -q '"saved": true' $D/last_walk1.out || { echo "C7_FAILED walk" >> $O; exit 1; }
WARM=1 ab c7 "w38_c90r:cut3 w38_c90r:o j38_c90r:cut3 j38_c90l:cut3 wdiag:o wdiag:cut3 wstart:o wstart:cut3"
echo "C7_DONE $(date +%T)" >> $O
