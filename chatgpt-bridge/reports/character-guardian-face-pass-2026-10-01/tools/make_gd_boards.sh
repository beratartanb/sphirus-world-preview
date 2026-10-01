#!/bin/bash
# make_gd_boards.sh [board numbers] : GUARDIAN face pass evidence boards 01-16 -> Saved/Codex/CharacterGuardian_20261001/boards
# 2e60b34 baseline: cj_* (face j, recon 3/4 cam), ks_/sc4_ (shorts), qw_/qs_ (Henley g16c with face h); new final: zf_* (face h + c14s + id18),
# z_<set>_* garment sets (Henley g17e, Chaos shorts m1), rr2_* after restart. 3/4 face frames: re-solved camera (camfit_close.json).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; SEL=${1:-01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16}
K=Saved/Codex/CharacterGuardian_20261001; O="$(cygpath -m "$(pwd)/$K/boards")"; P="$O/parts"; mkdir -p "$P"; C="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/captures")"
F="$(cygpath -m "$(pwd)/$K/frames")"; TD="$(cygpath -m "$(pwd)/Saved/Codex/CharacterIdentity_20260930/track")"; P2="$(cygpath -m "$(pwd)/Saved/Codex/CharacterCorrective_20261001/boards/parts")"
RF_="$(cygpath -m "$(pwd)/Saved/Codex/CharacterRevision_20260930/captures")"; GA="$(cygpath -m "$(pwd)/Saved/Codex/CharacterLookdev_20260930/garments")"; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
B() { "$PY" $T/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 30; echo; }
RECT() { "$BL" -b --factory-startup --python $T/id_crop_rect.py -- "$@" 2>&1 | grep -c RECT; }
has() { [[ ",$SEL," == *",$1,"* ]]; }
row() { local a=$1 b=$2 kind=$3 la=$4 lb=$5 r="" v; shift 5; for v in "$@"; do r="$r, ${a}_${kind}_${v}_custom.png|$la $kind $v, ${b}_${kind}_${v}_custom.png|$lb $v"; done; echo "${r#, }"; }
if has 01; then
  B 01_FACE_GATE_CLAY.jpg "01 FACE GATE (bald neutral clay): reference / 2e60b34 / GUARDIAN candidate H. Front + 3/4 at the reference-solved cameras, profile" 300 \
    "$TD/ref_front_x4.png|reference front, $P2/cj_clay_F.png|2e60b34 clay, $F/zf_clay_F.png|new clay" \
    "$TD/ref_close_x2.png|reference 3/4, $P2/cj_clay_C.png|2e60b34 (old 3/4 cam), $F/zf_clay_C.png|new (re-solved 3/4 cam)" \
    "$C/cj_clay_side_custom.png|2e60b34 profile, $C/zf_clay_side_custom.png|new profile, $C/zf_clay_front3q_custom.png|new std 3/4"
fi
if has 02; then
  B 02_FACE_OVERLAY.jpg "02 FACE 50% overlays (reference + candidate, real skin): 2e60b34 vs new, front + 3/4" 340 "$P2/cj_ovF.png|ref + 2e60b34 front, $F/zf_ovF.png|ref + new front, $P2/cj_ovC.png|ref + 2e60b34 3/4 (old cam), $F/zf_ovC.png|ref + new 3/4"
fi
if has 03 || has 04 || has 05 || has 06; then
  J=(); for s in ref cj zf; do src=$([ $s = ref ] && echo "$TD/ref_front_x4.png" || ([ $s = cj ] && echo "$P2/cj_real_F.png" || echo "$F/zf_real_F.png"))
    J+=("$src|$P/pl_${s}_eyes.png|0.18|0.33|0.82|0.52|480|285" "$src|$P/pl_${s}_nose.png|0.33|0.38|0.67|0.62|300|380" "$src|$P/pl_${s}_mid.png|0.08|0.40|0.92|0.70|480|340" "$src|$P/pl_${s}_mouth.png|0.26|0.57|0.74|0.72|420|260" "$src|$P/pl_${s}_jaw.png|0.12|0.60|0.88|0.86|480|330"); done
  for s in ref zf; do src=$([ $s = ref ] && echo "$TD/ref_close_x2.png" || echo "$F/zf_real_C.png"); J+=("$src|$P/pc_${s}_eyes.png|0.45|0.45|0.95|0.62|500|170" "$src|$P/pc_${s}_nose.png|0.55|0.5|0.92|0.76|370|260" "$src|$P/pc_${s}_mouth.png|0.5|0.66|0.92|0.92|420|260"); done
  RECT "${J[@]}"
