#!/bin/bash
# media238.sh : V2.38 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.38 production, pre238 = every V2.38 knob at its V2.37 value (the V2.37 jog 90 = loop curve). S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V238_20261030/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v238cap_j38_c90r_pre238S_r1 jog90_right_v237_side 1 "tempolu ileri > sert saga 90 | ONCE V2.37: dongu egrisi, fren temasi yok | sabit yan"
mk v238cap_j38_c90r_oS_r1 jog90_right_v238_side 1 "ayni girdi | V2.38: fizik planli fren - destek - yeni itis, kapsul klibin yolunu izler | sabit yan"
mk v238cap_j38_c90r_pre238G_r1 jog90_right_v237_game 1 "ayni girdi | ONCE V2.37 | oyun kamerasi"
mk v238cap_j38_c90r_oG_r1 jog90_right_v238_game 1 "ayni girdi | V2.38 | oyun kamerasi"
mk v238cap_j38_c90r_oD_r1 jog90_right_v238_diag 1 "ayni girdi | V2.38 | sabit capraz"
mk v238cap_j38_c90l_pre238S_r1 jog90_left_v237_side 1 "tempolu ileri > sert sola 90 | ONCE V2.37 | sabit yan"
mk v238cap_j38_c90l_oS_r1 jog90_left_v238_side 1 "ayni girdi | V2.38 | sabit yan"
mk v238cap_j38_c90rb_oS_r1 jog90_right_v238_favourable_side 1 "ayni girdi, daha erken istek (dis ayak sirada) | V2.38: normal destek, ek fren adimi yok | sabit yan"
mk v238cap_j38_c90lb_oS_r1 jog90_left_v238_favourable_side 1 "sola 90, dis ayak sirada | V2.38: normal destek | sabit yan"
mk v238cap_j38_cc90_oS_r1 jog_consecutive_cuts_v238_side 1 "W > D > W > A art arda | V2.38 | sabit yan"
