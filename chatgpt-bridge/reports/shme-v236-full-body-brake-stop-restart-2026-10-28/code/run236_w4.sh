#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
until grep -q S3A_DONE $O; do sleep 5; done
echo "W4 start $(date +%T)" >> $O
export SHME_KIND=write SHME_MANIFEST=$D/checkpoint/manifests/stop4.json
bash $R $D/req_gstop_w4.py gstopw4 2400 > $D/last_gstopw4.out 2>&1
bash $R $D/req_sdb2.py sdb4 1200 > $D/last_sdb4.out 2>&1
bash $R $D/req_bias2.py bias4 600 > $D/last_bias4.out 2>&1
export SHME_MANIFEST=$D/checkpoint/manifests/resume1.json
bash $R $D/req_resvar.py resvar 1800 > $D/last_resvar.out 2>&1
bash $R $D/req_resdb.py resdb 900 > $D/last_resdb.out 2>&1
echo "W4_DONE $(date +%T)" >> $O
