#!/bin/bash
# make_gd3_boards.sh [board numbers] : GUARDIAN-3 new-DNA / auto-rig boards 01-22 -> Saved/Codex/CharacterGuardian3_20261001/boards
# REFERENCE (Tier A front / ~33 deg 3/4; Tier B sheets only as aid) | P (GUARDIAN-2 e9f3149 final: zgf_*, zg_<set>_*) | NEW (GUARDIAN-3 N7: zhf_*, zh_<set>_*), same cameras;
# Blender evidence (pv/): clay at the Tier A cameras (fin_*), similarity-aligned tracker overlays (vizfin_*), Tier B sheet fits (sh_*), joints (jointviz); rr4* after restart.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SEL=${1:-01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22}
K=Saved/Codex/CharacterGuardian3_20261001; O="$(cygpath -m "$(pwd)/$K/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
F="$(cygpath -m "$(pwd)/$K/frames")"; F2="$(cygpath -m "$(pwd)/Saved/Codex/CharacterGuardian2_20261001/frames")"; TD="$(cygpath -m "$(pwd)/Saved/Codex/CharacterIdentity_20260930/track")"
PV="$(cygpath -m "$(pwd)/$K/pv")"; RB="$(cygpath -m "$(pwd)/Saved/Codex/CharacterGuardian2_20261001/refB")"; RV="$(cygpath -m "$(pwd)/Saved/Codex/CharacterRevision_20260930/captures")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
RECT() { "$BL" -b --factory-startup --python $T/id_crop_rect.py -- "$@" 2>&1 | grep -c RECT; }
CROPS() { "$BL" -b --factory-startup --python $T/blender_gd_crop.py -- "$@" 2>&1 | grep -ci error; }
has() { [[ ",$SEL," == *",$1,"* ]]; }
OLD=zgf; NEW=zhf
if has 03 || has 09; then
  for v in front right left back; do for k in P:sh_headP_baseline_headP_baseline N:sh_head_new_N7_head_new_N7; do a=${k%%:*}; f=${k#*:}
    CROPS "$P/sb_${a}_${v}_ref.png" 0 340 0 482 1 "$PV/${f}_$v.png" >/dev/null; CROPS "$P/sb_${a}_${v}_clay.png" 0 340 482 964 1 "$PV/${f}_$v.png" >/dev/null
    CROPS "$P/sb_${a}_${v}_blend.png" 0 340 964 1446 1 "$PV/${f}_$v.png" >/dev/null; done; done
fi
if has 01; then
  B 01_NEW_NEUTRAL_FRONT.jpg "01 NEW NEUTRAL FRONT (bald clay, UE): Tier A reference | P (GUARDIAN-2) | NEW (GUARDIAN-3 N7, new DNA). Same Tier A front camera" 360 \
    "$TD/ref_front_x4.png|Tier A reference, $F2/${OLD}_clay_F.png|P clay, $F/${NEW}_clay_F.png|NEW clay" "$PV/fin_headP_baseline_front_clay.png|P neutral (Blender clay), $PV/fin_head_new_N7_front_clay.png|NEW neutral (Blender clay)"
fi
if has 02; then
  B 02_NEW_NEUTRAL_3Q.jpg "02 NEW NEUTRAL 3/4 (bald clay, UE) at the verified ~33 deg Tier A camera: reference | P | NEW" 360 \
    "$TD/ref_close_x2.png|Tier A reference 3/4, $F2/${OLD}_clay_C.png|P clay, $F/${NEW}_clay_C.png|NEW clay" "$PV/fin_headP_baseline_close_clay.png|P (Blender clay), $PV/fin_head_new_N7_close_clay.png|NEW (Blender clay), $C/${OLD}_clay_front3q_custom.png|P std 3/4, $C/${NEW}_clay_front3q_custom.png|NEW std 3/4"
fi
if has 03; then
  B 03_NEW_NEUTRAL_PROFILE.jpg "03 NEW NEUTRAL PROFILE: Tier B right / left (aid, one fitted orthographic scale) P vs NEW; profile lines; UE side clay" 300 \
    "$P/sb_P_right_ref.png|Tier B right (aid), $P/sb_P_right_clay.png|P, $P/sb_P_right_blend.png|P 50%, $P/sb_N_right_clay.png|NEW, $P/sb_N_right_blend.png|NEW 50%" \
    "$P/sb_P_left_ref.png|Tier B left (aid), $P/sb_P_left_clay.png|P, $P/sb_P_left_blend.png|P 50%, $P/sb_N_left_clay.png|NEW, $P/sb_N_left_blend.png|NEW 50%" \
    "$PV/prof_turnaround_p5_headP_baseline.png|profile line P, $PV/prof_turnaround_p5_head_new_N7.png|profile line NEW, $C/${OLD}_clay_side_custom.png|P side (UE), $C/${NEW}_clay_side_custom.png|NEW side (UE)"
fi
has 04 && B 04_P_VS_NEW_CLAY_FRONT.jpg "04 P vs NEW CLAY FRONT with Tier A tracker curves (green ref, red candidate, fixed camera) and similarity-aligned overlays" 380 "$PV/fin_headP_baseline_front_ov.png|P clay + Tier A, $PV/fin_head_new_N7_front_ov.png|NEW clay + Tier A, $F2/${OLD}_clay_F.png|P UE clay, $F/${NEW}_clay_F.png|NEW UE clay"
has 05 && B 05_P_VS_NEW_CLAY_3Q.jpg "05 P vs NEW CLAY 3/4 (~33 deg) with Tier A tracker curves" 380 "$PV/fin_headP_baseline_close_ov.png|P clay + Tier A, $PV/fin_head_new_N7_close_ov.png|NEW clay + Tier A, $F2/${OLD}_clay_C.png|P UE clay, $F/${NEW}_clay_C.png|NEW UE clay"
if has 06; then
  B 06_REFERENCE_OVERLAY_FRONT.jpg "06 REFERENCE OVERLAY FRONT: 50% Tier A + real-skin render (no hair); tracker overlays after per-view similarity: template (start) / P / NEW" 400 \
    "$F2/${OLD}_ovF.png|ref + P (50%), $F/${NEW}_ovF.png|ref + NEW (50%)" "$PV/vizfin_head_template_front.png|template start, $PV/vizfin_headP_baseline_front.png|P, $PV/vizfin_head_new_N7_front.png|NEW"
fi
if has 07; then
  B 07_REFERENCE_OVERLAY_3Q.jpg "07 REFERENCE OVERLAY 3/4 (~33 deg): 50% Tier A + real skin; similarity-aligned tracker overlays template / P / NEW" 400 \
    "$F2/${OLD}_ovC.png|ref + P (50%), $F/${NEW}_ovC.png|ref + NEW (50%)" "$PV/vizfin_head_template_close.png|template start, $PV/vizfin_headP_baseline_close.png|P, $PV/vizfin_head_new_N7_close.png|NEW"
fi
if has 08 || has 10 || has 11 || has 12; then
  J=(); for s in ref old new; do src=$([ $s = ref ] && echo "$TD/ref_front_x4.png" || ([ $s = old ] && echo "$F2/${OLD}_real_F.png" || echo "$F/${NEW}_real_F.png"))
    J+=("$src|$P/pl_${s}_eyes.png|0.18|0.33|0.82|0.52|480|285" "$src|$P/pl_${s}_nose.png|0.33|0.38|0.67|0.62|300|380" "$src|$P/pl_${s}_mid.png|0.08|0.40|0.92|0.70|480|340" "$src|$P/pl_${s}_mouth.png|0.26|0.57|0.74|0.72|420|260" "$src|$P/pl_${s}_jaw.png|0.12|0.60|0.88|0.86|480|330")
    src=$([ $s = ref ] && echo "$TD/ref_close_x2.png" || ([ $s = old ] && echo "$F2/${OLD}_real_C.png" || echo "$F/${NEW}_real_C.png"))
    J+=("$src|$P/pc_${s}_eyes.png|0.45|0.45|0.95|0.62|500|170" "$src|$P/pc_${s}_nose.png|0.55|0.5|0.92|0.76|370|260" "$src|$P/pc_${s}_mid.png|0.40|0.45|0.95|0.85|440|320" "$src|$P/pc_${s}_mouth.png|0.5|0.66|0.92|0.92|420|260"); done
  RECT "${J[@]}"
fi
has 08 && B 08_EYE_CENTRES_AND_ORBITS.jpg "08 EYE CENTRES / ORBITS / BROWS: Tier A | P | NEW (front, 3/4). NEW eye joints: distance 5.89 cm (P 6.08), centre z +1.3 mm; brows ~4.5 mm lower, straighter; hooded upper-lid fold" 300 "$P/pl_ref_eyes.png|reference, $P/pl_old_eyes.png|P, $P/pl_new_eyes.png|NEW" "$P/pc_ref_eyes.png|reference 3/4, $P/pc_old_eyes.png|P 3/4, $P/pc_new_eyes.png|NEW 3/4"
if has 09; then
  B 09_CRANIUM.jpg "09 CRANIUM (bald): Tier B back / front (aid) with P and NEW at one scale; UE back / top clay" 300 \
    "$P/sb_P_back_ref.png|Tier B back (aid), $P/sb_P_back_clay.png|P back, $P/sb_P_back_blend.png|P 50%, $P/sb_N_back_clay.png|NEW back, $P/sb_N_back_blend.png|NEW 50%" \
    "$P/sb_P_front_ref.png|Tier B front (aid), $P/sb_P_front_clay.png|P, $P/sb_P_front_blend.png|P 50%, $P/sb_N_front_clay.png|NEW, $P/sb_N_front_blend.png|NEW 50%" \
    "$C/${OLD}_clay_back_custom.png|P back (UE), $C/${NEW}_clay_back_custom.png|NEW back (UE), $C/${OLD}_clay_top_custom.png|P top, $C/${NEW}_clay_top_custom.png|NEW top"
fi
has 10 && B 10_MIDFACE.jpg "10 MIDFACE / CHEEKS: Tier A | P | NEW (front, then 3/4)" 300 "$P/pl_ref_mid.png|reference, $P/pl_old_mid.png|P, $P/pl_new_mid.png|NEW" "$P/pc_ref_mid.png|reference 3/4, $P/pc_old_mid.png|P 3/4, $P/pc_new_mid.png|NEW 3/4"
has 11 && B 11_NOSE.jpg "11 NOSE: Tier A | P | NEW (front, then 3/4)" 330 "$P/pl_ref_nose.png|reference, $P/pl_old_nose.png|P, $P/pl_new_nose.png|NEW" "$P/pc_ref_nose.png|reference 3/4, $P/pc_old_nose.png|P 3/4, $P/pc_new_nose.png|NEW 3/4"
has 12 && B 12_MOUTH_JAW_CHIN.jpg "12 MOUTH / JAW / CHIN: Tier A | P | NEW (front mouth, front jaw, 3/4 mouth)" 280 "$P/pl_ref_mouth.png|reference, $P/pl_old_mouth.png|P, $P/pl_new_mouth.png|NEW" "$P/pl_ref_jaw.png|reference jaw, $P/pl_old_jaw.png|P jaw, $P/pl_new_jaw.png|NEW jaw" "$P/pc_ref_mouth.png|reference 3/4, $P/pc_old_mouth.png|P 3/4, $P/pc_new_mouth.png|NEW 3/4"
if has 13; then
  B 13_AUTORIG_JOINT_VALIDATION.jpg "13 AUTO-RIG JOINT VALIDATION: P (red) = archetype DNA joints under a BR_Neutral surface; NEW (green) = Epic auto-rig joints of the new neutral (652/843 facial joints moved > 1 mm; shared spine/neck/head == body)" 640 \
    "$PV/jointviz.png|top: P joints (front, side) / bottom: NEW joints (front, side)" "$C/${NEW}_rig_neutral_front_custom.png|NEW neutral (RigLogic), $C/${NEW}_rig_blink_front_custom.png|blink, $C/${NEW}_rig_jaw_open_front_custom.png|jaw open, $C/${NEW}_rig_ph_mbp_front_custom.png|MBP lip seal"
fi
has 14 && B 14_NEUTRAL_REAL_SKIN_FRONT.jpg "14 NEUTRAL REAL SKIN FRONT (no hair): Tier A | P (c17) | NEW (skin g3s1: less yellow, slightly red-brown, darker, more pore detail, matte; iris e2 lighter brown-hazel; no wrinkles)" 520 "$TD/ref_front_x4.png|reference, $F2/${OLD}_real_F.png|P, $F/${NEW}_real_F.png|NEW"
has 15 && B 15_NEUTRAL_REAL_SKIN_3Q.jpg "15 NEUTRAL REAL SKIN 3/4 + profile (no hair): Tier A | P | NEW" 420 "$TD/ref_close_x2.png|reference 3/4, $F2/${OLD}_real_C.png|P 3/4, $F/${NEW}_real_C.png|NEW 3/4" "$C/${OLD}_real_side_custom.png|P profile, $C/${NEW}_real_side_custom.png|NEW profile, $RB/turnaround_p5.png|Tier B profile (aid)"
if has 16; then
  B 16_REFERENCE_EXPRESSION.jpg "16 REFERENCE EXPRESSION (QA pose AS_GD3_RefExpression on the new rig; NOT baked into the neutral): calm, serious, alert - not sad" 330 \
    "$TD/ref_front_x4.png|Tier A reference, $F/${NEW}_expr_neutral_F.png|identity neutral, $F/${NEW}_expr_ref_expr_soft_F.png|soft, $F/${NEW}_expr_ref_expr_F.png|ref expr, $F/${NEW}_expr_ref_expr_firm_F.png|firm" \
    "$TD/ref_close_x2.png|Tier A reference 3/4, $F/${NEW}_expr_neutral_C.png|neutral 3/4, $F/${NEW}_expr_ref_expr_soft_C.png|soft 3/4, $F/${NEW}_expr_ref_expr_C.png|ref expr 3/4, $F/${NEW}_expr_ref_expr_firm_C.png|firm 3/4"
fi
if has 17; then
  B 17_HAIR.jpg "17 HAIR: Tier A | P (id20) | NEW (id21: sparser front edge, more baby hairs / face-framing strands, lower density) - still a dense cap" 280 \
    "$TD/ref_front_x4.png|reference front, $F2/${OLD}_hair_F.png|P id20, $F/${NEW}_hair_F.png|NEW id21, $TD/ref_close_x2.png|reference 3/4, $F2/${OLD}_hair_C.png|P id20 3/4, $F/${NEW}_hair_C.png|NEW id21 3/4" \
    "$RB/turnaround_p5.png|Tier B side (aid), $C/${OLD}_hair_side_custom.png|P side, $C/${NEW}_hair_side_custom.png|NEW side, $RB/turnaround_p4.png|Tier B back (aid), $C/${OLD}_hair_back_custom.png|P back, $C/${NEW}_hair_back_custom.png|NEW back, $C/${NEW}_hair_top_custom.png|NEW crown"
fi
if has 18; then
  B 18_HEAD_NECK_BODY.jpg "18 HEAD / NECK / BODY: Tier A full body (proportions only; shorts kept) | P | NEW; head/body seam; Henley neckline sets" 360 \
    "$RV/ref_full_front.png|Tier A full front, $C/zg_full_fl_studio_front_custom.png|P, $C/zh_full_fl_studio_front_custom.png|NEW, $RV/ref_full_3q.png|Tier A full 3/4, $C/zh_full_fl_studio_3q_custom.png|NEW 3/4" \
    "$C/zh_seam_studio_front_custom.png|NEW seam studio, $C/zh_seam_gameplay_3q_custom.png|NEW seam gameplay, $C/zh_neck_nk_b00_front_custom.png|neckline 0, $C/zh_neck_nk_b30_front_custom.png|neckline 30"
fi
if has 19; then
  B 19_FULL_CHARACTER.jpg "19 FULL CHARACTER (NEW face N7 + skin g3s1 + eyes e2 + hair id21 + Henley g17e + Chaos shorts m1): studio and gameplay light, walk / jog" 380 \
    "$C/zh_full_fl_studio_front_custom.png|studio front, $C/zh_full_fl_studio_3q_custom.png|studio 3/4, $C/zh_full_fl_studio_side_custom.png|studio side, $C/zh_full_fl_studio_back_custom.png|studio back" \
    "$C/zh_full_fl_gameplay_front_custom.png|gameplay front, $C/zh_full_fl_gameplay_3q_custom.png|gameplay 3/4, $C/zh_full_fl_walk_3q_custom.png|walk, $C/zh_full_fl_jog_side_custom.png|jog"
fi
if has 20; then
  L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
  r1=""; r2=""; r3=""; r4=""; for c in "${L1[@]}"; do r1="$r1, $C/${NEW}_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/${NEW}_rig_${c}_front_custom.png|$c"; done
  for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/${NEW}_rig_${c}_3q_custom.png|$c 3/4"; done
  for c in neutral blink jaw_open smile extreme; do r4="$r4, $C/${OLD}_rig_${c}_front_custom.png|P $c"; done
  B 20_RIG_TEST.jpg "20 RIG TEST (NEW DNA, RigLogic + auto-rig blend shapes): 23 cases front, closure checks 3/4, P reference row" 170 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
fi
if has 21; then
  r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/zh_lod_${l}_front_custom.png|face $l"; done; g=""; for l in glod0 glod1 glod2; do g="$g, $C/zh_lod_${l}_3q_custom.png|garment $l"; done
  B 21_LOD_TEST.jpg "21 LOD TEST (NEW face 8 LODs from the auto-rig export; garment LODs)" 330 "${r#, }" "${g#, }"
fi
if has 22; then
  B 22_AFTER_RESTART.jpg "22 AFTER RESTART (fresh editor, assets from disk): clay / real / hair / rig / full / LOD" 300 \
    "$F/rr4f_clay_F.png|clay front, $F/rr4f_real_F.png|real front, $F/rr4f_real_C.png|real 3/4, $F/rr4f_hair_F.png|hair front, $F/rr4f_hair_C.png|hair 3/4" \
    "$C/rr4f_rig_blink_front_custom.png|blink, $C/rr4f_rig_lips_closed_front_custom.png|lips closed, $C/rr4f_rig_jaw_open_front_custom.png|jaw open, $C/rr4f_rig_extreme_front_custom.png|extreme, $C/rr4_full_fl_studio_front_custom.png|full front, $C/rr4_lod_lod2_front_custom.png|LOD2"
fi
echo GD3_BOARDS_DONE
