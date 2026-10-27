#!/bin/bash
# run233_cap.sh : V2.33 normal-speed captures (after FIN_EVID_DONE, same editor): G = game camera, S = fixed side observer (full body).
# o = V2.33 production (keyboard harness -> the mouse recentre profile), pad233 = the gamepad profile, pre233 = every V2.33 knob at its
# V2.32 value, sc = the calm-sprint CANDIDATE (not in production).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; export O=$D/chain.out; source $D/lib233.sh
until grep -aq "FIN_EVID_DONE" $O; do sleep 30; done
{ echo "CAPV3='o pre233 pad233 sc'"; echo "CAP_START=3.0; CAP_SECS=9.5"; cat $D/vars233.sh; echo 'CAP="\"mcap\":{\"start\":${CAP_START:-3.8},\"seconds\":${CAP_SECS:-7.0},\"fps\":30,\"quality\":88}"'; cat $D/vars233_cap.sh; } > $D/vars233_capall.sh
export WARM=0 MEMPROBE=1
J="cam33_sturn:pre233G cam33_sturn:oG cam33_sturn:pad233G cam33_jturnj:pad233G cam33_look:pad233G cam33_back:pad233G cam32_chain:pad233G"
J="$J j30_slow:pre233S j30_slow:oS d_sprint:oS d_sprint:scS cam33_sturn:pad233S"
ab cap "$J" $D/vars233_capall.sh
echo "CAP_DONE $(date +%T)" >> $O
