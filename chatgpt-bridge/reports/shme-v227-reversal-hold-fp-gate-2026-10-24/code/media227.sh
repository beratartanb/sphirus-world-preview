#!/bin/bash
# media227.sh : V2.27 published media from the final fixed-step captures (30 FPS game time = real speed; unedited FULL frames, the docked
# viewport narrowed to a multiple of 64 - no crop). "URETIM" = saved V2.26 production (V2.27 knobs 0, NOT promoted); "ADAY rh" = candidate
# (32-bin SHM226 clips + hold + FootPlacement gate) in qa_pie candidate mode. GIF real speed; AVI realtime (mode 2 also 1/3 speed). Cameras: S side, G gameplay.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V227_20261024/pub/vid; mkdir -p $PUB
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi $O/${name}_slow3x.avi; do [ -f $f ] && cp $f $PUB/; done; echo "OK $name"; }
mk v227capfin_j24_sw_ph2_oS_r1 jogrev_SW_prod_side 2 "tempolu S > W | URETIM (V2.26, degismedi) | yan"
mk v227capfin_j24_sw_ph2_rhS_r1 jogrev_SW_cand_rh_side 2 "tempolu S > W | ADAY rh: yazili klip + tutma + FP kapisi (uretime alinmadi) | yan"
mk v227capfin_j24_sw_ph2_rhG_r1 jogrev_SW_cand_rh_game 1 "tempolu S > W | ADAY rh | oyun kamerasi (tam kare)"
mk v227capfin_j24_ph0_oS_r1 jogrev_WS_prod_side 2 "tempolu W > S > W | URETIM (V2.26) | yan"
mk v227capfin_j24_ph0_rhS_r1 jogrev_WS_cand_rh_side 2 "tempolu W > S > W | ADAY rh | yan"
mk v227capfin_j24_dbl_oS_r1 jogrev_double_prod_side 2 "cift geri donus (S 0,5 s / 0,3 s) | URETIM (V2.26) | yan"
mk v227capfin_j24_dbl_rhS_r1 jogrev_double_cand_rh_side 2 "cift geri donus | ADAY rh (yeni niyet karesinde tutma biter) | yan"
ls $PUB | wc -l
