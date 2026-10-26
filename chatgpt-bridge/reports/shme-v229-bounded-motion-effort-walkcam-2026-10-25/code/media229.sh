#!/bin/bash
# media229.sh : V2.29 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# cap4: ref = V2.28 behaviour + the RevTurn content fix (flags: no effort, old walk camera, no resume / push cancel); o = V2.29 production.

cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V229_20261025/pub/vid; mkdir -p $PUB
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; echo "OK $name"; }
mk v229cap4_s29_cam_oS_r1 sprint_cam180_v229_side 1 "depar + kamera 180, W basili: govde donusu | V2.29 uretim | yan"
mk v229cap4_s29_cam_oG_r1 sprint_cam180_v229_game 1 "depar + kamera 180, W basili | V2.29 uretim | oyun kamerasi (tam kare)"
mk v229cap4_s29_cam2_oG_r1 sprint_cam180b_v229_game 1 "depar + kamera 180 (ikinci evre) | V2.29 uretim | oyun kamerasi"
mk v229cap4_e29_load_refS_r1 sprint_WSWSW_ref_side 1 "depar W>S>W>S>W: son W'de geri kosu kilidi | REFERANS (V2.28 davranisi) | yan"
mk v229cap4_e29_load_oS_r1 sprint_WSWSW_v229_side 1 "depar W>S>W>S>W | V2.29 uretim (itis fazi iptali + efor) | yan"
mk v229cap4_e29_load_oG_r1 sprint_WSWSW_v229_game 1 "depar W>S>W>S>W | V2.29 uretim | oyun kamerasi"
mk v229cap4_e29_chain_refS_r1 effort_chain_ref_side 1 "depar > sert sol > sag > geri > ileri | REFERANS (efor yok) | yan"
mk v229cap4_e29_chain_oS_r1 effort_chain_v229_side 1 "ayni zincir | V2.29 uretim (efor) | yan"
mk v229cap4_e29_chain_oG_r1 effort_chain_v229_game 1 "ayni zincir | V2.29 uretim | oyun kamerasi"
mk v229cap4_e29_rest_refS_r1 effort_rest_ref_side 1 "dinlenmis depar + tek sert sol | REFERANS | yan"
mk v229cap4_e29_rest_oS_r1 effort_rest_v229_side 1 "dinlenmis depar + tek sert sol | V2.29 uretim | yan"
mk v229cap4_c29_combo_refG_r1 walkcam_combo_ref_game 1 "idle > ilk adim > ileri/capraz > A/D > kamera donusu > dur | REFERANS kamera | oyun kamerasi"
mk v229cap4_c29_combo_oG_r1 walkcam_combo_v229_game 1 "ayni dizi | V2.29 yuruyus kadraji | oyun kamerasi"
mk v229cap4_c29_combo_oS_r1 walkcam_combo_v229_side 1 "ayni dizi | V2.29 uretim | yan"
mk v229cap4_j24_rel_refS_r1 jogrev_release_ref_side 1 "tempolu geri donus icinde birak-bas | REFERANS (V2.28: kalkis klibi) | yan"
mk v229cap4_j24_rel_oS_r1 jogrev_release_v229_side 1 "tempolu geri donus icinde birak-bas: ayni klip itise devam | V2.29 uretim | yan"
ls $PUB | wc -l
