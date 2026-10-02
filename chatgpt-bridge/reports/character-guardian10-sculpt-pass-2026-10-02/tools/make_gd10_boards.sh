#!/bin/bash
# make_gd10_boards.sh : GUARDIAN-10 sculpt boards -> Saved/Codex/CharacterGuardian10_20261002/boards
# REFERENCE (Tier A front / ~33 deg 3/4 = authority; Tier B profile = low-weight aid) | CURRENT (GD9 G) | NEW SCULPT (r5), Blender clay at the
# Tier A cameras (pv/r_cur_r5_*, pv/r_new_r5_*), 50% blends over the Tier A photos (pv/rb_*), UE verification captures z10f_* / rr11f_*.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian10_20261002; O=$K/boards; P="$O/parts"; mkdir -p "$P"; C=Saved/Codex/CharacterLookdev_20260930/captures
F10=$K/frames; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_r5; NW=$PV/r_new_r5
B 01_FRONT_CLAY.jpg "01 FRONT CLAY (Tier A front camera): REFERENCE | CURRENT (GD9) | NEW SCULPT (GD10 r5)" 520 "$RF|REFERENCE, ${CU}_front_clay.png|CURRENT, ${NW}_front_clay.png|NEW SCULPT"
B 02_3Q_CLAY.jpg "02 3/4 CLAY (verified ~33 deg camera): REFERENCE | CURRENT | NEW SCULPT" 520 "$RC|REFERENCE, ${CU}_close_clay.png|CURRENT, ${NW}_close_clay.png|NEW SCULPT"
B 03_PROFILE_CLAY.jpg "03 PROFILE CLAY: Tier B profile (low-weight aid) | CURRENT | NEW SCULPT" 520 "$RP|REF profile (aid), ${CU}_side_clay.png|CURRENT, ${NW}_side_clay.png|NEW SCULPT"
ROW n_p.png 0,10000,560,1200 400 ${CU}_side_clay.png ${NW}_side_clay.png; ROW n_c.png 420,720,450,760 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW n_f.png 380,640,280,540 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 04_NOSE_PROFILE.jpg "04 NOSE (fuller tip / lobule / alae, wider alar base, continuous forehead-radix-bridge): profile CURRENT / NEW; 3/4 and front REF / CURRENT / NEW" 900 "$P/n_p.png|profile" "$P/n_c.png|3/4" "$P/n_f.png|front"
ROW m_c.png 360,860,250,794 420 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW m_f.png 360,800,140,660 420 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 05_MIDFACE_CHEEK_VOLUME.jpg "05 MIDFACE / CHEEK VOLUME (malar + mid-cheek flesh, lower cheek / jowl brought forward - not wider, no hollows): REF / CURRENT / NEW" 900 "$P/m_c.png|3/4" "$P/m_f.png|front"
ROW l_c.png 560,860,430,780 380 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW l_p.png 600,1150,700,1200 380 ${CU}_side_clay.png ${NW}_side_clay.png
B 06_LIPS_PROFILE.jpg "06 LIPS (vermilion volume upper / lower, width unchanged): 3/4 REF / CURRENT / NEW; profile CURRENT / NEW" 900 "$P/l_c.png|3/4" "$P/l_p.png|profile"
B 07_FULL_PROFILE_RHYTHM.jpg "07 FULL PROFILE RHYTHM forehead -> radix -> nose -> lips -> chin -> neck: Tier B (aid) | CURRENT | NEW (clay) + UE real NEW" 460 "$RP|REF (aid), ${CU}_side_clay.png|CURRENT, ${NW}_side_clay.png|NEW, $C/z10f_real_side_custom.png|NEW UE real"
B 08_FRONT_OVERLAY.jpg "08 FRONT OVERLAY (50% clay over Tier A front): CURRENT | NEW" 560 "$PV/rb_cur_r5_front.png|CURRENT over REF, $PV/rb_new_r5_front.png|NEW over REF"
B 09_3Q_OVERLAY.jpg "09 3/4 OVERLAY (50% clay over Tier A 3/4): CURRENT | NEW" 560 "$PV/rb_cur_r5_close.png|CURRENT over REF, $PV/rb_new_r5_close.png|NEW over REF"
B 10_SCULPT_ROUNDS.jpg "10 SCULPT ROUNDS (3/4 clay): r1 too weak | r2 lumpy (rejected) | r3 clean | r4 cheek lump (rejected) | r5 adopted" 360 "$PV/r_new_r1_close_clay.png|r1, $PV/r_new_r2_close_clay.png|r2 rejected, $PV/r_new_r3_close_clay.png|r3, $PV/r_new_r4_close_clay.png|r4 rejected, $PV/r_new_r5_close_clay.png|r5 adopted"
L1=(neutral blink blink_left blink_right look_left look_right look_up look_down brows_up brows_down smile frown); L2=(cheek_compress lips_closed mouth_open jaw_open jaw_left jaw_right ph_oo ph_ee ph_mbp ph_w extreme)
r1=""; r2=""; r3=""; for c in "${L1[@]}"; do r1="$r1, $C/z10f_rig_${c}_front_custom.png|$c"; done; for c in "${L2[@]}"; do r2="$r2, $C/z10f_rig_${c}_front_custom.png|$c"; done
for c in neutral blink lips_closed ph_mbp jaw_open smile frown cheek_compress extreme; do r3="$r3, $C/z10f_rig_${c}_3q_custom.png|$c 3/4"; done
B 11_RIG_TEST.jpg "11 RIG TEST (one fresh auto-rig on the r5 sculpt): blink / one-eye blink / gaze / brows / lips / jaw / visemes / extreme" 170 "${r1#, }" "${r2#, }" "${r3#, }"
r=""; for l in lod0 lod1 lod2 lod3; do r="$r, $C/z10_lod_${l}_front_custom.png|face $l"; done
B 12_LOD.jpg "12 LOD (GD10 face 8 LODs)" 330 "${r#, }"
B 13_AFTER_RESTART.jpg "13 AFTER FRESH RESTART (GD10 assets from disk)" 320 "$F10/rr11f_real_F.png|real front, $F10/rr11f_real_C.png|real 3/4, $C/rr11f_rig_blink_front_custom.png|blink, $C/rr11f_rig_jaw_open_front_custom.png|jaw open, $C/rr11f_rig_ph_mbp_front_custom.png|MBP"
ls "$O" | grep -c jpg
