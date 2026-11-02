#!/bin/bash
# run249_pre.sh : V2.49 BEFORE captures of the saved production (V2.48) in the current 60 FPS session, then release chain M3
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V249_20261102; source $D/lib249.sh
CAP_START=9.3 CAP_SECS=3.4 ab precap "j45_sl2:oG j45_sl2:oS j45_sl2:oD" $D/vars249_cap.sh
echo TPRE249_DONE >> $O
touch $D/data/GO_PROMOTE
