#!/bin/bash
# seq1.sh: saved-state verification batch (2026-11-18): house slope after / runtime-before, then flat-map turn + stop suite.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
HP="$(cat Saved/UE59Work/hp_plan.txt)"
BEFORE="PW_=u.GameplayStatics.get_player_controller(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),0).get_controlled_pawn(); PW_.get_movement_component().set_editor_property('use_flat_base_for_floor_checks',True,u.PropertyAccessChangeNotifyMode.NEVER); builtins.VID_MOTION={'SlopeOn':False}"
echo "== S4 after"; bash Tools/UE59_20261118/run2.sh S4_house_after 2640 420 322 -83 "$HP" "pass"
echo "== S4 before (runtime revert: flat base on, slope off)"; bash Tools/UE59_20261118/run2.sh S4_house_before 2640 420 322 -83 "$HP" "$BEFORE"
echo "== turns after"; TS="W J S STOP BRAKE" bash Tools/UE59_20261118/turns.sh A18 "pass"
echo SEQ1_DONE
