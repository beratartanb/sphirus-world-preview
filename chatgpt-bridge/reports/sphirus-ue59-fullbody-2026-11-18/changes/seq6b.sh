#!/bin/bash
# seq6b.sh: slope diagnostic videos with vegetation hidden in the rendered view only (ShowFlag; collision and gameplay unchanged)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; export VSHOT=1
HP="$(cat Saved/UE59Work/hp_plan.txt)"
SF="W_=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); [u.SystemLibrary.execute_console_command(W_,c_) for c_ in ('ShowFlag.InstancedFoliage 0','ShowFlag.InstancedGrass 0','ShowFlag.Foliage 0','ShowFlag.InstancedStaticMeshes 0')]"
BEF="$SF; PW_=u.GameplayStatics.get_player_controller(W_,0).get_controlled_pawn(); PW_.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); builtins.VID_MOTION={'SlopeOn':False}"
export VSIDE="(420,90,30,95,'pelvis')"
bash Tools/UE59_20261118/run2.sh V18_slopediag2_before 2640 420 322 -83 "$HP" "$BEF"
bash Tools/UE59_20261118/run2.sh V18_slopediag2_after 2640 420 322 -83 "$HP" "$SF"
echo SEQ6B_DONE

bash Tools/Day_20261107/ed.sh Tools/UE59_20261118/sf_restore.py measure 60 | grep SFRESTORE | head -1   # 2026-11-18: the show flags persist into the editor viewport
