#!/bin/bash
# make_id_boards.sh [list of board numbers, default all] : IDENTITY pass evidence boards 01-15 -> Saved/Codex/CharacterIdentity_20260930/boards
# 889b1d9 baseline captures: i0_* (face / hair at the reference-solved cams), fn_hl_* (hairline), fn_rig_* (facial rig), fx2_full_* / fnl_* (full body),
#   x889_* (shorts / Henley cams), d889_dfm_* (deformation), skH_* (skin seam)
# new candidate: if_* (face clay / real / hair / rig), ifh_hl_* (hairline), ifx_* (full, head-shoulder poses, LODs, shorts / Henley cams),
#   ifl_* (final views, deformation, gameplay), skN_* (skin seam), iv_* (after restart)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SEL=${1:-01,02,03,04,05,06,07,08,09,10,11,12,13,14,15}
I=Saved/Codex/CharacterIdentity_20260930; O="$(cygpath -m "$(pwd)/$I/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
TD="$(cygpath -m "$(pwd)/$I/track")"; RF_="$(cygpath -m "$(pwd)/Saved/Codex/CharacterRevision_20260930/captures")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
RF=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json front 800 960 '[0.95,129.7,170.3,-90.4,-3.8]' 15); RC=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json close 794 940 '[-91.0,88.6,143.3,-42.6,8.6]' 15)
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
RECT() { "$BL" -b --factory-startup --python $T/id_crop_rect.py -- "$@" 2>&1 | grep -c RECT; }
CROP() { "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "$@" 2>&1 | grep -c CROP; }
has() { [[ ",$SEL," == *",$1,"* ]]; }
# ---- matched reference frames (face) for 889 / new
J=(); for p in i0 if; do for m in clay real hair; do J+=("$C/${p}_${m}_reffront_custom.png|$P/${p}_${m}_F.png|${RF}|400|480" "$C/${p}_${m}_refclose_custom.png|$P/${p}_${m}_C.png|${RC}|397|470"); done
  J+=("$C/${p}_real_reffront_custom.png|$P/${p}_ovF.png|${RF}|400|480|$TD/ref_front_x4.png" "$C/${p}_real_refclose_custom.png|$P/${p}_ovC.png|${RC}|397|470|$TD/ref_close_x2.png"); done
RECT "${J[@]}"
if has 01; then
  B 01_FACE_CLAY_REFERENCE.jpg "01 FACE (bald, neutral clay): reference / 889b1d9 / identity candidate. Front + 3/4 at the reference-solved cameras, profile (no reference profile exists)" 300 \
    "$TD/ref_front_x4.png|reference front, $P/i0_clay_F.png|889b1d9 clay, $P/if_clay_F.png|candidate clay" "$TD/ref_close_x2.png|reference 3/4, $P/i0_clay_C.png|889b1d9 clay, $P/if_clay_C.png|candidate clay" \
    "$C/i0_clay_side_custom.png|889b1d9 clay profile, $C/if_clay_side_custom.png|candidate clay profile, $C/i0_clay_front3q_custom.png|889b1d9 clay 3/4 std, $C/if_clay_front3q_custom.png|candidate clay 3/4 std"
fi
if has 02; then
  B 02_FACE_OVERLAY.jpg "02 FACE 50% overlays (pupil / pose matched): reference + 889b1d9 vs reference + candidate" 330 "$P/i0_ovF.png|ref + 889b1d9 front, $P/if_ovF.png|ref + candidate front, $P/i0_ovC.png|ref + 889b1d9 3/4, $P/if_ovC.png|ref + candidate 3/4"
fi
if has 03; then
  J=(); for s in ref i0 if; do src=$([ $s = ref ] && echo "$TD/ref_front_x4.png" || echo "$P/${s}_real_F.png")
    J+=("$src|$P/pl_${s}_eyes.png|0.18|0.33|0.82|0.52|480|285" "$src|$P/pl_${s}_nose.png|0.33|0.40|0.67|0.62|300|380" "$src|$P/pl_${s}_cheek.png|0.10|0.42|0.90|0.68|480|300" "$src|$P/pl_${s}_mouth.png|0.26|0.57|0.74|0.72|420|260" "$src|$P/pl_${s}_jaw.png|0.12|0.60|0.88|0.86|480|330"); done
  RECT "${J[@]}"
  rows=(); for r in eyes nose cheek mouth jaw; do rows+=("$P/pl_ref_$r.png|reference $r, $P/pl_i0_$r.png|889b1d9 $r, $P/pl_if_$r.png|candidate $r"); done
  B 03_FACE_PLANES.jpg "03 FACE PLANES (front, matched frame): eyes / orbits, nose, cheek / midface, mouth, jaw / chin" 260 "${rows[@]}"
fi
if has 04; then
  B 04_HEAD_SHAPE.jpg "04 HEAD SHAPE (bald, real skin): 889b1d9 (top) vs candidate (bottom): front, 3/4, profile, back" 280 \
    "$C/i0_real_reffront_custom.png|889b1d9 front, $C/i0_real_front3q_custom.png|889b1d9 3/4, $C/i0_real_side_custom.png|889b1d9 profile, $C/i0_clay_front_custom.png|889b1d9 clay front" \
    "$C/if_real_reffront_custom.png|candidate front, $C/if_real_front3q_custom.png|candidate 3/4, $C/if_real_side_custom.png|candidate profile, $C/if_clay_back_custom.png|candidate clay back"
fi
if has 05; then
  RECT "$C/i0_hair_reffront_custom.png|$P/i0_hairS_F.png|${RF}|800|960" "$C/i0_hair_refclose_custom.png|$P/i0_hairS_C.png|${RC}|794|940" "$C/if_hair_reffront_custom.png|$P/if_hairS_F.png|${RF}|800|960" "$C/if_hair_refclose_custom.png|$P/if_hairS_C.png|${RC}|794|940"
  "$BL" -b --factory-startup --python $T/id_silhouette.py -- "$TD/ref_front_x4.png|$P/sil_ref_F_889.png|0.07|$P/i0_hairS_F.png" "$TD/ref_close_x2.png|$P/sil_ref_C_889.png|0.07|$P/i0_hairS_C.png" \
    "$TD/ref_front_x4.png|$P/sil_ref_F_new.png|0.07|$P/if_hairS_F.png" "$TD/ref_close_x2.png|$P/sil_ref_C_new.png|0.07|$P/if_hairS_C.png" "$TD/ref_front_x4.png|$P/sil_ref_F.png|0.07" "$TD/ref_close_x2.png|$P/sil_ref_C.png|0.07" \
    "$C/i0_hair_side_custom.png|$P/sil_S_889.png|0.07" "$C/if_hair_side_custom.png|$P/sil_S_new.png|0.07" "$C/i0_hair_back_custom.png|$P/sil_B_889.png|0.07" "$C/if_hair_back_custom.png|$P/sil_B_new.png|0.07" 2>&1 | grep -c SIL
  B 05_HAIR_SILHOUETTE.jpg "05 HAIR SILHOUETTE: reference (black) with 889b1d9 / candidate outline (red; pink = candidate outside reference). Profile / back: no reference view" 280 \
    "$P/sil_ref_F.png|reference front, $P/sil_ref_F_889.png|889b1d9 front, $P/sil_ref_F_new.png|candidate front" "$P/sil_ref_C.png|reference 3/4, $P/sil_ref_C_889.png|889b1d9 3/4, $P/sil_ref_C_new.png|candidate 3/4" \
    "$P/sil_S_889.png|889b1d9 profile, $P/sil_S_new.png|candidate profile, $P/sil_B_889.png|889b1d9 back, $P/sil_B_new.png|candidate back"
fi
if has 06; then
  B 06_HAIR_FORM.jpg "06 HAIR FORM: reference / 889b1d9 / candidate: front, 3/4, profile, back, top, temples, bun, face locks" 250 \
    "$TD/ref_front_x4.png|reference front, $TD/ref_close_x2.png|reference 3/4, $TD/ref_3q_x4.png|reference 3/4 (full)" \
    "$P/i0_hair_F.png|889b1d9 front, $P/i0_hair_C.png|889b1d9 3/4, $C/i0_hair_side_custom.png|889b1d9 profile, $C/i0_hair_back_custom.png|889b1d9 back / bun, $C/i0_hair_top_custom.png|889b1d9 top, $C/fn_hl_ltemple_custom.png|889b1d9 L temple" \
    "$P/if_hair_F.png|candidate front, $P/if_hair_C.png|candidate 3/4, $C/if_hair_side_custom.png|candidate profile, $C/if_hair_back_custom.png|candidate back / bun, $C/if_hair_top_custom.png|candidate top, $C/ifh_hl_ltemple_custom.png|candidate L temple"
fi
if has 07; then
  B 07_HAIRLINE.jpg "07 HAIRLINE: reference / 889b1d9 (v15c) / candidate: front hairline, crown, left + right temple" 280 \
    "$TD/ref_front_x4.png|reference front, $TD/ref_close_x2.png|reference 3/4" \
    "$C/fn_hl_front_custom.png|889b1d9 hairline, $C/fn_hl_crown_custom.png|889b1d9 crown, $C/fn_hl_ltemple_custom.png|889b1d9 L temple, $C/fn_hl_rtemple_custom.png|889b1d9 R temple" \
    "$C/ifh_hl_front_custom.png|candidate hairline, $C/ifh_hl_crown_custom.png|candidate crown, $C/ifh_hl_ltemple_custom.png|candidate L temple, $C/ifh_hl_rtemple_custom.png|candidate R temple"
fi
if has 08; then
  RECT "$C/ifx_full_front_custom.png|$P/new_sh_F.png|0.35|0.41|0.65|0.685|600|550" "$C/fx2_full_front_custom.png|$P/old_sh_F.png|0.35|0.41|0.65|0.685|600|550" "$RF_/ref_full_front.png|$P/ref_sh_F.png|-0.0775|0.3845|1.0775|0.6862|600|550"
  M=$("$PY" -c "import json; d=json.load(open('$I/shorts_measure.json')); f=lambda k: 'crotch sag %.1f cm, waistband-crotch %.1f, inseam %.1f, rise F/B %.1f/%.1f' % (d[k]['crotch_sag_below_body_cm'], d[k]['waistband_top_to_crotch_fabric_cm'], d[k]['inseam_below_body_crotch_cm'], d[k]['front_rise_cm'], d[k]['back_rise_cm']); print(f('g14h')+'|'+f('$NEWG'))")
  B 08_SHORTS_PATTERN_PROPORTION.jpg "08 SHORTS PATTERN / PROPORTION (front, z 55-110 cm same scale). body crotch z 76.5 cm" 420 "$P/ref_sh_F.png|reference, $P/old_sh_F.png|889b1d9 g14h: ${M%%|*}, $P/new_sh_F.png|candidate $NEWG: ${M#*|}"
fi
if has 09; then
  B 09_SHORTS_FINAL.jpg "09 SHORTS: reference / 889b1d9 (g14h) / candidate: front, 3/4, side, rear, crotch, seat, hem" 230 \
    "$RF_/ref_shorts_front.png|reference front, $RF_/ref_shorts_3q.png|reference 3/4" \
    "$C/x889_sh_front_custom.png|889 front, $C/x889_sh_3q_custom.png|889 3/4, $C/x889_sh_side_custom.png|889 side, $C/x889_sh_rear_custom.png|889 rear, $C/x889_sh_crotch_custom.png|889 crotch, $C/x889_sh_seat_custom.png|889 seat, $C/x889_sh_hem_custom.png|889 hem" \
    "$C/ifx_sh_front_custom.png|new front, $C/ifx_sh_3q_custom.png|new 3/4, $C/ifx_sh_side_custom.png|new side, $C/ifx_sh_rear_custom.png|new rear, $C/ifx_sh_crotch_custom.png|new crotch, $C/ifx_sh_seat_custom.png|new seat, $C/ifx_sh_hem_custom.png|new hem"
fi
if has 10; then
  RECT "$RF_/ref_full_front.png|$P/ref_hen_F.png|0|0.13|1|0.47|400|476" "$RF_/ref_full_3q.png|$P/ref_hen_3q.png|0|0.13|1|0.47|340|476"
  B 10_HENLEY_FINAL.jpg "10 HENLEY: reference / 889b1d9 (g14h) / candidate: front, 3/4, side, back" 260 \
    "$P/ref_hen_F.png|reference front, $P/ref_hen_3q.png|reference 3/4, $RF_/ref_neck_close.png|reference neckline" \
    "$C/x889_hen_front_custom.png|889 front, $C/x889_hen_3q_custom.png|889 3/4, $C/x889_hen_side_custom.png|889 side, $C/x889_hen_back_custom.png|889 back" \
    "$C/ifx_hen_front_custom.png|new front, $C/ifx_hen_3q_custom.png|new 3/4, $C/ifx_hen_side_custom.png|new side, $C/ifx_hen_back_custom.png|new back"
fi
if has 11; then
  B 11_FULL_CHARACTER.jpg "11 FULL CHARACTER: reference / 889b1d9 / candidate: front, 3/4, side, gameplay camera" 300 \
    "$RF_/ref_full_front.png|reference front, $RF_/ref_full_3q.png|reference 3/4" \
    "$C/fx2_full_front_custom.png|889 front, $C/fx2_full_3q_custom.png|889 3/4, $C/fnl_final_side.png|889 side, $C/fnl_gpcam_walk_custom.png|889 gameplay (walk)" \
    "$C/ifx_full_front_custom.png|candidate front, $C/ifx_full_3q_custom.png|candidate 3/4, $C/ifl_final_side.png|candidate side, $C/ifl_gpcam_walk_custom.png|candidate gameplay (walk)"
fi
if has 12; then
  J=(); for p in skH skN; do for l in studio grazing interior gameplay; do J+=("$C/${p}_${l}_3q_custom.png|$P/sk3_${p}_${l}.png|0.42|0.66|0.25|480" "$C/${p}_${l}_front_custom.png|$P/skf_${p}_${l}.png|0.5|0.72|0.25|480"); done; done; CROP "${J[@]}"
  rows=(); for l in studio grazing interior gameplay; do rows+=("$P/sk3_skH_$l.png|889 $l 3/4, $P/sk3_skN_$l.png|candidate $l 3/4, $P/skf_skH_$l.png|889 $l front, $P/skf_skN_$l.png|candidate $l front"); done
  B 12_SKIN_SEAM.jpg "12 HEAD / BODY SEAM (garments hidden): 889b1d9 vs candidate (seam-blended head normal map, body roughness match), 4 lights" 260 "${rows[@]}"
fi
if has 13; then
  L1=(neutral blink blink_left blink_right look_up look_down look_left look_right brows_up brows_down frown smile); L2=(lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w cheek_compress extreme)
  for v in front 3q; do r1=""; r2=""; r3=""; r4=""
    for c in "${L1[@]}"; do r1="$r1, $C/fn_rig_${c}_${v}_custom.png|$c 889b1d9"; r2="$r2, $C/if_rig_${c}_${v}_custom.png|$c candidate"; done
    for c in "${L2[@]}"; do r3="$r3, $C/fn_rig_${c}_${v}_custom.png|$c 889b1d9"; r4="$r4, $C/if_rig_${c}_${v}_custom.png|$c candidate"; done
    B 13_FACE_EXPRESSIONS_$v.jpg "13 FACIAL RIG ($v cam): 889b1d9 vs candidate, 23 RigLogic cases" 190 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"; done
fi
if has 14; then
  J=(); for p in d889 ifl; do for q in neutral pl_stride crouch squat hipflex pl_highknee_l; do for v in front side; do J+=("$C/${p}_dfm_${q}_${v}.png|$P/dm_${p}_${q}_${v}.png|0.5|0.55|0.2|320"); done; done; done; CROP "${J[@]}"
  rows=(); for v in front side; do r1=""; r2=""; for q in neutral pl_stride crouch squat hipflex pl_highknee_l; do r1="$r1, $P/dm_d889_${q}_${v}.png|889 $q $v"; r2="$r2, $P/dm_ifl_${q}_${v}.png|new $q $v"; done; rows+=("${r1#, }" "${r2#, }"); done
  rows+=("$C/ifx_hs_pl_twist_l_front_custom.png|head turn L, $C/ifx_hs_pl_twist_r_front_custom.png|head turn R, $C/ifx_hs_pl_bend45_side_custom.png|neck / trunk bend, $C/ifx_hs_walk_front_custom.png|walk")
  B 14_DEFORMATION.jpg "14 DEFORMATION: shorts / Henley under walk-stride, crouch, squat, hip flex, high knee (889b1d9 vs candidate) + bindings under turn / bend" 220 "${rows[@]}"
fi
if has 15; then
  r1=""; r2=""; for c in neutral blink smile jaw_open ph_mbp extreme; do r1="$r1, $C/if_rig_${c}_front_custom.png|$c before restart"; r2="$r2, $C/iv_rig_${c}_front_custom.png|$c after restart"; done
  B 15_AFTER_RESTART.jpg "15 AFTER RESTART (fresh editor, reopened from disk): facial rig before vs after restart + LOD0-3 + full character" 230 "${r1#, }" "${r2#, }" \
    "$C/iv_lod0_front_custom.png|LOD0, $C/iv_lod1_front_custom.png|LOD1, $C/iv_lod2_front_custom.png|LOD2, $C/iv_lod3_front_custom.png|LOD3, $C/iv_full_front_custom.png|full front after restart, $C/iv_full_3q_custom.png|full 3/4 after restart"
fi
echo ID_BOARDS_DONE $SEL
