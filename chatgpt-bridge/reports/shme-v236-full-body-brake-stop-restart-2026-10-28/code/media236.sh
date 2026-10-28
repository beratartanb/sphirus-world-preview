#!/bin/bash
# media236.sh : V2.36 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.36 production, pre236 = every V2.36 group at its V2.35 value (old CP2 jog stop, production start DBs, V2.35 reversal, V2.31 loaded),
# pad235 = gamepad profile. S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V236_20261028/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v236s2g_j36_stopr_oS_r1 stop_restart_before_side 1 "(s2g, terfi oncesi uretim = V2.35; kayit penceresi farkli, zaman eslesmez) tempolu > birak > durus > ileri > durus | ONCE (V2.35 CP2 durusu): diz yuksekliginde adim, kollar kosuda, geri cekme | sabit yan"
mk v236cap_j36_stopr_oS_r1 stop_restart_v236_side 1 "ayni girdi | V2.36: fren ayagi, kisa adim, kapanis, govde dikilir, kollar birakir; duz kalkis | sabit yan"
mk v236cap_j36_stopr_oG_r1 stop_restart_v236_game 1 "ayni girdi | V2.36 | oyun kamerasi"
mk v236cap_j36_stopr_oD_r1 stop_restart_v236_diag 1 "ayni girdi | V2.36 | sabit capraz"
mk v236cap_j36_stopb_oS_r1 stop_other_foot_v236_side 1 "birakma yarim adim sonra (diger fren ayagi) | V2.36 | sabit yan"
mk v236cap_j36_wjs_pre236S_r1 walk_jog_stop_before_side 1 "yuru > tempolu > durus > ileri | ONCE V2.35 | sabit yan"
mk v236cap_j36_wjs_oS_r1 walk_jog_stop_v236_side 1 "ayni girdi | V2.36 | sabit yan"
mk v236cap_j36_rsl_oS_r1 late_repress_v236_side 1 "durusun sonunda tekrar ileri | V2.36: sol ayakla duz kalkis (eski: TurnL045) | sabit yan"
mk v236cap_j35_rev_pre236S_r1 reversal_before_side 1 "tempolu > sert S > geri > W > dur | ONCE V2.35 | sabit yan"
mk v236cap_j35_rev_oS_r1 reversal_v236_side 1 "ayni girdi | V2.36: fren aninda kollar ve dirsekler | sabit yan"
mk v236cap_j35_rev_oG_r1 reversal_v236_game 1 "ayni girdi | V2.36 | oyun kamerasi"
mk v236cap_e29_load_pre236S_r1 effort_reversal_before_side 1 "eforlu zincir: ikinci ters donus | ONCE V2.31 yuklu: iki ayak ~0.4 s bekler | sabit yan"
mk v236cap_e29_load_oS_r1 effort_reversal_v236_side 1 "ayni girdi | V2.36 yuklu: yakalama adimi + olculu itis, bekleme 0.13 s | sabit yan"
mk v236cap_j34_chain1_oS_r1 chain1_restart_v236_side 1 "geri kalkis > ileri > durus > kisa yeniden hareket | V2.36 | sabit yan"
mk v236cap_j36_sside_oG_r1 stop_side_start_v236_game 1 "durus > yan kalkis (A) > capraz kalkis (W+D) | V2.36 | oyun kamerasi"
