#!/bin/bash
# make_gd17_final.sh : GD17 report boards into bd/final/ - every image is a real capture / render of the actual geometry (no paint-over).
# labels: g16B / g16BS = GD16 G16 (rigged) with the reference look (front / studio light); cg17c4 / cg17c4S = GD17 G17 (rigged) with the
# custom reference brow c4 and otherwise the same look. Blender clay: G16M / G17M = post-rig meshes in the solved reference cameras.
# A nose (REF / GD16 / GD17 close-ups, profile lines, right profile, clay), B brow + orbit (station shape board, 3/4, brow-lid close-ups,
# brow-bone clay, groomed real material), C anatomical clay, D full-face identity, E deformation GD16 -> GD17, F engine validation.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD17_Identity_20261010; G=Saved/Codex/GD13_Identity_20261009; S16=Saved/Codex/GD16_Identity_20261010
O=$W/bd/final; P=$W/bd/parts; mkdir -p $O $P; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
LB=Tools/CharacterLookdev_20260930/lk_board.py; REFP=SourceAssets/Characters/GD13_IdentityMaster_20261009/references
zoom() { "$B" -b --factory-startup --python "$(Wp $G/tools/gd13_zoom.py)" -- "$(Wp $1)" $2 $3 $4 $5 $6 $7 "${@:8}" 2>&1 | grep -c ZOOM_OK >/dev/null; }
vstack() { local o=$1 w=$2; shift 2; local A=(); for f in "$@"; do A+=("$(Wp $f)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd17_vstack.py)" -- "$(Wp $o)" $w "${A[@]}" 2>&1 | grep -c VSTACK >/dev/null; }
# ---- Blender clay (solved reference cameras, soft light A + side light B) for both post-rig meshes
for t in G16M:head_g16_postrig G17M:head_g17_postrig; do bash $W/tools/gd17_rset.sh $W/data/${t#*:}.npy ${t%%:*} $W/data/Ec_cams.json "REF_front:clay:A REF_q3_faceL:clay:A REF_q3_faceR:clay:A REF_prof_faceL:clay:A REF_front:clay:B REF_q3_faceL:clay:B REF_q3_faceR:clay:B REF_prof_faceL:clay:B" >/dev/null 2>&1; done
bash $W/tools/gd17_measnose.sh g17_postrig | grep -v "PROFLINE G15"
# ---- A nose
for r in "front 400 360 620 660 front" "q3L 60 360 400 660 q3_faceL" "q3R 560 360 900 660 q3_faceR" "prof 0 340 380 640 prof_faceL"; do set -- $r
  zoom $P/A1_$1.jpg $2 $3 $4 $5 1.25 $6 $W/ue/g16B_refnh_$6.png $W/ue/cg17c4_refnh_$6.png
  zoom $P/A4_$1_A.jpg $2 $3 $4 $5 1.25 $6 $W/r/G16M_REF_${6}_clayA.png $W/r/G17M_REF_${6}_clayA.png
  zoom $P/A4_$1_B.jpg $2 $3 $4 $5 1.25 $6 $W/r/G16M_REF_${6}_clayB.png $W/r/G17M_REF_${6}_clayB.png; done
vstack $O/A1_BURUN_YAKIN_REF_GD16_GD17.jpg 1500 $P/A1_front.jpg $P/A1_q3L.jpg $P/A1_q3R.jpg $P/A1_prof.jpg
vstack $O/A4_BURUN_KIL_YUMUSAK_ve_YAN_ISIK.jpg 1500 $P/A4_front_A.jpg $P/A4_prof_A.jpg $P/A4_q3L_B.jpg $P/A4_prof_B.jpg
"$B" -b --factory-startup --python "$(Wp $W/tools/gd17_profline.py)" -- "$(Wp $REFP/GD13_REF_panel_prof_faceL.png)" "$(Wp $O/A2_BURUN_PROFIL_CIZGILERI.jpg)" "$(Wp $W/meas/profline_final.json)" "GD16=$(Wp $S16/meas/g16_postrig_dumpF.json)" "GD17=$(Wp $W/meas/g17_postrig_dumpF.json)" 2>&1 | grep PROFLINE | cut -c1-300
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_A3.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for L in ('g16B', 'cg17c4'):
    for v, rc in (('prof_faceR', [620, 520, 1180, 1060]), ('prof_faceL', [420, 520, 980, 1060]), ('front', [520, 480, 1080, 1060]), ('q3_faceL', [460, 480, 1020, 1060])):
        f = f'{U}/{L}_commonnh_{v}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=360, out=f'{P}/A3_{L}_{v}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_A3.json)" 2>&1 | grep -c PARTS_OK >/dev/null
r1=""; r2=""; for v in prof_faceR prof_faceL front q3_faceL; do r1="${r1:+$r1, }$(Wp $P/A3_g16B_$v.jpg)|GD16 $v"; r2="${r2:+$r2, }$(Wp $P/A3_cg17c4_$v.jpg)|GD17 $v"; done
"$PY" $LB "$(Wp $O/A3_BURUN_ORTAK_KAMERA_SAG_PROFIL.jpg)" "A3 Burun - sabit ortak kameralar (150 cm - fov 15 - ayni lens): sag profil (referansta yok - anatomik kontrol) / sol profil / on / 3-4" 360 "$r1" "$r2" | tail -c 40
# ---- B brow + orbit
"$B" -b --factory-startup --python "$(Wp $W/tools/gd17_browstations.py)" -- "$(Wp $REFP/GD13_REF_panel_front.png)" "$(Wp $W/data/brow_stations_v2.json)" "$(Wp $O/B1_KAS_ISTASYONLARI_REF_GD16_GD17.jpg)" "GD16=$(Wp $W/ue/g16B_refnh_front.png)" "GD17=$(Wp $W/ue/cg17c4_refnh_front.png)" 2>&1 | grep -c BROWSTATIONS >/dev/null
for r in "front 300 300 720 500 front" "q3L 60 270 520 500 q3_faceL" "q3R 420 270 900 500 q3_faceR"; do set -- $r
  zoom $P/B2_$1.jpg $2 $3 $4 $5 1.0 $6 $W/ue/g16B_refnh_$6.png $W/ue/cg17c4_refnh_$6.png
  zoom $P/B5_$1.jpg $2 $3 $4 $5 1.0 $6 $W/ue/g16B_ref_$6.png $W/ue/cg17c4_ref_$6.png; done
vstack $O/B2_KAS_ON_ve_3_4_REF_GD16_GD17.jpg 1500 $P/B2_front.jpg $P/B2_q3L.jpg $P/B2_q3R.jpg
vstack $O/B5_KAS_GROOMLU_SACLI_GERCEK.jpg 1500 $P/B5_front.jpg $P/B5_q3L.jpg $P/B5_q3R.jpg
for r in "front 280 280 740 520 front" "q3L 40 260 520 520 q3_faceL" "q3R 440 260 920 520 q3_faceR" "prof 0 240 400 520 prof_faceL"; do set -- $r
  zoom $P/B4_$1_A.jpg $2 $3 $4 $5 1.0 $6 $W/r/G16M_REF_${6}_clayA.png $W/r/G17M_REF_${6}_clayA.png
  zoom $P/B4_$1_B.jpg $2 $3 $4 $5 1.0 $6 $W/r/G16M_REF_${6}_clayB.png $W/r/G17M_REF_${6}_clayB.png; done
vstack $O/B4_KAS_KEMIGI_ORBITA_KIL.jpg 1500 $P/B4_front_A.jpg $P/B4_q3L_A.jpg $P/B4_q3R_A.jpg $P/B4_prof_A.jpg $P/B4_q3L_B.jpg $P/B4_q3R_B.jpg
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_B3.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for L in ('g16B', 'cg17c4'):
    for k in ('brow_front', 'eyes_front', 'eyes_q3'):
        f = f'{U}/{L}_close_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=[0, 300, 1600, 1300], w=520, out=f'{P}/B3_{L}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_B3.json)" 2>&1 | grep -c PARTS_OK >/dev/null
