#!/bin/bash
# seqT.sh: time-base reference runs (data only) on the move test map, saved state: jog stop + sprint stop at
#   30 Hz, 60 Hz (fixed step via dilation, now allowed > 1), VARDT 25..90 Hz random step, NODIL real time.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
PL="[('',1.5,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift LeftControl',3.5,0),('',3.0,0)]"
CV="import builtins; print('CVARS', {k:u.SystemLibrary.get_console_variable_float_value(k) for k in ('t.MaxFPS','r.VSync','t.IdleWhenNotForeground','p.MaxSubstepDeltaTime')}, 'FIXED', u.SystemLibrary.get_console_variable_int_value('r.FixedFrameRate') if False else None)"
for m in ${MS:-F30 F60 VAR RT}; do case $m in
 F30) DFPS=30.0 bash Tools/UE59_20261118/run2.sh T_${m} -6000 2000 92 0 "$PL" "$CV";;
 F60) DFPS=60.0 bash Tools/UE59_20261118/run2.sh T_${m} -6000 2000 92 0 "$PL" "$CV";;
 VAR) DFPS=60.0 bash Tools/UE59_20261118/run2.sh T_${m} -6000 2000 92 0 "$PL" "$CV; builtins.VID_VARDT=(25.0,90.0)";;
 RT)  DFPS=60.0 bash Tools/UE59_20261118/run2.sh T_${m} -6000 2000 92 0 "$PL" "$CV; builtins.VID_NODIL=True";;
esac; done
echo SEQT_DONE
