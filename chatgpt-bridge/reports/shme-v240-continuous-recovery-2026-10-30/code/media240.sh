#!/bin/bash
# media240.sh : V2.40 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = saved production (V2.38 behaviour + inert V2.39/V2.40 knobs), tkh = V2.40 candidate (SHM239_Own 1 + SHM240_HeadOn 1). S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V240_20261030/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v240cap_j40_rlw_oS_r1 third_request_v238_side 1 "tempolu ileri > sert saga 90 > fren ortasinda SOL > destek kurulurken ILERI | uretim | sabit yan"
mk v240cap_j40_rlw_tkhS_r1 third_request_v240_side 1 "ayni girdi | V2.40 aday: devralma + ucuncu istekte plan teslimi | sabit yan"
mk v240cap_j40_rlw_tkhD_r1 third_request_v240_diag 1 "ayni girdi | V2.40 aday | sabit capraz (dortte uc)"
mk v240cap_j40_rlw_tkhG_r1 third_request_v240_game 1 "ayni girdi | V2.40 aday | oyun kamerasi"
mk v240cap_j40_rlw_oG_r1 third_request_v238_game 1 "ayni girdi | uretim | oyun kamerasi"
mk v240cap_j39_rl_oS_r1 right_then_left_v238_side 1 "saga 90 > fren ortasinda SOL | uretim | sabit yan"
mk v240cap_j39_rl_tkhS_r1 right_then_left_v240_side 1 "ayni girdi | V2.40 aday | sabit yan"
mk v240cap_j39_lr_oS_r1 left_then_right_v238_side 1 "sola 90 > fren ortasinda SAG | uretim | sabit yan"
mk v240cap_j39_lr_tkhS_r1 left_then_right_v240_side 1 "ayni girdi | V2.40 aday (devralma sonrasi yanal durus yok) | sabit yan"
mk v240cap_j38_cc90_oS_r1 consecutive_cuts_v238_side 1 "W > D > W > A | uretim | sabit yan"
mk v240cap_j38_cc90_tkhS_r1 consecutive_cuts_v240_side 1 "W > D > W > A | V2.40 aday | sabit yan"
mk v240cap_j39_push_plan_oS_r1 shove_during_cut_v238_side 1 "planli sag 90 sirasinda gercek itme (300 cm/s sola) | uretim: itme silinir | sabit yan"
mk v240cap_j39_push_plan_tkhS_r1 shove_during_cut_v240_side 1 "ayni itme | V2.40 aday: plan geri cekilir, toparlanma | sabit yan"
mk v240cap_j38_c90r_oG_r1 head_after_cut_v238_game 1 "sert saga 90 | uretim: bas kameraya bakiyor | oyun kamerasi"
mk v240cap_j38_c90r_tkhG_r1 head_after_cut_v240_game 1 "ayni girdi | V2.40 aday: elle bakis yokken bas hareket yonunde | oyun kamerasi"
mk v240capn_j40_wall_oN_r1 wall_during_cut_v238_side 1 "planli sag 90 yeni yonde duvara carpiyor | uretim: plan hizi duvara yaziliyor, yerinde kosu | sabit yan (-y)"
mk v240capn_j40_wall_tkhN_r1 wall_during_cut_v240_stand_side 1 "ayni duvar | V2.40 tkh: engel algisi + ayakta DB'ye tek zorlanmis arama | sabit yan (-y)"
mk v240capn_j40_wall_wstN_r1 wall_during_cut_v240_stop_side 1 "ayni duvar | V2.40 wst: engel algisi + durus DB'sine tek zorlanmis arama | sabit yan (-y)"
