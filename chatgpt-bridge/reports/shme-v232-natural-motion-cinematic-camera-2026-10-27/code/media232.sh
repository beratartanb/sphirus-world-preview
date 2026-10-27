#!/bin/bash
# media232.sh : V2.32 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.32 production; pre232 = the same production with every promoted V2.32 knob at its V2.31 value (before); ocam = V2.31 body + new camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V232_20261027/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v232cap_cam32_chain_pre232G_r1 camera_chain_before_game 1 "yuru > depar > sert sag > fren > yeni yonde itis | ONCE (V2.31 kamera) | oyun kamerasi"
mk v232cap_cam32_chain_oG_r1 camera_chain_v232_game 1 "ayni girdi | V2.32: fiziksel tepkili sinematik yay | oyun kamerasi"
mk v232cap_cam32_chain_ocamG_r1 camera_chain_newcam_v231body_game 1 "ayni girdi | V2.31 beden + V2.32 kamera (matris C) | oyun kamerasi"
mk v232cap_cam32_s90_pre232G_r1 sprint_hard_right_before_game 1 "depar > sert sag (D) | ONCE | oyun kamerasi"
mk v232cap_cam32_s90_oG_r1 sprint_hard_right_v232_game 1 "ayni girdi | V2.32 kamera yayi | oyun kamerasi"
mk v232cap_cam32_brk2_oG_r1 brake_second_request_v232_game 1 "depar > S > fren ortasinda D | V2.32 | oyun kamerasi"
mk v232cap_cam32_wallturn_oG_r1 wall_turn_v232_game 1 "duvar yaninda depar > sola sert donus | V2.32 (yay bosluga gore kisilir) | oyun kamerasi"
mk v232cap_cam_corr_oG_r1 corridor_v232_game 1 "dar koridor + 360 bakis | V2.32 (yay yok) | oyun kamerasi"
mk v232cap_cam32_look_oG_r1 mouse_look_walk_v232_game 1 "yururken fareyle bakis | V2.32 (oyuncu bakisi once) | oyun kamerasi"
mk v232cap_cam32_analog_oG_r1 analog_jog_v232_game 1 "analog capraz tempolu | V2.32 | oyun kamerasi"
mk v232cap_cam32_w45_oG_r1 walk45_v232_game 1 "yuruyus 45 derece yon degisimi | V2.32 (sakin) | oyun kamerasi"
mk v232cap_map_r1_oG_r1 house_route_v232_game 1 "gercek ev-orman rotasi | V2.32 | oyun kamerasi"
mk v232cap_e29_load_pre232S_r1 loaded_reversals_before_side 1 "efor zinciri: iki ters donus | ONCE | yan"
mk v232cap_e29_load_oS_r1 loaded_reversals_v232_side 1 "ayni girdi | V2.32: iki yonde yakalama adimi + cikis dongusu | yan"
mk v232cap_c30_calm_pre232S_r1 calm_walk_stop_before_side 1 "sakin yuruyus > capraz > dur > yuru | ONCE | yan"
mk v232cap_c30_calm_oS_r1 calm_walk_stop_v232_side 1 "ayni girdi | V2.32: salinim zemin korumasi | yan"
mk v232cap_wdiag_pre232S_r1 walk_diagonals_before_side 1 "capraz yuruyusler ve duruslar | ONCE | yan"
mk v232cap_wdiag_oS_r1 walk_diagonals_v232_side 1 "ayni girdi | V2.32 | yan"
mk v232cap_cam32_chain_oS_r1 camera_chain_body_v232_side 1 "kamera zincirinin bedeni | V2.32 | sabit yan kamera"
mk v232cap_jback_oS_r1 backward_start_v232_side 1 "durustan geri kalkis | V2.32 (acik: idle durus farki) | yan"
mk v232cap_cam32_s90_oS_r1 sprint_hard_right_body_v232_side 1 "depar sert sag: beden | V2.32 | yan"
mk v232cap_cam32_chain_oD_r1 camera_chain_body_v232_diagonal 1 "yuru > depar > sert sag > fren > govde tepkisi > yeni yonde itis | V2.32 | sabit capraz kamera"
mk v232cap_cam32_brk2_oD_r1 brake_second_request_body_v232_diagonal 1 "fren ortasinda ikinci istek: govde | V2.32 | sabit capraz kamera"
ls $PUB | wc -l
