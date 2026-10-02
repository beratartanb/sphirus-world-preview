#!/bin/bash
# make_gd4_boards.sh : GUARDIAN-4 boards 01-30 -> Saved/Codex/CharacterGuardian4_20261002/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = identity authority; Tier B sheets only as modelling aid) | N7 (GUARDIAN-3 e89a554 final: zhf_*, g3n7_*) | NEW (GUARDIAN-4 E1:
# face SKM_GD4_Face_e1, skin g4k3, hair h2: z4f_*, z4_*), same cameras. Blender clay evidence in pv/ (a2_head_N7_*, k_headE1_*, g_*), rr5* = after fresh restart.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian4_20261002; O="$(cygpath -m "$(pwd)/$K/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
F="$(cygpath -m "$(pwd)/$K/frames")"; F3="$(cygpath -m "$(pwd)/Saved/Codex/CharacterGuardian3_20261001/frames")"; TD="$(cygpath -m "$(pwd)/Saved/Codex/CharacterIdentity_20260930/track")"
PV="$(cygpath -m "$(pwd)/$K/pv")"; RB="$(cygpath -m "$(pwd)/Saved/Codex/CharacterGuardian2_20261001/refB")"; J="$(cygpath -m "$(pwd)/$K/boards/jaw_review")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png
# ---------------- A: cranium
B 01_CRANIUM_FRONT.jpg "01 CRANIUM FRONT (UE clay, Tier A front cam): REFERENCE | N7 | NEW - vault broader and rounder at +6..+8 cm (breadth 13.5 -> 14.3 / 11.6 -> 12.2 cm), no narrow-topped dome" 420 \
  "$RF|REFERENCE (Tier A), $C/g3n7_clay_reffront_custom.png|N7, $C/z4f_clay_reffront_custom.png|NEW, $C/z4f_clay_front_custom.png|NEW std front" \
  "$PV/a2_head_N7_frontstd_clay.png|N7 Blender clay, $PV/k_headE1_frontstd_clay.png|NEW Blender clay"
B 02_CRANIUM_3Q.jpg "02 CRANIUM 3/4 (~33 deg re-solved cam): REFERENCE | N7 | NEW - fuller forehead / temples, shorter occiput" 420 \
  "$RC|REFERENCE (Tier A 3/4), $C/g3n7_clay_refclose2_custom.png|N7, $C/z4f_clay_refclose2_custom.png|NEW, $C/z4f_clay_front3q_custom.png|NEW std 3/4"
B 03_CRANIUM_PROFILE_TOP_BACK.jpg "03 CRANIUM PROFILE / TOP / BACK: Tier B (aid) | N7 | NEW; glabella-opisthocranion 19.57 -> 18.97 cm; vertex above eyes 10.84 -> 10.41 cm" 330 \
  "$RB/turnaround_p5.png|Tier B profile (aid), $C/g3n7_clay_side_custom.png|N7 profile, $C/z4f_clay_side_custom.png|NEW profile" \
  "$RB/turnaround_p4.png|Tier B back (aid), $C/g3n7_clay_back_custom.png|N7 back, $C/z4f_clay_back_custom.png|NEW back" \
  "$C/g3n7_clay_top_custom.png|N7 top 50 deg, $C/z4f_clay_top_custom.png|NEW top 50 deg, $C/z4f_clay_vertex_custom.png|NEW vertex view, $PV/g_head_N7_top_clay.png|N7 Blender top, $PV/k_headE1_top_clay.png|NEW Blender top"
# ---------------- face clay / overlays / asymmetry
B 04_FACE_CLAY_FRONT.jpg "04 FACE CLAY FRONT (UE, Tier A front cam): REFERENCE | N7 | NEW" 520 "$RF|REFERENCE, $F3/zhf_clay_F.png|N7, $F/z4f_clay_F.png|NEW"
B 05_FACE_CLAY_3Q.jpg "05 FACE CLAY 3/4 (UE, ~33 deg cam): REFERENCE | N7 | NEW" 520 "$RC|REFERENCE, $F3/zhf_clay_C.png|N7, $F/z4f_clay_C.png|NEW"
B 06_OVERLAY_FRONT.jpg "06 OVERLAY FRONT: UE 50% blend over Tier A (N7 | NEW) + Blender mesh-curve overlay (red = candidate curves / outline, green = reference tracker, cyan = reference picks)" 520 \
  "$F3/zhf_ovF.png|N7 UE overlay, $F/z4f_ovF.png|NEW UE overlay, $PV/k_headE1_front_ov.png|NEW curves vs reference"
