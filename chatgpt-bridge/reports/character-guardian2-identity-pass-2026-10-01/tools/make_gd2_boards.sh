#!/bin/bash
# make_gd2_boards.sh [board numbers] : GUARDIAN-2 identity pass boards 01-17 -> Saved/Codex/CharacterGuardian2_20261001/boards
# REFERENCE (Tier A front / 3/4; Tier B sheet panels as modelling aid) | OLD H (GUARDIAN dcb061c final: zf_*, z_<set>_*) | NEW (GUARDIAN-2 final: zgf_*, zg_<set>_*),
# same cameras (Tier A front recon cam, re-solved ~33 deg 3/4 cam camfit_close.json; Tier B orthographic sheet fit), rr3_* after restart.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SEL=${1:-01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17}
K=Saved/Codex/CharacterGuardian2_20261001; O="$(cygpath -m "$(pwd)/$K/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
F="$(cygpath -m "$(pwd)/$K/frames")"; F1="$(cygpath -m "$(pwd)/Saved/Codex/CharacterGuardian_20261001/frames")"; TD="$(cygpath -m "$(pwd)/Saved/Codex/CharacterIdentity_20260930/track")"
PV="$(cygpath -m "$(pwd)/$K/pv")"; RB="$(cygpath -m "$(pwd)/$K/refB")"; RV="$(cygpath -m "$(pwd)/Saved/Codex/CharacterRevision_20260930/captures")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
RECT() { "$BL" -b --factory-startup --python $T/id_crop_rect.py -- "$@" 2>&1 | grep -c RECT; }
CROPS() { "$BL" -b --factory-startup --python $T/blender_gd_crop.py -- "$@" 2>&1 | grep -ci error; }
has() { [[ ",$SEL," == *",$1,"* ]]; }
NEW=zgf; OLD=zf
if has 01 || has 03; then   # Tier B sheet crops (head rows 0-340 of the 492-row panels): ref | clay | 50% blend
  for v in front right left back; do for k in H:sh0_headH N:shP_headP; do a=${k%%:*}; f=${k#*:}
    CROPS "$P/sb_${a}_${v}_ref.png" 0 340 0 482 1 "$PV/${f}_$v.png" >/dev/null; CROPS "$P/sb_${a}_${v}_clay.png" 0 340 482 964 1 "$PV/${f}_$v.png" >/dev/null
    CROPS "$P/sb_${a}_${v}_blend.png" 0 340 964 1446 1 "$PV/${f}_$v.png" >/dev/null; done; done
fi
if has 01; then
  B 01_BALD_CLAY_FRONT.jpg "01 BALD CLAY FRONT: Tier A reference / OLD H / NEW (Tier A front camera); below: Tier B turnaround front (aid), OLD H vs NEW, one orthographic scale" 330 \
    "$TD/ref_front_x4.png|Tier A reference, $F1/${OLD}_clay_F.png|OLD H clay, $F/${NEW}_clay_F.png|NEW clay" \
    "$P/sb_H_front_ref.png|Tier B front (aid), $P/sb_H_front_clay.png|OLD H, $P/sb_H_front_blend.png|OLD H 50%, $P/sb_N_front_clay.png|NEW, $P/sb_N_front_blend.png|NEW 50%"
fi
if has 02; then
  B 02_BALD_CLAY_3Q.jpg "02 BALD CLAY 3/4: Tier A reference / OLD H / NEW at the re-solved ~33 deg 3/4 camera (not the old 47 deg one); standard 3/4" 330 \
    "$TD/ref_close_x2.png|Tier A reference 3/4, $F1/${OLD}_clay_C.png|OLD H clay, $F/${NEW}_clay_C.png|NEW clay" \
    "$C/${OLD}_clay_front3q_custom.png|OLD H std 3/4, $C/${NEW}_clay_front3q_custom.png|NEW std 3/4, $C/${OLD}_clay_top_custom.png|OLD H top, $C/${NEW}_clay_top_custom.png|NEW top"
fi
if has 03; then
  B 03_BALD_CLAY_PROFILES.jpg "03 BALD CLAY PROFILES: Tier B right / left profile (aid; fitted brow->menton, one scale) OLD H vs NEW; profile lines (green ref, red candidate); UE side / back clay" 300 \
    "$P/sb_H_right_ref.png|Tier B right (aid), $P/sb_H_right_clay.png|OLD H, $P/sb_H_right_blend.png|OLD H 50%, $P/sb_N_right_clay.png|NEW, $P/sb_N_right_blend.png|NEW 50%" \
    "$P/sb_H_left_ref.png|Tier B left (aid), $P/sb_H_left_clay.png|OLD H, $P/sb_H_left_blend.png|OLD H 50%, $P/sb_N_left_clay.png|NEW, $P/sb_N_left_blend.png|NEW 50%" \
    "$P/sb_H_back_ref.png|Tier B back (aid), $P/sb_H_back_clay.png|OLD H back, $P/sb_H_back_blend.png|OLD H 50%, $P/sb_N_back_clay.png|NEW back, $P/sb_N_back_blend.png|NEW 50%" \
    "$PV/prof_turnaround_p5_headH.png|profile line OLD H, $PV/prof_turnaround_p5_headP.png|profile line NEW, $C/${OLD}_clay_side_custom.png|OLD H side, $C/${NEW}_clay_side_custom.png|NEW side, $C/${OLD}_clay_back_custom.png|OLD H back, $C/${NEW}_clay_back_custom.png|NEW back"
fi
has 04 && B 04_ORIGINAL_OVERLAY_FRONT.jpg "04 ORIGINAL OVERLAY FRONT (50% Tier A reference + real-skin candidate, no hair): OLD H vs NEW" 560 "$F1/${OLD}_ovF.png|ref + OLD H, $F/${NEW}_ovF.png|ref + NEW"
has 05 && B 05_ORIGINAL_OVERLAY_3Q.jpg "05 ORIGINAL OVERLAY 3/4 (50% Tier A reference + candidate, re-solved ~33 deg camera): OLD H vs NEW" 560 "$F1/${OLD}_ovC.png|ref + OLD H, $F/${NEW}_ovC.png|ref + NEW"
if has 06 || has 07 || has 08 || has 09; then
  J=(); for s in ref old new; do src=$([ $s = ref ] && echo "$TD/ref_front_x4.png" || ([ $s = old ] && echo "$F1/${OLD}_real_F.png" || echo "$F/${NEW}_real_F.png"))
    J+=("$src|$P/pl_${s}_eyes.png|0.18|0.33|0.82|0.52|480|285" "$src|$P/pl_${s}_nose.png|0.33|0.38|0.67|0.62|300|380" "$src|$P/pl_${s}_mid.png|0.08|0.40|0.92|0.70|480|340" "$src|$P/pl_${s}_mouth.png|0.26|0.57|0.74|0.72|420|260" "$src|$P/pl_${s}_jaw.png|0.12|0.60|0.88|0.86|480|330")
    src=$([ $s = ref ] && echo "$TD/ref_close_x2.png" || ([ $s = old ] && echo "$F1/${OLD}_real_C.png" || echo "$F/${NEW}_real_C.png"))
    J+=("$src|$P/pc_${s}_eyes.png|0.45|0.45|0.95|0.62|500|170" "$src|$P/pc_${s}_nose.png|0.55|0.5|0.92|0.76|370|260" "$src|$P/pc_${s}_mid.png|0.40|0.45|0.95|0.85|440|320" "$src|$P/pc_${s}_mouth.png|0.5|0.66|0.92|0.92|420|260"); done
  RECT "${J[@]}"
fi
has 06 && B 06_EYES_ORBITS.jpg "06 EYES / ORBITS / BROWS: Tier A reference / OLD H / NEW (front, then 3/4)" 300 "$P/pl_ref_eyes.png|reference, $P/pl_old_eyes.png|OLD H, $P/pl_new_eyes.png|NEW" "$P/pc_ref_eyes.png|reference 3/4, $P/pc_old_eyes.png|OLD H 3/4, $P/pc_new_eyes.png|NEW 3/4"
has 07 && B 07_NOSE.jpg "07 NOSE: Tier A reference / OLD H / NEW (front, then 3/4)" 330 "$P/pl_ref_nose.png|reference, $P/pl_old_nose.png|OLD H, $P/pl_new_nose.png|NEW" "$P/pc_ref_nose.png|reference 3/4, $P/pc_old_nose.png|OLD H 3/4, $P/pc_new_nose.png|NEW 3/4"
has 08 && B 08_MIDFACE_CHEEKS.jpg "08 MIDFACE / CHEEKS: Tier A reference / OLD H / NEW (front, then 3/4)" 300 "$P/pl_ref_mid.png|reference, $P/pl_old_mid.png|OLD H, $P/pl_new_mid.png|NEW" "$P/pc_ref_mid.png|reference 3/4, $P/pc_old_mid.png|OLD H 3/4, $P/pc_new_mid.png|NEW 3/4"
has 09 && B 09_MOUTH_JAW_CHIN.jpg "09 MOUTH / JAW / CHIN: Tier A reference / OLD H / NEW (front mouth, front jaw, 3/4 mouth)" 280 "$P/pl_ref_mouth.png|reference, $P/pl_old_mouth.png|OLD H, $P/pl_new_mouth.png|NEW" "$P/pl_ref_jaw.png|reference jaw, $P/pl_old_jaw.png|OLD H jaw, $P/pl_new_jaw.png|NEW jaw" "$P/pc_ref_mouth.png|reference 3/4, $P/pc_old_mouth.png|OLD H 3/4, $P/pc_new_mouth.png|NEW 3/4"
has 10 && B 10_REAL_SKIN_FRONT.jpg "10 REAL SKIN FRONT (neutral, no hair): Tier A reference / OLD H (c14s) / NEW (c17: cheek patch toned down, light freckles, muted lips; no wrinkles)" 520 "$TD/ref_front_x4.png|reference, $F1/${OLD}_real_F.png|OLD H, $F/${NEW}_real_F.png|NEW"
has 11 && B 11_REAL_SKIN_3Q.jpg "11 REAL SKIN 3/4 + profile (neutral, no hair): Tier A reference / OLD H / NEW" 420 "$TD/ref_close_x2.png|reference 3/4, $F1/${OLD}_real_C.png|OLD H 3/4, $F/${NEW}_real_C.png|NEW 3/4" "$C/${OLD}_real_side_custom.png|OLD H profile, $C/${NEW}_real_side_custom.png|NEW profile, $RB/turnaround_p5.png|Tier B profile (aid)"
if has 12; then
  B 12_REFERENCE_EXPRESSION.jpg "12 REFERENCE EXPRESSION (QA pose AS_GD2_RefExpression on the rig, NOT baked into the neutral): neutral / soft / ref_expr / firm" 330 \
    "$TD/ref_front_x4.png|Tier A reference, $F/${NEW}_expr_neutral_F.png|identity neutral, $F/${NEW}_expr_ref_expr_soft_F.png|ref expr soft, $F/${NEW}_expr_ref_expr_F.png|ref expr, $F/${NEW}_expr_ref_expr_firm_F.png|ref expr firm" \
    "$TD/ref_close_x2.png|Tier A reference 3/4, $F/${NEW}_expr_neutral_C.png|neutral 3/4, $F/${NEW}_expr_ref_expr_soft_C.png|soft 3/4, $F/${NEW}_expr_ref_expr_C.png|ref expr 3/4, $F/${NEW}_expr_ref_expr_firm_C.png|firm 3/4"
fi
if has 13; then
  B 13_HAIR_REFERENCE.jpg "13 HAIR: Tier A reference / OLD id18 / NEW id20 (looser crown than id18 without the id19 lumps, wider temporal mass, bigger irregular low bun, more nape escapes, darker brown-first auburn, no light tips)" 280 \
    "$TD/ref_front_x4.png|reference front, $F1/${OLD}_hair_F.png|OLD id18, $F/${NEW}_hair_F.png|NEW id20, $TD/ref_close_x2.png|reference 3/4, $F1/${OLD}_hair_C.png|OLD id18 3/4, $F/${NEW}_hair_C.png|NEW id20 3/4" \
    "$RB/turnaround_p5.png|Tier B side (aid), $C/${OLD}_hair_side_custom.png|OLD side, $C/${NEW}_hair_side_custom.png|NEW side, $RB/turnaround_p4.png|Tier B back (aid), $C/${OLD}_hair_back_custom.png|OLD back, $C/${NEW}_hair_back_custom.png|NEW back, $C/${NEW}_hair_top_custom.png|NEW crown"
fi
if has 14; then
  B 14_HEAD_NECK_BODY.jpg "14 HEAD / NECK / BODY: Tier A full-body original (proportions only; shorts kept, no long pants) / OLD H / NEW; Henley neckline under torso bend + head/body seam" 360 \
    "$RV/ref_full_front.png|Tier A full front, $C/z_full_fl_studio_front_custom.png|OLD H, $C/zg_full_fl_studio_front_custom.png|NEW, $RV/ref_full_3q.png|Tier A full 3/4, $C/zg_full_fl_studio_3q_custom.png|NEW 3/4" \
    "$C/zg_neck_nk_b00_front_custom.png|Henley neckline bend 0, $C/zg_neck_nk_b30_front_custom.png|neckline bend 30, $C/zg_neck_nk_b60_3q_custom.png|neckline bend 60 3/4, $C/zg_seam_studio_front_custom.png|head/body seam studio, $C/zg_seam_gameplay_3q_custom.png|seam gameplay light"
fi
if has 15; then
  B 15_FULL_CHARACTER.jpg "15 FULL CHARACTER (NEW face P + skin c17 + hair id20 + Henley g17e + Chaos shorts m1): studio and gameplay light, walk / jog" 380 \
    "$C/zg_full_fl_studio_front_custom.png|studio front, $C/zg_full_fl_studio_3q_custom.png|studio 3/4, $C/zg_full_fl_studio_side_custom.png|studio side, $C/zg_full_fl_studio_back_custom.png|studio back" \
    "$C/zg_full_fl_gameplay_front_custom.png|gameplay front, $C/zg_full_fl_gameplay_3q_custom.png|gameplay 3/4, $C/zg_full_fl_walk_3q_custom.png|walk, $C/zg_full_fl_jog_side_custom.png|jog"
fi
if has 16; then
  L1=(neutral blink blink_left look_left look_up brows_up brows_down frown smile cheek_compress); L2=(lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
  r1=""; r2=""; r3=""; r4=""; for c in "${L1[@]}"; do r1="$r1, $C/${OLD}_rig_${c}_front_custom.png|$c OLD H"; r2="$r2, $C/${NEW}_rig_${c}_front_custom.png|$c NEW"; done
  for c in "${L2[@]}"; do r3="$r3, $C/${OLD}_rig_${c}_front_custom.png|$c OLD H"; r4="$r4, $C/${NEW}_rig_${c}_front_custom.png|$c NEW"; done
  r5=""; for c in blink lips_closed ph_mbp jaw_open smile extreme; do r5="$r5, $C/${NEW}_rig_${c}_3q_custom.png|$c NEW 3/4"; done
  r6=""; for l in lod0 lod1 lod2 lod3; do r6="$r6, $C/zg_lod_${l}_front_custom.png|face $l"; done; for l in glod0 glod1 glod2; do r6="$r6, $C/zg_lod_${l}_3q_custom.png|garment $l"; done
  B 16_RIG_EXPRESSION_CHECK.jpg "16 RIG / EXPRESSION CHECK (RigLogic, same DNA; NEW neutral via BR_Neutral): OLD H vs NEW, 3/4 closure checks, LODs" 180 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }" "${r5#, }" "${r6#, }"
fi
if has 17; then
  B 17_AFTER_RESTART.jpg "17 AFTER RESTART (fresh editor, assets loaded from disk): face clay / real / hair / rig / full / LOD" 300 \
    "$F/rr3f_clay_F.png|clay front, $F/rr3f_real_F.png|real front, $F/rr3f_real_C.png|real 3/4, $F/rr3f_hair_F.png|hair front, $F/rr3f_hair_C.png|hair 3/4" \
    "$C/rr3f_rig_blink_front_custom.png|blink, $C/rr3f_rig_lips_closed_front_custom.png|lips closed, $C/rr3f_rig_jaw_open_front_custom.png|jaw open, $C/rr3f_rig_extreme_front_custom.png|extreme, $C/rr3_full_fl_studio_front_custom.png|full front, $C/rr3_lod_lod2_front_custom.png|LOD2"
fi
echo GD2_BOARDS_DONE
