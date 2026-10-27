#!/bin/bash
# run233_d60.sh : attribution of the 60 FPS jback late stop drag (A_LS_Jog_Left_Stop t 12.5 s, 55-63 cm with Q): production o vs
# body233 (stand-back only) vs cam233 (recentre only) vs pre233 (V2.32 values), 60 FPS fixed step, 2 rep o/body233 + 1 rep each other.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
echo "D60 start $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
relaunch d60 60
export WARM=1 MEMPROBE=1
ab d60 "jback:o:0 jback:o:1 jback:body233:1 jback:cam233:1 jback:pre233:1 jback:o:2 jback:body233:2 j30_slow:o:1 j30_slow:body233:1" $D/vars233.sh
echo "D60_DONE $(date +%T)" >> $O
