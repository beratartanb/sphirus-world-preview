#!/bin/bash
# make_gd9_boards.sh : GUARDIAN-9 profile-face boards 01-13 -> Saved/Codex/CharacterGuardian9_20261002/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = authority; Tier B turnaround / face-study profile = aid) | GD8 (C8 face + h23: z8f_*) | GD9 (G face + h23: z9f_*).
# Same cameras / lights / FOV per row; no head rotation. Blender clay (pv/b_head_C8_*, pv/b_headG_*) at the Tier A cameras + strict orthographic profile.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian9_20261002; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F8=Saved/Codex/CharacterGuardian8_20261002/frames; F9=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; RP2=$RB/face_study_p4.png
B 01_PROFILE_FULL.jpg "01 PROFILE FULL (strict side camera, studio): Tier B profile (aid) | GD8 | GD9 - real skin, clay, with hair" 440 \
  "$RP|REF profile (aid), $C/z8f_real_side_custom.png|GD8, $C/z9f_real_side_custom.png|GD9, $RP2|REF face study (aid)" \
  "$C/z8f_clay_side_custom.png|GD8 clay, $C/z9f_clay_side_custom.png|GD9 clay, $C/z8f_hair_side_custom.png|GD8 hair, $C/z9f_hair_side_custom.png|GD9 hair"
