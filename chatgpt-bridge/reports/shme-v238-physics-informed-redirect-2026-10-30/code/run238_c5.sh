#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "C5 start $(date +%T)" >> $O
A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V238_20261030/manifest238.py gaze1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/gaze1.json bash $R $D/req/gaze1.py gaze1 1800 > $D/last_gaze1.out 2>&1; grep -a -o "GAZE238 .*" $D/last_gaze1.out | cut -c1-900 >> $O
grep -a -q '"ok": true' $D/last_gaze1.out && grep -a -q '"saved": true' $D/last_gaze1.out || { echo "C5_FAILED gaze" >> $O; exit 1; }
WARM=1 ab c5 "j38_c90r:cut2 j38_c90r:cut3 j38_c90l:cut3 j38_c90r:o mt_jog:o mt_jog:gz"
ab c5 "j38_c90r:cut3S j38_c90l:cut3S j38_c90r:cut3G" $D/vars238_cap.sh
echo "C5_DONE $(date +%T)" >> $O
