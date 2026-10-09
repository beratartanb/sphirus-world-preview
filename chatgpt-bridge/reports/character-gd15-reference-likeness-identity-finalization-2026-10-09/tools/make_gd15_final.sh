#!/bin/bash
# make_gd15_final.sh : GD15 report boards A-F into bd/final/ - every image is a real capture / render of the actual geometry (no paint-over).
# labels: g15F / g15S = GD15 final (rigged G15, reference look, front / studio light); w9B / w9BS = GD14 W9 with the SAME reference look;
#         aW9 = GD14 W9 with its old look (x19a, e3n, M_SlightArch, h75c); clay / expr / lod / close sets from gd15_caps.sh
# A identity (same light + material: REF / W9 / GD15), B material effect (W9 old look / W9 ref look / GD15 ref look), C anatomical clay
# (UE 5 angles x 2 lights + Blender solved-camera clay), D regional close-ups, E deformation W9 -> GD15, F engine validation (rig, blink, LOD)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; W=Saved/Codex/GD15_Identity_20261009; G=Saved/Codex/GD13_Identity_20261009
O=$W/bd/final; P=$W/bd/parts; mkdir -p $O $P; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; Wp() { cygpath -w "$(pwd)/$1"; }
LB=Tools/CharacterLookdev_20260930/lk_board.py
# ---- A identity, same light and material
WD=340 bash $W/tools/gd15_uecmp.sh final/A1_KIMLIK_ONISIK_SACSIZ.jpg "A1 Kimlik - ayni isik ve materyal (referans lookdev) - cozulmus referans kameralari - on isik - sacsiz: REF / GD14 W9 / GD15" refnh w9B g15F >/dev/null
WD=340 bash $W/tools/gd15_uecmp.sh final/A2_KIMLIK_ONISIK_SACLI.jpg "A2 Kimlik - ayni - h75c sac + kas + kirpik: REF / GD14 W9 / GD15" ref w9B g15F >/dev/null
WD=340 bash $W/tools/gd15_uecmp.sh final/A3_KIMLIK_STUDYO_SACSIZ.jpg "A3 Kimlik - studyo isigi (form okuma) - sacsiz: REF / GD14 W9 / GD15" refnh w9BS g15S >/dev/null
VIEWS="front" COMMON=1 CSET=commonnh WD=300 bash $W/tools/gd15_uecmp.sh final/A4_ORTAK_KAMERA.jpg "A4 Sabit ortak kameralar (150 cm - fov 15 - ayni lens; adaya gore ayar yok): GD14 W9 / GD15" refnh w9B g15F >/dev/null
# ---- B material effect: old look vs reference look on W9, and GD15 with the reference look
WD=300 bash $W/tools/gd15_uecmp.sh final/B1_MATERYAL_ETKISI_SACLI.jpg "B1 Materyal etkisi - REF / GD14 W9 eski lookdev / GD14 W9 referans lookdev / GD15 referans lookdev (W9 iki sutunu = ayni geometri)" ref aW9 w9B g15F >/dev/null
WD=300 bash $W/tools/gd15_uecmp.sh final/B2_MATERYAL_ETKISI_SACSIZ.jpg "B2 Materyal etkisi - sacsiz: REF / W9 eski / W9 referans lookdev / GD15 referans lookdev" refnh aW9 w9B g15F >/dev/null
# ---- C anatomical clay: UE clay 5 angles x 2 lights (GD15 and W9 rows), Blender clay in the solved reference cameras
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_C1.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
CR = {'front': [380, 200, 1220, 1360], 'q3_faceR': [400, 200, 1240, 1360], 'q3_faceL': [360, 200, 1200, 1360], 'prof_faceL': [320, 200, 1160, 1360], 'prof_faceR': [440, 200, 1280, 1360]}
for L in ('g15F', 'w9B'):
    for v, rc in CR.items():
        for lt in ('studio', 'front'):
            f = f'{U}/{L}_clay_{v}_{lt}_custom.png'
            if os.path.exists(f): S.append(dict(src=f, rect=rc, w=360, out=f'{P}/C1_{L}_{v}_{lt}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_C1.json)" 2>&1 | grep -c PARTS_OK >/dev/null
rows=(); for lt in studio front; do for L in w9B g15F; do nm=$([ $L = g15F ] && echo GD15 || echo "GD14 W9"); r=""; for v in front q3_faceR q3_faceL prof_faceL prof_faceR; do r="${r:+$r, }$(Wp $P/C1_${L}_${v}_${lt}.jpg)|$nm $v $lt"; done; rows+=("$r"); done; done
"$PY" $LB "$(Wp $O/C1_ANATOMIK_KIL_UE_5ACI_2ISIK.jpg)" "C1 Anatomik kil - UE riglenmis geometri (kas/kirpik/sac gizli) - 5 aci x 2 isik (studyo / on) - GD14 W9 ve GD15 ayni kamera" 360 "${rows[@]}" | tail -c 40
bash $W/tools/gd15_rset.sh $W/data/head_w9_postrig.npy W9fin $W/data/Ec_cams.json "REF_front:clay:A REF_q3_faceL:clay:A REF_q3_faceR:clay:A REF_prof_faceL:clay:A REF_front:clay:B REF_q3_faceL:clay:B REF_q3_faceR:clay:B REF_prof_faceL:clay:B" >/dev/null 2>&1
bash $W/tools/gd15_rset.sh $W/data/head_g15_postrig.npy G15M $W/data/Ec_cams.json "REF_front:clay:A REF_q3_faceL:clay:A REF_q3_faceR:clay:A REF_prof_faceL:clay:A REF_front:clay:B REF_q3_faceL:clay:B REF_q3_faceR:clay:B REF_prof_faceL:clay:B" >/dev/null 2>&1
WD=340 bash $W/tools/gd15_claycmp.sh final/C2_KIL_BLENDER_ISIK_A.jpg "C2 Kil (Blender - ayni cozulmus kameralar - yumusak isik A): REF / GD14 W9 / GD15" clayA W9fin G15M >/dev/null
WD=340 bash $W/tools/gd15_claycmp.sh final/C3_KIL_BLENDER_ISIK_B.jpg "C3 Kil (Blender - isik B - yan/ust): REF / GD14 W9 / GD15" clayB W9fin G15M >/dev/null
# ---- D regional close-ups: same window in REF / W9 / GD15 (solved-camera captures warped onto the panel frame, front light)
"$PY" - "$(cygpath -m "$(pwd)/$W/data/zoomwin.json")" <<'PYE' > $W/bd/_zoomjobs15.txt
import json, sys
Z = json.load(open(sys.argv[1]))
for reg, view, st in (('eye', 'front', 'refnh'), ('eye', 'q3_faceR', 'refnh'), ('eye', 'q3_faceL', 'refnh'), ('brow', 'front', 'ref'), ('brow', 'q3_faceL', 'ref'),
                      ('cheek', 'q3_faceR', 'refnh'), ('cheek', 'q3_faceL', 'refnh'), ('nose', 'front', 'refnh'), ('nose', 'prof_faceL', 'refnh'), ('nose', 'q3_faceL', 'refnh'),
                      ('lips', 'front', 'refnh'), ('lips', 'q3_faceL', 'refnh'), ('lips', 'prof_faceL', 'refnh'), ('chin', 'front', 'refnh'), ('chin', 'prof_faceL', 'refnh')):
    x0, y0, x1, y1 = Z[view][reg]; print(reg, view, st, x0, y0, x1, y1)
PYE
while read reg view st x0 y0 x1 y1; do sc=$("$PY" -c "print(round(min(2.4, 520/($x1-$x0)), 2))"); o=$P/D_${reg}_${view}.jpg
  "$B" -b --factory-startup --python "$(Wp $G/tools/gd13_zoom.py)" -- "$(Wp $o)" $x0 $y0 $x1 $y1 $sc $view "$(Wp $W/ue/w9B_${st}_${view}.png)" "$(Wp $W/ue/g15F_${st}_${view}.png)" 2>&1 | grep -c ZOOM_OK >/dev/null
done < $W/bd/_zoomjobs15.txt
A=(); for r in eye_front eye_q3_faceR eye_q3_faceL brow_front brow_q3_faceL cheek_q3_faceR cheek_q3_faceL; do A+=("$(Wp $P/D_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd15_vstack.py)" -- "$(Wp $O/D1_YAKIN_GOZ_KAS_ORBITA_YANAK.jpg)" 1560 "${A[@]}" 2>&1 | grep -c VSTACK >/dev/null
A=(); for r in nose_front nose_q3_faceL nose_prof_faceL lips_front lips_q3_faceL lips_prof_faceL chin_front chin_prof_faceL; do A+=("$(Wp $P/D_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd15_vstack.py)" -- "$(Wp $O/D2_YAKIN_BURUN_DUDAK_CENE_PROFIL.jpg)" 1560 "${A[@]}" 2>&1 | grep -c VSTACK >/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_D3.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for L in ('w9B', 'g15F'):
    for k in ('eyes_front', 'eyes_q3', 'brow_front', 'cheek_q3', 'nose_front', 'nose_prof', 'mouth_front', 'mouth_q3', 'chin_prof', 'chin_q3'):
        f = f'{U}/{L}_close_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=[0, 250, 1600, 1350], w=480, out=f'{P}/D3_{L}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_D3.json)" 2>&1 | grep -c PARTS_OK >/dev/null
rows=(); for k in eyes_front eyes_q3 brow_front cheek_q3 nose_front nose_prof mouth_front mouth_q3 chin_prof chin_q3; do rows+=("$(Wp $P/D3_w9B_$k.jpg)|GD14 W9 $k, $(Wp $P/D3_g15F_$k.jpg)|GD15 $k"); done
"$PY" $LB "$(Wp $O/D3_UE_YAKIN_KAMERALAR.jpg)" "D3 UE yakin kameralar (ayni lens - ayni isik - ayni lookdev): GD14 W9 | GD15" 480 "${rows[@]}" | tail -c 40
# ---- E deformation GD14 W9 -> GD15 (post-rig meshes; signed along the W9 normal + magnitude; cranium views included)
"$B" -b "$(Wp $G/GD13_scene.blend)" --python "$(Wp $W/tools/gd15_dispmap.py)" -- "$(Wp $W/data/head_g15_postrig.npy)" "$(Wp $W/data/head_w9_postrig.npy)" "$(Wp $W/r/DM_G15_vsW9)" 3 2>&1 | grep DISPMAP
e1=""; e2=""; for c in front q3R q3L profL profR top back; do e1="${e1:+$e1, }$(Wp $W/r/DM_G15_vsW9_dsigned_$c.png)|isaretli $c"; e2="${e2:+$e2, }$(Wp $W/r/DM_G15_vsW9_dmag_$c.png)|buyukluk $c"; done
"$PY" $LB "$(Wp $O/E_DEFORMASYON_W9_GD15.jpg)" "E 3B deformasyon GD14 W9 -> GD15 (riglenmis meshler). Isaretli: kirmizi = disari/dolgun - mavi = iceri (+-3 mm); buyukluk: siyah 0 -> sari 3 mm" 300 "$e1" "$e2" | tail -c 40
# ---- F engine validation: RigLogic expression cases, blink / lid close-ups, LOD 0..3
NCOL=6 WD=280 bash $W/tools/gd15_exprboard.sh g15F F1_RIG_IFADE_TESTI.jpg "F1 GD15 yuz rigi (otomatik rig DNA) - RigLogic kontrol testleri - on isik - sac gizli" >/dev/null; mv $W/bd/F1_RIG_IFADE_TESTI.jpg $O/ 2>/dev/null
"$PY" - "$(cygpath -m "$(pwd)/$W/ue")" "$(cygpath -m "$(pwd)/$P")" "$(cygpath -m "$(pwd)/$W/bd/spec_F2.json")" <<'PYE'
import json, sys, os
U, P, OUT = sys.argv[1:4]; S = []
for c in ('neutral', 'blink', 'blink_left', 'look_down', 'look_up', 'smile', 'cheek_compress', 'extreme'):
    for k, rc in (('front', [500, 560, 1100, 820]), ('q3', [520, 560, 1120, 820])):
        f = f'{U}/g15F_expr_{c}_{k}_custom.png'
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=600, out=f'{P}/F2_{c}_{k}.jpg'))
for n in (0, 1, 2, 3):
    for k, rc in (('front', [380, 120, 1220, 1300]), ('q3', [380, 120, 1220, 1300])):
        f = f'{U}/g15F_lod{n}_{k}_custom.png' if os.path.exists(f'{U}/g15F_lod{n}_{k}_custom.png') else f'{U}/g15F_lod_{n}_{k}_custom.png'   # first run named lod<n>
        if os.path.exists(f): S.append(dict(src=f, rect=rc, w=360, out=f'{P}/F3_lod{n}_{k}.jpg'))
json.dump(S, open(OUT, 'w')); print(len(S))
PYE
"$B" -b --factory-startup --python "$(Wp $G/tools/gd13_parts.py)" -- "$(Wp $W/bd/spec_F2.json)" 2>&1 | grep -c PARTS_OK >/dev/null
A=(); for r in neutral_front neutral_q3 blink_front blink_q3 blink_left_front blink_left_q3 look_down_front look_down_q3 look_up_front look_up_q3 smile_front smile_q3 cheek_compress_front cheek_compress_q3 extreme_front extreme_q3; do A+=("$(Wp $P/F2_$r.jpg)"); done; "$B" -b --factory-startup --python "$(Wp $W/tools/gd15_grid.py)" -- "$(Wp $O/F2_GOZ_KAPAGI_KIRPMA_IFADE.jpg)" 4 600 "${A[@]}" 2>&1 | grep -c GRID >/dev/null
r1=""; r2=""; for n in 0 1 2 3; do r1="${r1:+$r1, }$(Wp $P/F3_lod${n}_front.jpg)|LOD$n on"; r2="${r2:+$r2, }$(Wp $P/F3_lod${n}_q3.jpg)|LOD$n 3/4"; done
"$PY" $LB "$(Wp $O/F3_LOD_0_3.jpg)" "F3 GD15 LOD 0-3 (tum bilesenlerde zorlanmis LOD - groom LOD otomatik - sac gorunur)" 360 "$r1" "$r2" | tail -c 40
ls $O
