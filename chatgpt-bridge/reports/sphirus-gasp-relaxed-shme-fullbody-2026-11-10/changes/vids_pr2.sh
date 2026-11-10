#!/bin/bash
# vids_pr2.sh (copy of vids_pr.sh; chop walk 1.4 s for the 165 cm/s Relaxed walk) <suffix> <tests...>: production-player regression after promotion (no candidate prelude).
#   VMOT overrides SphMotion props every frame (e.g. "{'EffortEnabled':False}"); default {} = production values.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P="$PWD"; S=$1; shift
MOT=${VMOT:-"{}"}; NS="import builtins; builtins.VID_MOTION=$MOT; "
PP="[('',0.8,0),('W LeftShift',1.7,0),('',1.8,0),('S',2.0,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.5,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PC="[('',0.8,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0),('W A',2.0,0),('',0.8,0),('W D',2.0,0),('',0.8,0),('W',1.5,0),('S',2.0,0),('',1.2,0)]"
PH="[('',0.6,0),('W',2.5,0),('W LeftShift',1.5,0),('',1.2,0),('',0.6,300),('W',2.5,0),('',1.0,0)]"
PO="[('',0.6,0),('W',6.0,0),('W LeftShift',3.0,0),('',1.5,0)]"
PD="[('',0.5,0,-22),('W',1.4,0,-22),('',0.6,0,-22),('E',0.15,0,-22),('',22.0,0,-22),('LeftMouseButton',0.15,0,-22),('',4.0,0,-22)]"
KT="[('',0.6,0),('W',2.0,0),('W D',1.2,0),('D',1.5,0),('S A',1.5,0),('W',1.5,0),('',1.2,0),('W LeftShift',2.2,0),('W D LeftShift',1.2,0),('D LeftShift',1.5,0),('S A LeftShift',1.5,0),('W LeftShift',1.5,0),('S LeftShift',1.5,0),('',1.8,0)]"
PS="[('',1.0,0),('W',4.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('S',2.0,0),('',2.0,0)]"
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
WL="[('',1.0,0),('W',30.0,0),('',2.0,0)]"; PI="[('',55.0,0)]"; RN="[('',0.8,0),('W LeftShift',18.0,0),('',2.5,0)]"
RH(){ for k in 1 2 3; do o=$(bash Tools/Embodied_20261105/relaunch.sh emb_p$S$1$k 2>&1 | tail -1); echo "$o" | cut -c1-40; echo "$o" | grep -q RUNNER_READY && break; taskkill //IM UnrealEditor.exe //F >/dev/null 2>&1; sleep 10; done; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
RT(){ RH $1; echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
USHA=8622025bd9234845ca0fd4132d0459d636c438a7
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav 2>/dev/null | cut -c1-40); [ "$h" = "$USHA" ] || { echo "USER_SLOT_CHANGED $h - batch stopped"; RH z; exit 3; }; }
for t in "$@"; do case $t in
 loco) RH a; V A_loco_$S 2200 -700 190 180 "$PA" "${NS}builtins.VID_SIDE=None";;
 phys) RH b; V PH_phys_$S 2200 -700 190 180 "$PP" "${NS}builtins.VID_SIDE=None";;
 turns) RH c; V B_turns_$S 1400 -700 190 0 "$PB" "${NS}builtins.VID_SIDE=None";;
 strafe) RH d; V CL_strafe_$S 2200 -700 190 180 "$PC" "${NS}builtins.VID_SIDE=None";;
 kturn) RH e; V KT_turns_$S 2200 -700 190 180 "$KT" "${NS}builtins.VID_SIDE=None";;
 hall) RH f; V H_hall_$S 720 400 245 90 "$PH" "${NS}builtins.VID_SIDE=None";;
 out) RH g; V HO_out_$S 720 400 245 90 "$PO" "${NS}builtins.VID_SIDE=None";;
 chop) RH h; V D_chopidle_$S 1640 -455 190 34 "$PD" "${NS}builtins.VID_SIDE=None";;
 efon) RT i; V TE_on_$S -6000 2000 92 0 "$EF" "${NS}builtins.VID_SIDE=None";;
 efoff) RT j; V TE_off_$S -6000 2000 92 0 "$EF" "import builtins; builtins.VID_MOTION=dict($MOT,EffortEnabled=False); builtins.VID_SIDE=None";;
 side) RT k; V TS_side_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=(330,90,25)";;
 q34) RT l; V TQ_q34_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=(300,140,35)";;
 front) RT m; V TF_front_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=(320,200,30)";;
 walk30) RT n; V TW_walk30_$S -6000 2000 92 0 "$WL" "${NS}builtins.VID_SIDE=None";;
 run18) RT o; V TR_run18_$S -6000 2000 92 0 "$RN" "${NS}builtins.VID_SIDE=None";;
 idle) RT q; V TI_idle55_$S -6000 2000 92 0 "$PI" "${NS}builtins.VID_SIDE=None";;
 kturnT) RT s; V KT_turnsT_$S -6000 2000 92 0 "$KT" "${NS}builtins.VID_SIDE=None";;
 kturnS) RT t; V KT_turnsS_$S -6000 2000 92 0 "$KT" "${NS}builtins.VID_SIDE=(420,90,60)";;
 fps60) RT r; VFPS=60 V TP_fps60_$S -6000 2000 92 0 "$PS" "${NS}builtins.VID_SIDE=None; builtins.VID_FPS=60.0";;
esac; done
RH z
