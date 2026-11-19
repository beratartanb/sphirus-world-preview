#!/bin/bash
# seqR.sh: stop control set (60 Hz fixed step unless DFPS), saved state, move test map. V0 = saved, RM = root-motion stop hook.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
PS="[('',1.5,0),('W',3.0,0),('',2.0,0),('W',3.4,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift',3.3,0),('',2.5,0),('W LeftShift',3.65,0),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0),('W LeftShift LeftControl',4.3,0),('',3.0,0),('W LeftShift LeftControl',4.6,0),('',3.0,0),('W',1.5,0),('W LeftShift',2.0,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.25,360),('',2.5,0),('W',3.0,0),('W',0.25,360),('',2.5,0)]"
echo "$PS" > Saved/UE59Work/stopset_plan.txt
OR0="u.SystemLibrary.execute_console_command(None,'DDCvar.OffsetRootBone.TranslationRadius 0')"
HK(){ echo "exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/$1',encoding='utf8').read())"; }
V0="pass"; VAR="import builtins; builtins.VID_VARDT=(25.0,90.0)"; RM="$(HK hk_rmstop.py)"; CB="$(HK hk_clipbrake.py)"; CBV="$(HK hk_clipbrake.py); builtins.VID_VARDT=(25.0,90.0)"
OR45="$(HK hk_orprobe.py)"; CBR="$(HK hk_curveread.py); import builtins; builtins.VID_MOTION={'ClipBrakeOn':True,'ClipK':1.0,'ClipMin':100.0,'ClipMax':3000.0}"; CBA="import builtins; builtins.VID_MOTION={'ClipBrakeOn':True,'ClipK':1.0,'ClipMin':100.0,'ClipMax':3000.0}"; CBAV="$CBA; builtins.VID_VARDT=(25.0,90.0)"
for v in ${VS:-V0 RM}; do eval X=\$$v
  for hz in ${HZ:-60}; do DFPS=$hz.0 bash Tools/UE59_20261118/run2.sh R_${v}_$hz${TAG} -6000 2000 92 0 "$PS" "$X"; done
done
echo SEQR_DONE
