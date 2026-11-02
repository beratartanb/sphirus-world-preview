#!/bin/bash
# run250_c.sh : V2.50 chain C = authored foot-path probe, then weighted idle (oi) start compatibility on the repaired starts at 30 / 60 / real
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V250_20261103; source $D/lib250.sh
until grep -q TB250_DONE $O; do sleep 20; done
SHME_KIND=measure SHME_OWNER=v250 bash $R $D/req/footpath_req.py v250footpath 300 | grep -a 'FOOTPATH250\|Traceback\|Error' > $D/data/footpath.out; echo "[footpath] $(wc -c < $D/data/footpath.out)" >> $O
relaunch c30 30; WARM=1 ab c30 "wstart:oi w42_id:oi gait:oi taps:oi w43_idle:oi j45_sl2:oi jstart:oi j41_rl_p10:oi"
relaunch c60 60; WARM=1 ab c60 "wstart:oi w43_idle:oi taps:oi j45_sl2:oi"
echo TC250_DONE >> $O