rows=(); for k in brow_front eyes_front eyes_q3; do rows+=("$(Wp $P/B3_g16B_$k.jpg)|GD16 $k, $(Wp $P/B3_cg17c4_$k.jpg)|GD17 $k"); done
"$PY" $LB "$(Wp $O/B3_KAS_KAPAK_YAKIN_UE.jpg)" "B3 Kas - kapak iliskisi - UE yakin kameralar (ayni lens - ayni isik - ayni cilt/iris): GD16 | GD17" 520 "${rows[@]}" | tail -c 40
# ---- C anatomical clay
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_C1.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
CR = {'front': [380, 200, 1220, 1360], 'q3_faceR': [400, 200, 1240, 1360], 'q3_faceL': [360, 200, 1200, 1360], 'prof_faceL': [320, 200, 1160, 1360], 'prof_faceR': [440, 200, 1280, 1360]}
for L in ('g16B', 'cg17c4'):
    for v, rc in CR.items():
        for lt in ('studio', 'front'):
            f = f'{U}/{L}_clay_{v}_{lt}_custom.png'
            if os.path.exists(f): S.append(dict(src=f, rect=rc, w=340, out=f'{P}/C1_{L}_{v}_{lt}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_C1.json)" 2>&1 | grep -c PARTS_OK >/dev/null
rows=(); for lt in studio front; do for L in g16B cg17c4; do nm=$([ $L = cg17c4 ] && echo GD17 || echo GD16); r=""; for v in front q3_faceR q3_faceL prof_faceL prof_faceR; do r="${r:+$r, }$(Wp $P/C1_${L}_${v}_${lt}.jpg)|$nm $v $lt"; done; rows+=("$r"); done; done
"$PY" $LB "$(Wp $O/C1_ANATOMIK_KIL_UE_5ACI_2ISIK.jpg)" "C1 Anatomik kil - UE riglenmis geometri (kas/kirpik/sac gizli) - 5 aci x 2 isik (studyo / on) - GD16 ve GD17 ayni kamera" 340 "${rows[@]}" | tail -c 40
WD=320 bash $W/tools/gd17_claycmp.sh final/C2_KIL_BLENDER_YUMUSAK_ISIK.jpg "C2 Kil (Blender - ayni cozulmus kameralar - yumusak isik A): REF / GD16 / GD17" clayA G16M G17M >/dev/null
WD=320 bash $W/tools/gd17_claycmp.sh final/C3_KIL_BLENDER_YAN_ISIK.jpg "C3 Kil (Blender - guclu yan form isigi B): REF / GD16 / GD17" clayB G16M G17M >/dev/null
# ---- D full face identity, same skin / iris / hair / light / camera
WD=330 bash $W/tools/gd17_uecmp.sh final/D1_TAM_YUZ_ONISIK_SACSIZ.jpg "D1 Tam yuz - ayni cilt - iris - isik - cozulmus referans kameralari - sacsiz: REF / GD16 / GD17" refnh g16B cg17c4 >/dev/null
WD=330 bash $W/tools/gd17_uecmp.sh final/D2_TAM_YUZ_ONISIK_SACLI.jpg "D2 Tam yuz - h75c sac ile: REF / GD16 / GD17" ref g16B cg17c4 >/dev/null
WD=330 bash $W/tools/gd17_uecmp.sh final/D3_TAM_YUZ_STUDYO.jpg "D3 Tam yuz - studyo isigi (form) - sacsiz: REF / GD16 / GD17" refnh g16BS cg17c4S >/dev/null
VIEWS="front" COMMON=1 CSET=commonnh WD=300 bash $W/tools/gd17_uecmp.sh final/D4_ORTAK_KAMERA.jpg "D4 Sabit ortak kameralar (adaya gore ayar yok): GD16 / GD17" refnh g16B cg17c4 >/dev/null
# ---- E deformation GD16 -> GD17
"$B" -b "$(Wp $G/GD13_scene.blend)" --python "$(Wp $W/tools/gd17_dispmap.py)" -- "$(Wp $W/data/head_g17_postrig.npy)" "$(Wp $W/data/head_g16_postrig.npy)" "$(Wp $W/r/DM_G17_vsG16)" 3 2>&1 | grep DISPMAP
e1=""; e2=""; for c in front q3R q3L profL profR top back; do e1="${e1:+$e1, }$(Wp $W/r/DM_G17_vsG16_dsigned_$c.png)|isaretli $c"; e2="${e2:+$e2, }$(Wp $W/r/DM_G17_vsG16_dmag_$c.png)|buyukluk $c"; done
"$PY" $LB "$(Wp $O/E_DEFORMASYON_GD16_GD17.jpg)" "E 3B deformasyon GD16 G16 -> GD17 G17 (riglenmis meshler). Isaretli: kirmizi = disari - mavi = iceri (+-3 mm); buyukluk: siyah 0 -> sari 3 mm" 300 "$e1" "$e2" | tail -c 40
# ---- F engine validation
NCOL=6 WD=280 bash $W/tools/gd17_exprboard.sh cg17c4 F1_RIG_IFADE_TESTI.jpg "F1 GD17 yuz rigi (otomatik rig DNA) - RigLogic kontrol testleri - on isik - sac gizli" >/dev/null; mv $W/bd/F1_RIG_IFADE_TESTI.jpg $O/ 2>/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_F2.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for c in ('neutral', 'blink', 'blink_left', 'look_down', 'look_up', 'brows_up', 'brows_down', 'smile', 'frown', 'extreme'):
    for k, rc in (('front', [420, 380, 1180, 820]), ('q3', [440, 380, 1200, 820])):
        f = f'{U}/cg17c4_expr_{c}_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=560, out=f'{P}/F2_{c}_{k}.jpg'))
for n in (0, 1, 2, 3):
    for k in ('front', 'q3'):
        for nm in (f'cg17c4_lod_{n}_{k}_custom.png', f'cg17c4_lod{n}_{k}_custom.png'):
            f = f'{U}/{nm}'
            if os.path.exists(f): S.append(dict(src=f, rect=[380, 120, 1220, 1300], w=340, out=f'{P}/F3_lod{n}_{k}.jpg')); break
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_F2.json)" 2>&1 | grep -c PARTS_OK >/dev/null
A=(); for c in neutral blink blink_left look_down look_up brows_up brows_down smile frown extreme; do for k in front q3; do A+=("$(Wp $P/F2_${c}_$k.jpg)"); done; done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd17_grid.py)" -- "$(Wp $O/F2_KAS_KAPAK_IFADE_YAKIN.jpg)" 4 560 "${A[@]}" 2>&1 | grep -c GRID >/dev/null
r1=""; r2=""; for n in 0 1 2 3; do r1="${r1:+$r1, }$(Wp $P/F3_lod${n}_front.jpg)|LOD$n on"; r2="${r2:+$r2, }$(Wp $P/F3_lod${n}_q3.jpg)|LOD$n 3/4"; done
"$PY" $LB "$(Wp $O/F3_LOD_0_3.jpg)" "F3 GD17 LOD 0-3 (tum bilesenlerde zorlanmis LOD - groom LOD otomatik - sac ve ozel kas gorunur)" 340 "$r1" "$r2" | tail -c 40
# ---- G GD17 regional close-ups (UE close cams, fov 5-5.5, front light, same lens): real material + clay (hair/brow/lash hidden)
# GD16 = g16B (GD16 own look s1t5), GD17 = cg17c4 (s1t6n). Candidates (quick-bake LOD0 evaluation, same cams): E = CH2 chin, F = CH1 chin, G = CH3 chin (chosen)
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_G.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for L in ('g16B', 'cg17c4', 'g16X', 'cg17ec4', 'cg17fc4', 'cg17gT', 'g15X'):
    for s in ('close', 'closeclay'):
        for k in ('nose_front', 'nose_prof', 'mouth_front', 'mouth_q3', 'chin_prof', 'chin_q3'):
            f = f'{U}/{L}_{s}_{k}_custom.png'
            if os.path.exists(f): S.append(dict(src=f, rect=[160, 160, 1440, 1440], w=420, out=f'{P}/G_{L}_{s}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_G.json)" 2>&1 | grep -c PARTS_OK >/dev/null
for grp in "G1_BURUN_YAKIN_GERCEK_ve_KIL:nose_front nose_prof" "G2_DUDAK_YAKIN_GERCEK_ve_KIL:mouth_front mouth_q3" "G3_CENE_YAKIN_GERCEK_ve_KIL:chin_prof chin_q3"; do
  nm=${grp%%:*}; rows=()
  for k in ${grp#*:}; do rows+=("$(Wp $P/G_g16B_close_$k.jpg)|GD16 gercek $k, $(Wp $P/G_cg17c4_close_$k.jpg)|GD17 gercek $k, $(Wp $P/G_g16B_closeclay_$k.jpg)|GD16 kil $k, $(Wp $P/G_cg17c4_closeclay_$k.jpg)|GD17 kil $k"); done
  "$PY" $LB "$(Wp $O/$nm.jpg)" "${nm%%_*} UE yakin plan (ayni kamera - ayni on isik): GD16 gercek | GD17 gercek | GD16 kil | GD17 kil (sac-kas-kirpik gizli)" 420 "${rows[@]}" | tail -c 40; done
rows=(); for k in nose_front nose_prof mouth_front chin_prof chin_q3; do rows+=("$(Wp $P/G_g16X_closeclay_$k.jpg)|GD16 $k, $(Wp $P/G_cg17ec4_closeclay_$k.jpg)|E (CH2) $k, $(Wp $P/G_cg17fc4_closeclay_$k.jpg)|F (CH1) $k, $(Wp $P/G_cg17c4_closeclay_$k.jpg)|GD17 = G (CH3) $k"); done
"$PY" $LB "$(Wp $O/G4_ADAYLAR_KIL.jpg)" "G4 Adaylar - kil yakin plan (ayni kamera/isik): GD16 | E | F | G = secilen GD17. E/F hizli-bake LOD0, GD17 tam fit+rig" 360 "${rows[@]}" | tail -c 40
ls $O
