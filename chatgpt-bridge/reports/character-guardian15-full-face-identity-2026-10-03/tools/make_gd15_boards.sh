#!/bin/bash
# make_gd15_boards.sh : GUARDIAN-15 clay face boards 01-18. REFERENCE (Tier A) | BASELINE (GD14b K5) | NEW (N1). Clay only, no rig.
set -u; cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
K=Saved/Codex/CharacterGuardian15_20261003; O=$K/boards; P="$O/parts"; mkdir -p "$P"; TD=Saved/Codex/CharacterIdentity_20260930/track; PV=$K/pv; HS=$K/hs; RB=Saved/Codex/CharacterGuardian2_20261001/refB; T=Tools/CharacterLookdev_20260930
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; ROOT="$(cygpath -m "$(pwd)")/"
B() { local rows=(); for r in "${@:4}"; do rows+=("$(echo "$r" | sed -E "s#(^|, )([^|,]+)\|#\1${ROOT}\2|#g")"); done; "$PY" $T/lk_board.py "$ROOT$O/$1" "$2" "$3" "${rows[@]}" | tail -c 30; echo; }
ROW() { local out=$1 crop=$2 h=$3; shift 3; CROP=$crop "$BL" -b --factory-startup --python $T/blender_gd_row.py -- "$P/$out" $h "$@" 2>&1 | grep -ci error >/dev/null; }
VS() { local out=$1; shift; "$BL" -b --factory-startup --python $T/blender_vstack.py -- "$P/$out" 1500 "$@" 2>&1 | grep -c VSTACK_OK >/dev/null; }
RF=$TD/ref_front_x4.png; RC=$TD/ref_close_x2.png; RP=$RB/turnaround_p5.png; CU=$PV/r_cur_FIN; NW=$PV/r_new_FIN
ROW f.png 60,900,60,740 640 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 01_FRONT_FULL_FACE.jpg "01 FRONT FULL FACE: REFERENCE | BASELINE (GD14b K5) | NEW (GD15 N1)" 1950 "$P/f.png|x"
ROW c.png 120,940,100,794 640 $RC ${CU}_close_clay.png ${NW}_close_clay.png
B 02_3Q_FULL_FACE.jpg "02 3/4 FULL FACE (verified ~33 deg): REFERENCE | BASELINE | NEW" 1950 "$P/c.png|x"
B 03_PROFILE_FACE.jpg "03 PROFILE: BASELINE | NEW (Tier B aid, low weight)" 560 "$RP|Tier B (aid), ${CU}_side_clay.png|BASELINE K5, ${NW}_side_clay.png|NEW N1"
B 04_FRONT_SILHOUETTE_OVERLAY.jpg "04 SILHOUETTE OVER TIER A: red = NEW, cyan = BASELINE (front / 3/4)" 700 "$PV/_olFIN_F.png|front, $PV/_olFIN_C.png|3/4"
B 05_FACE_WIDTH_HEIGHT.jpg "05 FACE WIDTH / HEIGHT: 50% clay over Tier A front (BASELINE | NEW); eye-stomion / IPD REF 1.153 | K5 1.073 | NEW 1.115" 600 "$PV/rb_cur_FIN_front.png|BASELINE, $PV/rb_new_FIN_front.png|NEW"
ROW z.png 250,620,60,740 560 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 06_ZYGOMATIC_FRONT.jpg "06 ZYGOMATIC FRONT: REFERENCE | BASELINE | NEW (zygoma reach +2 mm out / +0.8 mm up, malar apex lateral)" 1950 "$P/z.png|x"
ROW z3.png 250,760,150,794 560 $RC ${CU}_close_clay.png ${NW}_close_clay.png
B 07_ZYGOMATIC_3Q.jpg "07 ZYGOMATIC 3/4: REFERENCE | BASELINE | NEW" 1950 "$P/z3.png|x"
B 08_MALAR_POSITION.jpg "08 MALAR POSITION: 50% clay over Tier A 3/4 (BASELINE | NEW)" 600 "$PV/rb_cur_FIN_close.png|BASELINE, $PV/rb_new_FIN_close.png|NEW"
ROW md.png 150,1150,350,1200 500 ${CU}_side_clay.png ${NW}_side_clay.png
B 09_MIDFACE_DEPTH.jpg "09 MIDFACE DEPTH: profile BASELINE | NEW (midface +1.2 mm fwd, lateral lip support +0.7 mm)" 1950 "$P/md.png|x"
ROW lc.png 420,880,60,740 500 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW lc3.png 450,920,150,794 500 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_10.png "$P/lc.png|x" "$P/lc3.png|x"
B 10_LOWER_CHEEK_TISSUE.jpg "10 LOWER-CHEEK TISSUE: REFERENCE | BASELINE | NEW (lower cheek +1.5 mm, prejowl / marionette groove filled, jaw border unchanged)" 1950 "$P/stack_10.png|rows: front / 3/4"
ROW cp.png 560,900,200,600 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW cp3.png 600,940,300,794 460 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_11.png "$P/cp.png|x" "$P/cp3.png|x"
B 11_CHIN_PAD.jpg "11 CHIN PAD: REFERENCE | BASELINE | NEW (chin point -0.7 mm, lateral chin-pad fullness, softer chin-jaw blend)" 1950 "$P/stack_11.png|rows: front / 3/4"
ROW mw.png 520,760,200,600 460 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 12_MOUTH_WIDTH.jpg "12 MOUTH WIDTH: REFERENCE | BASELINE | NEW (corners +0.5 mm/side; IPD -2.4 mm -> mouth/IPD clay 0.853 -> 0.899, projected real-render ~0.86 vs REF 0.855)" 1950 "$P/mw.png|x"
B 13_FULL_PERIORAL.jpg "13 FULL PERIORAL (clay close-ups): BASELINE | NEW" 380 "$HS/fin_mouth_front_0.png|BASELINE front, $HS/fin_mouth_front_1.png|NEW front" "$HS/fin_mouth_3q_0.png|BASELINE 3/4, $HS/fin_mouth_3q_1.png|NEW 3/4, $HS/fin_mouth_side_0.png|BASELINE side, $HS/fin_mouth_side_1.png|NEW side"
ROW br.png 230,470,140,660 420 $RF ${CU}_front_clay.png ${NW}_front_clay.png
B 14_BROW_POSITION.jpg "14 BROW POSITION: REFERENCE | BASELINE | NEW (brow skin -1.2 mm, arch peak kept, tail -0.5 mm, shelter +0.5 mm; brow hair groom follows the skin after rig)" 1950 "$P/br.png|x"
ROW eo.png 280,560,140,660 400 $RF ${CU}_front_clay.png ${NW}_front_clay.png; ROW eo3.png 300,620,260,794 400 $RC ${CU}_close_clay.png ${NW}_close_clay.png
VS stack_15.png "$P/eo.png|x" "$P/eo3.png|x"
B 15_EYE_BROW_ORBIT.jpg "15 EYE / BROW / ORBIT: REFERENCE | BASELINE | NEW (eyes + orbit 1.2 mm medial per side: inner-canthal / IPD REF 0.538 | K5 0.545 | NEW 0.527)" 1950 "$P/stack_15.png|rows: front / 3/4" "$HS/fin_eye_front_0.png|BASELINE eye close, $HS/fin_eye_front_1.png|NEW eye close, $HS/fin_eye_3q_0.png|BASELINE 3/4, $HS/fin_eye_3q_1.png|NEW 3/4"
B 16_FULL_CLAY_FRONT.jpg "16 FULL CLAY FRONT (no labels): REFERENCE | NEW" 860 "$RF|, ${NW}_front_clay.png|"
B 17_FULL_CLAY_3Q.jpg "17 FULL CLAY 3/4: REFERENCE | NEW" 860 "$RC|, ${NW}_close_clay.png|"
B 18_FULL_CLAY_PROFILE.jpg "18 FULL CLAY PROFILE: Tier B (aid) | NEW" 760 "$RP|, ${NW}_side_clay.png|"
ls "$O" | grep -c jpg
