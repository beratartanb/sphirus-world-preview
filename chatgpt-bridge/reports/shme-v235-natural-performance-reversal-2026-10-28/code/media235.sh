#!/bin/bash
# media235.sh : V2.35 published media from fixed-step captures (30 FPS game time = real speed, full frames, unedited; no slow motion).
# o = V2.35 production, pre235 = every V2.35 knob at its V2.34 value (old reversal DBs, RevOverHard / RevGapKeep off, mouse 0.35),
# pad235 = gamepad profile. S side, D diagonal, G game camera.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
M=Tools/SHME_V211_20261016/make_media211.sh; O=Saved/Codex/SHME_V211_20261016/vid; PUB=Saved/Codex/SHME_V235_20261028/pub/vid; mkdir -p $PUB $O
mk() { lab=$1; name=$2; avi=$3; shift 3; [ -d Saved/Codex/SHME_V138_20260927/Video/$lab ] && [ -n "$(ls Saved/Codex/SHME_V138_20260927/Video/$lab)" ] || { echo "MISSING $lab"; return; }; AVI=$avi GIFSCALE=${GS:-0.38} bash $M $lab $name 0 0 1 1 "$*" > /dev/null 2>&1
  for f in $O/$name.gif $O/${name}_realtime.avi; do [ -f $f ] && cp $f $PUB/; done; rm -rf $O/_crop_$name $O/_avi_$name; echo "OK $name"; }
mk v235cap_j35_rev_pre235S_r1 reversal_chain_before_side 1 "dur > tempolu > sert S > geri > W > dur | ONCE (V2.34 icerik): ters istekte iki ayak yerde ~0.5 s bekler | sabit yan"
mk v235cap_j35_rev_oS_r1 reversal_chain_v235_side 1 "ayni girdi | V2.35: fren > yakalama adimi > olculu geri itis, bekleme yok | sabit yan"
mk v235cap_j35_rev_oD_r1 reversal_chain_v235_diag 1 "ayni girdi | V2.35 | sabit capraz"
mk v235cap_j35_rev_oG_r1 reversal_chain_v235_game 1 "ayni girdi | V2.35 | oyun kamerasi"
mk v235cap_j35_rev2_oS_r1 reversal_chain2_v235_side 1 "geri kalkis > W (B_F) > ileri > S (F_B, diger destek) > geri > dur | V2.35 | sabit yan"
mk v235cap_j30_rel_3200_pre235S_r1 release_repress_before_side 1 "tempolu > S > 0.15 s birak > tekrar S > W | ONCE V2.34 | sabit yan"
mk v235cap_j30_rel_3200_oS_r1 release_repress_v235_side 1 "ayni girdi | V2.35: bosluk bolumu bitirmez, ayni ters donus surer | sabit yan"
mk v235cap_j30_slow_oS_r1 back_start_forward_stop_v235_side 1 "durus > geri kalkis > ileri istek > ileri > durus | V2.35 | sabit yan"
mk v235cap_j34_chain1_oS_r1 chain1_restart_v235_side 1 "geri kalkis > ileri > durus > kisa yeniden hareket | V2.35 | sabit yan"
mk v235cap_cam33_wturn_pre235G_r1 walk_right_mouse_before_game 1 "yuru > saga, fare profili | ONCE: takip 0.35 (5.5 s sonra 29 derece geride) | oyun kamerasi"
mk v235cap_cam33_wturn_oG_r1 walk_right_mouse_v235_game 1 "ayni girdi | V2.35: fare takibi 0.7 (~2.4 s yerlesir) | oyun kamerasi"
mk v235cap_cam34_wflow_pad235G_r1 walk_flow_gamepad_v235_game 1 "analog akis, sag analog yok | V2.35 gamepad | oyun kamerasi"
