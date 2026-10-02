#!/bin/bash
# make_gd7_boards.sh : GUARDIAN-7 (GUARDIAN-6 correction) boards -> Saved/Codex/CharacterGuardian7_20261002/boards
# Columns: REFERENCE (Tier A) | CURRENT OVER-HOLLOW (GD6 S4) | ROLLBACK BASELINE (R7) | NEW CORRECTED (C8). Blender clay at the Tier A cameras (pv/c_*),
# UE real / hair captures: GD6 = z6f_* (S4 + h6), GD7 = z7f_* (C8 + h17). Identical cameras / lights per row. rr8* = GD7 after a fresh restart.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian7_20261002; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F6=Saved/Codex/CharacterGuardian6_20261002/frames; F7=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; S4=$PV/c_head_S4_overhollow; R7=$PV/c_headR7; C7=$PV/c_headC7; C8=$PV/c_headC8
# ---- A soft-tissue support
ROW a_f.png 330,800,170,630 380 $RF ${S4}_front_clay.png ${R7}_front_clay.png ${C8}_front_clay.png; ROW a_c.png 380,860,330,794 380 $RC ${S4}_close_clay.png ${R7}_close_clay.png ${C8}_close_clay.png
ROW a_rf.png 300,860,170,630 380 $RF $F6/z6f_real_F.png $F7/z7f_real_F.png; ROW a_rc.png 330,900,280,794 380 $RC $F6/z6f_real_C.png $F7/z7f_real_C.png
VS a_all.png "$P/a_f.png|f" "$P/a_c.png|c" "$P/a_rf.png|rf" "$P/a_rc.png|rc"
B A_SOFT_TISSUE_SUPPORT.jpg "A SOFT-TISSUE SUPPORT: REFERENCE | CURRENT OVER-HOLLOW (GD6 S4) | ROLLBACK BASELINE (R7) | NEW CORRECTED (C8) - clay at the Tier A cameras; bottom: REF | GD6 real | GD7 real" 1500 "$P/a_all.png|rows: front clay REF / S4 over-hollow / R7 rollback / C8 new; 3/4 clay same; front real REF / GD6 / GD7; 3/4 real REF / GD6 / GD7"
# ---- B nasolabial / submalar
ROW b_f.png 470,720,230,560 360 $RF ${S4}_front_clay.png ${R7}_front_clay.png ${C8}_front_clay.png; ROW b_c.png 520,800,420,760 360 $RC ${S4}_close_clay.png ${R7}_close_clay.png ${C8}_close_clay.png
ROW b_s.png 0,10000,0,10000 360 ${S4}_side_clay.png ${C8}_side_clay.png
VS b_all.png "$P/b_f.png|f" "$P/b_c.png|c" "$P/b_s.png|s"
B B_NASOLABIAL_SUBMALAR.jpg "B NASOLABIAL / SUBMALAR INTERPRETATION (transition kept as a soft plane relationship with tissue support outside the line; no trench, no submalar hollow): REF | S4 over-hollow | R7 rollback | C8 new" 1500 "$P/b_all.png|rows: front REF / S4 / R7 / C8; 3/4 REF / S4 / R7 / C8; profile clay S4 / C8"
# ---- C cranium width: OLD TOO-NARROW (R7) | OVER-WIDE / OVER-FLAT (C7) | NEW CORRECTED (C8), Blender clay, 5 views + UE clay
B C_CRANIUM_WIDTH.jpg "C CRANIUM WIDTH / TOP ARC (bald, before hair): OLD TOO-NARROW (R7) | OVER-WIDE / OVER-FLAT (C7, rejected) | NEW CORRECTED (C8). Breadth +4/+6/+8 cm above eyes: 14.78/14.30/12.17 | 15.36/15.21/13.26 | 15.10/14.58/12.27 cm; vertex above eyes 10.41 | 10.41 | 10.57 cm" 300   "${R7}_frontstd_clay.png|R7 front, ${C7}_frontstd_clay.png|C7 front, ${C8}_frontstd_clay.png|C8 front, ${R7}_q3std_clay.png|R7 3/4, ${C7}_q3std_clay.png|C7 3/4, ${C8}_q3std_clay.png|C8 3/4"   "${R7}_side_clay.png|R7 profile, ${C7}_side_clay.png|C7 profile, ${C8}_side_clay.png|C8 profile, ${R7}_rear_clay.png|R7 rear, ${C7}_rear_clay.png|C7 rear, ${C8}_rear_clay.png|C8 rear"   "${R7}_top_clay.png|R7 top, ${C7}_top_clay.png|C7 top, ${C8}_top_clay.png|C8 top, $C/z7f_clay_reffront_custom.png|C8 UE clay Tier A front, $C/z7f_clay_back_custom.png|C8 UE clay back, $C/z7f_clay_vertex_custom.png|C8 UE vertex"
# ---- D upper temple hair start
ROW d_f.png 40,430,120,680 360 $RF $F6/z6f_hair_F.png $F7/z7f_hair_F.png; ROW d_c.png 60,520,200,794 360 $RC $F6/z6f_hair_C.png $F7/z7f_hair_C.png
VS d_all.png "$P/d_f.png|f" "$P/d_c.png|c"
B D_UPPER_TEMPLE_HAIR_START.jpg "D UPPER TEMPLE HAIR START / TEMPORAL HAIRLINE (temporal hairline raised ~1 cm at 62 / 74 deg, stronger jag + wider density ramp, scalp visible at the break-up; sits on the C8 skull): REF | GD6 h6 | GD7 h17" 900 "$P/d_all.png|front REF / GD6 / GD7 h17, 3/4 REF / GD6 / GD7 h17" "$C/z7f_hair_front3q_custom.png|GD7 std 3/4, $C/z7f_hair_top_custom.png|GD7 top"
# ---- E side-view top hair / crown silhouette
B E_SIDE_TOP_HAIR_CROWN.jpg "E SIDE-VIEW TOP HAIR / CROWN SILHOUETTE (h17: profile stand-off at top 2.5 -> 3.1 cm, rear-upper 2.8-3.4 -> 4.5-5.1 cm, nape rolls down into the bun; front width at +4/+6 cm unchanged; no puff): Tier B profile (aid) | GD6 h6 | GD7 h17" 440 \
  "$RB/turnaround_p5.png|Tier B profile (aid), $C/z6f_hair_side_custom.png|GD6 side, $C/z7f_hair_side_custom.png|GD7 side" "$RB/turnaround_p4.png|Tier B back (aid), $C/z6f_hair_back_custom.png|GD6 back, $C/z7f_hair_back_custom.png|GD7 back" "$RC|REFERENCE 3/4, $F6/z6f_hair_C.png|GD6 3/4, $F7/z7f_hair_C.png|GD7 3/4"
