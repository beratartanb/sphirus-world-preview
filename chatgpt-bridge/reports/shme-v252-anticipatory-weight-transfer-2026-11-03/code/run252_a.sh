#!/bin/bash
# run252_a.sh : V2.52 chain A = A/B of the anticipatory weight transfer walk starts (apa), the smooth yaw hand-over (yt), both (apayt)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V252_20261103; source $D/lib252.sh
relaunch a60 60; WARM=1 ab a60 "wstart:o wstart:apa w42_id:o w42_id:apa gait:o gait:apa taps:o taps:apa w43_idle:apa jstart:o jstart:yt j45_sl2:apayt j40_rlw:o j40_rlw:apayt"
relaunch a30 30; WARM=1 ab a30 "wstart:apa w42_id:apa gait:apa taps:apa jstart:apayt j45_sl2:apayt j41_rl_p10:apayt"
relaunch a120 120; WARM=1 ab a120 "jstart:o jstart:yt wstart:apa"
relaunch areal real; WARM=1 ab areal "wstart:o wstart:apa wstart:apa:2 w42_id:apa jstart:apayt j40_rlw:o j40_rlw:o:2 j40_rlw:apayt"
echo TA252_DONE >> $O
