#!/bin/bash
# run248_b.sh : V2.48 A/B only (databases + ABP already installed, knob off): 30 FPS, real time x3, 60 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V248_20261102; source $D/lib248.sh
relaunch ts30 30; WARM=1 ab ts "j45_sl:ts j45_sl:o jstart:ts taps:ts wstart:ts j45_sl:ts:2"
relaunch tsreal real; WARM=1 ab tsreal "j45_sl:ts j45_sl:ts:2 j45_sl:ts:3 j45_sl:o j45_sl:o:2 jstart:ts taps:ts"
relaunch ts60 60; WARM=1 ab ts60 "j45_sl:ts jstart:ts"
echo TS248_DONE >> $O
