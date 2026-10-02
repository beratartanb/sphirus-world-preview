#!/bin/bash
# make_gd11_boards.sh : GUARDIAN-11 boards 01-18 -> Saved/Codex/CharacterGuardian11_20261002/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = authority; Tier B profile = low-weight aid) | GD10 (S5 + k7) | GD11 (E + k9). Blender clay pv/r_cur_fin_* (GD10) / pv/r_new_fin_* (GD11);
# UE captures z10f_* (GD10) / z11f_* (GD11); identical cameras / lights.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian11_20261002; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F10=Saved/Codex/CharacterGuardian10_20261002/frames; F11=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_fin; NW=$PV/r_new_fin
B 01_FRONT_CLAY.jpg "01 FRONT CLAY: REFERENCE | GD10 | GD11" 520 "$RF|REFERENCE, ${CU}_front_clay.png|GD10, ${NW}_front_clay.png|GD11"
B 02_3Q_CLAY.jpg "02 3/4 CLAY (verified ~33 deg): REFERENCE | GD10 | GD11" 520 "$RC|REFERENCE, ${CU}_close_clay.png|GD10, ${NW}_close_clay.png|GD11"
B 03_PROFILE_CLAY.jpg "03 PROFILE CLAY: Tier B (low-weight aid) | GD10 | GD11" 520 "$RP|REF profile (aid), ${CU}_side_clay.png|GD10, ${NW}_side_clay.png|GD11"
ROW n_p.png 0,10000,560,1200 400 ${CU}_side_clay.png ${NW}_side_clay.png; ROW n_c.png 380,720,420,780 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW n_f.png 380,640,280,540 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png
VS stack_04.png "$P/n_p.png|x" "$P/n_c.png|x" "$P/n_f.png|x"
B 04_PROFILE_NOSE.jpg "04 NOSE (tip ball flattened + slight de-projection 2.0 -> 1.87 cm, alar balls deflated / crease filled / blended into the tip, radix continuity): profile GD10 / GD11; 3/4 + front REF / GD10 / GD11" 1500 "$P/stack_04.png|rows: profile / 3/4 / front"
ROW m_c.png 360,860,250,794 420 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW m_r.png 360,860,250,794 420 $RC $F10/z10f_real_C.png $F11/z11f_real_C.png
VS stack_05.png "$P/m_c.png|x" "$P/m_r.png|x"
B 05_PROFILE_CHEEKBONE_MIDFACE.jpg "05 CHEEKBONE / MIDFACE (GD10 flesh kept; lower-orbit support; no hollowing): REF / GD10 / GD11 clay + real" 1500 "$P/stack_05.png|rows: 3/4 clay / 3/4 real"
ROW l_c.png 560,860,430,780 380 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW l_f.png 560,720,280,540 380 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW l_p.png 600,1150,700,1200 380 ${CU}_side_clay.png ${NW}_side_clay.png
VS stack_06.png "$P/l_c.png|x" "$P/l_f.png|x" "$P/l_p.png|x"
B 06_PROFILE_LIPS.jpg "06 LIPS (less padded: upper vermilion rolled in + deflated, lower lip deflated; width unchanged): 3/4 / front REF / GD10 / GD11; profile GD10 / GD11" 1500 "$P/stack_06.png|rows: 3/4 / front / profile"
B 07_PROFILE_MOUTH_CHIN.jpg "07 MOUTH-CHIN (chin pad 1.2 mm lower for a longer lower face, symmetric; jaw contour identical to GD10): REF | GD10 | GD11" 440 "$RP|REF (aid), $C/z10f_real_side_custom.png|GD10, $C/z11f_real_side_custom.png|GD11" "$RC|REF 3/4, $F10/z10f_real_C.png|GD10, $F11/z11f_real_C.png|GD11"
ROW e_f.png 330,500,200,620 320 $RF $F10/z10f_real_F.png $F11/z11f_real_F.png; ROW e_c.png 430,620,380,740 320 $RC $F10/z10f_real_C.png $F11/z11f_real_C.png; ROW e_cl.png 330,500,200,620 320 $RF ${CU}_front_clay.png ${NW}_front_clay.png
VS stack_08.png "$P/e_f.png|x" "$P/e_c.png|x" "$P/e_cl.png|x"
B 08_EYE_BROW_ORBIT_CHARACTER.jpg "08 EYE / BROW / ORBIT (heavier brow shelter down+forward, lateral hood weight, lower-orbit support; lid margins <= 0.4 mm, eye joints unchanged): REF / GD10 / GD11" 1500 "$P/stack_08.png|rows: front real / 3/4 real / front clay"
ROW a_f.png 280,820,160,640 420 $RF $F10/z10f_real_F.png $F11/z11f_real_F.png
VS stack_09.png "$P/a_f.png|x"
B 09_SOFT_TISSUE_AGE_CHARACTER.jpg "09 SOFT-TISSUE / AGE CHARACTER (restrained early-adult cues in normal + colour: faint forehead lines, glabella, delicate lower-lid creases, soft nasolabial; no deep folds / bags): REF / GD10 / GD11" 1500 "$P/stack_09.png|rows: front real" "$K/skin/_age_k8.png|age-cue placement on the UV (red)"
B 10_SKIN_TONE_COMPARISON.jpg "10 SKIN TONE (k9: olive-beige, warmer-neutral factor, low-frequency blotches evened, muted lighter lips): REFERENCE | GD10 k7 | GD11 k9" 520 "$RF|REFERENCE, $F10/z10f_real_F.png|GD10 k7, $F11/z11f_real_F.png|GD11 k9" "$RC|REFERENCE, $F10/z10f_real_C.png|GD10 k7, $F11/z11f_real_C.png|GD11 k9"
ROW s_cl.png 640,1040,430,830 420 $C/z10f_rig_neutral_front_custom.png $C/z11f_rig_neutral_front_custom.png; ROW s_n.png 380,640,200,600 420 $RF $F10/z10f_real_F.png $F11/z11f_real_F.png
VS stack_11.png "$P/s_cl.png|x" "$P/s_n.png|x"
B 11_SKIN_MACRO_MICRO.jpg "11 SKIN MACRO / MICRO: close cam GD10 / GD11; normal distance REF / GD10 / GD11" 1500 "$P/stack_11.png|rows: close / normal distance"
B 12_FULL_PROFILE_RHYTHM.jpg "12 FULL PROFILE RHYTHM: Tier B (aid) | GD10 | GD11 clay | GD11 real" 460 "$RP|REF (aid), ${CU}_side_clay.png|GD10, ${NW}_side_clay.png|GD11, $C/z11f_real_side_custom.png|GD11 real"
B 13_FRONT_OVERLAY.jpg "13 FRONT OVERLAY (50% clay over Tier A front): GD10 | GD11" 560 "$PV/rb_cur_fin_front.png|GD10, $PV/rb_new_fin_front.png|GD11"
B 14_3Q_OVERLAY.jpg "14 3/4 OVERLAY (50% clay over Tier A 3/4): GD10 | GD11" 560 "$PV/rb_cur_fin_close.png|GD10, $PV/rb_new_fin_close.png|GD11"
B 15_HAIR_PRESERVATION.jpg "15 HAIR PRESERVATION (h23 unchanged, rebound): GD10 | GD11" 400 "$C/z10f_hair_side_custom.png|GD10 side, $C/z11f_hair_side_custom.png|GD11 side, $C/z10f_hair_back_custom.png|GD10 rear, $C/z11f_hair_back_custom.png|GD11 rear, $F10/z10f_hair_F.png|GD10 front, $F11/z11f_hair_F.png|GD11 front"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z11f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z11f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z11f_rig_${c}_3q_custom.png|$c 3/4"; done
B 16_RIG_TEST.jpg "16 RIG TEST (one fresh auto-rig on E)" 170 "${r1#, }" "${r2#, }" "${r3#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z11_lod_${l}_front_custom.png|face $l"; done
B 17_LOD.jpg "17 LOD (GD11 face 8 LODs)" 330 "${r#, }"
B 18_AFTER_RESTART.jpg "18 AFTER FRESH RESTART (GD11 assets from disk)" 320 "$F11/rr12f_real_F.png|real front, $F11/rr12f_real_C.png|real 3/4, $F11/rr12f_hair_F.png|hair, $C/rr12f_rig_blink_front_custom.png|blink, $C/rr12f_rig_jaw_open_front_custom.png|jaw open"
ls "$O" | grep -c jpg
