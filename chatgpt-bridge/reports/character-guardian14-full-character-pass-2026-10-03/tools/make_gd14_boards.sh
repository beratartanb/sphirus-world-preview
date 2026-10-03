#!/bin/bash
# make_gd14_boards.sh : GUARDIAN-14 boards 01-50 -> Saved/Codex/CharacterGuardian14_20261003/boards
# REFERENCE = Tier A front / ~33 deg 3/4 (authority), Tier B profile = aid. PREVIOUS = GD13c HS3 clay / GD12C G UE (last rigged, h24, k11, g17e).
# NEW = GD14 K2 (k12 skin, h29 hair, M_Natural brows, Henley g18p). Clay: pv/r_cur_FIN_* (HS3) / pv/r_new_FIN_* (K2); close-ups hs/fin_<view>_{0,1}.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian14_20261003; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
FP=Saved/Codex/CharacterGuardian12C_20261003/frames; FN=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; HS=$K/hs; NS=$K/nose
RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_FIN; NW=$PV/r_new_FIN
# ---------------- FACE 01-20 ----------------
B 01_FACE_FRONT.jpg "01 FACE FRONT: REFERENCE | PREVIOUS | NEW (row 1 clay HS3 / K2, row 2 UE real GD12C / GD14)" 460 "$RF|REFERENCE, ${CU}_front_clay.png|PREVIOUS clay (GD13c HS3), ${NW}_front_clay.png|NEW clay (GD14 K2)" "$RF|REFERENCE, $FP/z12cf_real_F.png|PREVIOUS real (GD12C), $FN/z14f_real_F.png|NEW real (GD14)"
B 02_FACE_3Q.jpg "02 FACE 3/4 (verified ~33 deg): REFERENCE | PREVIOUS | NEW" 460 "$RC|REFERENCE, ${CU}_close_clay.png|PREVIOUS clay, ${NW}_close_clay.png|NEW clay" "$RC|REFERENCE, $FP/z12cf_real_C.png|PREVIOUS real, $FN/z14f_real_C.png|NEW real"
B 03_FACE_PROFILE.jpg "03 FACE PROFILE: Tier B (aid) | PREVIOUS | NEW clay | NEW real" 460 "$RP|REF profile (aid), ${CU}_side_clay.png|PREVIOUS, ${NW}_side_clay.png|NEW, $C/z14f_real_side_custom.png|NEW real"
B 04_FACE_PROPORTION.jpg "04 FACE PROPORTION: clay silhouette over Tier A (red = NEW, cyan = PREVIOUS): front / 3/4" 600 "$PV/_olFIN_front.png|front, $PV/_olFIN_3q.png|3/4"
ROW z_f.png 250,760,100,700 520 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 05_ZYGOMATIC_FRONT.jpg "05 ZYGOMATIC / MALAR FRONT: REFERENCE | PREVIOUS | NEW (lower-cheek tissue widened to the Tier A outline, mandible border / chin unchanged)" 1950 "$P/z_f.png|x"
ROW z_c.png 200,900,250,794 520 $RC ${CU}_close_clay.png ${NW}_close_clay.png
B 06_ZYGOMATIC_3Q.jpg "06 ZYGOMATIC / MALAR 3/4: REFERENCE | PREVIOUS | NEW" 1950 "$P/z_c.png|x"
ROW md_p.png 150,1150,450,1200 420 ${CU}_side_clay.png ${NW}_side_clay.png; ROW md_r.png 330,860,250,794 420 $RC $FP/z12cf_real_C.png $FN/z14f_real_C.png
VS stack_07.png "$P/md_p.png|x" "$P/md_r.png|x"
B 07_MIDFACE_DEPTH.jpg "07 MIDFACE DEPTH: profile clay PREVIOUS | NEW; 3/4 real REFERENCE | PREVIOUS | NEW (detail separation removed the accumulated creases; tissue support kept)" 1950 "$P/stack_07.png|rows: profile clay / 3/4 real"
ROW e_r.png 300,560,160,640 300 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png; ROW e_c.png 360,620,330,794 300 $RC $FP/z12cf_real_C.png $FN/z14f_real_C.png; ROW e_k.png 0,0,0,0 300 $HS/fin_eye_front_0.png $HS/fin_eye_front_1.png $HS/fin_eye_3q_0.png $HS/fin_eye_3q_1.png
VS stack_08.png "$P/e_r.png|x" "$P/e_c.png|x" "$P/e_k.png|x"
B 08_EYE_BROW_ORBIT.jpg "08 EYE / BROW / ORBIT: REFERENCE | PREVIOUS | NEW real (front, 3/4); clay PREVIOUS | NEW (front, 3/4) - upper lid rotated 6 deg down / lower lid 1.5 deg up about the eyeball (lids stay on the globe), M_Natural brows" 1950 "$P/stack_08.png|rows: front real / 3/4 real / clay close-ups"
ROW nb.png 280,620,240,560 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW nbr.png 280,620,240,560 460 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png
VS stack_09.png "$P/nb.png|x" "$P/nbr.png|x"
B 09_NASAL_BRIDGE_FRONT.jpg "09 NASAL BRIDGE FRONT: REFERENCE | PREVIOUS | NEW" 1950 "$P/stack_09.png|rows: clay / real"
ROW nd.png 250,1000,600,1200 460 ${CU}_side_clay.png ${NW}_side_clay.png
B 10_NOSE_DORSUM.jpg "10 NOSE DORSUM: Tier B (aid) | PREVIOUS | NEW profile clay + close-up profile" 520 "$RP|REF profile (aid), $P/nd.png|PREVIOUS | NEW" "$HS/fin_nose_side_0.png|PREVIOUS, $HS/fin_nose_side_1.png|NEW"
ROW nbf.png 380,700,260,540 420 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png
B 11_NOSE_BASE_FRONT.jpg "11 NOSE BASE FRONT: REFERENCE | PREVIOUS | NEW real; clay close-ups PREVIOUS | NEW" 520 "$P/nbf.png|real" "$HS/fin_nose_front_0.png|PREVIOUS clay, $HS/fin_nose_front_1.png|NEW clay"
ROW nb3.png 380,760,400,794 420 $RC $FP/z12cf_real_C.png $FN/z14f_real_C.png
B 12_NOSE_BASE_3Q.jpg "12 NOSE BASE 3/4: REFERENCE | PREVIOUS | NEW real; clay close-ups PREVIOUS | NEW" 520 "$P/nb3.png|real" "$HS/fin_nose_3q_0.png|PREVIOUS clay, $HS/fin_nose_3q_1.png|NEW clay"
B 13_NOSTRIL_BELOW.jpg "13 NOSTRIL FROM BELOW: PREVIOUS (inward-rolled rim, slit nostrils) | NEW (MetaHuman model nose base, frequency-transferred)" 560 "$HS/fin_nostril_0.png|PREVIOUS (GD13c HS3), $HS/fin_nostril_1.png|NEW (GD14)"
B 14_ALAR_CLOSEUP.jpg "14 ALAR / NOSE-BASE CANDIDATES (Phase A): model-only bases + composites; selected = 65% own model + 35% Celeste nose region, detail-only transfer (k=120)" 900 "$NS/msheet_nose_3q.jpg|model-only nose bases (3/4)" "$NS/csheet_nostril.jpg|composites into the sculpt (below)" "$NS/_m65.png|selected family: HS3 | hf60 | hf120 (SELECTED) | full"
"$BL" -b --factory-startup --python $PV/_mark.py -- $P/mw_ref.png $RF $K/track/tr_fin.json ref_front 540,700,260,560 >/dev/null 2>&1
"$BL" -b --factory-startup --python $PV/_mark.py -- $P/mw_new.png $FN/z14f_real_F.png $K/track/tr_fin.json new_real 540,700,260,560 >/dev/null 2>&1
B 15_MOUTH_WIDTH.jpg "15 MOUTH WIDTH (MetaHuman tracker curves, same frame): REFERENCE | NEW - real-render tracker mouth / IPD: REF 0.855 | GD12C 0.830 | GD14 0.818 (clay curves 0.853) - still slightly narrow in the real render" 520 "$P/mw_ref.png|REFERENCE, $P/mw_new.png|NEW real"
ROW pu.png 540,720,280,540 400 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png
B 16_PHILTRUM_UPPER_LIP.jpg "16 PHILTRUM / UPPER LIP: REFERENCE | PREVIOUS | NEW real; clay close-ups PREVIOUS | NEW (vermilion re-proportioned: upper 7.6 mm / lower 10.0 mm at centre, was 6.1 / 11.8)" 520 "$P/pu.png|real" "$HS/fin_mouth_front_0.png|PREVIOUS clay, $HS/fin_mouth_front_1.png|NEW clay"
ROW fp_f.png 500,800,220,580 380 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png; ROW fp_c.png 480,880,400,794 380 $RC $FP/z12cf_real_C.png $FN/z14f_real_C.png
VS stack_17.png "$P/fp_f.png|x" "$P/fp_c.png|x"
B 17_FULL_PERIORAL.jpg "17 FULL PERIORAL: REFERENCE | PREVIOUS | NEW (lip colour muted k12)" 1950 "$P/stack_17.png|rows: front / 3/4" "$HS/fin_mouth_3q_0.png|PREVIOUS clay 3/4, $HS/fin_mouth_3q_1.png|NEW clay 3/4, $HS/fin_mouth_side_0.png|PREVIOUS profile, $HS/fin_mouth_side_1.png|NEW profile"
ROW lf_f.png 520,800,140,660 380 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW lf_c.png 480,900,250,794 380 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_18.png "$P/lf_f.png|x" "$P/lf_c.png|x"
B 18_LOWER_FACE.jpg "18 LOWER FACE: REFERENCE | PREVIOUS | NEW clay" 1950 "$P/stack_18.png|rows: front / 3/4"
B 19_FRONT_OVERLAY.jpg "19 FRONT OVERLAY (50% clay over Tier A front): PREVIOUS | NEW" 560 "$PV/rb_cur_FIN_front.png|PREVIOUS, $PV/rb_new_FIN_front.png|NEW"
B 20_3Q_OVERLAY.jpg "20 3/4 OVERLAY (50% clay over Tier A 3/4): PREVIOUS | NEW" 560 "$PV/rb_cur_FIN_close.png|PREVIOUS, $PV/rb_new_FIN_close.png|NEW"
# ---------------- HAIR 21-35 ----------------
H0=z12cf; H1=z14f
B 21_HAIR_FRONT.jpg "21 HAIR FRONT: REFERENCE | h24 (GD12C) | NEW h29" 520 "$RF|REFERENCE, $C/${H0}_hair_reffront_custom.png|h24, $C/${H1}_hair_reffront_custom.png|h29"
B 22_HAIR_3Q.jpg "22 HAIR 3/4: REFERENCE | h24 | h29" 460 "$RC|REFERENCE, $C/${H0}_hair_refclose2_custom.png|h24, $C/${H1}_hair_refclose2_custom.png|h29" "$C/${H0}_hair_front3q_custom.png|h24 3/4 wide, $C/${H1}_hair_front3q_custom.png|h29 3/4 wide"
B 23_HAIR_LEFT_PROFILE.jpg "23 HAIR PROFILE (side): Tier B (aid) | h24 | h29" 520 "$RP|REF profile (aid), $C/${H0}_hair_side_custom.png|h24, $C/${H1}_hair_side_custom.png|h29"
B 24_HAIR_RIGHT_PROFILE.jpg "24 HAIR OTHER PROFILE: h24 | h29" 520 "$C/${H0}_hair_side2_custom.png|h24, $C/${H1}_hair_side2_custom.png|h29"
B 25_HAIR_REAR.jpg "25 HAIR REAR: h24 | h29 (rear lift 1.8 -> 0.9, stronger rear clumping, bun pushed back)" 520 "$C/${H0}_hair_back_custom.png|h24, $C/${H1}_hair_back_custom.png|h29"
B 26_HAIR_TOP.jpg "26 HAIR TOP: h24 | h29" 520 "$C/${H0}_hair_top_custom.png|h24, $C/${H1}_hair_top_custom.png|h29"
ROW hl.png 60,420,180,620 400 $RF $FP/z12cf_hair_F.png $FN/z14f_hair_F.png
B 27_HAIRLINE.jpg "27 HAIRLINE: REFERENCE | h24 | h29 (natural temple hairline restored, softer edge ramp, visible centre part)" 1950 "$P/hl.png|x"
ROW ts.png 0,0,0,0 420 $C/${H0}_hair_side_custom.png $C/${H1}_hair_side_custom.png
B 28_TEMPORAL_START.jpg "28 TEMPORAL START: h24 (bald temple band: roots removed) | h29 (roots back at the natural hairline, swept up / back, tight to the head)" 1950 "$P/ts.png|x"
B 29_PRIMARY_MASSES.jpg "29 PRIMARY MASSES (strand preview: main path brown, bun section red, loose green): h24 | h29" 600 "Saved/Codex/CharacterGuardian12C_20261003/hair/h24/preview.png|h24, $K/hair/h29/preview.png|h29"
ROW tf.png 0,0,0,0 460 $C/${H0}_hair_top_custom.png $C/${H1}_hair_top_custom.png
B 30_TOP_FLOW.jpg "30 TOP FLOW: h24 | h29 (multi-frequency irregular waves, crossing masses, lower top lift)" 1950 "$P/tf.png|x"
ROW rl.png 0,0,0,0 460 $C/${H0}_hair_back3q_custom.png $C/${H1}_hair_back3q_custom.png
B 31_REAR_LOCKS.jpg "31 REAR LOCKS: h24 | h29 (rear 3/4)" 1950 "$P/rl.png|x"
B 32_BUN_STRUCTURE.jpg "32 BUN STRUCTURE: Tier B (aid) | h24 | h29 (single-direction twist coil, compact, same height)" 520 "$RP|REF (aid), $C/${H0}_hair_side_custom.png|h24 side, $C/${H1}_hair_side_custom.png|h29 side" "$C/${H0}_hair_back3q_custom.png|h24 rear 3/4, $C/${H1}_hair_back3q_custom.png|h29 rear 3/4"
ROW ff.png 120,820,60,740 460 $RF $FP/z12cf_hair_F.png $FN/z14f_hair_F.png
B 33_FACE_FRAMING.jpg "33 FACE FRAMING: REFERENCE | h24 | h29 (asymmetric framing locks enabled on both sides, fuller, curlier)" 1950 "$P/ff.png|x"
ROW hc.png 0,520,0,794 460 $RC $FP/z12cf_hair_C.png $FN/z14f_hair_C.png
B 34_HAIR_COLOUR.jpg "34 HAIR COLOUR: REFERENCE | h24 (melanin 0.53 / redness 0.45) | h29 (0.60 / 0.38, highlights 0.55 / 0.40, loose 0.66)" 1950 "$P/hc.png|x"
B 35_HAIR_LIGHTING.jpg "35 HAIR + FACE UNDER QA LIGHTS A-E (GD14)" 300 "$C/z14l_A_studio_front_custom.png|A studio, $C/z14l_B_grazing_front_custom.png|B grazing, $C/z14l_C_grazingtop_front_custom.png|C grazing top, $C/z14l_D_gameplay_front_custom.png|D gameplay, $C/z14l_E_interior_front_custom.png|E interior" "$C/z14l_A_studio_3q_custom.png|A 3/4, $C/z14l_B_grazing_3q_custom.png|B 3/4, $C/z14l_C_grazingtop_3q_custom.png|C 3/4, $C/z14l_D_gameplay_3q_custom.png|D 3/4, $C/z14l_E_interior_3q_custom.png|E 3/4"
# ---------------- FULL CHARACTER 36-50 ----------------
ROW sk.png 300,800,160,640 420 $RF $FP/z12cf_real_F.png $FN/z14f_real_F.png
B 36_SKIN.jpg "36 SKIN: REFERENCE | GD12C k11 | GD14 k12 (k11 + muted lip colour)" 1950 "$P/sk.png|x"
B 37_HEAD_BODY_SEAM.jpg "37 HEAD / BODY SEAM (garments hidden): GD12C | GD14 under 4 lights" 300 "$C/z12c_seam_studio_front_custom.png|GD12C studio, $C/z12c_seam_grazing_front_custom.png|grazing, $C/z12c_seam_interior_front_custom.png|interior, $C/z12c_seam_gameplay_front_custom.png|gameplay" "$C/z14_seam_studio_front_custom.png|GD14 studio, $C/z14_seam_grazing_front_custom.png|grazing, $C/z14_seam_interior_front_custom.png|interior, $C/z14_seam_gameplay_front_custom.png|gameplay"
B 38_HEAD_NECK_BODY.jpg "38 HEAD / NECK / BODY: Tier B (aid) | GD14 studio front / side / 3/4" 520 "$RP|REF profile (aid), $C/z14_full_fl_studio_side_custom.png|GD14 side, $C/z14_full_fl_studio_front_custom.png|GD14 front, $C/z14_full_fl_studio_3q_custom.png|GD14 3/4"
B 39_HENLEY.jpg "39 HENLEY NECKLINE: g17e (GD12C) | g18p (GD14: neckline raised / narrowed on the same topology via a spatial displacement field (seams cannot open), V bottom 123 -> 126, HPS 12.5 -> ~8)" 360 "$C/z12c_neck_nk_b00_front_custom.png|g17e upright, $C/z12c_neck_nk_b00_3q_custom.png|g17e 3/4, $C/z12c_neck_nk_b45_front_custom.png|g17e bend 45" "$C/z14_neck_nk_b00_front_custom.png|g18p upright, $C/z14_neck_nk_b00_3q_custom.png|g18p 3/4, $C/z14_neck_nk_b45_front_custom.png|g18p bend 45"
B 40_SHORTS.jpg "40 SHORTS (Chaos m1, unchanged): GD14 waist / hem close-ups" 300 "$C/z14_waist_wb_neutral_3q_custom.png|neutral 3/4, $C/z14_waist_wb_neutral_side_custom.png|side, $C/z14_waist_wb_bend45_3q_custom.png|bend 45, $C/z14_waist_wb_stride_3q_custom.png|stride, $C/z14_waist_wb_walk_3q_custom.png|walk"
B 41_FULL_FRONT.jpg "41 FULL FRONT (studio)" 900 "$C/z14_full_fl_studio_front_custom.png|GD14"
B 42_FULL_3Q.jpg "42 FULL 3/4 (studio)" 900 "$C/z14_full_fl_studio_3q_custom.png|GD14"
B 43_FULL_PROFILE.jpg "43 FULL PROFILE (studio)" 900 "$RP|REF (aid), $C/z14_full_fl_studio_side_custom.png|GD14"
B 44_FULL_BACK.jpg "44 FULL BACK (studio)" 900 "$C/z14_full_fl_studio_back_custom.png|GD14"
B 45_GAMEPLAY_LIGHT.jpg "45 GAMEPLAY LIGHT (sun + sky)" 420 "$C/z14_full_fl_gameplay_front_custom.png|front, $C/z14_full_fl_gameplay_3q_custom.png|3/4, $C/z14_full_fl_gameplay_side_custom.png|side, $C/z14_full_fl_gameplay_back_custom.png|back" "$C/z14l_D_gameplay_front_custom.png|head front, $C/z14l_D_gameplay_3q_custom.png|head 3/4"
B 46_INTERIOR_LIGHT.jpg "46 INTERIOR LIGHT" 420 "$C/z14l_E_interior_front_custom.png|head front, $C/z14l_E_interior_3q_custom.png|head 3/4, $C/z14_seam_interior_front_custom.png|neck / seam front, $C/z14_seam_interior_3q_custom.png|neck / seam 3/4"
r=""; for c in neutral ref_expr_soft ref_expr ref_expr_firm; do r="$r, $FN/z14f_expr_${c}_F.png|$c F"; done; r2=""; for c in neutral ref_expr_soft ref_expr ref_expr_firm; do r2="$r2, $FN/z14f_expr_${c}_C.png|$c 3/4"; done
B 47_REFERENCE_EXPRESSION.jpg "47 REFERENCE EXPRESSION (calm, serious, alert): REFERENCE | GD14 sequence" 320 "$RF|REFERENCE${r}" "$RC|REFERENCE 3/4${r2}"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; r4=""; for c in "${L1[@]}"; do r1="$r1, $C/z14f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z14f_rig_${c}_front_custom.png|$c"; done
for c in squint_half squint nose_wrinkle upper_lip_raise sneer mouth_stretch smile_wide; do r3="$r3, $FN/z14f_expr_${c}_F.png|$c F"; r4="$r4, $FN/z14f_expr_${c}_C.png|$c 3/4"; done
B 48_RIG_TEST.jpg "48 RIG TEST (fresh auto-rig on K2): rig cases + squint / nose / upper-lip / sneer / stretch tests (nostril survival)" 170 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z14_lod_${l}_front_custom.png|face $l"; done; g=""; for l in glod0 glod1 glod2; do g="$g, $C/z14_lod_${l}_3q_custom.png|full $l"; done
B 49_LOD.jpg "49 LOD: face LOD0-3 + full character LOD0-2 (garments + groom)" 330 "${r#, }" "${g#, }"
B 50_AFTER_RESTART.jpg "50 AFTER FRESH EDITOR RESTART (all GD14 assets from disk)" 320 "$FN/rr15f_real_F.png|real front, $FN/rr15f_real_C.png|real 3/4, $FN/rr15f_hair_F.png|hair, $C/rr15f_rig_blink_front_custom.png|blink, $C/rr15f_rig_jaw_open_front_custom.png|jaw open, $C/rr15_lod_lod1_front_custom.png|LOD1"
ls "$O" | grep -c jpg
