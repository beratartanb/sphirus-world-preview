#!/bin/bash
# media226.sh : V2.26 published media from the final fixed-step captures (30 FPS game time = real speed; unedited FULL frames, the docked
# viewport narrowed to a multiple of 64 - no crop). All captures are PRODUCTION mode after the V2.26 promotion (no candidate overrides).
# GIF real speed; AVI realtime (mode 2 also 1/3 speed). Cameras: S side, D front-right diagonal, G gameplay camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V226_20261024/pub/vid; mkdir -p $PUB
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi $O/${name}_slow3x.avi; do [ -f $f ] && cp $f $PUB/; done; echo "OK $name"; }
mk v226capfin_j24_sw_ph2_oS_r1 jogrev_SW_prod_side 2 "tempolu S > W | URETIM V2.26 | yan"
mk v226capfin_j24_sw_ph2_oG_r1 jogrev_SW_prod_game 1 "tempolu S > W | URETIM V2.26 | oyun kamerasi (tam kare)"
mk v226capfin_j24_ph3_oS_r1 jogrev_WS_ph3_prod_side 2 "tempolu W > S > W (gec istek evresi) | URETIM V2.26 | yan"
mk v226capfin_j24_ph0_oD_r1 jogrev_WS_ph0_prod_diag 1 "tempolu W > S > W | URETIM V2.26 | capraz"
mk v226capfin_ins_ws_oG_r1 inspect_masks_game 1 "atolye: yuru - maskeye bak - incele - bakisi kaydir | URETIM V2.26 (gercek R05 maskeleri) | oyun kamerasi (tam kare)"
mk v226capfin_ins_ws_oD_r1 inspect_masks_diag 1 "atolye inceleme: bas / boyun / govde bakisi | capraz"
mk v226capfin_ins_ws2_oG_r1 inspect_two_masks_game 1 "iki yakin maske arasinda bakis gecisi | URETIM V2.26 | oyun kamerasi (tam kare)"
mk v226capfin_ter_drop_walk_oS_r1 terrain_step28_walk_side 2 "yuruyus 28 cm basamak cikis + inis | URETIM V2.26 | yan"
mk v226capfin_ter_drop_walk_oG_r1 terrain_step28_walk_game 1 "yuruyus 28 cm basamak | URETIM V2.26 | oyun kamerasi (tam kare)"
mk v226capfin_map_r2_oG_r1 route_house_forest_game 1 "gercek ev - orman rotasi (map_r2, 24 m) | URETIM V2.26 | oyun kamerasi (tam kare)"
ls $PUB | wc -l
