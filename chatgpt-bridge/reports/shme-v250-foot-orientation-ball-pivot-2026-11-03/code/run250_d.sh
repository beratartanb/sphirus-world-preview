#!/bin/bash
# run250_d.sh : V2.50 chain D = final clean-session verification (foot orientation repair + first-step ball pivot), all FPS + real time + captures
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V250_20261103; source $D/lib250.sh
relaunch d60 60
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v250 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v250verify2 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
WARM=1 ab d60 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j45_sl:o w42_id:o"
CAP_START=9.3 CAP_SECS=3.4 ab dcap "j45_sl2:oD j45_sl2:oS j45_sl2:oG" $D/vars250_cap.sh
CAP_START=13.8 CAP_SECS=2.6 ab dcap2 "jstart:oD jstart:oS" $D/vars250_cap.sh
relaunch d30 30; WARM=1 ab d30 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j42_lr_p10:o w42_id:o"
relaunch dreal real; WARM=1 ab dreal "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl2:o:4 j45_sl2:o:5 jstart:o jstart:o:2 taps:o wstart:o"
relaunch d20 20; WARM=1 ab d20 "j45_sl2:o jstart:o w43_idle:o"
relaunch d120 120; WARM=1 ab d120 "j45_sl2:o jstart:o w43_idle:o"
echo TD250_DONE >> $O
