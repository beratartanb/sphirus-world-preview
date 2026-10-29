#!/bin/bash
# run237_fin3.sh : stop-entry fix. The stop DB re-selected a new phase bin at clip time 0 on every search for ~0.08 s after the release
# (60/120 FPS: final bin starts ~0.07 s late with the release-speed clock, planted foot 15-20 cm). Candidate cb25 (continuing bias -25)
# held the first bin (A/B 120 + 30 FPS, run237_cb.sh) -> set the bias on the promoted PSD_SHM237_JogStop (backup manifest bias1), clean
# reopen -> verify -> cold -> re-run EVERY final-evidence run whose production run entered the stop DB (new tags fin2/g60/g120/g20/greal;
# runs that never search the stop DB cannot change and keep their first-build labels) -> captures again.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V237_20261029; export O=$D/chain.out; source $D/lib237.sh; R=Tools/SHME_V2_20261014/run_v2.sh; T=Tools/SHME_V237_20261029; MD=$D/checkpoint/manifests
V7=/Game/GraceRanger/SHME/Animations/V237
echo "BIAS start $(date +%T) (reason: stop-entry bin re-selection; cb25 promoted as a property of the production stop DB)" >> $O
MSYS_NO_PATHCONV=1 "$PY" $T/manifest237.py bias1 --assets $V7/PSD_SHM237_JogStop | tail -1 | cut -c1-160 >> $O
SHME_KIND=write SHME_MANIFEST=$MD/bias1.json bash $R $D/req/bias.py bias1 600 > $D/last_bias.out 2>&1
grep -a -o 'BIAS236 .*' $D/last_bias.out >> $O
grep -aq '"saved": true' $D/last_bias.out || { echo "BIAS_FAILED write" >> $O; exit 1; }
echo "FINV3 start $(date +%T) (reason: clean reopen = verification on the disk state)" >> $O
relaunch finv3 30
SHME_KIND=measure bash $R $D/req/verify237.py verify3 900 > $D/verify_fin3.out 2>&1; grep -a -o '"bad": \[[^]]*\], "ALL_OK": [a-z]*' $D/verify_fin3.out | tail -1 >> $O
grep -a -o 'VERIFY237 {.*' $D/verify_fin3.out | grep -q '"ALL_OK": true' || { echo "FIN3_FAILED verify" >> $O; exit 1; }
echo "COLD2 start $(date +%T) (first use after the clean reopen, NO warm run)" >> $O
unset WARM; ab cold2 "j36_stop:o j36_rsm:o j36_wjs:o j34_chain1:o j35_rev:o" $D/vars237.sh
echo "COLD2_DONE $(date +%T)" >> $O
export WARM=1 MEMPROBE=1
ST="j36_stop j36_stopb j36_stopr j36_rse j36_rsm j36_rsl j36_rsx j36_wjs j36_wjsb j36_sside j35_rev j30_rel_3200 j30_rel_3450 j30_slow j34_chain1 jstart ter_drop_jog"
J=""; for s in $ST; do J="$J $s:o"; done
for s in j36_stop j36_stopb j36_stopr j36_rse j36_rsm j36_rsl j36_rsx j36_wjs j36_wjsb j36_sside j35_rev j30_rel_3450 j34_chain1 jstart ter_drop_jog; do J="$J $s:pre237"; done
J="$J j36_stopr:camoff"
ab fin2 "$J" $D/vars237.sh
echo "FIN2_EVID_DONE $(date +%T)" >> $O
SF="j36_stop j36_stopr j36_rsm j36_wjs j34_chain1 j35_rev j30_rel_3450 jstart j36_sside"
for m in 60 120 20 real; do
  echo "G start $m $(date +%T) (reason: frame-rate mode is an editor launch argument)" >> $O
  relaunch g$m $m
  J=""; for s in $SF; do J="$J $s:o $s:pre237"; done
  ab g$m "$J" $D/vars237.sh
  echo "G_DONE $m $(date +%T)" >> $O
done
echo "CAP2 start $(date +%T) (reason: back to fixed 30 for the normal-speed captures)" >> $O
relaunch cap2 30
export WARM=1
J="j36_stopr:oS j36_stopr:pre237S j36_stopr:oG j36_stopr:oD j36_stopb:oS j36_wjs:oS j36_wjs:pre237S j36_rsm:oS j36_rsm:pre237S j36_rse:oS j36_rsl:oS j36_rsx:oS j35_rev:oS j35_rev:pre237S j34_chain1:oS j36_sside:oG j36_sside:oS"
ab cap2 "$J" $D/vars237_capfin.sh
echo "CAP2_DONE $(date +%T)" >> $O
