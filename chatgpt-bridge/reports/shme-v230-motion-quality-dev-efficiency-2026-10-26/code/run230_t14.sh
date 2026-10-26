#!/bin/bash
# run230_t14.sh : real-time editor: 0.4 s stall in the push-off acceleration after the sprint RevTurn (cold-run pelvis 47 cm behind the
# capsule) - production vs PBI off / settle+terrain body off / spine counter-rotation off, to find the dt-sensitive owner.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "T14 start $(date +%T)" >> $O
relaunch t14 real; export WARM=1 MEMPROBE=1
ab t14 "s29_camh3:o s29_camh3:oPBI s29_camh3:oSET s29_camh3:oSCR s29_camh3:o:2 s29_camh3:oPBI:2" $D/vars230c.sh
echo "T14_DONE $(date +%T)" >> $O
