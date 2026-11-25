#!/bin/bash
# sc.sh <label> <plan file> '<scene json>' "<pos>" : lane run with an in-memory test scene; logs coast telemetry
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
[ -f Saved/Codex/Grip_20261106/rec/$1.json ] && { echo "EXISTS $1"; exit 0; }
echo "$3" > Saved/UE59Work/b4/scene.json
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh Saved/UE59Work/b4/scene_place.py b4scene 120 2>&1 | grep -a "SCENE\|Error" | cut -c1-200
X="import builtins; builtins.CT_FAT=None; builtins.CT_CARRY=None; builtins.CT_SET=None; builtins.CT_PROP=None; builtins.CT_EXS=('CS_Clear',); builtins.CT_EXM=None; builtins.CT_EXTRA=('CS_T','CS_Avail','CS_Floor','CS_Budget','CS_Dist'); exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/hk_fall9.py',encoding='utf8').read())"
DFPS=60.0 POS="${4:--6000 2000 92 0}" bash Tools/UE59_20261120/seqP.sh $1 $2 "$X" | grep -E "VIDREC|Error|mp4" | cut -c1-120
