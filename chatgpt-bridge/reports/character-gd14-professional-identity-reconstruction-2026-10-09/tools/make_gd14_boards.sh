#!/bin/bash
# make_gd14_boards.sh <final tag e.g. w8> : GD14 report boards A-F into bd/final/ (all images = real captures / renders of the actual geometry)
# A: identity (UE real material, solved reference cameras warped onto the panel frame; front light; no hair / h75c hair; studio light; fixed common
#    cameras) + Blender clay (same solved cameras); B: UE clay 5 angles x 2 lights; C: regional close-ups (REF | E | GD14, same window);
# D: real-material identity (hair, brows, iris, skin, natural expression); E: deformation maps GD14 vs E incl. cranium; F: rig / expression.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; F=$1; W=Saved/Codex/GD14_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009; T=tools
O=$W/bd/final; mkdir -p $O; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
U=$(echo $F | tr a-z A-Z)
# ---- A
WD=300 bash $W/tools/gd14_uecmp.sh final/A1_KIMLIK_UE_ONISIK_SACSIZ.jpg "A1 Kimlik - UE gercek materyal, cozulmus referans kameralari, on isik, sacsiz: REF / E (taban) / GD12 / GD13 / GD14" refnh w0F cgd12F cgd13F ${F}F >/dev/null
WD=300 bash $W/tools/gd14_uecmp.sh final/A2_KIMLIK_UE_ONISIK_SACLI.jpg "A2 Kimlik - ayni, h75c sac + M_SlightArch kas + S_Thin kirpik: REF / E / GD12 / GD13 / GD14" ref w0F cgd12F cgd13F ${F}F >/dev/null
WD=300 bash $W/tools/gd14_uecmp.sh final/A3_KIMLIK_UE_STUDYO_SACSIZ.jpg "A3 Kimlik - studyo isigi (form): REF / E / GD12 / GD13 / GD14" refnh w0 cgd12S cgd13S ${F}S >/dev/null
VIEWS="front" COMMON=1 CSET=commonnh WD=300 bash $W/tools/gd14_uecmp.sh final/A4_ORTAK_KAMERA_UE.jpg "A4 Sabit ortak kameralar (150 cm, fov 15, ayni lens; kamera modele gore ayarlanmadi): E / GD12 / GD13 / GD14" refnh w0F cgd12F cgd13F ${F}F >/dev/null
bash $W/tools/gd14_rset.sh $W/data/head_${U}_mhc.npy ${U}M $W/data/Ec_cams.json "REF_front:clay:A REF_q3_faceL:clay:A REF_q3_faceR:clay:A REF_prof_faceL:clay:A REF_front:clay:B REF_q3_faceL:clay:B REF_q3_faceR:clay:B REF_prof_faceL:clay:B" >/dev/null 2>&1
WD=300 bash $W/tools/gd14_claycmp.sh final/A5_KIL_BLENDER.jpg "A5 Kil (Blender, ayni cozulmus kameralar, yumusak isik): REF / E / GD12 / GD13 / GD14" clayA E GD12 GD13 ${U}M >/dev/null
# ---- B: UE clay of the rigged candidate, 5 fixed angles x 2 lights
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$W/bd/parts")" "$(cygpath -m "$(pwd)/$W/bd/spec_B.json")" ${F}F <<'PYE'
import json, sys, os
U, P, OUT, L = sys.argv[1:5]; S = []
CR = {'front': [380, 200, 1220, 1360], 'q3_faceR': [400, 200, 1240, 1360], 'q3_faceL': [360, 200, 1200, 1360], 'prof_faceL': [320, 200, 1160, 1360], 'prof_faceR': [440, 200, 1280, 1360]}
for v, rc in CR.items():
    for lt in ('studio', 'front'):
        f = f'{U}/{L}_clay_{v}_{lt}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=420, out=f'{P}/B_{v}_{lt}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_B.json)" 2>&1 | grep -c PARTS_OK >/dev/null
