#!/bin/bash
# run249_s.sh : V2.49 chain S = owner of the turning-start entry toe dig (inertialization / dead blending / velocity) at 60 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; source $D/lib249.sh
relaunch s60 60; WARM=1 ab s60 "j45_sl2:oNI j45_sl2:oDB j45_sl2:oIV"
echo TS249_DONE >> $O
