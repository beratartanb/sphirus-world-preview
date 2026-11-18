#!/bin/bash
# ab1.sh <suffix> <profiles...>: Phase-1 locomotion A/B/C on the flat test map, same plan / camera / map / 30 Hz step for every profile.
# Profiles: A (Relaxed prod), Bn (GASP Normal, native speeds), Bs (GASP Normal at A speeds), C (curated map from Tools/UE59_20261116/cmap.py)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; P="$PWD"; S=$1; shift; export VWAIT=${VWAIT:-1500}
[ -f Saved/SaveGames/SFSaveSlot.sav ] || { echo "NO_SLOT"; exit 8; }
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); echo "SLOT $USHA"
NS0="import builtins; builtins.VID_MOTION={}; builtins.VID_ABP={}; builtins.VID_CAM={}; builtins.VIDC_CAMVARS=(); builtins.VID_BODY={}; builtins.VID_BODYSEQ={}; builtins.VID_PAWN={}; builtins.VID_REFPOSE=None; builtins.VID_NECK=True; builtins.VID_SIDE=(260,90,20,95,'pelvis'); "
RH(){ for k in 1 2 3; do o=$(bash Tools/Embodied_20261105/relaunch.sh emb_u$S$1$k 2>&1 | tail -1); echo "$o" | grep -q RUNNER_READY && break; taskkill //IM UnrealEditor.exe //F >/dev/null 2>&1; sleep 10; done; bash Tools/Day_20261107/ed.sh Tools/GASP_20261109/warm.py measure 600 | grep -c WARM; }
RT(){ RH $1; echo "${MAP:-/Game/Sphirus/Test/L_Sph_MoveTest}" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$P/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
CK(){ h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav 2>/dev/null | cut -c1-40); [ "$h" = "$USHA" ] || { echo "SLOT_CHANGED $h"; exit 3; }; }
V(){ bash Tools/Camera_20261112/vc55.sh "$@" 2>&1 | grep -E "VIDREC|FRAMES|mp4"; CK; }
PLAN=${PLAN:-"[('',2.0,0),('W',10.0,0),('W LeftShift',8.0,0),('W LeftShift LeftControl',6.0,0),('',3.0,0),('W',4.0,0),('',2.0,0),('S',4.0,0),('S A',3.0,0),('',2.0,0)]"}
PF="exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/prof.py',encoding='utf8').read())"
for t in "$@"; do case $t in
 A)  RT a; V ${LP:-U1}_A_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='A'; $PF; ${XP:-pass}";;
 Bn) RT b; V ${LP:-U1}_Bn_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='B'; builtins.SPH_SPEEDS=None; $PF; ${XP:-pass}";;
 Bs) RT c; V ${LP:-U1}_Bs_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='B'; builtins.SPH_SPEEDS=((165,165,165),(375,375,375),(585,585,585)); $PF; ${XP:-pass}";;
 D1) RT e; V ${LP:-U1}_D1_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=1; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
 D2) RT f; V ${LP:-U1}_D2_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=2; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
 D3) RT g; V ${LP:-U1}_D3_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=3; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
 E)  RT h; V ${LP:-U1}_E_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=3; builtins.C_STOP=1; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
 X)  RT x; V ${LP:-U1}_X_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=3; ${CPRE:-pass}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
 P)  RT p; V ${LP:-U1}_P_$S -6000 2000 92 0 "$PLAN" "${NS0}${XP:-pass}";;
 C)  RT d; V ${LP:-U1}_C_$S -6000 2000 92 0 "$PLAN" "${NS0}builtins.SPH_PROF='C'; builtins.C_FWD=0; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/cmap.py',encoding='utf8').read()); $PF; ${XP:-pass}";;
esac; cp Saved/UE59Work/probe/prof_set_*.txt Saved/UE59Work/probe/last_prof_$t.txt 2>/dev/null; done
RH z
