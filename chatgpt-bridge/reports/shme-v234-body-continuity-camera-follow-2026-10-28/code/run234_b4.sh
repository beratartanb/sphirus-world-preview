#!/bin/bash
# run234_b4.sh : V2.34 B4 (same editor as B3, no build): candidate C2 (exploration limited to walk / jog, stable input, rate-limited body
# frame, net-deviation hand-over) camera / input suite with camera on / off + manual look DURING the recentre + release-repress on C2.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; export O=$D/chain.out; source $D/lib234.sh; T=Tools/SHME_V234_20261028
until grep -aq "^B3_DONE" $O; do sleep 20; done
tail -1 $O | grep -aq "^B3_FAILED" && { echo "B4_SKIPPED (B3 failed)" >> $O; exit 1; }
echo "B4 start $(date +%T) (no rebuild: B3 built the current source)" >> $O
export WARM=1 MEMPROBE=1
J="cam33_sturn:C2p:1 cam33_sturn:C2offp:1 cam33_wturn:C2p:1 cam33_wturn:C2offp:1 cam33_jturnj:C2p:1 cam33_jturnj:C2offp:1 cam33_jturnj:C2:1"
J="$J cam34_jlook:C2p:1 cam34_jlook:op:1 cam34_slook:C2p:1 cam34_slook:op:1 cam34_jrot:C2p:1 cam34_jcor:C2p:1 cam34_jcor:C2offp:1 cam34_wflow:C2p:1 cam34_wflow:C2offp:1 cam34_wflow:C2:1"
J="$J cam34_wdrift:C2p:1 cam34_jrel:C2p:1 cam33_back:C2p:1 cam33_idlelook:C2p:1 cam32_wallturn:C2p:1 cam_corr:C2p:1 ins_ws:C2p:1"
J="$J e29_chain:C2p:1 cam32_chain:C2p:1 c29_combo:C2p:1 jback:C2p:1 j30_rel_3200:C2R:1 j30_slow:C2R:1 j34_chain1:C2R:1 wstart:C2R:1 jstart:C2R:1"
ab b4 "$J" $D/vars234.sh
echo "B4_DONE $(date +%T)" >> $O
