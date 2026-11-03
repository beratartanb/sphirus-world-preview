#!/bin/bash
# run254_g.sh : V2.54 chain G = cancel exit (v4) + regression set + FPS sweep 20/30/120/real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V254_20261104; O=$D/run254_g.out; source $D/lib254.sh
relaunch g60 60
WARM=1 ab g60 "s54_tap:rvcam s54_mid:rvcam s54_lr:rvcam s54_revR:rvcam s54_revL:rvcam s54_l90:rvcam j54_rev:o j54_rev:rvcam j54_r90:o j54_r90:rvcam wstart:o wstart:rvcam w42_id:o w42_id:rvcam taps:rvcam jstart:o jstart:rvcam j36_stop:o j36_stop:rvcam j45_sl2:o j45_sl2:rvcam gait:rvcam w43_idle:o w43_idle:rvcam j40_rlw:o j40_rlw:rvcam"
for F in 20 30 120 real; do relaunch g$F $F; WARM=1 ab g$F "s54_revR:o s54_revR:rvcam s54_r90:o s54_r90:rvcam s54_tap:rvcam"; done
echo TG254_DONE >> $O
