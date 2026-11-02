#!/bin/bash
# run248_f.sh : V2.48 chain F = 30 FPS regressions (skipped in chain D by a stale guard match) after chain E
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; source $D/lib248.sh
until grep -q TE248_DONE $O; do sleep 20; done
relaunch tf30 30; WARM=1 ab tf30 "j45_sl:ts taps:ts wstart:ts jstart:ts w42_id:ts gait:ts j41_rl_p10:ts j45_sl2:ts j45_sl2:o"
echo TF248_DONE >> $O
