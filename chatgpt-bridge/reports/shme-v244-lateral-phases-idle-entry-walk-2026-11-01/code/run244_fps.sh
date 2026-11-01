#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V244_20261101; source $D/lib244.sh
relaunch f60 60;  WARM=1 ab f60 "j41_rl_p04:lat4 j41_rl_p10:lat4 j42_lr_p10:lat4 j41_rl_p10:o"
relaunch f20 20;  WARM=1 ab f20 "j41_rl_p10:lat4 j41_rl_p04:lat4 j41_rl_p10:o"
relaunch f120 120; WARM=1 ab f120 "j41_rl_p10:lat4 j41_rl_p10:o"
relaunch freal real; WARM=1 ab freal "j41_rl_p04:lat4 j41_rl_p10:lat4 j42_lr_p10:lat4 j41_rl_p10:lat4:2 w43_idle:idl4"
relaunch fend 30
CAP_START=10.4 CAP_SECS=4.0 WARM=1 ab cap "j41_rl_p10:lat4S j41_rl_p10:oS j41_rl_p10:lat4D j41_rl_p10:oD j42_lr_p10:lat4D j42_lr_p10:oD j41_rl_p10:lat4G j41_rl_p10:oG" $D/vars244_cap.sh
CAP_START=3.8 CAP_SECS=9.5 WARM=1 ab capi "w43_idle:idl4D w43_idle:idl4S" $D/vars244_cap.sh
echo FPS244_DONE >> $O
