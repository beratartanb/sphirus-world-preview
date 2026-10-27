#!/bin/bash
# run232_cap.sh : V2.32 captures (same editor as FIN, after FIN_EVID_DONE): real-time media, full frame, 30 fps, no slow motion.
# G = the gameplay camera, S = a fixed side observer camera (full body). pre232 = the V2.31 values of every promoted knob; ocam = the V2.31
# body knobs + the new camera (matrix C); o = production (matrix D).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "FIN_EVID_DONE" $O; do sleep 30; done
{ echo "CAPV3='o pre232 ocam'"; echo "CAP_START=3.6; CAP_SECS=9.5"; cat $D/vars232.sh $D/vars232_post.sh; echo 'CAP="\"mcap\":{\"start\":${CAP_START:-3.8},\"seconds\":${CAP_SECS:-7.0},\"fps\":30,\"quality\":88}"'; cat $D/vars232_cap.sh; } > $D/vars232_capall.sh
export WARM=0 MEMPROBE=1
J="cam32_chain:pre232G cam32_chain:oG cam32_chain:ocamG cam32_s90:pre232G cam32_s90:oG cam32_brk2:oG cam32_wallturn:oG cam_corr:oG cam32_look:oG cam32_analog:oG cam32_w45:oG map_r1:oG"
J="$J e29_load:pre232S e29_load:oS c30_calm:pre232S c30_calm:oS wdiag:pre232S wdiag:oS cam32_chain:oS jback:oS cam32_s90:oS cam32_chain:oD cam32_brk2:oD"
ab cap "$J" $D/vars232_capall.sh
echo "CAP_DONE $(date +%T)" >> $O
