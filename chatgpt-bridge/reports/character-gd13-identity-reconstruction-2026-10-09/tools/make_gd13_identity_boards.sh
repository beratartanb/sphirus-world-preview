#!/bin/bash
# make_gd13_identity_boards.sh : GD13 boards (A clay / B identity / C close-ups / D deformation / E silhouette) -> Saved/Codex/GD13_Identity_20261009/bd
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; O=Saved/Codex/GD13_Identity_20261009; P=$O/bd/parts
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T=Tools/CharacterLookdev_20260930
w() { cygpath -w "$(pwd)/$1"; }
B() { local out=$1 title=$2 cell=$3; shift 3; "$PY" $T/lk_board.py "$(w $O/bd/$out)" "$title" $cell "$@" | tail -c 60; echo; }
V="front q3_faceR q3_faceL prof_faceL"; declare -A VL=([front]="ON" [q3_faceR]="SAG 3-4 (yuz saga)" [q3_faceL]="SOL 3-4 (yuz sola)" [prof_faceL]="SOL PROFIL")
rows() { local pre=$1 var=$2 r=(); for v in $V; do r+=("$(w $P/${pre}ref_$v.jpg)|ORIJINAL REF ${VL[$v]}, $(w $P/GD12_${v}_$var.jpg)|GD12 ${VL[$v]}, $(w $P/GD13_${v}_$var.jpg)|GD13 ${VL[$v]}"); done; printf '%s\n' "${r[@]}"; }
mapfile -t R < <(rows "" clayA); B A1_CLAY_REF_KAMERALARI_ISIK_A.jpg "A1 CLAY - cozulmus referans kameralari - isik A (on yumusak): ORIJINAL REFERANS / GD12 / GD13" 470 "${R[@]}"
mapfile -t R < <(rows "" clayB); B A2_CLAY_REF_KAMERALARI_ISIK_B.jpg "A2 CLAY - ayni kameralar - isik B (yan sert): ORIJINAL REFERANS / GD12 / GD13" 470 "${R[@]}"
rv() { local h=$1 var=$2; echo "$(w $P/${h}_rev_front_$var.jpg)|$h ON, $(w $P/${h}_rev_q3R_$var.jpg)|$h SAG 3-4, $(w $P/${h}_rev_q3L_$var.jpg)|$h SOL 3-4, $(w $P/${h}_rev_profR_$var.jpg)|$h SAG PROFIL (referansta yok - yardimci), $(w $P/${h}_rev_profL_$var.jpg)|$h SOL PROFIL"; }
B A3_CLAY_5_ACI_INCELEME.jpg "A3 CLAY - 5 inceleme acisi (referanssiz yardimci kamera): GD12 / GD13 - isik A" 400 "$(rv GD12 clayA)" "$(rv GD13 clayA)"
mapfile -t R < <(rows "" skinA); B B1_KIMLIK_TEN_REF_KAMERALARI.jpg "B1 KIMLIK - basit ten + iris + gecici kas/kirpik cizgisi (sacsiz - tani materyali): ORIJINAL REFERANS / GD12 / GD13" 470 "${R[@]}"
B B2_KIMLIK_5_ACI.jpg "B2 KIMLIK - 5 inceleme acisi (yardimci kamera): GD12 / GD13" 400 "$(rv GD12 skinA)" "$(rv GD13 skinA)"
cl() { local k=$1 lab=$2; echo "$(w $P/cl_${k}_ref.jpg)|ORIJINAL REF $lab, $(w $P/cl_${k}_GD12.jpg)|GD12 $lab, $(w $P/cl_${k}_GD13.jpg)|GD13 $lab"; }
B C1_YAKIN_GOZ_KAS_ORBITA.jpg "C1 GOZ / KAS / ORBITA - ORIJINAL REFERANS / GD12 / GD13" 620 "$(cl eyes_front 'on ten')" "$(cl eyes_front_clay 'on clay isik B')" "$(cl eye_q3R 'sag 3-4 ten')"
B C2_YAKIN_ELMACIK_ORTA_YUZ.jpg "C2 ELMACIK / ORTA YUZ (clay isik B) - ORIJINAL REFERANS / GD12 / GD13" 560 "$(cl midface_q3L 'sol 3-4')" "$(cl midface_front 'on')"
B C3_YAKIN_BURUN.jpg "C3 BURUN - ORIJINAL REFERANS / GD12 / GD13" 520 "$(cl nose_front 'on ten')" "$(cl nose_q3R 'sag 3-4 clay')" "$(cl nose_prof 'profil clay')"
B C4_YAKIN_DUDAK_AGIZ.jpg "C4 DUDAK / AGIZ KOSELERI - ORIJINAL REFERANS / GD12 / GD13" 600 "$(cl mouth_front 'on ten')" "$(cl mouth_q3R 'sag 3-4 clay')"
B C5_YAKIN_CENE_MANDIBULA.jpg "C5 CENE / MANDIBULA - ORIJINAL REFERANS / GD12 / GD13" 560 "$(cl jaw_front 'on clay B')" "$(cl jaw_q3L 'sol 3-4 clay B')" "$(cl jaw_q3R 'sag 3-4 clay A')"
B C6_PROFIL_DERINLIK.jpg "C6 PROFIL DERINLIGI - pembe = model siluet cizgisi referans uzerinde (ayni kamera): GD12 / GD13 + clay" 500 "$(w $P/refovl_GD12_prof_faceL.jpg)|GD12 siluet / REF, $(w $P/refovl_GD13_prof_faceL.jpg)|GD13 siluet / REF, $(w $P/GD12_prof_faceL_clayA.jpg)|GD12 clay, $(w $P/GD13_prof_faceL_clayA.jpg)|GD13 clay"
dm() { local pr=$1 m=$2 lab=$3; echo "$(w $P/dm_${pr}_${m}_front.jpg)|$lab on, $(w $P/dm_${pr}_${m}_q3R.jpg)|$lab sag 3-4, $(w $P/dm_${pr}_${m}_q3L.jpg)|$lab sol 3-4, $(w $P/dm_${pr}_${m}_profL.jpg)|$lab sol profil"; }
B D1_DEFORMASYON_GD12_GD13.jpg "D1 GD12 -> GD13 GERCEK MESH FARKI: ust = yuzey normali yonu (kirmizi disari / mavi iceri +-4 mm) / alt = 3B vektor buyuklugu (siyah 0 -> sari 4 mm)" 420 "$(dm GD12toGD13 dsigned normal)" "$(dm GD12toGD13 dmag '3B buyukluk')"
B D2_DEFORMASYON_F1H_GD13.jpg "D2 F1H (GD11 taban) -> GD13 GERCEK MESH FARKI: ust = normal yonu +-4 mm / alt = 3B buyukluk 0-4 mm" 420 "$(dm F1HtoGD13 dsigned normal)" "$(dm F1HtoGD13 dmag '3B buyukluk')"
so() { local h=$1; local r=(); for v in $V; do r+=("$(w $P/refovl_${h}_$v.jpg)|$h siluet ${VL[$v]}"); done; local IFS=,; echo "${r[*]}"; }
B E1_SILUET_UST_USTE.jpg "E1 SILUET - pembe = modelin cozulmus kameradaki dis hatti referans uzerinde: GD12 (ust) / GD13 (alt)" 470 "$(so GD12)" "$(so GD13)"
