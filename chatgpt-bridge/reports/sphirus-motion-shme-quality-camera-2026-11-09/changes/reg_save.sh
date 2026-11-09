#!/bin/bash
# reg_save.sh <label>: save/load regression on the real house map. Live user slot moved aside for the test and restored.
#  1. new game -> wake -> teleport to the yard, walk 2 s, SaveGame (Story Framework), note pose
#  2. teleport 7 m away, LoadGame(True) -> position must return to the saved spot; walk 2 s (locomotion after load)
#  3. PIE stopped and started again with the test slot present (boot load path) -> position after boot; walk 2 s
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; . Tools/Grip_20261106/g.sh
LBL=${1:-reg_save}; SV=Saved/SaveGames/SFSaveSlot.sav; O=Saved/Codex/Day_20261107/$LBL; mkdir -p $O; TF=$O/t.txt; : > $TF
[ -f $SV ] && mv $SV $O/slot_user.sav
AA(){ powershell.exe -NoProfile -Command "(New-Object -ComObject WScript.Shell).AppActivate('sphirus') | Out-Null"; }
H="exec(open(u.Paths.project_dir()+'Tools/SF52_20261105/h.py',encoding='utf8').read())"
Q="print('RS',TAG,round(u.GameplayStatics.get_time_seconds(W),2),[round(v) for v in PW.get_actor_location().to_tuple()],round(PW.get_actor_rotation().yaw),round(PW.get_velocity().length()),PW.get_editor_property('GR_HomeContext'))"
walk(){ DX "tap('W')" >/dev/null; W 2; DX "TAG='$1'; $Q" | grep RS | tee -a $TF; W 0.5; DX "rel('W'); TAG='$1_rel'; $Q" | grep RS | tee -a $TF; }
AA; PS; NOTHR; W 16
DX "[rel(k) for k in ('W','A','S','D','C','SpaceBar','LeftShift')]; at(2000,-700,190,180,-12)" >/dev/null; W 2
walk s1_walk
DX "$H; save(); TAG='s1_saved'; $Q" | grep -E "RS|rror" | tee -a $TF; W 2
ls -la $SV 2>/dev/null | awk '{print "SLOT_WRITTEN",$5}' | tee -a $TF
DX "at(1300,-700,190,0,-12); TAG='s2_moved'; $Q" | grep RS | tee -a $TF; W 1
DX "$H; load(); TAG='s2_load_called'; $Q" | grep -E "RS|rror" | tee -a $TF; W 4
DX "TAG='s2_after_load'; $Q" | grep RS | tee -a $TF
walk s2_walk
W 1; PE; W 4
AA; PS; NOTHR; W 18
DX "TAG='s3_boot'; $Q" | grep RS | tee -a $TF
walk s3_walk
W 1; PE
[ -f $O/slot_user.sav ] && cp -p $O/slot_user.sav $SV
cat $TF
