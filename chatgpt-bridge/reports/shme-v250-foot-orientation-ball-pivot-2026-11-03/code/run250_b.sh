#!/bin/bash
# run250_b.sh : V2.50 chain B = clean-session verification after the foot repair (6 crops + 16 Candidate-derived copies; production flags)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V250_20261103; source $D/lib250.sh
echo "[verify] $(SHME_KIND=measure SHME_OWNER=v250 bash $R /c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/v242/verify241_req.py v250verify1 300 | tail -1 | grep -o '\"ALL_OK\": [a-z]*\|\"bad\": \[[^]]*\]' | tr '\n' ' ' | cut -c1-300)" >> $O
relaunch b60 60; WARM=1 ab b60 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j45_sl:o w42_id:o"
CAP_START=9.3 CAP_SECS=3.4 ab bcap "j45_sl2:oD j45_sl2:oS j45_sl2:oG" $D/vars250_cap.sh
CAP_START=13.8 CAP_SECS=2.6 ab bcap2 "jstart:oD jstart:oS" $D/vars250_cap.sh
echo TB250_60 >> $O
relaunch b30 30; WARM=1 ab b30 "j45_sl2:o jstart:o taps:o wstart:o w43_idle:o j41_rl_p10:o j40_rlw:o gait:o j42_lr_p10:o w42_id:o"
relaunch breal real; WARM=1 ab breal "j45_sl2:o j45_sl2:o:2 j45_sl2:o:3 j45_sl2:o:4 jstart:o jstart:o:2 taps:o wstart:o w43_idle:o"
relaunch b20 20; WARM=1 ab b20 "j45_sl2:o jstart:o w43_idle:o"
relaunch b120 120; WARM=1 ab b120 "j45_sl2:o jstart:o w43_idle:o"
echo TB250_DONE >> $O
