#!/bin/bash
# media228.sh : V2.28 published media from the final fixed-step captures (production after the switch; 30 FPS game time = real speed, full frames, unedited).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V228_20261025/pub/vid; mkdir -p $PUB
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; echo "OK $name"; }
mk v228capfin_j24_sw_ph2_oS_r1 jogrev_SW_v228_side 1 "tempolu S > W | URETIM V2.28 (klip-bagli kapsul + tutma) | yan"
mk v228capfin_j24_sw_ph2_oG_r1 jogrev_SW_v228_game 1 "tempolu S > W | URETIM V2.28 | oyun kamerasi (tam kare)"
mk v228capfin_j24_ph0_oS_r1 jogrev_WS_ph0_v228_side 1 "tempolu W > S > W | URETIM V2.28 | yan"
mk v228capfin_j24_ph3_oS_r1 jogrev_WS_ph3_v228_side 1 "tempolu W > S > W (gec istek evresi) | URETIM V2.28 | yan"
mk v228capfin_j24_dbl_oS_r1 jogrev_double_v228_side 1 "cift geri donus: ikinci istekte karsi aile klibine rota | URETIM V2.28 | yan"
mk v228capfin_j24_rel_oS_r1 jogrev_release_v228_side 1 "geri donus icinde birakma: fren sonuna tutma | URETIM V2.28 | yan"
mk v228capter_ter_drop_jog_oS_r1 terrain_step28_jog_v228_side 1 "28 cm basamak, tempolu: ilk ayak basamagin ustune | URETIM V2.28 | yan"
mk v228capter_ter_drop_walk_oS_r1 terrain_step28_walk_v228_side 1 "28 cm basamak, yuruyus | URETIM V2.28 | yan"
mk v228capins_ins_ws2_oG_r1 inspect_two_masks_v228_game 1 "iki yakin maske: kimlik tabanli hedef | URETIM V2.28 | oyun kamerasi"
mk v228capins_ins_ws2_oS_r1 inspect_two_masks_v228_side 1 "iki yakin maske | URETIM V2.28 | yan"
ls $PUB | wc -l
