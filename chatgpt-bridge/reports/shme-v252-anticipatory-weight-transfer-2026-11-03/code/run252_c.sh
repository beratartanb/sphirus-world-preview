#!/bin/bash
# run252_c.sh : V2.52 chain C = owner test of the crop-end pop (orientation warping / foot placement off for the whole run, same selection
# as V2.50 showed for jstart) at 60 FPS
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V252_20261103; source $D/lib252.sh
until grep -q TB252_DONE $O; do sleep 20; done
relaunch c60 60; WARM=1 ab c60 "jstart:oOW jstart:oFP0"
echo TC252_DONE >> $O
