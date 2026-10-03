#!/bin/bash
# make_g11rb_boards.sh : GD11 head refinement B report boards 01-10 -> Saved/Codex/GD11_HeadRefinementB_20261004/public_report/boards
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; R="$(cygpath -m "$PWD")"; C="$R/Saved/Codex/CharacterLookdev_20260930/captures"; K="$R/Saved/Codex/GD11_HeadRefinementB_20261004"
F="$K/frames"; P="$K/pv"; TD="$R/Saved/Codex/CharacterIdentity_20260930/track"; O="$K/public_report/boards"; mkdir -p "$O" "$P/crop"; DR=SourceAssets/Characters/Guardian16_CustomIdentity_20261003/scripts/draw.sh
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
B() { "$PY" Tools/CharacterLookdev_20260930/lk_board.py "$O/$1" "$2" "$3" "${@:4}" | tail -c 25; echo; }
cr() { echo "{\"src\": \"$C/$1_custom.png\", \"out\": \"$P/crop/$1.png\", \"crop\": $2, \"scale\": $3, \"grid\": 0}" > "$K/pv/_s.json"; bash $DR "$K/pv/_s.json" >/dev/null; }
HEADF="[230, 0, 1140, 1380]"
for x in g11rbw_r3h32_studio_front g11rbw_d85h32_studio_front g11rbw_r3h34_studio_front g11rbw_d85h34b_studio_front g11rbafter_studio_front; do cr $x "$HEADF" 0.5; done
c() { echo "$C/$1_custom.png|$2"; }
pc() { echo "$P/crop/$1.png|$2"; }
B 01_CAMERA_CHECK.jpg "01 CAMERA CHECK - same R3/h32 geometry: REFERENCE | old 30deg pitch 11 | chosen 32deg pitch 1 | 40deg" 420 \
  "$TD/ref_close_x2.png|REFERENCE 3/4, $F/cam_hair_c30.png|old 30deg p11, $F/cam_hair_c32.png|chosen 32deg p1, $F/cam_hair_c40.png|40deg p1" \
  "$TD/ref_close_x2.png|REFERENCE, $F/cam_real_c30.png|old (no hair), $F/cam_real_c32.png|chosen (no hair), $F/cam_real_c40.png|40deg (no hair)"
B 02_WHOLE_HEAD_FRONT.jpg "02 WHOLE HEAD FRONT - REFERENCE | R3/h32 | NEW D85/h34 ; change isolation" 430 \
  "$TD/ref_front_x4.png|REFERENCE, $(pc g11rbw_r3h32_studio_front 'R3 + h32 (start)'), $(pc g11rbw_d85h34b_studio_front 'NEW D85 + h34')" \
  "$(pc g11rbw_r3h32_studio_front 'R3 + h32'), $(pc g11rbw_d85h32_studio_front 'D85 + h32 (nose only)'), $(pc g11rbw_r3h34_studio_front 'R3 + h34 (hair only)'), $(pc g11rbw_d85h34b_studio_front 'D85 + h34 (both)')"
B 03_WHOLE_HEAD_3Q.jpg "03 WHOLE HEAD 3/4 (chosen 32deg camera, reference frame) - REFERENCE | R3/h32 | NEW ; change isolation" 430 \
  "$TD/ref_close_x2.png|REFERENCE, $F/q3m_r3h32.png|R3 + h32 (start), $F/q3m_d85h34b.png|NEW D85 + h34" \
  "$F/q3m_r3h32.png|R3 + h32, $F/q3m_d85h32.png|D85 + h32 (nose only), $F/q3m_r3h34.png|R3 + h34 (hair only), $F/q3m_d85h34b.png|D85 + h34 (both)"
B 04_NOSE_DORSUM.jpg "04 NOSE DORSUM - R3 (top) vs D85 (middle) real; clay (bottom); REFERENCE / AUX at right" 300 \
  "$(c g11rbnr3_real_q3head 'R3 3/4 head'), $(c g11rbnr3_real_q3 'R3 3/4 nose'), $(c g11rbnr3_real_profR 'R3 profile R'), $(c g11rbnr3_real_profL 'R3 profile L'), $(c g11rbnr3_real_front 'R3 front'), $P/ref_nose_q3.png|REFERENCE 3/4 nose" \
  "$(c g11rbnd85_real_q3head 'D85 3/4 head'), $(c g11rbnd85_real_q3 'D85 3/4 nose'), $(c g11rbnd85_real_profR 'D85 profile R'), $(c g11rbnd85_real_profL 'D85 profile L'), $(c g11rbnd85_real_front 'D85 front'), $P/aux_nose_prof.png|AUX generated profile" \
  "$P/d85_0_dorsumProfR.png|R3 clay profile, $P/d85_1_dorsumProfR.png|D85 clay profile, $P/d85_0_dorsum32.png|R3 clay 32deg, $P/d85_1_dorsum32.png|D85 clay 32deg, $(c g11rbnr3_clay_profhead 'R3 clay head'), $(c g11rbnd85_clay_profhead 'D85 clay head')"
B 05_NOSE_BASE_PRESERVATION.jpg "05 NOSE BASE PRESERVATION - R3 | D85 from below and 3/4 (geometry clay + UE real)" 380 \
  "$P/d85_0_noseBelow.png|R3 base below (clay), $P/d85_1_noseBelow.png|D85 base below (clay), $(c g11rbnr3_clay_q3 'R3 3/4 clay'), $(c g11rbnd85_clay_q3 'D85 3/4 clay')" \
  "$(c g11rbnr3_real_below 'R3 below (real)'), $(c g11rbnd85_real_below 'D85 below (real)'), $(c g11rbnr3_real_q3head 'R3 whole 3/4'), $(c g11rbnd85_real_q3head 'D85 whole 3/4')"
