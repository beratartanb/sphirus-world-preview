#!/bin/bash
# media239.sh : V2.39 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.38 production, pre238 = every V2.38 knob at its V2.37 value (the V2.37 jog 90 = loop curve). S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V239_20261030/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v239cap_j39_rl_oS_r1 chain_right_then_left_v238_side 1 "tempolu ileri > sert saga 90 > fren ortasinda SOL istek | V2.38 uretim | sabit yan"
mk v239cap_j39_rl_tkS_r1 chain_right_then_left_v239_side 1 "ayni girdi | V2.39 aday: mevcut hiz/destek devralinir, sonraki temasta yeni plan | sabit yan"
mk v239cap_j39_rl_oG_r1 chain_right_then_left_v238_game 1 "ayni girdi | V2.38 | oyun kamerasi"
mk v239cap_j39_rl_tkG_r1 chain_right_then_left_v239_game 1 "ayni girdi | V2.39 aday | oyun kamerasi"
mk v239cap_j39_rl_tkD_r1 chain_right_then_left_v239_diag 1 "ayni girdi | V2.39 aday | sabit capraz"
mk v239cap_j39_rw_tkS_r1 chain_right_then_forward_v239_side 1 "saga 90 > fren ortasinda ILERI istek | V2.39 aday | sabit yan"
mk v239cap_j39_lr_tkS_r1 chain_left_then_right_v239_side 1 "sola 90 > fren ortasinda SAG istek (ayna) | V2.39 aday | sabit yan"
mk v239cap_j38_cc90_oS_r1 consecutive_cuts_v238_side 1 "W > D > W > A | V2.38 | sabit yan"
mk v239cap_j38_cc90_tkS_r1 consecutive_cuts_v239_side 1 "W > D > W > A | V2.39 aday | sabit yan"
mk v239cap_j39_push_plan_oS_r1 shove_during_cut_v238_side 1 "planli sag 90 sirasinda gercek itme (300 cm/s sola) | V2.38: itme silinir | sabit yan"
mk v239cap_j39_push_plan_tkS_r1 shove_during_cut_v239_side 1 "ayni itme | V2.39 aday: plan geri cekilir, toparlanma adimi | sabit yan"