fi
has 03 && B 03_FACE_EYES.jpg "03 EYES / ORBITS / BROWS: reference / 2e60b34 / new (front) + 3/4" 360 "$P/pl_ref_eyes.png|reference, $P/pl_cj_eyes.png|2e60b34, $P/pl_zf_eyes.png|new" "$P/pc_ref_eyes.png|reference 3/4, $P/pc_zf_eyes.png|new 3/4"
has 04 && B 04_FACE_NOSE.jpg "04 NOSE: reference / 2e60b34 / new (front) + 3/4" 330 "$P/pl_ref_nose.png|reference, $P/pl_cj_nose.png|2e60b34, $P/pl_zf_nose.png|new" "$P/pc_ref_nose.png|reference 3/4, $P/pc_zf_nose.png|new 3/4"
has 05 && B 05_FACE_MIDFACE.jpg "05 MIDFACE / CHEEKS: reference / 2e60b34 / new" 360 "$P/pl_ref_mid.png|reference, $P/pl_cj_mid.png|2e60b34, $P/pl_zf_mid.png|new"
has 06 && B 06_FACE_MOUTH_JAW.jpg "06 MOUTH / JAW / CHIN: reference / 2e60b34 / new (front) + 3/4" 330 "$P/pl_ref_mouth.png|reference, $P/pl_cj_mouth.png|2e60b34, $P/pl_zf_mouth.png|new" "$P/pl_ref_jaw.png|reference jaw, $P/pl_cj_jaw.png|2e60b34 jaw, $P/pl_zf_jaw.png|new jaw" "$P/pc_ref_mouth.png|reference 3/4, $P/pc_zf_mouth.png|new 3/4"
if has 07; then
  B 07_FACE_REAL_SKIN.jpg "07 FACE REAL SKIN (neutral, no hair): reference / 2e60b34 / new (skin c14s, SlightArch brows, short lashes)" 300 \
    "$TD/ref_front_x4.png|reference, $P2/cj_real_F.png|2e60b34, $F/zf_real_F.png|new" "$TD/ref_close_x2.png|reference 3/4, $F/zf_real_C.png|new 3/4, $C/zf_real_side_custom.png|new profile"
fi
if has 08; then
  L1=(neutral blink blink_left look_left look_up brows_up brows_down frown smile); L2=(lips_closed mouth_open jaw_open jaw_left ph_oo ph_ee ph_mbp ph_w extreme)
  r1=""; r2=""; r3=""; r4=""; for c in "${L1[@]}"; do r1="$r1, $C/cj_rig_${c}_front_custom.png|$c 2e60b34"; r2="$r2, $C/zf_rig_${c}_front_custom.png|$c new"; done
  for c in "${L2[@]}"; do r3="$r3, $C/cj_rig_${c}_front_custom.png|$c 2e60b34"; r4="$r4, $C/zf_rig_${c}_front_custom.png|$c new"; done
  B 08_FACE_EXPRESSION_CHECK.jpg "08 FACIAL RIG (RigLogic, same DNA; new neutral via BR_Neutral): 2e60b34 vs new" 190 "${r1#, }" "${r2#, }" "${r3#, }" "${r4#, }"
fi
if has 09; then
  B 09_HAIR_REFERENCE.jpg "09 HAIR id18 (centre part, fuller crown, looser bun): reference / 2e60b34 id17 / new" 260 \
    "$TD/ref_front_x4.png|reference front, $P2/cj_hair_F.png|2e60b34 front, $F/zf_hair_F.png|new front, $TD/ref_close_x2.png|reference 3/4, $F/zf_hair_C.png|new 3/4" \
    "$C/cj_hair_side_custom.png|2e60b34 profile, $C/zf_hair_side_custom.png|new profile, $C/cj_hair_back_custom.png|2e60b34 back / bun, $C/zf_hair_back_custom.png|new back / bun, $C/zf_hair_top_custom.png|new crown"
fi
if has 10; then
  B 10_HENLEY_PATTERN.jpg "10 HENLEY PATTERN: g16a (2e60b34 pattern) vs g17e (hem girth 99->104, hip 97->100.5, waist 93->95, sleeve reserve 1.08->1.10); g17a/b (longer hem) slid off the shoulder: rejected" 300 \
    "$GA/g16a/render/f_front.png|g16a front, $GA/g16a/render/f_side.png|g16a side, $GA/g16a/render/f_back.png|g16a back, $GA/g16a/render/f_hips_side.png|g16a hip" \
    "$GA/g17e/render/f_front.png|g17e front, $GA/g17e/render/f_side.png|g17e side, $GA/g17e/render/f_back.png|g17e back, $GA/g17e/render/f_hips_side.png|g17e hip" \
    "$GA/g17a/render/f_front.png|g17a REJECTED, $GA/g17b/render/f_back.png|g17b REJECTED"
