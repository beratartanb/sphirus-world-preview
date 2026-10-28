#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S3A start $(date +%T)" >> $O
ab s3a "j35_rev:wb j35_rev:wb:2 j35_rev:o j35_rev2:wb j35_rev2:o j30_rel_3200:wb j30_rel_3200:o j30_rel_3450:wb j30_rel_3450:o j35_relstop:wb j35_relstop:o j34_chain1:wb e29_load:wb e29_load:o e29_chain:wb e29_chain:o j30_slow:wb c29_combo:wb jback:wb jback:o j35_rev:wbS j35_rev:oS e29_load:wbS e29_load:oS" $D/vars236_cap.sh
echo "S3A_DONE $(date +%T)" >> $O
