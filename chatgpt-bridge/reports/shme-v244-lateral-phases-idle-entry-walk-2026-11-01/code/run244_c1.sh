#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh
source $D/lib244.sh
echo "[walkdb] $(SHME_KIND=measure SHME_OWNER=v244 bash $RUN $REQ/probe_walkdb.py v244walkdb 300 | grep -a 'WALKDB244\|REFUSED\|Error' | cut -c1-3000)" >> $O
WARM=1 ab c1 "j41_rl_p04:lat4 j41_rl_p10:lat4 j42_lr_p10:lat4 w42_id:idl4 w43_idle:idl4 taps:idl4 jstart:idl4 j40_rlw:idl4 gait:idl4 j42_lr_p10:all4 taps:all4"
echo C1_DONE >> $O
