#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2H start $(date +%T)" >> $O
ab s2h "j36_stopr:s2stS j36_stopb:s2stS j36_stopr:s2stG j36_wjsb:s2stS j36_stopr:oG" $D/vars236_cap.sh
export SHME_KIND=write SHME_MANIFEST=$D/checkpoint/manifests/rev1.json
bash $R $D/req_grev_w.py grevw 3600 > $D/last_grevw.out 2>&1
bash $R $D/req_gload_w.py gloadw 3600 > $D/last_gloadw.out 2>&1
echo "S2H_DONE $(date +%T)" >> $O
