#!/bin/bash
# media234.sh : V2.34 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.34 production (keyboard harness -> mouse recentre profile), pad234 = gamepad profile, pre234 / pre234p = every V2.34 knob at its
# V2.33 value (mouse / gamepad). The stop-clip toe clearance is content and is in every capture.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V234_20261028/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v234cap_cam33_wturn_pre234pG_r1 walk_right_before_game 1 "yuru > saga don, sag analog yok | ONCE V2.33: yuruyuste otomatik takip kapali | oyun kamerasi gamepad"
mk v234cap_cam33_wturn_pad234G_r1 walk_right_v234_game 1 "ayni girdi | V2.34: govde saga yonelir, kamera govdeyi izler (hiz/yon degismez) | oyun kamerasi gamepad"
mk v234cap_cam33_sturn_pre234pG_r1 sprint_right_before_game 1 "depar > sert sag | ONCE V2.33: kamera donerken hiz 417->490 | oyun kamerasi gamepad"
mk v234cap_cam33_sturn_pad234G_r1 sprint_right_v234_game 1 "ayni girdi | V2.34: tepki fren/donus aninda, sonra arkadan takip, hiz sabit | oyun kamerasi gamepad"
mk v234cap_cam34_wflow_pad234G_r1 walk_flow_v234_gamepad_game 1 "analog: yuru > sag > ileri > sol > ileri > capraz > dur > devam, sag analog yok | V2.34"
mk v234cap_cam34_jlook_pad234G_r1 jog_look_during_follow_v234_game 1 "tempolu sag, otomatik takip SURERKEN manuel bakis | oyuncu kazanir, aci korunur, takip sonra devam"
mk v234cap_cam32_chain_pad234G_r1 camera_chain_v234_game 1 "yuru > depar > sert sag > fren > capraz > arkadan takip | V2.34 gamepad"
mk v234cap_s34_straight_pre234S_r1 sprint_attitude_before_side 1 "duz depar | ONCE: atletik govde/kol | sabit yan"
mk v234cap_s34_straight_oS_r1 sprint_attitude_v234_side 1 "ayni girdi | V2.34 uretim: daha dik govde, daha kucuk kol/omuz salinimi | sabit yan"
mk v234cap_j30_rel_3200_pre234S_r1 release_repress_before_side 1 "tempolu ileri > S > birak > tekrar S | ONCE: durus baslangicina zorlanir | sabit yan"
mk v234cap_j30_rel_3200_oS_r1 release_repress_v234_side 1 "ayni girdi | V2.34: ters donus devam eder | sabit yan"
mk v234cap_j30_slow_oS_r1 back_start_forward_stop_v234_side 1 "durus > geri kalkis > ileri > durus (kapanis adimi ayak kaldirir) | V2.34 | sabit yan"
mk v234cap_c29_combo_pre234S_r1 walk_lateral_chain_before_side 1 "yuru W, W+D, D, A, dur | ONCE | sabit yan"
mk v234cap_c29_combo_oS_r1 walk_lateral_chain_v234_side 1 "ayni girdi | V2.34: govde yeni yone adimlarla yerlesir | sabit yan"