P=$W/bd/parts; r1=""; r2=""; for v in front q3_faceR q3_faceL prof_faceL prof_faceR; do r1="${r1:+$r1, }$(Wp $P/B_${v}_studio.jpg)|$v studyo (anahtar+dolgu+kontur)"; r2="${r2:+$r2, }$(Wp $P/B_${v}_front.jpg)|$v on isik"; done
"$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(Wp $O/B_ANATOMIK_KIL_5ACI_2ISIK.jpg)" "B Anatomik kil - GD14 (UE, riglenmis aday geometrisi, kas/kirpik/sac gizli): 5 aci x 2 isik" 420 "$r1" "$r2" | tail -c 40
# ---- C: regional close-ups, same window in REF / E / GD14 (warped solved-camera captures, front light, no hair; brow row WITH grooms)
"$PY" - "$(cygpath -m "$(pwd)/$W/data/zoomwin.json")" <<'PYE' > $W/bd/_zoomjobs.txt
import json, sys
Z = json.load(open(sys.argv[1]))
for reg, view, st in (('eye', 'front', 'refnh'), ('eye', 'q3_faceR', 'refnh'), ('brow', 'front', 'ref'), ('brow', 'q3_faceL', 'ref'), ('cheek', 'q3_faceR', 'refnh'), ('cheek', 'q3_faceL', 'refnh'),
                      ('nose', 'front', 'refnh'), ('nose', 'prof_faceL', 'refnh'), ('lips', 'front', 'refnh'), ('lips', 'q3_faceL', 'refnh'), ('chin', 'front', 'refnh'), ('chin', 'prof_faceL', 'refnh')):
    x0, y0, x1, y1 = Z[view][reg]; print(reg, view, st, x0, y0, x1, y1)
PYE
rows=(); while read reg view st x0 y0 x1 y1; do sc=$("$PY" -c "print(round(min(2.4, 560/($x1-$x0)), 2))"); o=$W/bd/parts/C_${reg}_${view}.jpg
  "$B" -b --factory-startup --python "$(Wp $G/tools/gd13_zoom.py)" -- "$(Wp $o)" $x0 $y0 $x1 $y1 $sc $view "$(Wp $W/ue/w0F_${st}_${view}.png)" "$(Wp $W/ue/${F}F_${st}_${view}.png)" 2>&1 | grep -c ZOOM_OK >/dev/null
  done < $W/bd/_zoomjobs.txt
