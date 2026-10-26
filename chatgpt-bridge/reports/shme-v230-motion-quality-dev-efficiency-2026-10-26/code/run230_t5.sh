#!/bin/bash
# run230_t5.sh : SAME editor: character re-author of the sprint loop / curves / push links / rear walk / lateral jog (in place, checkpoint
# checkpoint/pre_reauthor), then before/after tests (lr2 state) on the families that play them.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib230.sh
echo "T5 start $(date +%T)" >> $O
bash $R $D/req/ra_write_measure.py ra_wm 1800 > $D/ra_wm.out 2>&1; grep -a "Traceback" $D/ra_wm.out | head -2 >> $O
bash $R $D/req/ra_write.py ra_write 2400 > $D/ra_write.out 2>&1; grep -a "Traceback\|LEG_GUARD_FAIL" $D/ra_write.out | head -3 | cut -c1-400 >> $O
grep -aq "RA230 {" $D/ra_write.out && echo "T5 reauthor written $(date +%T)" >> $O || { echo "T5_STOP reauthor" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J=""; for s in d_sprint s29_ws e29_rest e29_chain chain_sscut s29_dg s29_sa c29_combo a29_ang a29_angb j24_ad_ph0 c29_jlook j24_ph0 taps s23_jstart; do J="$J $s:lr2"; done
ab t5 "$J" $D/vars230.sh
echo "T5_DONE $(date +%T)" >> $O
