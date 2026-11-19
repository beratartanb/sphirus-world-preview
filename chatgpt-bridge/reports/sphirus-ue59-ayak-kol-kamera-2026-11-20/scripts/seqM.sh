#!/bin/bash
# seqM.sh: short interaction checks on the house map, saved state, player camera video (30 Hz = real speed):
#  tea   hub gate state via the hub's own event LoadFromDataString (Fire 2 + Herb 1 = "2100"), stand in front of GR_Day_Tea, E
#  mask  stand at GR_MaskBench, E      bed  stand at GR_Day_Bed (upper floor), E      door  stand at SPH_Door_LowerStoreDoor, E
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
HK="exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/hk_interact.py',encoding='utf8').read())"
HUB="h_=[a_ for a_ in u.GameplayStatics.get_all_actors_of_class(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),u.Actor) if a_.get_class().get_name().startswith('BP_GR_DayHub')][0]; h_.call_method('LoadFromDataString',('2100',)); print('HUBSET')"
EP(){ echo "('',1.5,0,-15,$1),('W',0.3,0,-15,$1),('',1.0,0,-15,$1),('E',0.15,0,-15,$1),('',8.0,0,-15,$1),('E',0.15,0,-15,$1),('',6.0,0,-15)"; }
for t in ${TS:-tea mask bed door}; do case $t in
 tea)  VSHOT=1 bash Tools/UE59_20261118/run2.sh M_tea 1418 340 249 -90 "[$(EP "(1418,246,249)")]" "$HUB; $HK";;
 mask) VSHOT=1 bash Tools/UE59_20261118/run2.sh M_mask 397 320 245 -90 "[$(EP "(397,226,245)")]" "$HK";;
 bed)  VSHOT=1 bash Tools/UE59_20261118/run2.sh M_bed 1205 680 575 90 "[$(EP "(1205,767,570)")]" "$HK";;
 door) VSHOT=1 bash Tools/UE59_20261118/run2.sh M_door${DT:-} 410 ${DY:-843} 152 180 "[$(EP "${DAIM:-(302,843,200)}")]" "$HK";;
esac; done
echo SEQM_DONE
