#!/bin/bash
# make_gd13_faceboards.sh : GUARDIAN-13 face-structure boards 01-12 (before hair resumes). REFERENCE | CURRENT (H = D2 checkpoint) | NEW (E6). Clay only (no auto-rig yet).
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian13_20261003; O=$K/boards_face; P="$O/parts"; mkdir -p "$P"; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_E6; NW=$PV/r_new_E6
B 01_FACE_PROPORTION_FRONT.jpg "01 FACE PROPORTION FRONT: REFERENCE | CURRENT (H) | NEW (E6) + 50% overlays (bizygomatic 13.75 -> 14.34 cm, jaw widths identical)" 460 "$RF|REFERENCE, ${CU}_front_clay.png|CURRENT, ${NW}_front_clay.png|NEW, $PV/rb_cur_E6_front.png|CURRENT over REF, $PV/rb_new_E6_front.png|NEW over REF"
ROW z_f.png 250,760,100,700 520 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 02_ZYGOMATIC_MALAR_FRONT.jpg "02 ZYGOMATIC / MALAR FRONT: REFERENCE | CURRENT | NEW (zygomatic band +3 mm/side, malar +1.4 mm fwd, lower-cheek +1.4 mm, malar->temporal transition)" 1950 "$P/z_f.png|x"
ROW z_c.png 200,900,250,794 520 $RC ${CU}_close_clay.png ${NW}_close_clay.png
B 03_ZYGOMATIC_MALAR_3Q.jpg "03 ZYGOMATIC / MALAR 3Q: REFERENCE | CURRENT | NEW" 1950 "$P/z_c.png|x"
ROW mp.png 150,1150,300,1200 520 ${CU}_side_clay.png ${NW}_side_clay.png
B 04_MIDFACE_PROFILE.jpg "04 MIDFACE PROFILE: Tier B (aid) | CURRENT | NEW" 520 "$RP|REF profile (aid), $P/mp.png|CURRENT | NEW"
ROW nb.png 280,620,240,560 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 05_NOSE_BRIDGE_FRONT.jpg "05 NOSE BRIDGE FRONT: REFERENCE | CURRENT | NEW (radix 1.41 -> 1.50, bridge 0.86 -> 0.97 cm, sidewalls widened into the orbit)" 1950 "$P/nb.png|x"
ROW n3.png 380,760,400,794 460 $RC ${CU}_close_clay.png ${NW}_close_clay.png
B 06_NOSE_3Q.jpg "06 NOSE 3Q: REFERENCE | CURRENT | NEW" 1950 "$P/n3.png|x"
ROW nd.png 250,1000,600,1200 460 ${CU}_side_clay.png ${NW}_side_clay.png
B 07_NOSE_PROFILE_DORSUM.jpg "07 NOSE PROFILE DORSUM: Tier B (aid) | CURRENT | NEW (supratip break removed: one dorsum line into the tip)" 520 "$RP|REF profile (aid), $P/nd.png|CURRENT | NEW"
ROW a_f.png 440,700,280,540 300 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW a_c.png 480,740,480,760 300 $RC ${CU}_close_clay.png ${NW}_close_clay.png; ROW a_p.png 520,900,880,1200 300 ${CU}_side_clay.png ${NW}_side_clay.png
"$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/stack_08.png" 1500 "$P/a_f.png|x" "$P/a_c.png|x" "$P/a_p.png|x" 2>&1 | grep -c VSTACK_OK >/dev/null
B 08_NOSTRIL_ALAR_BASE.jpg "08 NOSTRIL / ALAR BASE: front / 3/4 (REF | CURRENT | NEW) / profile (CURRENT | NEW) - alar base +0.8 mm, sill / alar-cheek fill, nostril rim relax" 1950 "$P/stack_08.png|rows: front / 3/4 / profile"
ROW mw.png 500,780,240,560 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 09_MOUTH_WIDTH.jpg "09 MOUTH WIDTH: REFERENCE | CURRENT | NEW (mouth/IPD in the front image: REF 0.855 | CURRENT 0.838 | NEW 0.853)" 1950 "$P/mw.png|x"
ROW lf.png 500,800,300,500 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW lc.png 480,840,420,794 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png
"$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/stack_10.png" 1500 "$P/lf.png|x" "$P/lc.png|x" 2>&1 | grep -c VSTACK_OK >/dev/null
B 10_LIP_FORM.jpg "10 LIP FORM: REFERENCE | CURRENT | NEW (upper lip +0.6 mm, lateral upper lip, corners widened +0.85 mm/side and relaxed)" 1950 "$P/stack_10.png|rows: front / 3/4"
B 11_FULL_FACE_FRONT.jpg "11 FULL FACE FRONT: REFERENCE | CURRENT | NEW" 640 "$RF|REFERENCE, ${CU}_front_clay.png|CURRENT, ${NW}_front_clay.png|NEW"
B 12_FULL_FACE_3Q.jpg "12 FULL FACE 3Q + PROFILE: REFERENCE | CURRENT | NEW" 520 "$RC|REFERENCE 3/4, ${CU}_close_clay.png|CURRENT, ${NW}_close_clay.png|NEW" "$RP|REF profile (aid), ${CU}_side_clay.png|CURRENT, ${NW}_side_clay.png|NEW"
ls "$O" | grep -c jpg
