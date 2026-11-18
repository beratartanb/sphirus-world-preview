#!/bin/bash
# seq6.sh: diagnostic-camera videos redone with a wider side camera (520 cm, whole body + feet + ground in frame)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export VSHOT=1
HP="$(cat Saved/UE59Work/hp_plan.txt)"
BEF="PW_=u.GameplayStatics.get_player_controller(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),0).get_controlled_pawn(); PW_.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); builtins.VID_MOTION={'SlopeOn':False}"
LM(){ echo "$1" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
export VSIDE="(520,90,30,95,'pelvis')"
LM /Game/GraceRanger/Maps/L_GR_SphirusHouse
bash Tools/UE59_20261118/run2.sh V18_slopediag_before 2640 420 322 -83 "$HP" "$BEF"
bash Tools/UE59_20261118/run2.sh V18_slopediag_after 2640 420 322 -83 "$HP" "pass"
LM /Game/Sphirus/Test/L_Sph_MoveTest
P="[('',2.0,0),('W',3.0,0),('W',0.25,720),('W',3.0,0),('W',0.25,-720),('W',3.0,0),('W LeftShift',3.0,0),('W LeftShift',0.25,540),('W LeftShift',3.0,0),('W LeftShift',0.25,-720),('W LeftShift',3.0,0),('',2.0,0)]"
bash Tools/UE59_20261118/run2.sh V18_turnsdiag_after -6000 2000 92 0 "$P" "pass"
P2="[('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift LeftControl',4.0,0),('',3.0,0),('W',3.0,0),('',2.0,0)]"
bash Tools/UE59_20261118/run2.sh V18_stopsdiag_after -6000 2000 92 0 "$P2" "pass"
LM /Game/GraceRanger/Maps/L_GR_SphirusHouse
echo SEQ6_DONE