A=(); for r in eye_front eye_q3_faceR brow_front brow_q3_faceL cheek_q3_faceR cheek_q3_faceL; do A+=("$(Wp $W/bd/parts/C_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd14_vstack.py)" -- "$(Wp $O/C_YAKIN_PLANLAR_1.jpg)" 1500 "${A[@]}" 2>&1 | grep -cE "VSTACK|GRID"
A=(); for r in nose_front nose_prof_faceL lips_front lips_q3_faceL chin_front chin_prof_faceL; do A+=("$(Wp $W/bd/parts/C_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd14_vstack.py)" -- "$(Wp $O/C_YAKIN_PLANLAR_2.jpg)" 1500 "${A[@]}" 2>&1 | grep -cE "VSTACK|GRID"
# ---- D: real-material identity (hair + brows + lashes + iris + x19a skin), large; plus UE close-up camera set of the candidate
WD=560 VIEWS="front q3_faceR q3_faceL prof_faceL" bash $W/tools/gd14_uecmp.sh final/D1_GERCEK_MATERYAL_KIMLIK.jpg "D1 Gercek materyal kimlik - x19a cilt + cil, e3n iris, M_SlightArch kas, S_Thin kirpik, h75c sac; dogal notr ifade: REF / GD14" ref ${F}F >/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$W/bd/parts")" "$(cygpath -m "$(pwd)/$W/bd/spec_D2.json")" ${F}F <<'PYE'
import json, sys, os
U, P, OUT, L = sys.argv[1:5]; S = []
for k in ('eyes_front', 'eyes_q3', 'brow_front', 'cheek_q3', 'nose_front', 'nose_prof', 'mouth_front', 'mouth_q3', 'chin_prof', 'chin_q3'):
    f = f'{U}/{L}_close_{k}_custom.png'
    if os.path.exists(f): S.append(dict(src=f, rect=[0, 250, 1600, 1350], w=560, out=f'{P}/D2_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_D2.json)" 2>&1 | grep -c PARTS_OK >/dev/null
D=(); for k in eyes_front eyes_q3 brow_front cheek_q3 nose_front nose_prof mouth_front mouth_q3 chin_prof chin_q3; do D+=("$(Wp $P/D2_$k.jpg)|$k"); done
A=(); for r in eyes_front eyes_q3 brow_front cheek_q3 nose_front nose_prof mouth_front mouth_q3 chin_prof chin_q3; do A+=("$(Wp $P/D2_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd14_grid.py)" -- "$(Wp $O/D2_GERCEK_MATERYAL_YAKIN.jpg)" 2 700 "${A[@]}" 2>&1 | grep -cE "VSTACK|GRID"
# ---- E: deformation maps GD14 vs E (incl. cranium top / back)
"$B" -b "$(Wp $G/GD13_scene.blend)" --python "$(Wp $W/tools/gd14_dispmap.py)" -- "$(Wp $W/data/head_${U}_mhc.npy)" "$(Wp $W/data/head_E.npy)" "$(Wp $W/r/DM_${U}_vsE)" 3 2>&1 | grep DISPMAP
e1=""; e2=""; for c in front q3R q3L profL profR top back; do e1="${e1:+$e1, }$(Wp $W/r/DM_${U}_vsE_dsigned_$c.png)|isaretli $c"; e2="${e2:+$e2, }$(Wp $W/r/DM_${U}_vsE_dmag_$c.png)|buyukluk $c"; done
"$PY" Tools/CharacterLookdev_20260930/lk_board.py "$(Wp $O/E_DEFORMASYON_HARITALARI.jpg)" "E 3B deformasyon: GD14 - E (taban). Isaretli: kirmizi = disari/dolgun, mavi = iceri (+-3 mm); buyukluk: siyah 0 -> sari 3 mm. Ust/arka = kafatasi" 300 "$e1" "$e2" | tail -c 40
# ---- F: facial rig / expression (RigLogic controls) + blink lid close-ups
NCOL=6 WD=280 bash $W/tools/gd14_exprboard.sh ${F}F F1_RIG_IFADE_TESTI.jpg "F1 GD14 yuz rigi (otomatik rig DNA, 858 morph) - RigLogic kontrol testleri, on isik, sac gizli" >/dev/null; mv $W/bd/F1_RIG_IFADE_TESTI.jpg $O/
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$W/bd/parts")" "$(cygpath -m "$(pwd)/$W/bd/spec_F2.json")" ${F}F <<'PYE'
import json, sys, os
U, P, OUT, L = sys.argv[1:5]; S = []
for c in ('neutral', 'blink', 'blink_left', 'look_down', 'look_up', 'smile', 'cheek_compress', 'extreme'):
    for k, rc in (('front', [500, 560, 1100, 820]), ('q3', [520, 560, 1120, 820])):
        f = f'{U}/{L}_expr_{c}_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=600, out=f'{P}/F2_{c}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_F2.json)" 2>&1 | grep -c PARTS_OK >/dev/null
f2=(); for c in neutral blink blink_left look_down look_up smile cheek_compress extreme; do f2+=("$(Wp $P/F2_${c}_front.jpg)|$c on, $(Wp $P/F2_${c}_q3.jpg)|$c 3/4"); done
A=(); for r in neutral_front neutral_q3 blink_front blink_q3 blink_left_front blink_left_q3 look_down_front look_down_q3 look_up_front look_up_q3 smile_front smile_q3 cheek_compress_front cheek_compress_q3 extreme_front extreme_q3; do A+=("$(Wp $P/F2_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd14_grid.py)" -- "$(Wp $O/F2_GOZ_KAPAGI_KIRPMA.jpg)" 4 600 "${A[@]}" 2>&1 | grep -cE "VSTACK|GRID"
ls $O
