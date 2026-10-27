#!/bin/bash
# run232_b3.sh : V2.32 B3 (same editor, after B2_DONE): C backward start bind - checkpoint the start clip, write its speed / witness curves,
# install the ABP start term (knob 0 = production unchanged), then A/B sb vs o on the backward-start family (fixed 30).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; R=Tools/SHME_V2_20261014/run_v2.sh; export O=$D/chain.out; source $D/lib232.sh
until grep -aq "B2_DONE" $O; do sleep 30; done
C=$D/checkpoint/pre_v232/content/GraceRanger/SHME/Animations/Starts/Jog; mkdir -p $C; cp -n Content/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS.uasset $C/
bash $R $D/req/sc_write.py scw 600 > $D/sc_write.out 2>&1; grep -a "SC232 " $D/sc_write.out | cut -c1-500 >> $O
bash $R $D/req/sb_save.py sbs 900 > $D/sb_save.out 2>&1; grep -a "SB232 " $D/sb_save.out | cut -c1-600 >> $O
grep -aq '"saved": true' $D/sb_save.out || { echo "B3_FAILED startbind not saved" >> $O; exit 1; }
export WARM=1 MEMPROBE=1
J=""; for v in o sb sbtk; do for s in j30_slow j30_rel_3200 j30_rel_3400 j30_rel_3450 k_jogback jback d_back jstart wstart; do J="$J $s:$v"; done; done
ab b3 "$J" $D/vars232.sh
echo "B3_DONE $(date +%T)" >> $O
