#!/bin/bash
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V245_20261101; REQ=$D/req; RUN=Tools/SHME_V2_20261014/run_v2.sh
source $D/lib245.sh
echo "[hipline] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN $REQ/walk_hipline.py v245hip 300 | grep -a 'HIPLINE245\|REFUSED\|Error\|Traceback' | cut -c1-600)" >> $O
echo "[chooser2] $(SHME_KIND=measure SHME_OWNER=v245 bash $RUN $REQ/probe_chooser2.py v245chooser 300 | grep -a 'CHOOSER245\|REFUSED\|Error\|Traceback' | cut -c1-2500)" >> $O
WARM=1 ab sweep "j45_rl_r0:o j45_rl_r1:o j45_rl_r2:o j45_rl_r3:o j45_rl_r4:o j45_rl_r5:o j45_lr_r0:o j45_lr_r1:o j45_lr_r2:o j45_lr_r3:o j45_lr_r4:o j45_lr_r5:o"
echo SWEEP245_DONE >> $O
