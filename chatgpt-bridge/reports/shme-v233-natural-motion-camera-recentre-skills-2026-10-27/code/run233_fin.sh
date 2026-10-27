#!/bin/bash
# run233_fin.sh : V2.33 promotion (after S_DONE and the manual PROMOTE_GO marker with the group list): fresh editor -> promote233 (manifest)
# -> clean reopen -> verify233 -> final production evidence + A/B/C/D matrix. Each step waits for the previous chains' markers.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V233_20261027; MD=$D/checkpoint/manifests
until grep -aq "^S_DONE\|^S_FAILED" $O && grep -aq "^PROMOTE_GO" $O; do sleep 30; done
PG=$(grep -a "^PROMOTE_GO" $O | tail -1 | cut -d' ' -f2)   # (not GROUPS: a read-only bash builtin)
echo "FIN start $(date +%T) groups $PG (reason: promotion in a fresh fixed-30 editor)" >> $O
relaunch fin 30
MSYS_NO_PATHCONV=1 "$PY" $T/manifest233.py promo233 --assets /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase /Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching /Game/GraceRanger/SHME/DA_SHM_Response_Default >> $O 2>&1
"$PY" -c "import json,sys; g=sys.argv[1].split(','); open('$D/req/promo_save.py','w').write('import builtins\nbuiltins.V233_PROMO = %s\nbuiltins.V233_SAVE = True\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V233_20261027/promote233.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g})); open('$D/req/verify_fin.py','w').write('import builtins\nbuiltins.V233_EXP = %s\nexec(open(r\"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V233_20261027/verify233.py\", encoding=\"utf8\").read())\n' % repr({x: True for x in g}))" "$PG"
SHME_KIND=write SHME_MANIFEST=$MD/promo233.json bash $R $D/req/promo_save.py promo 900 > $D/promo_fin.out 2>&1; grep -a -o 'PROMO233 {.*' $D/promo_fin.out | cut -c1-900 >> $O
grep -aq '"saved": true' $D/promo_fin.out || { echo "FIN_FAILED promotion not saved" >> $O; exit 1; }
echo "FINV start $(date +%T) (reason: clean reopen = verification on disk state)" >> $O
relaunch finv 30
SHME_KIND=measure bash $R $D/req/verify_fin.py verify 900 > $D/verify_fin.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin.out | tail -1 >> $O
grep -a -o 'VERIFY233 {.*' $D/verify_fin.out | grep -q '"ALL_OK": true' || { echo "FIN_FAILED verify" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J="j30_slow:o:0"; for s in j30_slow jback d_back k_jogback jstart j30_rel_3200 j30_rel_3450 wstart c30_calm wdiag e29_load e29_chain s29_swl12 c29_combo d_sprint cam33_wturn cam33_jturnj cam33_sturn cam33_look cam33_back cam33_idlelook cam32_wallturn cam_corr ins_ws map_r1 ter_drop_walk legs_slope_sprint; do J="$J $s:o"; done
for s in cam33_jturnj cam33_sturn cam33_look; do J="$J $s:pad233"; done
for s in j30_slow cam33_jturnj cam33_sturn; do J="$J $s:pre233 $s:body233 $s:cam233"; done
ab fin "$J" $D/vars233.sh
echo "FIN_EVID_DONE $(date +%T)" >> $O
