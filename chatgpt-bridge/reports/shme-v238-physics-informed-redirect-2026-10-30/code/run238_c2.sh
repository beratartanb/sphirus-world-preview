#!/bin/bash
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
echo "C2 start $(date +%T)" >> $O
A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V238_20261030/manifest238.py fam1 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/fam1.json bash $R $D/req/fam1.py fam1 1800 > $D/last_fam1.out 2>&1; grep -a -o "FAM238 .*" $D/last_fam1.out | cut -c1-900 >> $O
grep -a -q '"ok": true' $D/last_fam1.out && grep -a -q '"saved": true' $D/last_fam1.out || { echo "C2_FAILED fam" >> $O; exit 1; }
WARM=1 ab c2 "j38_c90r:cut1 j38_c90l:cut1 j38_c90r:cut1:2 j38_c90l:cut1:2 j38_c90r:o j38_c90l:o"
ab c2 "j38_c90r:cut1S j38_c90l:cut1S j38_c90r:cut1G j38_c90r:oG" $D/vars238_cap.sh
echo "C2_DONE $(date +%T)" >> $O
