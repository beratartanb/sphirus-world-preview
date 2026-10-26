#!/bin/bash
# run230_t13.sh : real-time editor (no fixed step): the FIRST run is cold (s29_cam), then real stalls inside the sprint RevTurn (s29_camh /
# s29_camh2 hitches 0.4 s), then a warm s29_cam.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T13 start $(date +%T)" >> $O
relaunch t13 real; export WARM=0 MEMPROBE=1
ab t13 "s29_cam:lr2" $D/vars230.sh
export WARM=1; ab t13 "s29_camh:lr2 s29_camh2:lr2 s29_cam:lr2:2 s29_camh:lr2:2" $D/vars230.sh
echo "T13_DONE $(date +%T)" >> $O