B 06_HAIR_TOP_POSTURE.jpg "06 HAIR TOP POSTURE - h32 (top) vs h34 (bottom) on D85: front, top-front, profile top, whole side" 380 \
  "$(c g11rbc2_d85h32_studio_forehead 'h32 front'), $(c g11rbc2_d85h32_studio_topfront 'h32 top-front'), $(c g11rbc2_d85h32_studio_proftop 'h32 profile top'), $(c g11rbw_d85h32_studio_side 'h32 whole side')" \
  "$(c g11rbc2_d85h34_studio_forehead 'h34 front'), $(c g11rbc2_d85h34_studio_topfront 'h34 top-front'), $(c g11rbc2_d85h34_studio_proftop 'h34 profile top'), $(c g11rbw_d85h34b_studio_side 'h34 whole side')"
B 07_FOREHEAD_ROOTS_HAIRLINE.jpg "07 FOREHEAD ROOTS / PART / TEMPLE - h32 vs h34, neutral and side light, with whole head" 330 \
  "$(c g11rbc2_d85h32_studio_forehead 'h32 roots'), $(c g11rbc2_d85h32_grazing_forehead 'h32 roots side light'), $(c g11rbc2_d85h32_studio_hairline3q 'h32 temple 3/4'), $(c g11rbc2_d85h32_grazing_hairline3q 'h32 temple side light'), $(pc g11rbw_d85h32_studio_front 'h32 whole')" \
  "$(c g11rbc2_d85h34_studio_forehead 'h34 roots'), $(c g11rbc2_d85h34_grazing_forehead 'h34 roots side light'), $(c g11rbc2_d85h34_studio_hairline3q 'h34 temple 3/4'), $(c g11rbc2_d85h34_grazing_hairline3q 'h34 temple side light'), $(pc g11rbw_d85h34b_studio_front 'h34 whole')"
B 08_HAIR_REAR_BUN.jpg "08 HAIR REAR / BUN - h32 (top) vs h34 (bottom): back, rear 3/4, both profiles, bun close" 330 \
  "$(c g11rbw_d85h32_studio_back 'h32 back'), $(c g11rbw_d85h32_studio_rear3q 'h32 rear 3/4'), $(c g11rbw_d85h32_studio_side 'h32 profile R'), $(c g11rbw_d85h32_studio_side2 'h32 profile L'), $(c g11rbc2_d85h32_studio_bun 'h32 bun')" \
  "$(c g11rbw_d85h34b_studio_back 'h34 back'), $(c g11rbw_d85h34b_studio_rear3q 'h34 rear 3/4'), $(c g11rbw_d85h34b_studio_side 'h34 profile R'), $(c g11rbw_d85h34b_studio_side2 'h34 profile L'), $(c g11rbc2_d85h34_studio_bun 'h34 bun')"
B 09_COLOUR_MATERIAL.jpg "09 COLOUR / MATERIAL / SKIN - same colour values (h32c) on h32 and h34 ; skin k9 + head-neck under 3 lights" 330 \
  "$(c g11rbc2_d85h32_studio_hairline3q 'h32 colour'), $(c g11rbc2_d85h34_studio_hairline3q 'h34 same colour'), $(c g11rbc2_d85h34_grazing_hairline3q 'h34 side light'), $(c g11rbskin_gameplay_q3 'h34 gameplay sun'), $(c g11rbskin_studio_front 'skin studio')" \
  "$(c g11rbskin_grazing_front 'skin side light'), $(c g11rbskin_studio_nape 'nape studio'), $(c g11rbskin_grazing_nape 'nape side light'), $(c g11rbskin_studio_neckside 'head-neck studio'), $(c g11rbskin_grazing_neckside 'head-neck side light')"
B 10_TECHNICAL.jpg "10 TECHNICAL - rig (27 cases), automatic groom LOD by distance (retuned), face LOD, motion, after fresh-editor restart" 260 \
  "$(c g11rbfin_rig_neutral_front neutral), $(c g11rbfin_rig_blink_left_front 'blink L'), $(c g11rbfin_rig_look_up_front 'look up'), $(c g11rbfin_rig_brows_up_front 'brows up'), $(c g11rbfin_rig_smile_front smile), $(c g11rbfin_rig_ph_mbp_front 'lips MBP'), $(c g11rbfin_rig_sneer_front sneer), $(c g11rbfin_rig_upper_lip_raise_3q 'upper lip 3/4'), $(c g11rbfin_rig_nostril_dilate_front 'nostril dilate')" \
  "$P/lod3_125_front.png|hair 1.25 m, $P/lod3_300_front.png|3 m, $P/lod3_600_front.png|6 m, $P/lod3_900_front.png|9 m, $P/lod3_1200_front.png|12 m (mesh LOD), $(c g11rblod_face1 'face LOD1'), $(c g11rblod_face3 'face LOD3'), $(c g11rbmot_turnR06_q3 'turn R'), $(c g11rbmot_stop06_q3 'run-stop')" \
  "$(c g11rbmot_turnL06_q3 'turn L'), $(c g11rbmot_turnL12_back 'turn L back'), $(c g11rbmot_look40_side 'look-around'), $(c g11rbmot_look85_front 'look-around 2'), $(pc g11rbafter_studio_front 'after restart front'), $(c g11rbafter_studio_q3 'after restart 3/4'), $(c g11rbafter_studio_side 'after restart side'), $(c g11rbafter_studio_back 'after restart back'), $(c g11rbafter_studio_top 'after restart top')"
echo BOARDS_DONE