fi
if has 11; then
  rows=(); for k in neutral walk crouch bend45 twist_l; do rows+=("$(row qw z_waist_wb $k g16c g17e 3q side rear3q | sed 's#z_waist_wb_\([a-z0-9_]*\)_\([a-z0-9]*\)_custom#z_waist_wb_\1_\2_custom#g')"); done
  rows=(); for k in neutral walk crouch bend45 twist_l; do r=""; for v in 3q side rear3q; do r="$r, $C/qw_wb_${k}_${v}_custom.png|g16c $k $v, $C/z_waist_wb_${k}_${v}_custom.png|g17e $v"; done; rows+=("${r#, }"); done
  B 11_HENLEY_WAISTBAND.jpg "11 HENLEY HEM / WAISTBAND (skinned + correctives over the Chaos shorts): 2e60b34 g16c vs new g17e" 230 "${rows[@]}"
fi
if has 12; then
  rows=(); for k in neutral bend45 walk crouch jog; do r=""; for v in l_out r_out l_back; do r="$r, $C/z_sleeve_sl_${k}_${v}_custom.png|$k $v"; done; rows+=("${r#, }"); done
  B 12_SLEEVES.jpg "12 SLEEVES (g17e, sleeve reserve 1.10; SHCB / elbow correctives kept)" 280 "${rows[@]}"
fi
if has 13; then
  rows=(); for k in dy_walk dy_crouch st_highknee_l st_stride dy_sprint; do r=""; for v in 3q side rear3q; do r="$r, $C/ks_${k}_${v}_custom.png|skinned $k $v, $C/z_shorts_${k}_${v}_custom.png|Chaos $v"; done; rows+=("${r#, }"); done
  B 13_SHORTS_CHAOS.jpg "13 SHORTS: skinned reference (2e60b34 g16a) vs retained selective Chaos runtime (CA_CR_Shorts_m1) on the final character" 250 "${rows[@]}"
fi
if has 14; then
  B 14_FULL_CHARACTER.jpg "14 FULL CHARACTER: reference / final candidate (studio, gameplay light, walk / jog in flight)" 290 \
    "$RF_/ref_full_front.png|reference front, $RF_/ref_full_3q.png|reference 3/4" \
    "$C/z_full_fl_studio_front_custom.png|new front, $C/z_full_fl_studio_3q_custom.png|new 3/4, $C/z_full_fl_studio_side_custom.png|new side, $C/z_full_fl_studio_back_custom.png|new back" \
    "$C/z_full_fl_gameplay_front_custom.png|gameplay front, $C/z_full_fl_gameplay_3q_custom.png|gameplay 3/4, $C/z_full_fl_walk_3q_custom.png|walk 3/4, $C/z_full_fl_jog_side_custom.png|jog side"
fi
if has 15; then
  J=(); for p in sdS z_seam; do for l in studio grazing interior gameplay; do J+=("$C/${p}_${l}_3q_custom.png|$P/sk_${p}_${l}.png|0.42|0.66|0.25|480"); done; done
  "$BL" -b --factory-startup --python $T/blender_lk_crop.py -- "${J[@]}" 2>&1 | grep -c CROP
  rows=(); for l in studio grazing interior gameplay; do rows+=("$P/sk_sdS_$l.png|2e60b34 c12s $l, $P/sk_z_seam_$l.png|new c14s $l"); done
  B 15_SKIN_SEAM.jpg "15 HEAD / BODY SEAM (garments hidden), 4 lights: 2e60b34 (head-side shading match) vs new (same seam shading + common skin tint)" 330 "${rows[@]}"
fi
if has 16; then
  r1=""; r2=""; for c in neutral blink smile jaw_open ph_mbp extreme; do r1="$r1, $C/zf_rig_${c}_front_custom.png|$c before restart"; r2="$r2, $C/rr2_rig_${c}_front_custom.png|$c after restart"; done
  B 16_AFTER_RESTART.jpg "16 AFTER RESTART (fresh editor, reopened from disk): facial rig, LODs, full character, garments" 220 "${r1#, }" "${r2#, }" \
    "$C/rr2_lod_lod0_front_custom.png|LOD0, $C/rr2_lod_lod1_front_custom.png|LOD1, $C/rr2_lod_lod2_front_custom.png|LOD2, $C/rr2_lod_lod3_front_custom.png|LOD3, $C/rr2_lod_glod1_3q_custom.png|garment LOD1" \
    "$C/rr2_full_fl_studio_front_custom.png|full front, $C/rr2_full_fl_studio_3q_custom.png|full 3/4, $C/rr2_henley_dy_walk_3q_custom.png|Henley walk, $C/rr2_henley_dy_crouch_3q_custom.png|crouch, $C/rr2_shorts_st_highknee_l_3q_custom.png|shorts high knee"
fi
echo GD_BOARDS_DONE $SEL
