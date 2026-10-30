#!/bin/bash
# V2.38 final 3: narrowed walk guard (install238_walk3) -> clean reopen -> verify -> cold -> 30 FPS evidence -> captures -> 60 / 120 / real
source Saved/Codex/SHME_V238_20261030/lib238.sh; O=$D/chain.out; MD=$D/checkpoint/manifests; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
A=/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations
echo "FIN4 start $(date +%T)" >> $O
# relaunch w4 30 - editor already up
MSYS_NO_PATHCONV=1 "$PY" Tools/SHME_V238_20261030/manifest238.py walk3 --assets $A/ABP_GR_MotionMatchingBase $A/ABP_GR_MotionMatching | tail -c 150 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/walk3.json bash $R $D/req/walk3.py walk3 1800 > $D/last_walk3.out 2>&1; grep -a -o "WALK238C .*" $D/last_walk3.out | cut -c1-600 >> $O
grep -a -q '"ok": true' $D/last_walk3.out && grep -a -q '"saved": true' $D/last_walk3.out || { echo "FIN4_FAILED walk3" >> $O; exit 1; }
relaunch fin4 30
SHME_KIND=measure bash $R $D/req/verify.py verify 1800 > $D/verify_fin4.out 2>&1; grep -a -o "VERIFY238 .*" $D/verify_fin4.out | cut -c1-1200 >> $O
grep -a -q '"ALL_OK": true' $D/verify_fin4.out || { echo "FIN4_FAILED verify" >> $O; exit 1; }
ab cold4 "j38_c90r:o j38_c90l:o"
WARM=1 ab fin4 "j38_c90rb:o j38_c90rb:pre238 j38_c90lb:o j38_c90lb:pre238  j38_c90r:o j38_c90r:pre238 j38_c90l:o j38_c90l:pre238 j38_c45r:o j38_c45r:pre238 j38_c135r:o j38_c135r:pre238 j38_cc90:o j38_cc90:pre238 w38_c90r:o w38_c90r:pre238 s38_c90r:o s38_c90r:pre238 s38_c90l:o s38_c90l:pre238 jdiag:o jdiag:pre238 jswap:o jswap:pre238 jlean:o jlean:pre238 ad_jog:o ad_jog:pre238 chain_jogcut:o chain_jogcut:pre238 mt_jog:o mt_jog:pre238 mtf_jog:o mtf_jog:pre238 cam32_j90:o cam32_j90:pre238 j36_stop:o j36_stop:pre238 j36_stopr:o j36_stopr:pre238 j36_rsm:o j36_rsm:pre238 j36_wjs:o j36_wjs:pre238 j36_sside:o j36_sside:pre238 j35_rev:o j35_rev:pre238 j30_rel_3450:o j30_rel_3450:pre238 j34_chain1:o j34_chain1:pre238 jstart:o jstart:pre238 e29_chain:o e29_chain:pre238 c29_combo:o c29_combo:pre238 wdiag:o wdiag:pre238 wstart:o wstart:pre238"
ab cap "j38_c90rb:oS j38_c90lb:oS j38_c90r:oS j38_c90r:pre238S j38_c90l:oS j38_c90l:pre238S j38_c90r:oG j38_c90r:pre238G j38_cc90:oS j38_c90r:oD" $D/vars238_capfin.sh
echo "FIN4_EVID_DONE $(date +%T)" >> $O
for m in 60 120 real; do relaunch i$m $m; WARM=1 ab i$m "j38_c90r:o j38_c90r:pre238 j38_c90l:o j38_c90l:pre238 j35_rev:o j35_rev:pre238 j30_rel_3450:o j30_rel_3450:pre238 e29_chain:o e29_chain:pre238 w38_c90r:o w38_c90r:pre238 jlean:o jlean:pre238"; echo "I_DONE $m $(date +%T)" >> $O; done
relaunch end4 30
echo "FIN4_DONE $(date +%T)" >> $O
