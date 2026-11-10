#!/bin/bash
# vids_rx.sh <suffix> <tests...>: candidate B (GASP Relaxed + clip speeds + PhysBrake) recordings on the production pawn.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; P="$PWD"; S=$1; shift
CFG=${RXCFG:-1}; MOT=${RXMOT:-"{'PhysBrake':True}"}
RX="import builtins; builtins.VID_MOTION=$MOT; exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/rx_cfg.py',encoding='utf8').read()); rxcfg($CFG); "
PP="[('',0.8,0),('W LeftShift',1.7,0),('',1.8,0),('S',2.0,0),('',1.5,0),('W',1.5,0),('S',1.5,0),('',1.5,0)]"
PB="[('',0.5,0),('W',1.5,0),('W',0.5,360),('W',1.5,0),('W',0.5,-360),('W',1.2,0),('W',0.3,150),('W',0.6,0),('W',0.3,-150),('W',0.8,0),('',1.2,0),('',0.8,180),('W',0.4,0),('',1.0,0),('W LeftShift',1.0,0),('W LeftShift',0.5,360),('W LeftShift',1.2,0),('',1.5,0)]"
PA="[('',0.7,0),('W',2.0,0),('W LeftShift',1.1,0),('W LeftShift',1.2,150),('W LeftShift',1.3,0),('W',1.2,0),('',1.3,0),('W',1.2,0),('',1.0,0)]"
PC="[('',0.8,0),('A',2.5,0),('',1.0,0),('D',2.5,0),('',1.0,0),('W A',2.0,0),('',0.8,0),('W D',2.0,0),('',0.8,0),('W',1.5,0),('S',2.0,0),('',1.2,0)]"
PS="[('',1.0,0),('W',4.0,0),('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W',1.5,0),('S',2.0,0),('',2.0,0)]"
EF="[('',0.8,0),('W LeftShift',1.6,0),('S LeftShift',1.4,0),('W LeftShift',1.0,0),('S LeftShift',1.0,0),('W LeftShift',1.0,0),('',2.0,0),('S LeftShift',1.4,0),('',5.0,0),('W LeftShift',1.4,0),('S LeftShift',1.4,0),('',2.0,0)]"
WL="[('',1.0,0),('W',30.0,0),('',2.0,0)]"; PI="[('',55.0,0)]"
RH(){ bash Tools/Embodied_20261105/relaunch.sh emb_x$S$1 2>&1 | tail -1 | cut -c1-40; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
RT(){ RH $1; echo "/Game/Sphirus/Test/L_Sph_MoveTest" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
V(){ bash Tools/Day_20261107/v55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; }
for t in "$@"; do case $t in
 loco) RH a; V A_loco_$S 2200 -700 190 180 "$PA" "${RX}builtins.VID_SIDE=None";;
 phys) RH b; V PH_phys_$S 2200 -700 190 180 "$PP" "${RX}builtins.VID_SIDE=None";;
 turns) RH c; V B_turns_$S 1400 -700 190 0 "$PB" "${RX}builtins.VID_SIDE=None";;
 strafe) RH d; V CL_strafe_$S 2200 -700 190 180 "$PC" "${RX}builtins.VID_SIDE=None";;
 efon) RT e; V TE_on_$S -6000 2000 92 0 "$EF" "${RX}builtins.VID_SIDE=None";;
 efoff) RT f; V TE_off_$S -6000 2000 92 0 "$EF" "${RX/\{\'PhysBrake\':True\}/{'PhysBrake':True,'EffortEnabled':False}}builtins.VID_MOTION=dict(builtins.VID_MOTION,EffortEnabled=False); builtins.VID_SIDE=None";;
 side) RT g; V TS_side_$S -6000 2000 92 0 "$PS" "${RX}builtins.VID_SIDE=(330,90,25)";;
 q34) RT h; V TQ_q34_$S -6000 2000 92 0 "$PS" "${RX}builtins.VID_SIDE=(300,140,35)";;
 walk30) RT i; V TW_walk30_$S -6000 2000 92 0 "$WL" "${RX}builtins.VID_SIDE=None";;
 idle) RT j; V TI_idle55_$S -6000 2000 92 0 "$PI" "${RX}builtins.VID_SIDE=None";;
esac; done
RH z
