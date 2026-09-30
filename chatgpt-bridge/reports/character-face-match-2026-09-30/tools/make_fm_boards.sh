#!/bin/bash
# make_fm_boards.sh [ABCDEFG] : FACE-MATCH pass evidence boards A-G -> Saved/Codex/CharacterFaceMatch_20260930/boards
# baseline = commit 4003557 composition re-captured with the same cameras (bl_*: RV face, hair v14k, skin c3 / body C);
# final = fn_* / fnl_* (face SKM_FM_FaceMesh_c, hair v15c, face skin c8, body skin F); rig baseline = fr_* (RV face)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SETS=${1:-ABCDEF}
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; T=Tools/CharacterLookdev_20260930
O="$(cygpath -m "$(pwd)/Saved/Codex/CharacterFaceMatch_20260930/boards")"; mkdir -p "$O/parts"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"; RF="$(cygpath -m "$(pwd)/Saved/Codex/CharacterRevision_20260930/captures")"
S="$O/parts"
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 40; echo; }
OV() { OV_A=$1 "$BL" -b --factory-startup --python $T/blender_fm_overlay.py -- "${@:2}" 2>&1 | grep -c OVERLAY; }
if [[ $SETS == *A* ]]; then
  B A_FACE_REFERENCE_MATCH.jpg "A  face reference match: concept / commit 4003557 / face-match candidate (same cameras)" 330 \
    "$RF/ref_hair_front.png|concept front, $RF/ref_hair_3q.png|concept 3/4, $RF/ref_hair_close.png|concept close" \
    "$C/bl_hair_front_custom.png|4003557 front, $C/bl_hair_front3q_custom.png|4003557 3/4, $C/bl_hair_close_custom.png|4003557 close, $C/bl_hair_side_custom.png|4003557 side" \
    "$C/fn_hair_front_custom.png|candidate front, $C/fn_hair_front3q_custom.png|candidate 3/4, $C/fn_hair_close_custom.png|candidate close, $C/fn_hair_side_custom.png|candidate side"
fi
if [[ $SETS == *B* ]]; then
  RL="0.4013:0.4358|0.6335:0.4350"; CL="0.3890:0.3958|0.5952:0.3958"; CR="0.24:0.30:0.76:0.84"; RM="0.517:0.3795;0.517:0.553;0.517:0.6397;0.517:0.7827"
  BM=""; FM=""   # candidate landmarks: pupils only (projected profile landmarks were not exact); concept level lines span every frame
  for a in 0.5 1; do
    OV $a "$RF/ref_hair_front.png|$C/bl_nohair_front_custom.png|$S/ov_bl_$a.png|$RL|$CL|$CR|600|$RM|$BM" "$RF/ref_hair_front.png|$C/fn_nohair_front_custom.png|$S/ov_fn_$a.png|$RL|$CL|$CR|600|$RM|$FM"
  done
  OV 0 "$RF/ref_hair_front.png|$C/fn_nohair_front_custom.png|$S/ov_ref_0.png|$RL|$CL|$CR|600|$RM|"
  R3="0.7467:0.3837|0.8700:0.3990"; C3="0.6489:0.3975|0.7816:0.4012"
  OV 0.5 "$RF/ref_hair_3q.png|$C/bl_hair_front3q_custom.png|$S/ov3_bl.png|$R3|$C3|0.45:0.15:1.0:0.8|600" "$RF/ref_hair_3q.png|$C/fn_hair_front3q_custom.png|$S/ov3_fn.png|$R3|$C3|0.45:0.15:1.0:0.8|600"
  B B_FACE_OVERLAY.jpg "B  pupil-aligned overlays. red lines = concept levels (brow, subnasale, stomion, menton) drawn across every frame; green = pupils. 3/4: concept gaze differs" 330 \
    "$S/ov_ref_0.png|concept (aligned), $S/ov_bl_1.png|4003557 (aligned), $S/ov_bl_0.5.png|50% concept + 4003557, $S/ov3_bl.png|3/4 50% concept + 4003557" \
    "$S/ov_ref_0.png|concept (aligned), $S/ov_fn_1.png|candidate (aligned), $S/ov_fn_0.5.png|50% concept + candidate, $S/ov3_fn.png|3/4 50% concept + candidate"
fi
if [[ $SETS == *C* ]]; then
  B C_HAIRLINE.jpg "C  hairline: concept / 4003557 (v14k) / candidate (v15c): front, crown, character-left temple, character-right temple" 300 \
    "$RF/ref_hair_front.png|concept front, $RF/ref_hair_3q.png|concept 3/4, $RF/ref_hair_close.png|concept close" \
    "$C/bl_hl_front_custom.png|4003557 hairline, $C/bl_hl_crown_custom.png|4003557 crown, $C/bl_hl_ltemple_custom.png|4003557 L temple, $C/bl_hl_rtemple_custom.png|4003557 R temple, $C/bl_hair_front3q_custom.png|4003557 3/4" \
    "$C/fn_hl_front_custom.png|candidate hairline, $C/fn_hl_crown_custom.png|candidate crown, $C/fn_hl_ltemple_custom.png|candidate L temple, $C/fn_hl_rtemple_custom.png|candidate R temple, $C/fn_hair_front3q_custom.png|candidate 3/4"
