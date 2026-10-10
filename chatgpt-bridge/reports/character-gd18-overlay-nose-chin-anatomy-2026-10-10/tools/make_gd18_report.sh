#!/bin/bash
# make_gd18_report.sh : GD18 report boards into bd/final/ - every image is a real capture / render of the actual geometry (no paint-over, no image warping
# beyond the exact solved-camera re-projection). Labels: cg17c4 = GD17 G17 (rigged, s1t6n look, custom brow c4) from GD17/ue; cg18c4 = GD18 G18 (rigged,
# same look, same cameras, same light). Blender clay: G17M / G18M = post-rig meshes in the solved reference cameras (gd18_rset).
# O overlays (diagnosis GD17, result REF/GD17/GD18 real + clay, nose + chin zooms), A profile lines, C clay, D full face, E deformation, F engine, G candidates.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD18_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009; W7=Saved/Codex/GD17_Identity_20261010
O=$W/bd/final; P=$W/bd/parts; mkdir -p $O $P; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
LB=Tools/CharacterLookdev_20260930/lk_board.py; REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references; T=${TAG:-G18S}; L18=${L18:-cg18c4}
vstack() { local o=$1 w=$2; shift 2; local A=(); for f in "$@"; do A+=("$(Wp $f)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd18_vstack.py)" -- "$(Wp $o)" $w "${A[@]}" 2>&1 | grep -c VSTACK >/dev/null; }
ovl() { "$B" -b --factory-startup --python "$(Wp $W/tools/gd18_overlay.py)" -- "$@" 2>&1 | grep -c OVERLAY_OK >/dev/null; }
# GD17 captures / renders needed next to the GD18 ones (copies of read-only GD17 outputs; removed again at the end, see data/report_tmp_copies.txt)
: > $W/data/report_tmp_copies.txt
for f in $(ls $W7/ue | grep -E "^cg17c4_(refnh|ref|commonnh|clay|close|closeclay)_"); do [ -e $W/ue/$f ] || { cp $W7/ue/$f $W/ue/$f; echo ue/$f >> $W/data/report_tmp_copies.txt; }; done
for f in $(ls $W7/r | grep -E "^G17M_REF_"); do [ -e $W/r/$f ] || { cp $W7/r/$f $W/r/$f; echo r/$f >> $W/data/report_tmp_copies.txt; }; done
declare -A RC=([front]="240 260 740 830" [q3_faceR]="380 250 880 820" [q3_faceL]="120 250 620 820" [prof_faceL]="60 220 560 790")
# ---- O1 diagnosis overlays of GD17 (made before any sculpt): full views, real + clay
vstack $O/O1_TESHIS_OVERLAY_GD17_TAM_YUZ.jpg 1680 $W/r/OV_g17_front.jpg $W/r/OV_g17_q3_faceR.jpg $W/r/OV_g17_q3_faceL.jpg $W/r/OV_g17_prof_faceL.jpg
vstack $O/O2_TESHIS_OVERLAY_GD17_BURUN_YAKIN.jpg 1760 $W/r/OVZ_nose_g17_front.jpg $W/r/OVZ_nose_g17_q3_faceR.jpg $W/r/OVZ_nose_g17_q3_faceL.jpg $W/r/OVZ_nose_g17_prof_faceL.jpg
vstack $O/O3_TESHIS_OVERLAY_GD17_CENE_YAKIN.jpg 1760 $W/r/OVZ_chin_g17_front.jpg $W/r/OVZ_chin_g17_q3_faceR.jpg $W/r/OVZ_chin_g17_q3_faceL.jpg $W/r/OVZ_chin_g17_prof_faceL.jpg
# ---- O4..O6 result overlays: REF | candidate | 50 % | red-cyan, rows GD17 real, GD18 real, GD17 clay, GD18 clay (same solved cameras)
for v in front q3_faceR q3_faceL prof_faceL; do
  ovl "$(Wp $P/O4_$v.jpg)" $v ${RC[$v]} 420 "GD17real=$(Wp $W/ue/cg17c4_refnh_$v.png)|$(Wp $W/r/G17M_REF_${v}_alpha.png)" "GD18real=$(Wp $W/ue/${L18}_refnh_$v.png)|$(Wp $W/r/${T}M_REF_${v}_alpha.png)" "GD17clay=$(Wp $W/r/G17M_REF_${v}_clayA.png)|$(Wp $W/r/G17M_REF_${v}_alpha.png)" "GD18clay=$(Wp $W/r/${T}M_REF_${v}_clayA.png)|$(Wp $W/r/${T}M_REF_${v}_alpha.png)"
  for r in "nose front 400 360 620 660" "nose q3_faceR 560 360 900 660" "nose q3_faceL 60 360 400 660" "nose prof_faceL 0 340 380 640" "chin front 360 560 640 830" "chin q3_faceR 500 540 880 820" "chin q3_faceL 120 540 520 820" "chin prof_faceL 40 500 440 790"; do set -- $r; [ $2 = $v ] || continue
    ovl "$(Wp $P/O5_${1}_$v.jpg)" $v $3 $4 $5 $6 440 "GD17real=$(Wp $W/ue/cg17c4_refnh_$v.png)|$(Wp $W/r/G17M_REF_${v}_alpha.png)" "GD18real=$(Wp $W/ue/${L18}_refnh_$v.png)|$(Wp $W/r/${T}M_REF_${v}_alpha.png)" "GD17clay=$(Wp $W/r/G17M_REF_${v}_clayA.png)|$(Wp $W/r/G17M_REF_${v}_alpha.png)" "GD18clay=$(Wp $W/r/${T}M_REF_${v}_clayA.png)|$(Wp $W/r/${T}M_REF_${v}_alpha.png)"; done; done
for v in front q3_faceR q3_faceL prof_faceL; do "$PY" $LB "$(Wp $O/O4_SONUC_OVERLAY_${v}.jpg)" "O4 $v - REF | aday | %50 | kirmizi=REF cyan=aday : satirlar GD17 gercek / GD18 gercek / GD17 kil / GD18 kil (ayni cozulmus kamera, deformasyon yok)" 1680 "$(Wp $P/O4_$v.jpg)|" | tail -c 30; done
vstack $O/O5_SONUC_OVERLAY_BURUN_YAKIN.jpg 1760 $P/O5_nose_front.jpg $P/O5_nose_q3_faceR.jpg $P/O5_nose_q3_faceL.jpg $P/O5_nose_prof_faceL.jpg
vstack $O/O6_SONUC_OVERLAY_CENE_YAKIN.jpg 1760 $P/O5_chin_front.jpg $P/O5_chin_q3_faceR.jpg $P/O5_chin_q3_faceL.jpg $P/O5_chin_prof_faceL.jpg
# ---- A profile lines (fixed solved profile camera): GD17 / GD18 post-rig vs the reference edge
"$B" -b --factory-startup --python "$(Wp $W/tools/gd18_profline.py)" -- "$(Wp $REFP/GD13_REF_panel_prof_faceL.png)" "$(Wp $O/A2_BURUN_PROFIL_CIZGILERI.jpg)" "$(Wp $W/meas/profline_final.json)" "GD17=$(Wp $W/meas/g17_postrig_dumpF.json)" "GD18=$(Wp $W/meas/g18_postrig_dumpF.json)" 2>&1 | grep PROFLINE | cut -c1-300
# ---- C clay: Blender (soft light A, side light B) REF / GD17 / GD18 + UE clay close-ups
WD=320 bash $W/tools/gd18_claycmp.sh final/C2_KIL_BLENDER_YUMUSAK_ISIK.jpg "C2 Kil (Blender - ayni cozulmus kameralar - yumusak isik A): REF / GD17 / GD18" clayA G17M ${T}M >/dev/null
WD=320 bash $W/tools/gd18_claycmp.sh final/C3_KIL_BLENDER_YAN_ISIK.jpg "C3 Kil (Blender - guclu yan form isigi B): REF / GD17 / GD18" clayB G17M ${T}M >/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_G.json")" "$L18" <<'PYE'
import json, sys, os
U, P, OUT, L18 = sys.argv[1:5]; S = []
for L in ('cg17c4', L18):
    for s in ('close', 'closeclay'):
        for k in ('nose_front', 'nose_prof', 'mouth_front', 'mouth_q3', 'chin_prof', 'chin_q3'):
            f = f'{U}/{L}_{s}_{k}_custom.png'
            if os.path.exists(f): S.append(dict(src=f, rect=[160, 160, 1440, 1440], w=420, out=f'{P}/G_{L}_{s}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_G.json)" 2>&1 | grep -c PARTS_OK >/dev/null
for grp in "C4_BURUN_YAKIN_GERCEK_ve_KIL:nose_front nose_prof" "C5_DUDAK_YAKIN_GERCEK_ve_KIL:mouth_front mouth_q3" "C6_CENE_YAKIN_GERCEK_ve_KIL:chin_prof chin_q3"; do
  nm=${grp%%:*}; rows=()
  for k in ${grp#*:}; do rows+=("$(Wp $P/G_cg17c4_close_$k.jpg)|GD17 gercek $k, $(Wp $P/G_${L18}_close_$k.jpg)|GD18 gercek $k, $(Wp $P/G_cg17c4_closeclay_$k.jpg)|GD17 kil $k, $(Wp $P/G_${L18}_closeclay_$k.jpg)|GD18 kil $k"); done
  "$PY" $LB "$(Wp $O/$nm.jpg)" "${nm%%_*} UE yakin plan (ayni kamera - ayni on isik - ayni cilt): GD17 gercek | GD18 gercek | GD17 kil | GD18 kil (sac-kas-kirpik gizli)" 420 "${rows[@]}" | tail -c 30; done
# ---- D full face identity, same skin / iris / hair / light / camera
WD=330 bash $W/tools/gd18_uecmp.sh final/D1_TAM_YUZ_ONISIK_SACSIZ.jpg "D1 Tam yuz - ayni cilt - iris - isik - cozulmus referans kameralari - sacsiz: REF / GD17 / GD18" refnh cg17c4 $L18 >/dev/null
WD=330 bash $W/tools/gd18_uecmp.sh final/D2_TAM_YUZ_ONISIK_SACLI.jpg "D2 Tam yuz - h75c sac ile: REF / GD17 / GD18" ref cg17c4 $L18 >/dev/null
VIEWS="front" COMMON=1 CSET=commonnh WD=300 bash $W/tools/gd18_uecmp.sh final/D4_ORTAK_KAMERA.jpg "D4 Sabit ortak kameralar (adaya gore ayar yok): GD17 / GD18" refnh cg17c4 $L18 >/dev/null
# ---- E deformation GD17 -> GD18 (post-rig meshes)
"$B" -b "$(Wp $G/GD13_scene.blend)" --python "$(Wp $W/tools/gd18_dispmap.py)" -- "$(Wp $W/data/head_g18_postrig.npy)" "$(Wp $W/data/head_g17_postrig.npy)" "$(Wp $W/r/DM_G18_vsG17)" 3 2>&1 | grep DISPM
e1=""; e2=""; for c in front q3R q3L profL profR top back; do e1="${e1:+$e1, }$(Wp $W/r/DM_G18_vsG17_dsigned_$c.png)|isaretli $c"; e2="${e2:+$e2, }$(Wp $W/r/DM_G18_vsG17_dmag_$c.png)|buyukluk $c"; done
"$PY" $LB "$(Wp $O/E_DEFORMASYON_GD17_GD18.jpg)" "E 3B deformasyon GD17 G17 -> GD18 G18 (riglenmis meshler). Isaretli: kirmizi = disari - mavi = iceri (+-3 mm); buyukluk: siyah 0 -> sari 3 mm" 300 "$e1" "$e2" | tail -c 30
# ---- F engine validation
NCOL=6 WD=280 bash $W/tools/gd18_exprboard.sh $L18 F1_RIG_IFADE_TESTI.jpg "F1 GD18 yuz rigi (otomatik rig DNA) - RigLogic kontrol testleri - on isik - sac gizli" >/dev/null; mv $W/bd/F1_RIG_IFADE_TESTI.jpg $O/ 2>/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_F2.json")" "$L18" <<'PYE'
import json, sys, os
U, P, OUT, L18 = sys.argv[1:5]; S = []
for c in ('neutral', 'blink', 'look_down', 'brows_up', 'smile', 'frown'):
    for k, rc in (('front', [420, 380, 1180, 820]), ('q3', [440, 380, 1200, 820])):
        f = f'{U}/{L18}_expr_{c}_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=560, out=f'{P}/F2_{c}_{k}.jpg'))
for n in (0, 1, 2, 3):
    for k in ('front', 'q3'):
        for nm in (f'{L18}_lod_{n}_{k}_custom.png', f'{L18}_lod{n}_{k}_custom.png'):
            f = f'{U}/{nm}'
            if os.path.exists(f): S.append(dict(src=f, rect=[380, 120, 1220, 1300], w=340, out=f'{P}/F3_lod{n}_{k}.jpg')); break
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_F2.json)" 2>&1 | grep -c PARTS_OK >/dev/null
A=(); for c in neutral blink look_down brows_up smile frown; do for k in front q3; do A+=("$(Wp $P/F2_${c}_$k.jpg)"); done; done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd18_grid.py)" -- "$(Wp $O/F2_KAS_KAPAK_IFADE_YAKIN.jpg)" 4 500 "${A[@]}" 2>&1 | grep -c GRID >/dev/null
r1=""; r2=""; for n in 0 1 2 3; do r1="${r1:+$r1, }$(Wp $P/F3_lod${n}_front.jpg)|LOD$n on"; r2="${r2:+$r2, }$(Wp $P/F3_lod${n}_q3.jpg)|LOD$n 3/4"; done
"$PY" $LB "$(Wp $O/F3_LOD_0_3.jpg)" "F3 GD18 LOD 0-3 (tum bilesenlerde zorlanmis LOD - groom LOD otomatik - sac ve ozel kas gorunur)" 340 "$r1" "$r2" | tail -c 30
# ---- G candidates A / B (Blender clay overlays in the solved cameras, pre-rig): rows GD17, A, B
for v in front prof_faceL q3_faceR; do ovl "$(Wp $P/G1_$v.jpg)" $v ${RC[$v]} 400 "GD17=$(Wp $W/r/G17M_REF_${v}_clayA.png)|$(Wp $W/r/G17M_REF_${v}_alpha.png)" "A=$(Wp $W/r/G18AM_REF_${v}_clayA.png)|$(Wp $W/r/G18AM_REF_${v}_alpha.png)" "B=$(Wp $W/r/G18BM_REF_${v}_clayA.png)|$(Wp $W/r/G18BM_REF_${v}_alpha.png)"; done
vstack $O/G1_ADAYLAR_A_B_KIL_OVERLAY.jpg 1600 $P/G1_front.jpg $P/G1_prof_faceL.jpg $P/G1_q3_faceR.jpg
ls $O
