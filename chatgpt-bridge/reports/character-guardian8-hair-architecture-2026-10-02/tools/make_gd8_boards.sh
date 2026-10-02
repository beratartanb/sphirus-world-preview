#!/bin/bash
# make_gd8_boards.sh : GUARDIAN-8 hair-architecture boards A-G -> Saved/Codex/CharacterGuardian8_20261002/boards
# REFERENCE (Tier A front / 3/4; Tier B turnaround as aid for side / rear) | GD7 (C8 face + h17: HC_*, z7f_*) | GD8 (same locked C8 face + h23: z8f_*, z8_*).
# Identical pose / camera / scale / light per row. rr9* = GD8 after a fresh restart.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian8_20261002; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F7=Saved/Codex/CharacterGuardian7_20261002/frames; F8=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png
B A_SIDE_HAIR_START_PROFILE.jpg "A SIDE HAIR START / PROFILE MASS POSITION: Tier B profile (aid) | GD7 h17 | GD8 h23 (both sides). Guide: orthographic profile of the LATERAL hair (|x|>4.5 cm) on the C8 head - red = GD7 only (forward side curtain, low side wall, nape bun), green = GD8 only, yellow = both, white = GD8 front boundary. Side-mass lower edge above the ear z 160.5 -> 164.4 cm, forward reach at 164.5-166 cm -1.0 cm, ear coverage ~21k -> ~0.5k hair points" 420 \
  "$RB/turnaround_p5.png|REF side (aid), $C/HC_hair_side_custom.png|GD7 side, $C/z8f_hair_side_custom.png|GD8 side, $RB/turnaround_p3.png|REF side 2 (aid), $C/HC_hair_side2_custom.png|GD7 side 2, $C/z8f_hair_side2_custom.png|GD8 side 2" \
  "$PV/sideguide_h17_final.png|GUIDE GD7 (red) vs GD8 (green)"
B B_BUN_HEIGHT_POSITION.jpg "B BUN HEIGHT / POSITION: bun anchor moved from the nape (z 155.0, 5.7 cm off the neck) to the lower occiput (z 159.6); bun-section centroid z 156.0 -> 160.6 cm (mid-ear height), 2.4 cm off the skull: REF | GD7 | GD8" 420 \
  "$RB/turnaround_p5.png|REF side (aid), $C/HC_hair_side_custom.png|GD7 side, $C/z8f_hair_side_custom.png|GD8 side" "$RB/turnaround_p4.png|REF rear (aid), $C/HC_hair_back_custom.png|GD7 rear, $C/z8f_hair_back_custom.png|GD8 rear"
B C_REAR_MASS_DENSITY_AIRINESS.jpg "C REAR MASS DENSITY / AIRINESS (rear root density -32%, stronger rear group separation, less lateral fill, more secondary depth variation, nape coverage + short nape wisps): REF | GD7 | GD8" 420 \
  "$RB/turnaround_p4.png|REF rear (aid), $C/HC_hair_back_custom.png|GD7 rear, $C/z8f_hair_back_custom.png|GD8 rear" "$RC|REF 3/4, $C/HC_hair_back3q_custom.png|GD7 back 3/4, $C/z8f_hair_back3q_custom.png|GD8 back 3/4"
B D_TOP_CROWN_SILHOUETTE.jpg "D TOP / CROWN SILHOUETTE (kept from GD7: profile stand-off top / rear-upper GD7 3.1 / 5.1 cm -> GD8 see data; main-mass-only silhouette right): REF | GD7 | GD8" 420 \
  "$RB/turnaround_p5.png|REF side (aid), $C/HC_hair_side_custom.png|GD7 side, $C/z8f_hair_side_custom.png|GD8 side, $PV/_silmask8.png|MAIN MASS ONLY: top GD7 h17 / bottom GD8 h23"
B E_FULL_HAIR_BEFORE_AFTER.jpg "E FULL HAIR BEFORE (GD7 h17) / AFTER (GD8 h23): identical camera / pose / light, locked C8 face" 330 \
  "$C/HC_hair_reffront_custom.png|BEFORE front, $C/z8f_hair_reffront_custom.png|AFTER front, $C/HC_hair_refclose2_custom.png|BEFORE 3/4, $C/z8f_hair_refclose2_custom.png|AFTER 3/4, $C/HC_hair_top_custom.png|BEFORE top, $C/z8f_hair_top_custom.png|AFTER top" \
  "$C/HC_hair_side_custom.png|BEFORE side, $C/z8f_hair_side_custom.png|AFTER side, $C/HC_hair_side2_custom.png|BEFORE side 2, $C/z8f_hair_side2_custom.png|AFTER side 2, $C/HC_hair_back_custom.png|BEFORE rear, $C/z8f_hair_back_custom.png|AFTER rear"
B F_FACE_FRONT_3Q_NEUTRAL.jpg "F FACE FRONT / 3/4 NEUTRAL (face geometry, DNA and skin unchanged from GD7 C8 - locked): REFERENCE | GD7 | GD8" 500 \
  "$RF|REFERENCE, $F7/z7f_real_F.png|GD7, $F8/z8f_real_F.png|GD8, $F8/z8f_hair_F.png|GD8 with hair" "$RC|REFERENCE, $F7/z7f_real_C.png|GD7, $F8/z8f_real_C.png|GD8, $F8/z8f_hair_C.png|GD8 with hair"
B G_RIG_LOD_AFTER_RESTART.jpg "G RIG / LOD / AFTER RESTART (new GD8 groom bindings on the locked C8 face; fresh-editor reopen)" 300 \
  "$C/z8f_rig_neutral_front_custom.png|neutral, $C/z8f_rig_blink_front_custom.png|blink, $C/z8f_rig_jaw_open_front_custom.png|jaw open, $C/z8f_rig_smile_front_custom.png|smile, $C/z8f_rig_extreme_front_custom.png|extreme" \
  "$C/z8_lod_lod0_front_custom.png|LOD0, $C/z8_lod_lod1_front_custom.png|LOD1, $C/z8_lod_lod2_front_custom.png|LOD2, $C/z8_lod_lod3_front_custom.png|LOD3" \
  "$F8/rr9f_hair_F.png|after restart hair, $F8/rr9f_hair_C.png|after restart 3/4, $C/rr9f_hair_side_custom.png|after restart side, $C/rr9f_rig_blink_front_custom.png|after restart blink, $C/rr9_full_fl_studio_front_custom.png|after restart full"
B H_FULL_CHARACTER.jpg "H FULL CHARACTER (GD8)" 440 "$C/z8_full_fl_studio_front_custom.png|studio front, $C/z8_full_fl_studio_3q_custom.png|studio 3/4, $C/z8_full_fl_studio_side_custom.png|side, $C/z8_full_fl_studio_back_custom.png|back"
ls "$O" | grep -c jpg