B 07_OVERLAY_3Q.jpg "07 OVERLAY 3/4: UE 50% blend (N7 | NEW) + Blender mesh-curve overlay" 520 "$F3/zhf_ovC.png|N7 UE overlay, $F/z4f_ovC.png|NEW UE overlay, $PV/k_headE1_close_ov.png|NEW curves vs reference"
"$BL" -b --factory-startup --python $T/blender_gd4_split.py -- $K/boards/parts/split4.png 130,670,140,860 300 ref=$RF "$PV/a2_head_N7_front_clay.png@$K/head_N7.npy" "$PV/g_headA7_front_clay.png@$K/headA7.npy" "$PV/k_headE1_front_clay.png@$K/headE1.npy" 2>&1 | grep -c SPLIT_OK >/dev/null
B 08_MIRROR_ASYMMETRY.jpg "08 MIRRORED SPLIT-FACE (Tier A front frame; columns: image | character-LEFT half mirrored | character-RIGHT half mirrored). Rows: REFERENCE, N7, A7 (REJECTED overcorrection), NEW" 900 "$P/split4.png|rows REF / N7 / A7 rejected / NEW"
B 09_LEFT_JAW_CHIN_DIAGNOSIS.jpg "09 LEFT JAW / CHIN: REFERENCE | A7 overcorrected (rejected) | R0 rollback | S1 subtle (user-approved baseline); bottom: REFERENCE | R0 | S1 | S2 (chin -> centreline, used in NEW)" 330 \
  "$J/J1_REF_OVERCORRECTED_ROLLBACK_SUBTLE_front.png|front, $J/J2_REF_OVERCORRECTED_ROLLBACK_SUBTLE_lowerface.png|lower face" "$PV/J_lowerface_S2.png|REF / R0 / S1 / S2"
# ---------------- features (crops of the Tier-A-aligned frames)
ROW f_eyes.png 350,490,230,600 300 $RF $F3/zhf_real_F.png $F/z4f_real_F.png; ROW c_eyes.png 450,590,400,720 300 $RC $F3/zhf_real_C.png $F/z4f_real_C.png
ROW fc_eyes.png 350,490,230,600 300 $RF $F3/zhf_clay_F.png $F/z4f_clay_F.png
B 10_EYE_PLACEMENT.jpg "10 EYE PLACEMENT (eye joints 5.89 cm N7 -> 5.90 cm NEW: N7 gain kept): REFERENCE | N7 | NEW" 260 "$P/f_eyes.png|front real: REF / N7 / NEW" "$P/fc_eyes.png|front clay: REF / N7 / NEW"
B 11_EYE_SHAPE.jpg "11 EYE SHAPE (lateral canthi lengthened, L 0.444 -> 0.466 / R 0.444 -> 0.454 IPD vs ref 0.469 / 0.451; aperture kept) + lid / gaze checks" 260 \
  "$P/c_eyes.png|3/4 real: REF / N7 / NEW" "$C/z4f_rig_blink_front_custom.png|blink, $C/z4f_rig_blink_left_front_custom.png|blink L, $C/z4f_rig_look_left_front_custom.png|look left, $C/z4f_rig_look_up_front_custom.png|look up, $C/z4f_rig_brows_down_front_custom.png|brows down"
ROW f_mid.png 380,700,170,650 340 $RF $PV/a2_head_N7_front_clay.png $PV/k_headE1_front_clay.png; ROW c_mid.png 420,800,380,780 340 $RC $PV/a2_head_N7_close_clay.png $PV/k_headE1_close_clay.png
B 12_ZYGOMA_MIDFACE.jpg "12 ZYGOMA / MIDFACE (soft-tissue cheek fullness, L slightly more; 3/4 far-cheek overshoot 16 -> 10.7 px; cheek_mid / cheek_lo kept): REF / N7 / NEW clay" 340 "$P/f_mid.png|front" "$P/c_mid.png|3/4"
ROW f_nose.png 440,620,320,520 300 $RF $F3/zhf_real_F.png $F/z4f_real_F.png; ROW c_nose.png 470,700,480,720 300 $RC $F3/zhf_real_C.png $F/z4f_real_C.png
B 13_NOSE.jpg "13 NOSE (re-checked at the ~33 deg cam, not the 47 deg one; no change made): REF / N7 / NEW" 300 "$P/f_nose.png|front" "$P/c_nose.png|3/4"
ROW f_mouth.png 560,690,290,540 280 $RF $F3/zhf_real_F.png $F/z4f_real_F.png; ROW c_mouth.png 640,800,460,700 280 $RC $F3/zhf_real_C.png $F/z4f_real_C.png
B 14_MOUTH.jpg "14 MOUTH (corners +1.05 mm each structurally, subtle corner drop; mesh width 0.97 -> 1.01 of ref): REF / N7 / NEW" 280 "$P/f_mouth.png|front" "$P/c_mouth.png|3/4"
ROW f_jaw.png 500,900,180,640 340 $RF $F3/zhf_clay_F.png $F/z4f_clay_F.png; ROW c_jaw.png 600,900,350,760 340 $RC $F3/zhf_clay_C.png $F/z4f_clay_C.png
B 15_JAW_CHIN.jpg "15 JAW / CHIN (S1/S2 balanced: symmetric narrowing, menton 6.9 -> 2.5 mm off the nose midline, jaw-border paths 16.4 / 16.3 cm): REF / N7 / NEW clay" 340 "$P/f_jaw.png|front" "$P/c_jaw.png|3/4"
B 16_NEW_AUTORIG_JOINTS.jpg "16 NEW AUTO-RIG JOINTS (Epic auto-rig on the corrected neutral E1; 79 / 843 facial joints moved > 1 mm vs N7; eye joints 5.899 cm; mouth-corner joints +0.8 mm; shared spine / neck / head == body)" 520 \
  "$PV/jointviz.png|top N7 joints / bottom NEW joints" "$C/z4f_rig_neutral_front_custom.png|NEW neutral (RigLogic), $C/z4f_rig_jaw_open_front_custom.png|jaw open, $C/z4f_rig_ph_mbp_front_custom.png|MBP lip seal"
