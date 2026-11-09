#!/bin/bash
# v56.sh <label> <plan> [x y yaw prelude]: locomotion video in the empty test corridor (L_Sph_MoveTest); optional start spot.
# Loads the test map, records with vid.py (fixed 30 fps step), encodes, then reloads the house map.
. Tools/Grip_20261106/g.sh
O=Saved/Codex/Day_20261107/videos; mkdir -p $O/$1
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep LOADED | cut -c1-120
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
SD=Saved/Screenshots/WindowsEditor; rm -f $SD/ScreenShot*.png
AA; PS; NOTHR; W 8
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at(${3:--200},${4:-0},100,${5:-0},-12); ${6:-pass}" >/dev/null; W 1
J "exec(open(u.Paths.project_dir()+'Tools/Grip_20261106/gx.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/Day_20261107/vid.py',encoding='utf8').read())
vidrec('$1',$2)" measure 1 | grep VIDREC
for i in $(seq 1 120); do W 2; [ -f Saved/Codex/Grip_20261106/rec/$1.json ] && break; done
W 2; PE
N=$(ls $SD/ScreenShot*.png 2>/dev/null | wc -l); echo "FRAMES $N"
mkdir -p $O/$1/png; mv $SD/ScreenShot*.png $O/$1/png/ 2>/dev/null
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python Tools/Day_20261107/mkvid.py -- "$PWD/$O/$1.mp4" 30 5 168 1515 1090 "$PWD/$O/$1/png" 2>&1 | grep -E "VIDEO|Error" | head -3
mkdir -p Saved/Codex/Day_20261107/frames/$1; ls $O/$1/png/*.png 2>/dev/null | awk 'NR%30==1' | while read f; do cp "$f" Saved/Codex/Day_20261107/frames/$1/; done
[ -f $O/$1.mp4 ] && rm -rf $O/$1/png
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep LOADED | cut -c1-120
ls -la $O/$1.mp4 2>/dev/null | awk '{print $5,$9}'
