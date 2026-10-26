#!/bin/bash
# media231.sh : V2.31 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.31 production; pre = the same production with every V2.31 knob at its V2.30 value (before). Curved sprint loops were re-baked in place:
# their "before" is the V2.30 published media.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V231_20261026/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v231cap_c30_calm_oS_r1 calm_walk_diag_stop_restart_v231_side 1 "sakin: idle > yuruyus > capraz > dur > yeniden yuru | V2.31 uretim | yan"
mk v231cap_c30_calm_oG_r1 calm_walk_diag_stop_restart_v231_game 1 "ayni sakin akis | V2.31 uretim | oyun kamerasi"
mk v231cap_s29_swl12_preS_r1 lowspeed_back_forward_before_side 1 "depar > S 1.2 s > W (49-63 cm/s geri) | ONCE: V2.31 dugmeleri kapali | yan"
mk v231cap_s29_swl12_oS_r1 lowspeed_back_forward_v231_side 1 "ayni girdi | V2.31: dusuk hiz dönüs ailesi | yan"
mk v231cap_s29_swl12_oG_r1 lowspeed_back_forward_v231_game 1 "ayni girdi | V2.31 | oyun kamerasi"
mk v231cap_e29_chain_oS_r1 sprint_hardturn_reverse_repush_v231_side 1 "depar > sert sol > sag > ters > yeniden itis | V2.31 | yan"
mk v231cap_e29_chain_oG_r1 sprint_hardturn_reverse_repush_v231_game 1 "ayni zincir | V2.31 | oyun kamerasi"
mk v231cap_e29_load_preS_r1 loaded_reversal_before_side 1 "birikmis efor: ikinci ters donus | ONCE (V2.30 yolu) | yan"
mk v231cap_e29_load_oS_r1 loaded_reversal_catchstep_v231_side 1 "ayni girdi | V2.31: yakalama adimli yuklu donus | yan"
mk v231cap_e29_rest_oS_r1 rested_reversal_v231_side 1 "dinlenmis ayni manevra | V2.31 | yan"
mk v231cap_j30_rel_3100_preS_r1 release_repress_early_before_side 1 "frende erken birak > yeniden bas | ONCE | yan"
mk v231cap_j30_rel_3100_oS_r1 release_repress_early_v231_side 1 "ayni girdi | V2.31: dusuk hiz F_B + epizot | yan"
mk v231cap_legs_slope_sprint_preS_r1 slope_sprint_cam180_before_side 1 "egimde depar > dur > kamera 180 > kalkis | ONCE | yan"
mk v231cap_legs_slope_sprint_oS_r1 slope_sprint_cam180_v231_side 1 "ayni girdi | V2.31: TIP bitis karesi | yan"
mk v231cap_s29_cam_oG_r1 sprint_cam180_v231_game 1 "depar + kamera 180 | V2.31 | oyun kamerasi"
mk v231cap_d_sprint_oS_r1 sprint_curves_v231_side 1 "depar + egriler (oran 1.0 ile yeniden pisirilmis) | V2.31 | yan"
mk v231cap_a29_angb_oS_r1 rear_diagonal_walk_v231_side 1 "geri capraz yuruyus (-90 > -112.5 > -135) | V2.31 | yan"
mk v231cap_ter_drop_walk_preS_r1 step30_walk_before_side 1 "30 cm basamak yukselis / inis (yuruyus) | ONCE | yan"
mk v231cap_ter_drop_walk_oS_r1 step30_walk_v231_side 1 "ayni parkur | V2.31: kapsul yukselisi kaldirmadan dusulur | yan"
mk v231cap_ins_ws_preG_r1 inspect_masks_before_game 1 "atolye maskeleri inceleme | ONCE (V2.30: sorgu kuresi odagi) | oyun kamerasi"
mk v231cap_ins_ws_oG_r1 inspect_masks_v231_game 1 "ayni bakis | V2.31: GR_Inspect etiketi + mask yuzey odagi | oyun kamerasi"
mk v231cap_map_r1_oG_r1 house_route_v231_game 1 "gercek ev-orman rotasi | V2.31 | oyun kamerasi"
ls $PUB | wc -l
