#!/bin/bash
# v55.sh <label> <x> <y> <z> <yaw> <plan-python-list> [prelude-python]: fresh game at the given spot, gameplay video recorded by
# vid.py at a fixed 30 fps game step, encoded to Saved/Codex/Day_20261107/videos/<label>.mp4, PNGs removed.
. Tools/Grip_20261106/g.sh
W(){ sleep $1; }   # flow.sh's `timeout N cat /dev/zero` hung once for 3.5 h on Windows (B_turns_shme3, 2026-11-09)
SV=Saved/SaveGames/SFSaveSlot.sav; O=Saved/Codex/Day_20261107/videos; mkdir -p $O/$1; [ -f $SV ] && mv $SV $O/$1/slot_before.sav
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
SD=Saved/Screenshots/WindowsEditor; rm -f $SD/ScreenShot*.png
AA; PS; NOTHR; W 16
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at($2,$3,$4,$5,-12); $7" >/dev/null; W 2
J "exec(open(u.Paths.project_dir()+'Tools/Grip_20261106/gx.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/Day_20261107/vid.py',encoding='utf8').read())
vidrec('$1',$6)" measure 1 | grep VIDREC
for i in $(seq 1 300); do W 2; [ -f Saved/Codex/Grip_20261106/rec/$1.json ] && break; done
W 2; PE; [ -f $O/$1/slot_before.sav ] && cp -p $O/$1/slot_before.sav $SV
N=$(ls $SD/ScreenShot*.png 2>/dev/null | wc -l); echo "FRAMES $N"
mkdir -p $O/$1/png; mv $SD/ScreenShot*.png $O/$1/png/ 2>/dev/null
"/c/Program Files/Blender Foundation/Blender 5.2/blender.exe" --background --factory-startup --python Tools/Day_20261107/mkvid.py -- "$PWD/$O/$1.mp4" 30 5 168 1515 1090 "$PWD/$O/$1/png" 2>&1 | grep -E "VIDEO|Error" | head -3
mkdir -p Saved/Codex/Day_20261107/frames/$1; ls $O/$1/png/*.png 2>/dev/null | awk 'NR%30==1' | while read f; do cp "$f" Saved/Codex/Day_20261107/frames/$1/; done
[ -f $O/$1.mp4 ] && rm -rf $O/$1/png
ls -la $O/$1.mp4 2>/dev/null | awk '{print $5,$9}'
