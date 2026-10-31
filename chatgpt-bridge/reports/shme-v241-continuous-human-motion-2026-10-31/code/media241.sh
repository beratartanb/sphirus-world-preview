#!/bin/bash
# media241.sh : V2.41 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = saved production (V2.38..V2.40 behaviour + inert V2.41 knobs), tkha = V2.41 candidate (SHM239_Own 1 + SHM240_HeadOn 1 + SHM241_KOn 1
# + regional head aim offset BS_SHM241_AO_Head switched in memory), tkp = Own + HeadOn + KOn + SHM241_PushYawK 0.15 (no aim offset switch). S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V241_20261031/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v241cap_j40_rlw_oS_r1 third_request_prod_side 1 "ileri > sert saga 90 > fren ortasinda SOL > ILERI > dur | uretim | sabit yan"
mk v241cap2_j40_rlw_tkhaS_r1 third_request_v241_side 1 "ayni girdi | V2.41 aday tkha (temas bazli giris + bolgesel bas AO) | sabit yan"
mk v241cap2_j40_rlw_tkhaD_r1 third_request_v241_diag 1 "ayni girdi | V2.41 aday tkha | sabit capraz (dortte uc)"
mk v241cap2_j40_rlw_tkhaG_r1 third_request_v241_game 1 "ayni girdi | V2.41 aday tkha | oyun kamerasi"
mk v241cap_j40_rlw_oG_r1 third_request_prod_game 1 "ayni girdi | uretim | oyun kamerasi"
mk v241cap_j39_lr_oS_r1 left_then_right_prod_side 1 "sola 90 > fren ortasinda SAG | uretim | sabit yan"
mk v241cap2_j39_lr_tkhaS_r1 left_then_right_v241_side 1 "ayni girdi | V2.41 aday tkha | sabit yan"
mk v241cap_j38_cc90_oS_r1 consecutive_cuts_prod_side 1 "W > D > W > A | uretim | sabit yan"
mk v241cap2_j38_cc90_tkhaS_r1 consecutive_cuts_v241_side 1 "W > D > W > A | V2.41 aday tkha | sabit yan"
mk v241cap_j39_push_plan_oS_r1 shove_prod_side 1 "planli sag 90 sirasinda itme | uretim: itme silinir | sabit yan"
mk v241cap2_j39_push_plan_tkhaS_r1 shove_v241_side 1 "ayni itme | V2.41 tkha: yakalama adimi | sabit yan"
mk v241cap_j39_push_plan_tkpS_r1 shove_v241_yawhold_side 1 "ayni itme | V2.41 tkp: itme yonu tutma (PushYawK 0.15, AO yok) | sabit yan"
mk v241cap_j38_c90r_oG_r1 head_after_cut_prod_game 1 "sert saga 90 | uretim | oyun kamerasi"
mk v241cap2_j38_c90r_tkhaG_r1 head_after_cut_v241_game 1 "ayni girdi | V2.41 tkha: bolgesel bas AO + takip | oyun kamerasi"
mk v241cap2_j38_c90r_aohG_r1 head_after_cut_aoonly_game 1 "ayni girdi | yalniz bolgesel bas AO (uretim davranisi) | oyun kamerasi"
mk v241cap2_j40_wall_oG_r1 wall_prod_game 1 "planli sag 90 yeni yonde duvara | uretim | oyun kamerasi"
mk v241cap2_j40_wall_tkhaG_r1 wall_v241_game 1 "ayni duvar | V2.41 tkha | oyun kamerasi"
mk v241cap_j41_rl_p10_oS_r1 right_left_gated_prod_side 1 "saga 90 > fren ortasinda SOL (kosu fazina kapili) > dur > A ile yeniden kalkis | uretim | sabit yan"
mk v241cap_j41_rl_p10_tkhS_r1 right_left_gated_v240_side 1 "ayni girdi | V2.40 aday tkh (yanlis K girisi) | sabit yan"
mk v241cap2_j41_rl_p10_tkhaS_r1 right_left_gated_v241_side 1 "ayni girdi | V2.41 aday tkha (dogru K) | sabit yan"
