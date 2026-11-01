#!/bin/bash
# run242_fps.sh : A8 FPS matrix for the lateral stop + settle gate (j41_rl_p04 o vs latg) at 60 / 120 / real time, then back to 30.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
for i in $(seq 1 120); do n=$(powershell.exe -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'v242_ab\.sh|v212_run\.sh' }).Count" | tr -d '\r'); [ "$n" = "0" ] && break; sleep 30; done
source Saved/Codex/SHME_V242_20261101/lib242.sh
relaunch f60 60; WARM=1 ab f60 "j41_rl_p04:o j41_rl_p04:latg j42_lr_p10:latg"
relaunch f120 120; WARM=1 ab f120 "j41_rl_p04:o j41_rl_p04:latg"
relaunch freal real; WARM=1 ab freal "j41_rl_p04:o j41_rl_p04:latg"
relaunch fend 30
echo FPS242_DONE >> $O