# ---------------- skin
B 17_SKIN_MACRO.jpg "17 SKIN MACRO (k3: c17 base + regional sun / pigment mottling / sun spots / periorbital neutralised, olive-beige tint on face AND body): REFERENCE | N7 (g3s1) | NEW" 460 \
  "$RF|REFERENCE, $F3/zhf_real_F.png|N7, $F/z4f_real_F.png|NEW" "$RC|REFERENCE, $F3/zhf_real_C.png|N7, $F/z4f_real_C.png|NEW"
ROW micro.png 640,1040,430,830 420 $C/zhf_rig_neutral_front_custom.png $C/z4f_rig_neutral_front_custom.png; ROW micro_ref.png 470,620,230,400 420 $RF
B 18_SKIN_MICRO_CLOSEUP.jpg "18 SKIN MICRO CLOSE-UP (4K regional pore normal: nose / inner cheek large + dense, forehead / chin medium, lids / lips none; no wrinkles / bags / folds)" 420 "$P/micro_ref.png|REFERENCE cheek, $P/micro.png|N7 | NEW (close cam)"
B 19_SKIN_LIGHTING.jpg "19 SKIN LIGHTING QA A-E (NEW): A studio | B grazing | C grazing top | D gameplay sun+sky | E interior" 300 \
  "$C/z4l_A_studio_front_custom.png|A studio, $C/z4l_B_grazing_front_custom.png|B grazing, $C/z4l_C_grazingtop_front_custom.png|C grazing top, $C/z4l_D_gameplay_front_custom.png|D gameplay, $C/z4l_E_interior_front_custom.png|E interior" \
  "$C/z4l_A_studio_3q_custom.png|A 3/4, $C/z4l_B_grazing_3q_custom.png|B 3/4, $C/z4l_C_grazingtop_3q_custom.png|C 3/4, $C/z4l_D_gameplay_3q_custom.png|D 3/4, $C/z4l_E_interior_3q_custom.png|E 3/4"
B 20_HEAD_BODY_SEAM.jpg "20 HEAD / BODY SEAM (same tint factor on face + body; collar band of SRMF / normal kept from the c14s seam fix)" 330 \
  "$C/z4_seam_studio_front_custom.png|studio, $C/z4_seam_grazing_front_custom.png|grazing, $C/z4_seam_gameplay_front_custom.png|gameplay, $C/z4_seam_interior_front_custom.png|interior" \
  "$C/z4_seam_studio_3q_custom.png|studio 3/4, $C/z4_seam_grazing_3q_custom.png|grazing 3/4, $C/z4_seam_gameplay_3q_custom.png|gameplay 3/4, $C/z4_seam_interior_3q_custom.png|interior 3/4"
B 21_REFERENCE_EXPRESSION.jpg "21 REFERENCE EXPRESSION (AS_GD4_RefExpression QA pose on the new rig, NOT baked into the neutral): calm / serious / controlled / observant" 380 \
  "$RF|REFERENCE, $F/z4f_expr_neutral_F.png|NEW neutral, $F/z4f_expr_ref_expr_soft_F.png|soft, $F/z4f_expr_ref_expr_F.png|ref expression, $F/z4f_expr_ref_expr_firm_F.png|firm" \
  "$RC|REFERENCE, $F/z4f_expr_neutral_C.png|NEW neutral, $F/z4f_expr_ref_expr_C.png|ref expression 3/4"
