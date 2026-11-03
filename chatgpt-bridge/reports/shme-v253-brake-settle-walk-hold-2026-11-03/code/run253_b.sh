#!/bin/bash
# run253_b.sh : V2.53 chain B = fresh launch after the writes (crop kink re-key in place, walk entry knob, APA3 + settle new assets),
# membership check, then the 60 fixed A/B of every candidate against the saved production
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V253_20261104; O=$D/run253_b.out; source $D/lib253.sh
relaunch b60 60
SHME_KIND=measure SHME_OWNER=v253 bash $R $D/req/dbc_dry_req.py v253dbcb 600 2>&1 | grep -a -o '"before": {.\{0,40\}\|PSD_SHM237_JogStop": \[[^]]\{0,80\}' | head -2 >> $O
WARM=1 ab b60 "wstart:o wstart:we wstart:weap3 w42_id:o w42_id:we w42_id:weap3 taps:o taps:we taps:weap3 jstart:o jstart:st j36_stop:o j36_stop:st j36_stopb:o j36_stopb:st j36_stopr:o j36_stopr:st j45_sl2:o j45_sl2:st gait:o gait:all w43_idle:o w43_idle:all j40_rlw:o j40_rlw:all"
echo TB253_DONE >> $O
