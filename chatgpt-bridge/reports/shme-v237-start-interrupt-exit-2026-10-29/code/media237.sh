#!/bin/bash
# media237.sh : V2.37 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.37 production, pre237 = every V2.37 group at its V2.36 value (V2.36 stop family, V2.36 start DB copies, CP2 start route).
# S side, D diagonal, G game camera. Same input timing in each before/after pair (same scenario, same recording window).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V237_20261029/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; [ -d Saved/Codex/SHME_V138_20260927/Video/${lab/v237cap_/v237cap2_} ] && lab=${lab/v237cap_/v237cap2_}; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v237cap_j36_stopr_pre237S_r1 stop_restart_v236_side 1 "tempolu > birak > durus > ileri > durus | ONCE V2.36: fren dizi bukuk (FootPlacement pelvisi 6-9 cm indirir), sol kalkis 0.8 hizda | sabit yan"
mk v237cap_j36_stopr_oS_r1 stop_restart_v237_side 1 "ayni girdi | V2.37: pelvis klipte (fren 89.8 cm, diz 144), adim planli duz kalkis 1.0 hizda | sabit yan"
mk v237cap_j36_stopr_oG_r1 stop_restart_v237_game 1 "ayni girdi | V2.37 | oyun kamerasi"
mk v237cap_j36_stopr_oD_r1 stop_restart_v237_diag 1 "ayni girdi | V2.37 | sabit capraz"
mk v237cap_j36_rsm_pre237S_r1 midstop_repress_v236_side 1 "tempolu > birak > duraksarken tekrar ileri | ONCE V2.36: duragan kalkis klibi hareket halinde (CP2 kalkisi) | sabit yan"
mk v237cap_j36_rsm_oS_r1 midstop_repress_v237_side 1 "ayni girdi | V2.37: durusun o anki pozundan yeniden itis baglantisi | sabit yan"
mk v237cap_j36_rse_oS_r1 early_repress_v237_side 1 "durusun basinda tekrar ileri | V2.37 | sabit yan"
mk v237cap_j36_rsl_oS_r1 late_repress_v237_side 1 "durusun sonunda tekrar ileri | V2.37 | sabit yan"
mk v237cap_j36_rsx_oS_r1 midstop_opposite_v237_side 1 "durusun ortasinda ters istek | V2.37 (ters donus ailesi) | sabit yan"
mk v237cap_j36_wjs_pre237S_r1 walk_jog_stop_v236_side 1 "yuru > tempolu > durus > ileri | ONCE V2.36 | sabit yan"
mk v237cap_j36_wjs_oS_r1 walk_jog_stop_v237_side 1 "ayni girdi | V2.37 | sabit yan"
mk v237cap_j36_stopb_oS_r1 stop_other_foot_v237_side 1 "birakma yarim adim sonra (diger fren ayagi) | V2.37 | sabit yan"
mk v237cap_j35_rev_pre237S_r1 reversal_v236_side 1 "tempolu > sert S > geri > W > dur | ONCE V2.36 | sabit yan"
mk v237cap_j35_rev_oS_r1 reversal_v237_side 1 "ayni girdi | V2.37 | sabit yan"
mk v237cap_e29_load_oS_r1 effort_reversal_v237_side 1 "eforlu zincir | V2.37 | sabit yan"
mk v237cap_j34_chain1_oS_r1 chain1_restart_v237_side 1 "geri kalkis > ileri > durus > yeniden hareket | V2.37 | sabit yan"
mk v237cap_j36_sside_oG_r1 stop_side_start_v237_game 1 "durus > yan kalkis (A) > capraz kalkis (W+D) | V2.37 (vendor yan kalkis, degismedi) | oyun kamerasi"
mk v237cap_j36_sside_oS_r1 stop_side_start_v237_side 1 "ayni girdi | V2.37 | sabit yan"
