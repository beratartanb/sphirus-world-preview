#!/bin/bash
# seq4.sh: real-speed evidence videos (30 Hz fixed game step, one screenshot per frame) for the saved state and the runtime 'before'.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export VSHOT=1
HP="$(cat Saved/UE59Work/hp_plan.txt)"
BEF="PW_=u.GameplayStatics.get_player_controller(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),0).get_controlled_pawn(); PW_.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); builtins.VID_MOTION={'SlopeOn':False}"
LFN="builtins.LF=None; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/lf_set.py',encoding='utf8').read())"
OLDS="builtins.CM_ADD={'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops'}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
LM(){ echo "$1" > Saved/Codex/Day_20261107/loadmap.txt; SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED; }
LT="$(cat Tools/UE59_20261118/light_route.txt)"
for t in ${VT:-slope_pc slope_diag light jstop turns}; do case $t in
 slope_pc) bash Tools/UE59_20261118/run2.sh V18_slope_pc_before 2640 420 322 -83 "$HP" "$BEF"; bash Tools/UE59_20261118/run2.sh V18_slope_pc_after 2640 420 322 -83 "$HP" "pass";;
 slope_diag) VSIDE="(260,90,20,95,'pelvis')" bash Tools/UE59_20261118/run2.sh V18_slope_diag_before 2640 420 322 -83 "$HP" "$BEF"; VSIDE="(260,90,20,95,'pelvis')" bash Tools/UE59_20261118/run2.sh V18_slope_diag_after 2640 420 322 -83 "$HP" "pass";;
 light) LP="$(cat Tools/UE59_20261118/light_patch.txt)"; LX="$(cat Tools/UE59_20261118/light_exit.txt)"
        bash Tools/UE59_20261118/run2.sh V18_lightpatch_before 520 160 241 180 "$LP" "$LFN"; bash Tools/UE59_20261118/run2.sh V18_lightpatch_after 520 160 241 180 "$LP" "pass"
        bash Tools/UE59_20261118/run2.sh V18_lightexit_before 1080 200 245 180 "$LX" "$LFN"; bash Tools/UE59_20261118/run2.sh V18_lightexit_after 1080 200 245 180 "$LX" "pass";;
 jstop) LM /Game/Sphirus/Test/L_Sph_MoveTest; P="[('',2.0,0),('W LeftShift',3.0,0),('',2.5,0),('W LeftShift',3.3,0),('',2.5,0),('W LeftShift',3.0,0),('W LeftShift',0.5,90),('',2.5,0)]"
        VSIDE="(260,90,20,95,'pelvis')" bash Tools/UE59_20261118/run2.sh V18_jstop_old -6000 2000 92 0 "$P" "$OLDS"; VSIDE="(260,90,20,95,'pelvis')" bash Tools/UE59_20261118/run2.sh V18_jstop_new -6000 2000 92 0 "$P" "pass";;
 turns) LM /Game/Sphirus/Test/L_Sph_MoveTest; P="[('',2.0,0),('W',3.0,0),('W',0.25,720),('W',3.0,0),('W',0.25,-720),('W',3.0,0),('W LeftShift',3.0,0),('W LeftShift',0.25,540),('W LeftShift',3.0,0),('W LeftShift',0.25,-720),('W LeftShift',3.0,0),('',2.0,0)]"
        VSIDE="(260,90,20,95,'pelvis')" bash Tools/UE59_20261118/run2.sh V18_turns_diag_after -6000 2000 92 0 "$P" "pass";;
esac; done
LM /Game/GraceRanger/Maps/L_GR_SphirusHouse
echo SEQ4_DONE
