#!/bin/bash
# run232_b11.sh : V2.32 C2 + B11 (same editor, after B10_DONE): owned JogQ start clips begin from the idle stance (pinstart232: ball pinned
# at the idle ball until the first lift, then handed over to the clip's swing in 0.3 s; checkpoint pre_v232/.../Starts/Jog), warm-up, then the
# start family again (the before = B3 o runs of this session) with and without the start-speed bind (sb).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B10_DONE\|B10_FAILED" $O; do sleep 30; done
bash $R $D/req/ps_write.py psw 1500 > $D/ps_write.out 2>&1; echo "PSW $(grep -a -o 'PS232 {.\{0,300\}' $D/ps_write.out | head -1)" >> $O
grep -aq "LEG_GUARD_FAIL\|Traceback" $D/ps_write.out && echo "PSW_WARN guard/traceback (see ps_write.out / pinstart232_write.json)" >> $O
export WARM=1 MEMPROBE=1
J=""; for v in o sb; do for s in j30_slow j30_rel_3200 j30_rel_3400 j30_rel_3450 jback d_back jstart k_jogback wstart d_sprint; do J="$J $s:$v"; done; done
ab b11 "$J" $D/vars232.sh
echo "B11_DONE $(date +%T)" >> $O
