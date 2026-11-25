#!/bin/bash
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; R=-4793; SP=Saved/UE59Work/b4/plan_sprel.txt; RP=Saved/UE59Work/b4/plan_runrel.txt; O=Saved/UE59Work/b4/coast_results.txt
run() { bash Saved/UE59Work/b4/sc.sh $1 $2 "$3" "$5" > /dev/null 2>&1; "$PY" Saved/UE59Work/b4/an_coast.py $1 $4 >> $O 2>&1; }
# corner: wall turned 45 deg across the path, centre 200 cm past the release, offset 60 cm to the side
run b4C3_corner $SP "[[$((R+200)),2060,150,30,400,300,45]]" 1400
# narrow passage 110 cm wide from 100 before the release to 400 after: the sweep must NOT block
run b4C3_narrow $SP "[[$((R+150)),1915,150,500,60,300],[$((R+150)),2085,150,500,60,300]]"
# knee-high box (35 cm) 200 cm past the release
run b4C3_lowbox $SP "[[$((R+215)),2000,17,30,300,35]]" 1400
# cliff: the lane continues on a 60 cm platform that ends 160 cm past the release (pawn starts on it)
run b4C3_cliff $SP "[[$((R-600)),2000,30,1520,400,60]]" "" "-6000 2000 152 0"
# up ramp 12 deg starting 60 cm past the release, and a 45 deg ramp (not walkable)
run b4C3_ramp12 $SP "[[$((R+300)),2000,-10,500,400,100,0,12]]"
run b4C3_ramp45 $SP "[[$((R+200)),2000,-20,300,400,100,0,45]]"
# stairs: 5 steps of 18 cm, 30 cm deep, from 120 cm past the release
run b4C3_stairs $SP "[[$((R+135)),2000,9,30,300,18],[$((R+165)),2000,18,30,300,36],[$((R+195)),2000,27,30,300,54],[$((R+225)),2000,36,30,300,72],[$((R+255)),2000,45,30,300,90]]" 1340
# run (not sprint) release on the open lane, and a release followed by a new key 0.3 s later
run b4C3_run_open $RP "[]"
echo "[('', 1.0, 0), ('W LeftShift LeftControl', 2.75, 0), ('', 0.3, 0), ('D', 1.5, 0), ('', 2.0, 0)]" > Saved/UE59Work/b4/plan_sprel_turn.txt
run b4C3_rel_then_D Saved/UE59Work/b4/plan_sprel_turn.txt "[]"
echo "[('', 1.0, 0), ('W LeftShift LeftControl', 2.75, 0), ('', 0.25, 0), ('C', 0.15, 0), ('', 2.0, 0), ('C', 0.15, 0), ('', 1.0, 0)]" > Saved/UE59Work/b4/plan_sprel_crouch.txt
run b4C3_rel_then_crouch Saved/UE59Work/b4/plan_sprel_crouch.txt "[]"
echo "[('', 1.0, 0), ('W LeftShift LeftControl', 2.75, 0), ('', 0.25, 0), ('SpaceBar', 0.15, 0), ('', 2.5, 0)]" > Saved/UE59Work/b4/plan_sprel_jump.txt
run b4C3_rel_then_jump Saved/UE59Work/b4/plan_sprel_jump.txt "[]"
bash Saved/UE59Work/b4/sc.sh b4C3_cleanup Saved/UE59Work/b4/plan_idle4.txt "[]" > /dev/null 2>&1
echo COAST_BATCH_DONE >> $O