# ---- F hair volume / lock correction (user directive): BEFORE h9 | AFTER h17, same pose / camera / scale / light (C8 face)
B F_HAIR_VOLUME_LOCKS_BEFORE_AFTER.jpg "F HAIR VOLUME / LOCK CORRECTION: BEFORE (h9) | AFTER (h17) per view, identical pose / camera / light. h17 = new lift field along each lock path (hairline low -> crown -> rear-upper roll -> nape), 60 smaller primary masses, loose partial convergence + lateral fill (no rope / dreadlock cords), per-lock bun entries (no funnel), no part-edge dip (no symmetric ridges); skull / face untouched" 330   "$RB/turnaround_p5.png|REF Tier B side, $C/HB_hair_side_custom.png|BEFORE side, $C/HC_hair_side_custom.png|AFTER side, $RB/turnaround_p3.png|REF Tier B side 2, $C/HB_hair_side2_custom.png|BEFORE side 2, $C/HC_hair_side2_custom.png|AFTER side 2"   "$RB/turnaround_p4.png|REF Tier B back, $C/HB_hair_back_custom.png|BEFORE back, $C/HC_hair_back_custom.png|AFTER back, $RF|REF front, $C/HB_hair_reffront_custom.png|BEFORE front, $C/HC_hair_reffront_custom.png|AFTER front"   "$RC|REF 3/4, $C/HB_hair_refclose2_custom.png|BEFORE 3/4, $C/HC_hair_refclose2_custom.png|AFTER 3/4, $C/HB_hair_back3q_custom.png|BEFORE back 3/4, $C/HC_hair_back3q_custom.png|AFTER back 3/4, $PV/_silmask.png|MAIN MASS ONLY (no fine strands / shine): top h9, bottom h17"
# ---- standard
B 01_FACE_FRONT_NEUTRAL.jpg "01 FACE FRONT NEUTRAL: REFERENCE | GD6 | GD7" 520 "$RF|REFERENCE, $F6/z6f_real_F.png|GD6, $F7/z7f_real_F.png|GD7" "$RF|REFERENCE, $F6/z6f_clay_F.png|GD6 clay, $F7/z7f_clay_F.png|GD7 clay"
B 02_FACE_3Q_NEUTRAL.jpg "02 FACE 3/4 NEUTRAL: REFERENCE | GD6 | GD7" 520 "$RC|REFERENCE, $F6/z6f_real_C.png|GD6, $F7/z7f_real_C.png|GD7" "$RC|REFERENCE, $F6/z6f_clay_C.png|GD6 clay, $F7/z7f_clay_C.png|GD7 clay"
B 03_FACE_PROFILE_NEUTRAL.jpg "03 PROFILE: Tier B (aid) | GD6 | GD7" 420 "$RB/turnaround_p5.png|Tier B (aid), $C/z6f_real_side_custom.png|GD6, $C/z7f_real_side_custom.png|GD7"
r6=""; r7=""; for L in A_studio B_grazing C_grazingtop D_gameplay E_interior; do r6="$r6, $C/z6l_${L}_front_custom.png|GD6 $L"; r7="$r7, $C/z7l_${L}_front_custom.png|GD7 $L"; done
B 04_SKIN_LIGHTING_A_E.jpg "04 LIGHTING A-E: GD6 row | GD7 row" 300 "${r6#, }" "${r7#, }"
s7=""; for L in studio grazing gameplay interior; do s7="$s7, $C/z7_seam_${L}_front_custom.png|GD7 $L"; done
B 05_HEAD_BODY_SEAM.jpg "05 HEAD / BODY SEAM (GD7; skin k7 / body seam SRMF unchanged from GD5)" 330 "${s7#, }"
B 06_REFERENCE_EXPRESSION.jpg "06 REFERENCE EXPRESSION (GD7 rig)" 380 "$RF|REFERENCE, $F7/z7f_expr_neutral_F.png|GD7 neutral, $F7/z7f_expr_ref_expr_F.png|GD7 ref expr, $F7/z7f_expr_ref_expr_C.png|GD7 ref expr 3/4"
B 07_FULL_CHARACTER.jpg "07 FULL CHARACTER (GD7)" 440 "$C/z7_full_fl_studio_front_custom.png|studio front, $C/z7_full_fl_studio_3q_custom.png|studio 3/4, $C/z7_full_fl_studio_side_custom.png|side, $C/z7_full_fl_studio_back_custom.png|back" "$C/z7_full_fl_gameplay_front_custom.png|gameplay, $C/z7_full_fl_walk_3q_custom.png|walk, $C/z7_full_fl_jog_side_custom.png|jog"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z7f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z7f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z7f_rig_${c}_3q_custom.png|$c 3/4"; done
B 08_RIG_TEST.jpg "08 RIG TEST (GD7 fresh auto-rig C8)" 170 "${r1#, }" "${r2#, }" "${r3#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z7_lod_${l}_front_custom.png|face $l"; done
B 09_LOD_TEST.jpg "09 LOD TEST (GD7)" 330 "${r#, }"
B 10_AFTER_RESTART.jpg "10 AFTER FRESH RESTART (GD7 assets from disk)" 300 "$F7/rr8f_clay_F.png|clay, $F7/rr8f_real_F.png|real, $F7/rr8f_hair_F.png|hair front, $F7/rr8f_hair_C.png|hair 3/4" "$C/rr8f_rig_blink_front_custom.png|blink, $C/rr8f_rig_jaw_open_front_custom.png|jaw open, $C/rr8_full_fl_studio_front_custom.png|full, $C/rr8_lod_lod2_front_custom.png|LOD2"
ls "$O" | grep -c jpg
