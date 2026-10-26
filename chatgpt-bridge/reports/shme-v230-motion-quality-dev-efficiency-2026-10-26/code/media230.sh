#!/bin/bash
# media230.sh : V2.30 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.30 production; nolr = production with the low-speed reversal route off (V2.29 routing on the V2.30 content). Before media for the
# re-authored content (sprint / walk rear / jog lateral clips changed in place) = the V2.29 published media (same scenarios, linked in REPORT).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V230_20261026/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v230cap_c30_calm_oS_r1 calm_idle_walk_stop_restart_v230_side 1 "idle > ilk adim > yuruyus > capraz > dur > yeniden basla | V2.30 uretim | yan"
mk v230cap_c30_calm_oG_r1 calm_idle_walk_stop_restart_v230_game 1 "ayni sakin akis | V2.30 uretim | oyun kamerasi (tam kare)"
mk v230cap_s29_swl14_nolrS_r1 sprint_brake_repush_routeoff_side 1 "depar W > S 1.4 s > W (dusuk hizli geri kosu) | ONCE: dusuk hiz rotasi kapali (V2.29 yolu) | yan"
mk v230cap_s29_swl14_oS_r1 sprint_brake_repush_v230_side 1 "ayni girdi | V2.30 uretim (dusuk hiz geri donus sinifi) | yan"
mk v230cap_s29_swl14_oG_r1 sprint_brake_repush_v230_game 1 "ayni girdi | V2.30 uretim | oyun kamerasi"
mk v230cap_e29_chain_oS_r1 effort_chain_v230_side 1 "depar > sert sol > sag > geri > ileri (birikmis efor) | V2.30 uretim | yan"
mk v230cap_e29_chain_oG_r1 effort_chain_v230_game 1 "ayni zincir | V2.30 uretim | oyun kamerasi"
mk v230cap_s29_cam_oS_r1 sprint_cam180_v230_side 1 "depar + kamera 180, W basili | V2.30 uretim | yan"
mk v230cap_s29_cam_oG_r1 sprint_cam180_v230_game 1 "depar + kamera 180 | V2.30 uretim | oyun kamerasi"
mk v230cap_j24_rel_oS_r1 jogrev_release_v230_side 1 "tempolu geri donus icinde birak-bas (iptal) | V2.30 uretim | yan"
mk v230cap_j30_slow_nolrS_r1 slow_backjog_forward_routeoff_side 1 "yavaslayan geri kosu > ileri > devam | ONCE: dusuk hiz rotasi kapali | yan"
mk v230cap_j30_slow_oS_r1 slow_backjog_forward_v230_side 1 "ayni girdi | V2.30 uretim | yan"
mk v230cap_j30_slow_oG_r1 slow_backjog_forward_v230_game 1 "ayni girdi | V2.30 uretim | oyun kamerasi"
mk v230cap_d_sprint_oS_r1 sprint_straight_sway_v230_side 1 "duz depar: bas / omuz / kol salinimi (yeniden yazilmis klip) | V2.30 uretim | yan"
mk v230cap_d_sprint_oD_r1 sprint_straight_sway_v230_diag 1 "duz depar | V2.30 uretim | on-sag capraz"
mk v230cap_legs_slope_sprint_oS_r1 slope_sprint_turn_v230_side 1 "rampada depar > dur > kamera 180 > geri kalkis | V2.30 uretim | yan"
ls $PUB | wc -l
