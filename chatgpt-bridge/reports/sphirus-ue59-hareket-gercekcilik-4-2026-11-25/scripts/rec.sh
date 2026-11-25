#!/bin/bash
# rec.sh <label> <plan file> [scene json|-] [pos] [hz|var] [extra prelude]: one recording on the move test map with brake/contact telemetry.
# Scene boxes (b4 scene_place.py format) are placed in the editor world in memory and removed with '[]'. Labels are never reused.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
[ -f Saved/Codex/Grip_20261106/rec/$1.json ] && { echo "EXISTS $1"; exit 0; }
SC="${3:--}"; [ "$SC" = "-" ] && SC='[]'
echo "${MAP:-/Game/Sphirus/Test/L_Sph_MoveTest}" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 > /dev/null 2>&1
echo "$SC" > Saved/UE59Work/b4/scene.json
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/b4/scene_place.py p4scene 120 2>&1 | grep -a "SCENE\|Error" | cut -c1-200
M=${5:-60}; V=""; [ "$M" = var ] && { M=60; V="; builtins.VID_VARDT=(22.0,60.0)"; }
X="import builtins; builtins.VID_VARDT=None; builtins.CT_FAT=None; builtins.CT_CARRY=None; builtins.CT_SET=None; builtins.CT_PROP=None; builtins.CT_EXS=('CS_Clear',); builtins.CT_EXM=None; builtins.CT_EXTRA=('CS_T','CS_Avail','CS_Floor','CS_Budget','CS_Dist','CS_Slope'); exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/hk_fall9.py',encoding='utf8').read())$V; ${6:-builtins.MOV5=None}"
DFPS=$M.0 POS="${4:--6000 2000 92 0}" bash Tools/UE59_20261120/seqP.sh $1 $2 "$X" | grep -E "VIDREC|Error|mp4" | cut -c1-120
