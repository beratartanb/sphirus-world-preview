#!/bin/bash
# seq2.sh: runtime candidates for the turn / stop findings (flat map, exact-angle flicks). Nothing is saved.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
HP="$(cat Saved/UE59Work/hp_plan.txt)"
BEFORE="PW_=u.GameplayStatics.get_player_controller(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),0).get_controlled_pawn(); PW_.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); builtins.VID_MOTION={'SlopeOn':False}"
echo "== S5 before (runtime revert)"; bash Tools/UE59_20261118/run2.sh S5_house_before 2640 420 322 -83 "$HP" "$BEFORE"
TS="W" bash Tools/UE59_20261118/turns.sh rx "builtins.CM_ADD={'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Walk_F_Turns':'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Walk_F_Turns'}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
TS="W" bash Tools/UE59_20261118/turns.sh ua90 "builtins.PLANT={'unplant_angle':90.0}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/plant_set.py',encoding='utf8').read())"
TS="W" bash Tools/UE59_20261118/turns.sh twist "builtins.PLANT={'ankle_twist_reduction':0.4}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/plant_set.py',encoding='utf8').read())"
TS="J" bash Tools/UE59_20261118/turns.sh n "builtins.CM_ADD={'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Run_F_Turns':'/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Run_F_Turns','/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Run_F_Pivots':'/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Run_F_Pivots'}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
TS="STOP" bash Tools/UE59_20261118/turns.sh ds "builtins.CM_ADD={'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops':'/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_Sprint_Stops'}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/cm_add.py',encoding='utf8').read())"
echo SEQ2_DONE
