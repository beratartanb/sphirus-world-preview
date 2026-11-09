#!/bin/bash
# trajprobe.sh: PIE in the yard, generate the MM trajectory with the engine function for 90 frames while walking, print it.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"
. Tools/Grip_20261106/g.sh
SV=Saved/SaveGames/SFSaveSlot.sav; O=Saved/Codex/Day_20261107/videos/trajprobe; mkdir -p $O; [ -f $SV ] && mv $SV $O/slot_before.sav
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
rm -f Saved/Codex/Grip_20261106/rec/trajprobe.json
AA; PS; NOTHR; W 16
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at(2200,-700,190,180,-12)" >/dev/null; W 2
J "exec(open(u.Paths.project_dir()+'Tools/Grip_20261106/gx.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/Day_20261107/trajprobe.py',encoding='utf8').read())" measure 12 | cut -c1-300
for i in $(seq 1 40); do W 2; [ -f Saved/Codex/Grip_20261106/rec/trajprobe.json ] && break; done
W 1; PE; [ -f $O/slot_before.sav ] && cp -p $O/slot_before.sav $SV
cat Saved/Codex/Grip_20261106/rec/trajprobe.json 2>/dev/null | cut -c1-3000; echo
