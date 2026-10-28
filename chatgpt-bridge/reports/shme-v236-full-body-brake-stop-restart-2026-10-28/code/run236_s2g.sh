#!/bin/bash
source Saved/Codex/SHME_V236_20261028/lib236.sh; O=$D/chain.out; export O
echo "S2G start $(date +%T)" >> $O
ab s2g "j36_stopr:s2stS j36_stopr:oS j36_stopb:s2stS j36_stopr:s2stG j36_wjsb:s2stS" $D/vars236_cap.sh
export SHME_KIND=measure
bash $R $D/req_grev_dry.py grevd 1800 > $D/last_grevd.out 2>&1
bash $R $D/req_gload_dry.py gloadd 1800 > $D/last_gloadd.out 2>&1
echo "S2G_DONE $(date +%T)" >> $O
