#!/bin/bash
# id_hair_cycle.sh <tag> <face sfx> : IDENTITY-pass hair cycle: build (env hair/<tag>/build_env.txt, builder blender_lk_hair_locks.py on the
# identity scalp) -> preview -> import GR_LK_Hair_{Main,Loose}_<tag> (+ MI) -> hair_grooms.json -> bindings on SKM_ID_FaceMesh_<sfx>
# -> hair captures h<tag> at the reference-solved / profile / back / top cams -> silhouette board
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; TAG=$1; FS=$2; E=Saved/Codex/CharacterLookdev_20260930; I=Saved/Codex/CharacterIdentity_20260930; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
SC="C:/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/53df87b2-1800-4b0d-8cb5-35bc735c40a0/scratchpad"
[ -n "${SKIP_BUILD:-}" ] || env $(grep -v '^$' $E/hair/$TAG/build_env.txt | tr '\n' ' ') "$B" -b --factory-startup --python "$(cygpath -w "$(pwd)/$T/blender_lk_hair_locks.py")" -- "$(cygpath -w "$(pwd)/Saved/Codex/CharacterFinal_20260929/sculpt_package_v6.json.gz")" "$(cygpath -w "$(pwd)/$E/hair/$TAG")" > $E/hair/$TAG/build_log.txt 2>&1
grep -E "HAIR_OK" $E/hair/$TAG/build_log.txt | cut -c1-140 || { echo BUILD_FAIL; tail -5 $E/hair/$TAG/build_log.txt; exit 1; }
D="$(cygpath -w "$(pwd)/$E/hair/$TAG")"
{ echo "import builtins; builtins.RV_HAIR = {'dir': r'$D', 'tag': '$TAG', 'mi': 'MI_LK_Hair_$TAG', 'mat': $(cat ${HAIR_MAT:-$E/hair/hair_mat_v14d.txt}), 'width_main': ${WM:-0.0075}, 'width_loose': ${WL:-0.006}, 'mi_loose': 'MI_LK_HairLoose_$TAG', 'mat_loose': $(cat $E/hair/hair_mat_loose.txt 2>/dev/null || echo '{}')}"; cat $T/ue_lk_hair.py; } > "$SC/lk_hair_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/lk_hair_$TAG.py" lkhair-$TAG 1800 | grep -E "^(OK|ERROR)|Traceback" | head -3
H=/Game/Sphirus/CharacterLab/CharacterLookdev_20260930/Hair; echo "{\"main\": \"$H/GR_LK_Hair_Main_$TAG\", \"loose\": \"$H/GR_LK_Hair_Loose_$TAG\", \"tag\": \"$TAG\"}" > $I/hair_grooms.json
{ echo "import builtins; builtins.FM_BIND = {'face': '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/SKM_ID_FaceMesh_$FS', 'suffix': '$FS', 'prefix': 'GB_ID', 'folder': '/Game/Sphirus/CharacterLab/CharacterIdentity_20260930/Face/Bindings', 'grooms': {'HairMain': '$H/GR_LK_Hair_Main_$TAG', 'HairLoose': '$H/GR_LK_Hair_Loose_$TAG'}}"; cat $T/ue_fm_bind.py; } > "$SC/id_hbind_$TAG.py"
bash Tools/OutfitHome_20260929/run_of.sh "$SC/id_hbind_$TAG.py" id-hbind-$TAG 900 | tail -1 | grep -o '"dirty": \[[^]]*\]'
bash $T/id_face_captures.sh h$TAG $FS id_$TAG hair 2>&1 | grep -E "DONE|ERROR"
O="$(cygpath -m "$(pwd)/$I/gate")"; C="$(cygpath -m "$(pwd)/$E/captures")"; TD="$(cygpath -m "$(pwd)/$I/track")"
RF=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json front 800 960 '[0.95,129.7,170.3,-90.4,-3.8]' 15); RC=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json close 794 940 '[-91.0,88.6,143.3,-42.6,8.6]' 15)
"$B" -b --factory-startup --python $T/id_crop_rect.py -- "$C/h${TAG}_hair_reffront_custom.png|$O/h${TAG}_F.png|${RF}|800|960" "$C/h${TAG}_hair_refclose_custom.png|$O/h${TAG}_C.png|${RC}|794|940" 2>&1 | grep -c RECT
"$B" -b --factory-startup --python $T/id_silhouette.py -- "$TD/ref_front_x4.png|$O/sil_ref_F_$TAG.png|0.07|$O/h${TAG}_F.png" "$TD/ref_close_x2.png|$O/sil_ref_C_$TAG.png|0.07|$O/h${TAG}_C.png" "$C/h${TAG}_hair_side_custom.png|$O/sil_S_$TAG.png|0.07" "$C/h${TAG}_hair_back_custom.png|$O/sil_B_$TAG.png|0.07" 2>&1 | grep -c SIL
"$PY" $T/lk_board.py "$O/_hair_$TAG.jpg" "hair $TAG on id-$FS: silhouette vs reference (black = ref, red = candidate outline, pink = outside ref) + renders" 300 "$O/sil_ref_F_$TAG.png|front sil, $O/sil_ref_C_$TAG.png|3/4 sil, $O/sil_S_$TAG.png|profile sil, $O/sil_B_$TAG.png|back sil" "$TD/ref_front_x4.png|ref, $O/h${TAG}_F.png|front, $TD/ref_close_x2.png|ref, $O/h${TAG}_C.png|3/4" "$C/h${TAG}_hair_side_custom.png|profile, $C/h${TAG}_hair_back_custom.png|back, $C/h${TAG}_hair_top_custom.png|top, $C/h${TAG}_hair_front3q_custom.png|3/4 std" | tail -c 20