# ---------------- hair
B 22_HAIR_FLOW_FRONT_3Q.jpg "22 HAIR FLOW FRONT / 3/4 (h2: hierarchical rebuild 16 primary -> 118 secondary -> ~700 tertiary): REFERENCE | N7 id21 | NEW h2" 460 \
  "$RF|REFERENCE, $F3/zhf_hair_F.png|N7 id21, $F/z4f_hair_F.png|NEW h2" "$RC|REFERENCE, $F3/zhf_hair_C.png|N7 id21, $F/z4f_hair_C.png|NEW h2"
B 23_HAIR_SIDE_BACK.jpg "23 HAIR SIDE / BACK: Tier B (aid) | NEW h2 (h1 first build too voluminous / dark - rejected)" 400 \
  "$RB/turnaround_p5.png|Tier B profile, $C/z4f_hair_side_custom.png|NEW profile, $RB/turnaround_p4.png|Tier B back, $C/z4f_hair_back_custom.png|NEW back"
ROW hl.png 0,700,300,1300 360 $C/z4f_hair_front_custom.png $C/z4f_hair_vertex_custom.png $C/z4f_hair_top_custom.png
B 24_HAIRLINE_CLOSEUP.jpg "24 HAIRLINE CLOSE-UP (irregular v15b hairline, root-free part band so the scalp reads at the centre part)" 360 "$P/hl.png|front / vertex / top" "$RF|REFERENCE"
B 25_BUN_STRUCTURE.jpg "25 BUN STRUCTURE (low irregular bun: every secondary lock wraps its own loop, 9 loop groups, escaping ends)" 400 \
  "$RB/turnaround_p4.png|Tier B back, $C/z4f_hair_back_custom.png|NEW back, $C/z4f_hair_side_custom.png|NEW side, $C/z4f_hair_top_custom.png|NEW top"
# ---------------- integration / rig / LOD / restart
B 26_HEAD_NECK_BODY.jpg "26 HEAD / NECK / BODY (neck bends 0 / 30 / 60 / 90; body B2 + correctives, Henley g17e, Chaos shorts m1 preserved)" 330 \
  "$C/z4_neck_nk_b00_front_custom.png|neck 0, $C/z4_neck_nk_b30_front_custom.png|30, $C/z4_neck_nk_b60_front_custom.png|60, $C/z4_neck_nk_b90_front_custom.png|90" \
  "$C/z4_neck_nk_b00_3q_custom.png|0 3/4, $C/z4_neck_nk_b30_3q_custom.png|30 3/4, $C/z4_neck_nk_b60_3q_custom.png|60 3/4, $C/z4_neck_nk_b90_3q_custom.png|90 3/4"
B 27_FULL_CHARACTER.jpg "27 FULL CHARACTER (NEW face + k3 skin + h2 hair + Henley g17e + Chaos shorts m1)" 440 \
  "$C/z4_full_fl_studio_front_custom.png|studio front, $C/z4_full_fl_studio_3q_custom.png|studio 3/4, $C/z4_full_fl_studio_side_custom.png|side, $C/z4_full_fl_studio_back_custom.png|back" \
  "$C/z4_full_fl_gameplay_front_custom.png|gameplay front, $C/z4_full_fl_gameplay_3q_custom.png|gameplay 3/4, $C/z4_full_fl_walk_3q_custom.png|walk, $C/z4_full_fl_jog_side_custom.png|jog"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z4f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z4f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z4f_rig_${c}_3q_custom.png|$c 3/4"; done
B 28_RIG_TEST.jpg "28 RIG TEST (new DNA, RigLogic + auto-rig blend shapes): 23 cases front + closure checks 3/4" 170 "${r1#, }" "${r2#, }" "${r3#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z4_lod_${l}_front_custom.png|face $l"; done; g=""; for l in glod0 glod1 glod2; do g="$g, $C/z4_lod_${l}_3q_custom.png|garment $l"; done
B 29_LOD_TEST.jpg "29 LOD TEST (NEW face 8 LODs: 34657 / 19285 / 9714 / 4067 / 1967 / 903 / 460 / 243 verts; groom LODs 4)" 330 "${r#, }" "${g#, }"
B 30_AFTER_RESTART.jpg "30 AFTER FRESH RESTART (assets from disk, DNA attached + consolidated): clay / real / hair / rig / full / LOD" 300 \
  "$F/rr5f_clay_F.png|clay front, $F/rr5f_real_F.png|real front, $F/rr5f_real_C.png|real 3/4, $F/rr5f_hair_F.png|hair front, $F/rr5f_hair_C.png|hair 3/4" \
  "$C/rr5f_rig_blink_front_custom.png|blink, $C/rr5f_rig_lips_closed_front_custom.png|lips closed, $C/rr5f_rig_jaw_open_front_custom.png|jaw open, $C/rr5f_rig_extreme_front_custom.png|extreme, $C/rr5_full_fl_studio_front_custom.png|full front, $C/rr5_lod_lod2_front_custom.png|LOD2"
ls "$O" | grep -c jpg