ROW nose_p.png 0,10000,560,1200 420 $PV/b_head_C8_side_clay.png $PV/b_headG_side_clay.png; ROW nose_c.png 450,720,470,760 420 $RC $PV/b_head_C8_close_clay.png $PV/b_headG_close_clay.png; ROW nose_f.png 420,640,300,530 420 $RF $PV/b_head_C8_front_clay.png $PV/b_headG_front_clay.png
B 02_PROFILE_NOSE.jpg "02 PROFILE NOSE (tip projection from subnasale 1.49 -> 1.64 cm, nasion-tip 4.25 -> 4.56 cm, tip lowered, lower dorsum straightened, lobule fuller, columella lowered): profile / ~33 deg 3/4 / front - REF | GD8 | GD9" 900 "$P/nose_p.png|profile clay GD8 / GD9" "$P/nose_c.png|3/4: REF / GD8 / GD9" "$P/nose_f.png|front: REF / GD8 / GD9"
ROW mid_c.png 380,820,330,794 420 $RC $F8/z8f_real_C.png $F9/z9f_real_C.png; ROW mid_cc.png 380,820,330,794 420 $RC $PV/b_head_C8_close_clay.png $PV/b_headG_close_clay.png
B 03_PROFILE_CHEEKBONE_MIDFACE.jpg "03 CHEEKBONE / MALAR / MIDFACE (malar apex +1.0 mm, anterior cheek +0.9 mm mean, maxilla +0.6 mm - projection / volume only, no hollows): REF | GD8 | GD9" 900 "$P/mid_c.png|3/4 real: REF / GD8 / GD9" "$P/mid_cc.png|3/4 clay: REF / GD8 / GD9" "$C/z8f_real_side_custom.png|GD8 profile, $C/z9f_real_side_custom.png|GD9 profile"
ROW lip_c.png 560,860,450,780 400 $RC $F8/z8f_real_C.png $F9/z9f_real_C.png; ROW lip_cc.png 560,860,450,780 400 $RC $PV/b_head_C8_close_clay.png $PV/b_headG_close_clay.png
B 04_PROFILE_LIPS.jpg "04 LIPS (upper vermilion border raised along the tracked border + everted, upper / lower lip projected ~1.2-1.3 mm, lower-lip body +0.6 mm; width unchanged): REF | GD8 | GD9" 900 "$P/lip_c.png|3/4 real" "$P/lip_cc.png|3/4 clay" "$P/nose_p.png|profile clay GD8 / GD9"
B 05_PROFILE_MOUTH_CHIN.jpg "05 MOUTH-CHIN (chin pad back 2 mm, soft labiomental, lower lip ahead of pogonion 0.66 -> 0.96 cm; chin centred, jaw contour identical to C8): REF | GD8 | GD9" 440 "$RP|REF profile (aid), $C/z8f_real_side_custom.png|GD8, $C/z9f_real_side_custom.png|GD9" "$RC|REF 3/4, $F8/z8f_real_C.png|GD8, $F9/z9f_real_C.png|GD9"
B 06_PROFILE_OVERLAY.jpg "06 PROFILE OVERLAY: Tier B profile extracted (green) vs candidate orthographic profile fitted brow->menton (red): left GD8 C8, right GD9 G; bottom: Tier A 3/4 with clay shading edges (red GD8, green GD9)" 900 "$PV/profile_overlay_C8_G.png|GD8 | GD9 vs Tier B profile" "$PV/_eov_G.png|Tier A 3/4 edge overlay (red GD8, green GD9)"
B 07_3Q_AFTER_PROFILE_EDITS.jpg "07 3/4 AFTER PROFILE EDITS (verified ~33 deg camera): REFERENCE | GD8 | GD9" 500 "$RC|REFERENCE, $F8/z8f_real_C.png|GD8, $F9/z9f_real_C.png|GD9, $F9/z9f_hair_C.png|GD9 hair" "$RC|REFERENCE, $F8/z8f_clay_C.png|GD8 clay, $F9/z9f_clay_C.png|GD9 clay"
B 08_FRONT_REGRESSION_CHECK.jpg "08 FRONT REGRESSION CHECK: REFERENCE | GD8 | GD9" 500 "$RF|REFERENCE, $F8/z8f_real_F.png|GD8, $F9/z9f_real_F.png|GD9, $F9/z9f_hair_F.png|GD9 hair" "$RF|REFERENCE, $F8/z8f_clay_F.png|GD8 clay, $F9/z9f_clay_F.png|GD9 clay"
B 09_SOFT_TISSUE_SUPPORT.jpg "09 SOFT-TISSUE SUPPORT (signed offset vs C8 along the surface normal: nasolabial / submalar / perioral / tear trough all >= 0 mm, malar / anterior cheek +0.9-1.0 mm; data/hollowing_and_jaw_vs_C8.txt): GD8 | GD9 clay" 500 "$PV/b_head_C8_front_clay.png|GD8 front clay, $PV/b_headG_front_clay.png|GD9 front clay, $PV/b_head_C8_close_clay.png|GD8 3/4 clay, $PV/b_headG_close_clay.png|GD9 3/4 clay"
B 10_HAIR_PRESERVATION.jpg "10 HAIR PRESERVATION (h23 unchanged, only rebound to the new face): GD8 | GD9" 400 "$C/z8f_hair_side_custom.png|GD8 side, $C/z9f_hair_side_custom.png|GD9 side, $C/z8f_hair_back_custom.png|GD8 rear, $C/z9f_hair_back_custom.png|GD9 rear, $F8/z8f_hair_F.png|GD8 front, $F9/z9f_hair_F.png|GD9 front"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z9f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z9f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z9f_rig_${c}_3q_custom.png|$c 3/4"; done
B 11_RIG_TEST.jpg "11 RIG TEST (GD9 fresh auto-rig on G): 23 cases front + closure 3/4" 170 "${r1#, }" "${r2#, }" "${r3#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z9_lod_${l}_front_custom.png|face $l"; done
B 12_LOD.jpg "12 LOD (GD9 face 8 LODs, groom h23 LODs)" 330 "${r#, }"
B 13_AFTER_RESTART.jpg "13 AFTER FRESH RESTART (GD9 assets from disk)" 300 "$F9/rr10f_real_F.png|real front, $F9/rr10f_real_C.png|real 3/4, $F9/rr10f_hair_F.png|hair front, $C/rr10f_hair_side_custom.png|hair side" "$C/rr10f_rig_blink_front_custom.png|blink, $C/rr10f_rig_jaw_open_front_custom.png|jaw open, $C/rr10f_rig_ph_mbp_front_custom.png|MBP, $C/rr10_lod_lod2_front_custom.png|LOD2"
ls "$O" | grep -c jpg
