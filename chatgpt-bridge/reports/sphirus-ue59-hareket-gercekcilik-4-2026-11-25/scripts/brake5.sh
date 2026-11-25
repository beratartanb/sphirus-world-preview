#!/bin/bash
# brake5.sh <tag>: brake-assist v3 scene tests (sprint release ~584 cm/s at x ~ R); results -> p4/res/brake_<tag>.txt
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T=$1
R=-4793; SP=Saved/UE59Work/b4/plan_sprel.txt; RP=Saved/UE59Work/b4/plan_runrel.txt; O=Saved/UE59Work/p4/res/brake_$T.txt; P=Saved/UE59Work/p4
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/UE59_20261125/c_p4_defaults.py" p4def 120 2>&1 | grep -a P4DEF | cut -c1-200 >> $O
run() { bash $P/rec.sh p4K${T}_$1 $2 "$3" "$4" 60 "$5" > /dev/null 2>&1; "$PY" Tools/UE59_20261125/an_coast5.py p4K${T}_$1 "$3" >> $O 2>&1; }
run open $SP "[]"
run wall260 $SP "[[$((R+290)),2000,150,30,400,300]]"
run wall150 $SP "[[$((R+180)),2000,150,30,400,300]]"
run corner $SP "[[$((R+200)),2060,150,30,400,300,45]]"
run narrow $SP "[[$((R+150)),1915,150,500,60,300],[$((R+150)),2085,150,500,60,300]]"
run lowbox $SP "[[$((R+215)),2000,17,30,300,35]]"
run cliff $SP "[[$((R-600)),2000,30,1520,400,60]]" "-6000 2000 152 0"
run ramp12 $SP "[[$((R+300)),2000,-10,500,400,100,0,12]]"
run ramp45 $SP "[[$((R+200)),2000,-20,300,400,100,0,45]]"
run stairs $SP "[[$((R+135)),2000,9,30,300,18],[$((R+165)),2000,18,30,300,36],[$((R+195)),2000,27,30,300,54],[$((R+225)),2000,36,30,300,72],[$((R+255)),2000,45,30,300,90]]"
run moving $SP "[[$((R+520)),2000,80,60,300,160,0,0,1]]" "" "import builtins; builtins.MOV5=(3.75,-260.0); exec(open(u.Paths.project_dir()+'Tools/UE59_20261125/hk_mov5.py',encoding='utf8').read())"
run runopen $RP "[]"
bash $P/rec.sh p4K${T}_cleanup Saved/UE59Work/b4/plan_idle4.txt "[]" "" 60 "import builtins; builtins.MOV5=None" > /dev/null 2>&1
echo BRAKE5_DONE >> $O
