#!/bin/bash
# vid.sh <label> <plan> <rear tuple or ''> : house-map video from the shore start; rear = fixed full-body camera behind the start, '' = gameplay camera
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; [ -f Saved/Codex/Day_20261107/videos/$1.mp4 ] && { echo "EXISTS $1"; exit 0; }
X="import builtins; builtins.REAR=${3:-None}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/hk_rear9.py',encoding='utf8').read())"
VSHOT=1 DFPS=60.0 bash Tools/UE59_20261118/run2.sh $1 ${POS:-1400 2980 79 42} "$(cat Saved/UE59Work/mr1/p_$2.txt)" "$X" 2>&1 | grep -E "VIDREC|Error" | cut -c1-80