fi
if [[ $SETS == *D* ]]; then
  B D_HEAD_SHAPE.jpg "D  head shape (no hair / clay): 4003557 (top) vs candidate (bottom). Cranium / scalp unchanged; face soft tissue only" 300 \
    "$C/bl_nohair_front_custom.png|4003557 no hair front, $C/bl_nohair_side_custom.png|4003557 side, $C/bl_clay_front_custom.png|4003557 clay front, $C/bl_clay_front3q_custom.png|4003557 clay 3/4, $C/bl_clay_side_custom.png|4003557 clay side" \
    "$C/fn_nohair_front_custom.png|candidate no hair front, $C/fn_nohair_side_custom.png|candidate side, $C/fn_clay_front_custom.png|candidate clay front, $C/fn_clay_front3q_custom.png|candidate clay 3/4, $C/fn_clay_side_custom.png|candidate clay side"
fi
if [[ $SETS == *E* ]]; then
  rows=(); for l in studio grazing interior gameplay; do rows+=("$C/skC_${l}_front_custom.png|before $l front, $C/skC_${l}_3q_custom.png|before $l 3/4, $C/skH_${l}_front_custom.png|after $l front, $C/skH_${l}_3q_custom.png|after $l 3/4, $C/skH_${l}_side_custom.png|after $l side"); done
  B E_SKIN_CONTINUITY.jpg "E  skin continuity face-neck-clavicle-chest-shoulder (garments hidden). before: body C / face c3. after: body F / face c8 (seam-matched)" 300 "${rows[@]}"
  J=(); for p in skC skH; do for l in studio interior grazing gameplay; do J+=("$C/${p}_${l}_front_custom.png|$S/sz_${p}_${l}.png|0.5|0.72|0.25|520"); J+=("$C/${p}_${l}_3q_custom.png|$S/sz3_${p}_${l}.png|0.42|0.66|0.25|520"); done; done
  "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "${J[@]}" 2>&1 | grep -c CROP
  rows=(); for l in studio interior grazing gameplay; do rows+=("$S/sz_skC_$l.png|before $l front, $S/sz3_skC_$l.png|before $l 3/4, $S/sz_skH_$l.png|after $l front, $S/sz3_skH_$l.png|after $l 3/4"); done
  B E2_SEAM_ZOOM.jpg "E2  head/body seam zone zoom: before (body C, face c3) vs after (body F, face c8)" 300 "${rows[@]}"
fi
if [[ $SETS == *F* ]]; then
  L1=(neutral blink blink_left blink_right look_up look_down look_left look_right brows_up brows_down frown smile); L2=(lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w cheek_compress extreme)
  for v in front 3q; do
    r1=""; r2=""; r3=""; r4=""
    for c in "${L1[@]}"; do r1="$r1, $C/fr_rig_${c}_${v}_custom.png|$c 4003557"; r2="$r2, $C/fn_rig_${c}_${v}_custom.png|$c candidate"; done
    for c in "${L2[@]}"; do r3="$r3, $C/fr_rig_${c}_${v}_custom.png|$c 4003557"; r4="$r4, $C/fn_rig_${c}_${v}_custom.png|$c candidate"; done
    B F_EXPRESSIONS_$v.jpg "F  facial rig ($v cam, RigLogic ctrl_expressions): 4003557 face vs candidate, 23 cases" 200 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
  done
  J=(); for p in fr fn; do for c in neutral blink blink_left look_down look_up brows_up; do J+=("$C/${p}_rig_${c}_front_custom.png|$S/e_${p}_${c}.png|0.49|0.35|0.2|500"); done; for c in lips_closed ph_mbp ph_oo jaw_open smile cheek_compress; do J+=("$C/${p}_rig_${c}_front_custom.png|$S/m_${p}_${c}.png|0.5|0.64|0.2|420"); done; done
  "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "${J[@]}" 2>&1 | grep -c CROP
  r1=""; r2=""; r3=""; r4=""
  for c in neutral blink blink_left look_down look_up brows_up; do r1="$r1, $S/e_fr_$c.png|$c 4003557"; r2="$r2, $S/e_fn_$c.png|$c candidate"; done
  for c in lips_closed ph_mbp ph_oo jaw_open smile cheek_compress; do r3="$r3, $S/m_fr_$c.png|$c 4003557"; r4="$r4, $S/m_fn_$c.png|$c candidate"; done
  B F2_EXPRESSIONS_ZOOM.jpg "F2  eyelid / eyeball contact and lip seal zoom: 4003557 vs candidate" 260 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
fi
if [[ $SETS == *G* ]]; then
  "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "$C/fnl_gpcam_walk_custom.png|$S/g_gp.png|0.5|0.5|0.5|900" 2>&1 | grep -c CROP
  B G_FINAL_CONCEPT_VS_CHARACTER.jpg "G  final: concept vs face-match candidate (full front, 3/4, face close, gameplay camera)" 360 \
    "$RF/ref_full_front.png|concept full front, $RF/ref_full_3q.png|concept 3/4, $RF/ref_hair_close.png|concept face close" \
    "$C/fnl_final_front.png|candidate full front, $C/fnl_final_front3q.png|candidate 3/4, $C/fn_hair_close_custom.png|candidate face close, $C/fnl_gpcam_walk_custom.png|candidate gameplay camera (walk)"
fi
echo BOARDS_DONE $SETS
