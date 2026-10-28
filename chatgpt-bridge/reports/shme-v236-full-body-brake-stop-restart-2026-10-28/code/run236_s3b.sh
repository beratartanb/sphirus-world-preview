#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S3B start $(date +%T)" >> $O
export SHME_KIND=write SHME_MANIFEST=$D/checkpoint/manifests/rev2.json
bash $R $D/req_grev_w.py grevw2 3600 > $D/last_grevw2.out 2>&1
bash $R $D/req_curves.py curves2 1800 > $D/last_curves2.out 2>&1
bash $R $D/req_rdb.py rdb2 1800 > $D/last_rdb2.out 2>&1
for db in PSD_SHM236_JogRevFwd PSD_SHM236_JogRevBwdX; do bash $R $D/req_b_$db.py b2$db 600 >> $D/last_bias5.out 2>&1; done
echo "S3B_W $(date +%T)" >> $O
ab s3b "j36_stop:wbr j36_rsm:wbr j36_rsm:wbr:2 j36_rse:wbr j36_rsl:wbr j36_stopr:wbr j34_chain1:wbr j36_wjs:wbr j36_wjsb:wbr jstart:wbr j35_rev:wbr j35_rev:wbr:2 e29_load:wbr e29_load:wbr:2 j30_rel_3450:wbr j30_rel_3450:o j35_rev:wbrS j36_stopr:wbrS j36_stopb:wbrS e29_load:wbrS" $D/vars236_cap.sh
echo "S3B_DONE $(date +%T)" >> $O
