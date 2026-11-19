#!/bin/bash
# fin19.sh <suffix> <tests...> (2026-11-19): final-state gameplay flow on the house map, saved player, real inputs only.
#  flow     kitchen walk -> short jog -> run-to-walk while moving -> rear door out -> garden path walk + jog (downhill) -> stop ->
#           180 turn and back -> wood: pick (E) -> carry -> block (E, click) -> collect BOTH pieces (live GOTO to BP_GR_SplitPiece) ->
#           rear door in -> hearth: E (lay) E (light). VSHOT=1 = player-camera video (30 Hz step, 30 fps = real speed).
#  pieces   same up to the pieces (data only), the written test save is kept
#  loadfire load that test save by the hearth -> E, E   |  emptyfire  fresh state, no wood: E refused
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; S=$1; shift; export VWAIT=${VWAIT:-900}
USHA=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); echo "USER_SLOT $USHA"
echo "/Game/GraceRanger/Maps/L_GR_SphirusHouse" > Saved/Codex/Day_20261107/loadmap.txt
SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Tools/Day_20261107/loadmap.py" emb_loadmap 120 2>&1 | grep -c LOADED
LOADG="[c_ for c_ in u.GameplayStatics.get_player_controller(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(),0).get_components_by_class(u.ActorComponent) if c_.get_class().get_name().startswith('SFSaveManager')][0].call_method('LoadGame (StoryFramework)',(True,)); print('GAMELOAD')"
WOOD="(1700,-520,96)"; BLK="(1830,-330,128)"; FIR="(1405,905,205)"
HOUSE="('',1.5,0,-12),('GOTO',1.5,0,-12,(1150,320,245)),('GOTOJ',1.6,0,-12,(1160,620,245)),('GOTO',2.0,0,-12,(1160,320,245)),('GOTO',2.0,0,-12,(1080,200,245))"
EXIT="('GOTO',2.5,0,-12,(1000,200,245)),('GOTO',2.5,0,-12,(840,60,240)),('GOTO',2.0,0,-12,(840,-40,220)),('GOTO',3.0,0,-12,(880,-150,210))"
PTH="('GOTO',3.0,0,-12,(1100,-200,205)),('GOTOJ',4.0,0,-12,(1300,-250,200)),('',1.5,0,-12),('W',0.3,600,-12),('W',1.5,0,-12),('',1.0,0,-12),('W',0.3,600,-12),('GOTOJ',4.0,0,-12,(1450,-480,150)),('GOTO',3.0,0,-14,(1540,-520,190)),('',1.5,0,-20,$WOOD)"
CHOP="('',1.0,0,-20,$WOOD),('W',0.6,0,-20,$WOOD),('',0.7,0,-20),('',1.0,0,-20,$WOOD),('E',0.15,0,-20,$WOOD),('',7.5,0,-20,$WOOD),('',0.8,0,-15,(1756,-380,200)),('W',1.0,0,-15,(1756,-380,200)),('',0.8,0,-15,(1756,-380,200)),('',1.2,0,-22,$BLK),('E',0.15,0,-22,$BLK),('',4.4,0,-22,$BLK),('LeftMouseButton',0.15,0,-22,$BLK),('',7.0,0,-22,$BLK)"
PICK="('GOTO',2.5,0,-25,(1780,-440,190)),('GOTO',3.0,0,-25,(1920,-420,190)),('GOTO',4.0,0,-25,'BP_GR_SplitPiece'),('',2.0,0,-25),('GOTO',4.0,0,-25,'BP_GR_SplitPiece'),('',2.0,0,-25),('GOTO',4.0,0,-25,'BP_GR_SplitPiece'),('',2.5,0,-25)"
ROUTE="('GOTO',2.5,0,-12,(1920,-420,190)),('GOTO',2.5,0,-12,(1780,-440,190)),('GOTO',3.0,0,-12,(1540,-520,190)),('GOTO',5.0,0,-12,(1300,-250,200)),('GOTO',5.0,0,-12,(880,-150,210)),('GOTO',2.0,0,-12,(840,-40,220)),('GOTO',2.0,0,-12,(840,60,240)),('GOTO',2.5,0,-12,(1000,200,245)),('GOTO',1.5,0,-12,(1080,200,245)),('GOTO',2.0,0,-12,(1160,320,245)),('GOTO',4.0,0,-12,(1160,760,245)),('GOTO',2.0,0,-12,(1280,800,245)),('GOTO',1.5,0,-12,(1320,840,245)),('GOTO',1.5,0,-12,(1340,905,245))"
FIRE="('',1.2,0,-14,$FIR),('E',0.15,0,-14,$FIR),('',9.0,0,-14,$FIR),('E',0.15,0,-14,$FIR),('',9.0,0,-14,$FIR),('',1.0,0,-12)"
for t in "$@"; do case $t in
 flow) bash Tools/UE59_20261118/run2.sh F19_flow_$S 1080 200 245 90 "[$HOUSE,$EXIT,$PTH,$CHOP,$PICK,$ROUTE,$FIRE]" "${XPRE:-pass}";;
 pieces) VSHOT= bash Tools/UE59_20261118/run2.sh F19_pieces_$S 1080 200 245 90 "[$HOUSE,$EXIT,$PTH,$CHOP,$PICK,('',2.0,0,-20)]" "${XPRE:-pass}"
         cp -p Saved/Codex/Day_20261107/videos/F19_pieces_$S/slot_test.sav Saved/Codex/Motion_20261112/slot_f19_$S.sav 2>/dev/null && echo "TESTSLOT kept";;
 loadfire) VSHOT= VLOADSLOT=Saved/Codex/Motion_20261112/slot_f19_$S.sav bash Tools/UE59_20261118/run2.sh F19_loadfire_$S 1290 905 242 0 "[('',1.5,0,-12),('W',0.4,0,-12),('',0.8,0,-12),$FIRE]" "$LOADG";;
 emptyfire) VSHOT= bash Tools/UE59_20261118/run2.sh F19_emptyfire_$S 1290 905 242 0 "[('',1.5,0,-12),('W',0.4,0,-12),('',0.8,0,-12),$FIRE]" "pass";;
esac; h=$(sha1sum Saved/SaveGames/SFSaveSlot.sav | cut -c1-40); [ "$h" = "$USHA" ] || { echo "USER_SLOT_CHANGED $h - stop"; exit 3; }; done
echo FIN19_DONE
