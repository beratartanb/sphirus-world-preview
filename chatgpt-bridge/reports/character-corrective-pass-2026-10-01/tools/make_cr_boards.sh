#!/bin/bash
# make_cr_boards.sh [board numbers, default all] : CORRECTIVE pass evidence boards 01-14 -> Saved/Codex/CharacterCorrective_20261001/boards
# 6255d92 baseline captures: if_* (face clay / real / hair / rig), ifx_* (shorts / Henley / full), skN_* (seam)
# corrective candidate: cj_* (face / hair / rig, final), ks_* / sc4_* (shorts skinned g16a / selective Chaos), kc_* / hc3_* (Henley skinned g16c / hybrid g16d + Chaos hem),
#   kw_* / hw_* (waistband interaction), fn_* (neckline progression, final), ff_* (full character, final), sk2_* (seam), rr_* (after restart)
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SEL=${1:-01,02,03,04,05,06,07,08,09,10,11,12,13,14}
I=Saved/Codex/CharacterIdentity_20260930; K=Saved/Codex/CharacterCorrective_20261001; O="$(cygpath -m "$(pwd)/$K/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
TD="$(cygpath -m "$(pwd)/$I/track")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
RF=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json front 800 960 '[0.95,129.7,170.3,-90.4,-3.8]' 15); RC=$("$PY" $T/id_ref_frame.py $I/recon_c/recon.json close 794 940 '[-91.0,88.6,143.3,-42.6,8.6]' 15)
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
RECT() { "$BL" -b --factory-startup --python $T/id_crop_rect.py -- "$@" 2>&1 | grep -c RECT; }
CROP() { "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "$@" 2>&1 | grep -c CROP; }
has() { [[ ",$SEL," == *",$1,"* ]]; }
# row <prefixA> <prefixB> <case> <labelA> <labelB> <views...> : A/B cells per view
row() { local a=$1 b=$2 kind=$3 la=$4 lb=$5 r="" v; shift 5; for v in "$@"; do r="$r, ${a}_${kind}_${v}_custom.png|$la $kind $v, ${b}_${kind}_${v}_custom.png|$lb $v"; done; echo "${r#, }"; }
if has 01 || has 02 || has 03 || has 04; then
  J=(); for p in if cj; do for m in clay real hair; do J+=("$C/${p}_${m}_reffront_custom.png|$P/${p}_${m}_F.png|${RF}|400|480" "$C/${p}_${m}_refclose_custom.png|$P/${p}_${m}_C.png|${RC}|397|470"); done
    J+=("$C/${p}_real_reffront_custom.png|$P/${p}_ovF.png|${RF}|400|480|$TD/ref_front_x4.png" "$C/${p}_real_refclose_custom.png|$P/${p}_ovC.png|${RC}|397|470|$TD/ref_close_x2.png"); done
  RECT "${J[@]}"
fi
if has 01; then
  B 01_FACE_CLEANUP.jpg "01 FACE CLEANUP (ageing removed): reference / 6255d92 / corrective candidate. Bald clay + real skin, front, 3/4 (reference-solved cams), profile" 270 \
    "$TD/ref_front_x4.png|reference front, $P/if_clay_F.png|6255d92 clay, $P/cj_clay_F.png|new clay, $P/if_real_F.png|6255d92 skin, $P/cj_real_F.png|new skin" \
    "$TD/ref_close_x2.png|reference 3/4, $P/if_clay_C.png|6255d92 clay, $P/cj_clay_C.png|new clay, $P/if_real_C.png|6255d92 skin, $P/cj_real_C.png|new skin" \
    "$C/if_clay_side_custom.png|6255d92 clay profile, $C/cj_clay_side_custom.png|new clay profile, $C/if_real_side_custom.png|6255d92 skin profile, $C/cj_real_side_custom.png|new skin profile"
fi
if has 02; then
  J=(); for s in ref if cj; do src=$([ $s = ref ] && echo "$TD/ref_front_x4.png" || echo "$P/${s}_real_F.png")
    J+=("$src|$P/pl_${s}_eyes.png|0.18|0.33|0.82|0.52|480|285" "$src|$P/pl_${s}_nose.png|0.33|0.40|0.67|0.62|300|380" "$src|$P/pl_${s}_cheek.png|0.10|0.42|0.90|0.68|480|300" "$src|$P/pl_${s}_mouth.png|0.26|0.57|0.74|0.72|420|260" "$src|$P/pl_${s}_jaw.png|0.12|0.60|0.88|0.86|480|330"); done
  RECT "${J[@]}"
  rows=("$P/if_ovF.png|50% ref + 6255d92 front, $P/cj_ovF.png|50% ref + new front, $P/if_ovC.png|50% ref + 6255d92 3/4, $P/cj_ovC.png|50% ref + new 3/4")
  for r in eyes nose cheek mouth jaw; do rows+=("$P/pl_ref_$r.png|reference $r, $P/pl_if_$r.png|6255d92 $r, $P/pl_cj_$r.png|new $r"); done
  B 02_FACE_PLANES.jpg "02 FACE PLANES + 50% overlays (pupil / pose matched): eyes / orbits, nose, cheek / midface, mouth, jaw / chin" 250 "${rows[@]}"
fi
if has 03; then
  B 03_FACE_SKIN_NEUTRAL.jpg "03 FACE SKIN (neutral, brows + lashes, no hair): 6255d92 (top) vs face j + skin c12 (bottom): front, 3/4, profile, close" 300 \
    "$C/if_real_front_custom.png|6255d92 front, $C/if_real_front3q_custom.png|6255d92 3/4, $C/if_real_side_custom.png|6255d92 profile, $P/if_real_C.png|6255d92 ref 3/4" \
    "$C/cj_real_front_custom.png|new front, $C/cj_real_front3q_custom.png|new 3/4, $C/cj_real_side_custom.png|new profile, $P/cj_real_C.png|new ref 3/4"
fi
if has 04; then
  RECT "$C/if_hair_reffront_custom.png|$P/if_hairS_F.png|${RF}|800|960" "$C/if_hair_refclose_custom.png|$P/if_hairS_C.png|${RC}|794|940" "$C/cj_hair_reffront_custom.png|$P/cj_hairS_F.png|${RF}|800|960" "$C/cj_hair_refclose_custom.png|$P/cj_hairS_C.png|${RC}|794|940"
  "$BL" -b --factory-startup --python $T/id_silhouette.py -- "$TD/ref_front_x4.png|$P/sil_ref_F_old.png|0.07|$P/if_hairS_F.png" "$TD/ref_close_x2.png|$P/sil_ref_C_old.png|0.07|$P/if_hairS_C.png" \
    "$TD/ref_front_x4.png|$P/sil_ref_F_new.png|0.07|$P/cj_hairS_F.png" "$TD/ref_close_x2.png|$P/sil_ref_C_new.png|0.07|$P/cj_hairS_C.png" 2>&1 | grep -c SIL
  B 04_HAIR_FINAL.jpg "04 HAIR (id17): silhouette vs reference (red outline; pink = outside reference), 6255d92 vs new: front, 3/4, profile, back, top" 250 \
    "$P/sil_ref_F_old.png|6255d92 silhouette front, $P/sil_ref_F_new.png|new silhouette front, $P/sil_ref_C_old.png|6255d92 silhouette 3/4, $P/sil_ref_C_new.png|new silhouette 3/4" \
    "$TD/ref_front_x4.png|reference front, $P/if_hair_F.png|6255d92 front, $P/cj_hair_F.png|new front, $TD/ref_close_x2.png|reference 3/4, $P/if_hair_C.png|6255d92 3/4, $P/cj_hair_C.png|new 3/4" \
    "$C/if_hair_side_custom.png|6255d92 profile, $C/cj_hair_side_custom.png|new profile, $C/if_hair_back_custom.png|6255d92 back / bun, $C/cj_hair_back_custom.png|new back / bun, $C/if_hair_top_custom.png|6255d92 crown, $C/cj_hair_top_custom.png|new crown"
fi
if has 05; then
  M=$("$PY" -c "import json; d=json.load(open('$K/shorts_measure_g16.json')); f=lambda k: 'crotch %.1f cm below body, band-crotch %.1f, rise F/B %.1f/%.1f' % (d[k]['crotch_sag_below_body_cm'], d[k]['waistband_top_to_crotch_fabric_cm'], d[k]['front_rise_cm'], d[k]['back_rise_cm']); print(f('g15b')+' | g16a: '+f('g16a'))")
  B 05_SHORTS_STATIC.jpg "05 SHORTS STATIC (neutral). Raised crotch kept: 6255d92 g15b: $M" 260 \
    "$C/ifx_sh_front_custom.png|6255d92 front, $C/ifx_sh_3q_custom.png|6255d92 3/4, $C/ifx_sh_side_custom.png|6255d92 side, $C/ifx_sh_rear_custom.png|6255d92 rear" \
    "$C/ks_st_neutral_front_custom.png|g16a skinned front, $C/ks_st_neutral_3q_custom.png|skinned 3/4, $C/ks_st_neutral_side_custom.png|skinned side, $C/ks_st_neutral_rear3q_custom.png|skinned rear 3/4" \
    "$C/rrs2_st_neutral_front_custom.png|FINAL Chaos m1 (after restart) front, $C/rrs2_st_neutral_3q_custom.png|FINAL 3/4, $C/rrs2_st_neutral_side_custom.png|FINAL side, $C/rrs2_st_neutral_rear3q_custom.png|FINAL rear 3/4"
fi
if has 06; then
  B 06_SHORTS_CHAOS_a.jpg "06 SHORTS: skinned/corrective (g16a) vs selective Chaos (CA_CR_Shorts_g16a): walk, crouch, high knee L, stride" 300 "$(row ks sc4 dy_walk SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_crouch SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 st_highknee_l SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 st_stride SKINNED CHAOS 3q side rear3q)"
  B 06_SHORTS_CHAOS_b.jpg "06b SHORTS: skinned vs selective Chaos: jog, sprint, hard stop, turn, squat, hip flex" 250 "$(row ks sc4 dy_jog SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_sprint SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_stop SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_turn SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_squat SKINNED CHAOS 3q side rear3q)" "$(row ks sc4 dy_hipflex SKINNED CHAOS 3q side rear3q)"
fi
if has 07; then
  B 07_HENLEY_STATIC.jpg "07 HENLEY: 6255d92 g15b / FINAL g16c + lived-in m1 (neutral) / crouch chest fix + neckline 20-45 deg" 260 \
    "$C/ifx_hen_front_custom.png|6255d92 front, $C/ifx_hen_3q_custom.png|6255d92 3/4, $C/ifx_hen_side_custom.png|6255d92 side, $C/ifx_hen_back_custom.png|6255d92 back" \
    "$C/fh_st_neutral_front_custom.png|FINAL g16c m1 front, $C/fh_st_neutral_3q_custom.png|FINAL 3/4, $C/fh_st_neutral_side_custom.png|FINAL side, $C/fh_st_neutral_rear3q_custom.png|FINAL rear 3/4" \
    "$C/dg_crouch_ref_custom.png|g16a crouch: chest through shirt, $C/fx_crouch_3q_custom.png|g16c crouch: fixed, $C/fn2_nk_b20_front_custom.png|FINAL neckline 20 deg, $C/fn2_nk_b45_front_custom.png|FINAL neckline 45 deg"
fi
if has 08; then
  B 08_HENLEY_CHAOS.jpg "08 HENLEY: skinned/corrective (g16c) vs hybrid selective Chaos hem (g16d + CA_CR_HenleyLower_g16b): neutral, walk, bend 45, crouch, twist" 280 "$(row kc hc3 st_neutral SKINNED HYBRID 3q side rear3q)" "$(row kc hc3 dy_walk SKINNED HYBRID 3q side rear3q)" "$(row kc hc3 st_bend45 SKINNED HYBRID 3q side rear3q)" "$(row kc hc3 dy_crouch SKINNED HYBRID 3q side rear3q)" "$(row kc hc3 st_twist_l SKINNED HYBRID 3q side rear3q)"
fi
if has 09; then
  rows=(); for k in neutral bend45 twist_l stride walk crouch turn; do rows+=("$(row kw hw wb_$k SKINNED HYBRID 3q side rear3q)"); done
  B 09_GARMENT_INTERACTION.jpg "09 HEM / WAISTBAND: skinned Henley + skinned shorts vs hybrid Chaos hem + Chaos shorts (PHYS_CR_HenleyCollider waistband proxy)" 230 "${rows[@]}"
  rows=(); for k in neutral bend45 twist_l stride walk crouch turn; do rows+=("$(row kf hf wb_$k FINAL HEM-EASE 3q side rear3q)"); done
  B 09b_GARMENT_INTERACTION_HEM_EASE.jpg "09b FINAL skinned Henley over Chaos shorts vs hybrid Chaos hem WITH hem ease (+7% / -1 cm rest shape): not adopted" 230 "${rows[@]}"
fi
if has 10; then
  B 10_FULL_CHARACTER.jpg "10 FULL CHARACTER (final composition, after restart): studio, gameplay light, walk / jog in flight; 6255d92 for comparison" 280 \
    "$C/ifx_full_front_custom.png|6255d92 front, $C/ifx_full_3q_custom.png|6255d92 3/4, $C/ifl_final_side.png|6255d92 side" \
    "$C/rrf2_fl_studio_front_custom.png|new front, $C/rrf2_fl_studio_3q_custom.png|new 3/4, $C/rrf2_fl_studio_side_custom.png|new side, $C/rrf2_fl_studio_back_custom.png|new back" \
    "$C/rrf2_fl_gameplay_front_custom.png|gameplay front, $C/rrf2_fl_gameplay_3q_custom.png|gameplay 3/4, $C/rrf2_fl_walk_3q_custom.png|walk 3/4, $C/rrf2_fl_jog_side_custom.png|jog side"
fi
if has 11; then
  r1=""; r2=""; for b in b00 b20 b30 b45 b60 b90; do r1="$r1, $C/fn2_nk_${b}_front_custom.png|neckline $b front"; r2="$r2, $C/fn2_nk_${b}_3q_custom.png|neckline $b 3/4"; done
  B 11_DEFORMATION.jpg "11 DEFORMATION (final composition): neckline / placket at 0-20-30-45-60-90 deg bend; both garments in jog, sprint, hard stop, turn, squat, hip flex, high knee, stride" 230 "${r1#, }" "${r2#, }" \
    "$C/fh_dy_jog_3q_custom.png|jog, $C/fh_dy_sprint_3q_custom.png|sprint, $C/fh_dy_stop_3q_custom.png|hard stop, $C/fh_dy_turn_3q_custom.png|turn, $C/fh_dy_squat_3q_custom.png|squat, $C/fh_dy_hipflex_3q_custom.png|hip flex" \
    "$C/fh_st_highknee_l_3q_custom.png|high knee L, $C/fh_st_stride_3q_custom.png|stride, $C/fh_dy_crouch_front_custom.png|crouch front, $C/fh_st_twist_l_rear3q_custom.png|twist rear, $C/fh_dy_walk_side_custom.png|walk side, $C/fh_st_bend45_side_custom.png|bend 45 side"
fi
if has 12; then
  J=(); for p in skN sdS; do for l in studio grazing interior gameplay; do J+=("$C/${p}_${l}_3q_custom.png|$P/sk3_${p}_${l}.png|0.42|0.66|0.25|480" "$C/${p}_${l}_front_custom.png|$P/skf_${p}_${l}.png|0.5|0.72|0.25|480"); done; done; CROP "${J[@]}"
  rows=(); for l in studio grazing interior gameplay; do rows+=("$P/sk3_skN_$l.png|6255d92 $l 3/4, $P/sk3_sdS_$l.png|new $l 3/4, $P/skf_skN_$l.png|6255d92 $l front, $P/skf_sdS_$l.png|new $l front"); done
  B 12_SKIN_SEAM.jpg "12 HEAD / BODY SEAM (garments hidden), 4 lights: 6255d92 vs corrective candidate" 260 "${rows[@]}"
fi
if has 13; then
  L1=(neutral blink blink_left blink_right look_up look_down look_left look_right brows_up brows_down frown smile); L2=(lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w cheek_compress extreme)
  for v in front 3q; do r1=""; r2=""; r3=""; r4=""
    for c in "${L1[@]}"; do r1="$r1, $C/if_rig_${c}_${v}_custom.png|$c 6255d92"; r2="$r2, $C/cj_rig_${c}_${v}_custom.png|$c new"; done
    for c in "${L2[@]}"; do r3="$r3, $C/if_rig_${c}_${v}_custom.png|$c 6255d92"; r4="$r4, $C/cj_rig_${c}_${v}_custom.png|$c new"; done
    B 13_FACE_EXPRESSIONS_$v.jpg "13 FACIAL RIG ($v cam): 6255d92 vs corrective candidate, 23 RigLogic cases" 190 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"; done
fi
if has 14; then
  r1=""; r2=""; for c in neutral blink smile jaw_open ph_mbp extreme; do r1="$r1, $C/cj_rig_${c}_front_custom.png|$c before restart"; r2="$r2, $C/rr_rig_${c}_front_custom.png|$c after restart"; done
  B 14_AFTER_RESTART.jpg "14 AFTER RESTART (fresh editor, reopened from disk): facial rig, LOD0-3, full character, garment behaviour after restart" 220 "${r1#, }" "${r2#, }" \
    "$C/rrl2_lod0_front_custom.png|LOD0, $C/rrl2_lod1_front_custom.png|LOD1, $C/rrl2_lod2_front_custom.png|LOD2, $C/rrl2_lod3_front_custom.png|LOD3, $C/rrl2_glod1_3q_custom.png|garment LOD1, $C/rrl2_glod2_3q_custom.png|garment LOD2" \
    "$C/rrf2_fl_studio_front_custom.png|full front, $C/rrf2_fl_studio_3q_custom.png|full 3/4, $C/rrh_dy_walk_3q_custom.png|Henley walk, $C/rrh_dy_crouch_3q_custom.png|Henley crouch, $C/rrs2_st_highknee_l_3q_custom.png|shorts high knee, $C/rrs2_dy_walk_side_custom.png|shorts walk"
fi
echo CR_BOARDS_DONE $SEL
