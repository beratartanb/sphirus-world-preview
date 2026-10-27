#!/bin/bash
# media233.sh : V2.33 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.33 production; pre233 = every V2.33 knob at its V2.32 value (before); pad233 = gamepad recentre profile; sc = calm-sprint CANDIDATE.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V233_20261027/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v233cap_cam33_sturn_pre233G_r1 sprint_hard_right_before_game 1 "depar > sert sag | ONCE (V2.32: yorunge var, arkaya donus yok) | oyun kamerasi"
mk v233cap_cam33_sturn_oG_r1 sprint_hard_right_v233_mouse_game 1 "ayni girdi | V2.33 uretim, fare/klavye profili (yavas arkaya donus) | oyun kamerasi"
mk v233cap_cam33_sturn_pad233G_r1 sprint_hard_right_v233_gamepad_game 1 "ayni girdi | V2.33 gamepad profili: tepki > yerlesme > arkadan takip | oyun kamerasi"
mk v233cap_cam33_jturnj_pad233G_r1 jog_left_v233_gamepad_game 1 "tempolu > sol (sag analog yok) | V2.33 gamepad: arkadan takibe donus | oyun kamerasi"
mk v233cap_cam33_look_pad233G_r1 walk_look_no_recentre_v233_game 1 "yuruyus + fare bakisi | uretimde yuruyuste otomatik donus kapali: bakis aynen kalir | oyun kamerasi"
mk v233cap_cam33_back_pad233G_r1 backward_no_halfturn_v233_game 1 "geri hareket | kamera etrafinda donmez | oyun kamerasi"
mk v233cap_cam32_chain_pad233G_r1 camera_chain_v233_gamepad_game 1 "yuru > depar > sert sag > fren > capraz > yeni yonde arkadan takip | gamepad | oyun kamerasi"
mk v233cap_j30_slow_pre233S_r1 stand_back_start_before_side 1 "gercek durus > geri kalkis | ONCE (AAMS baslangici, 38 cm) | sabit yan"
mk v233cap_j30_slow_oS_r1 stand_back_start_v233_side 1 "ayni girdi | V2.33 karaktere ozel geri kalkis | sabit yan"
mk v233cap_d_sprint_oS_r1 sprint_attitude_current_side 1 "depar | uretim tavri | sabit yan"
mk v233cap_d_sprint_scS_r1 sprint_attitude_calm_candidate_side 1 "ayni girdi | ADAY (uretimde degil): daha dik govde, sakin ust beden | sabit yan"
mk v233cap_cam33_sturn_pad233S_r1 sprint_hard_right_body_v233_side 1 "depar sert sag: beden | V2.33 | sabit yan"
