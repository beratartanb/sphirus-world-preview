#!/bin/bash
# ab_safe216.sh (V2.16) : run v212_ab.sh ONLY when no other A/B loop / run / runner job of this session is active (two loops against one
# editor interleave PRE / POST and runs - V2.9 lost two batches to that). Same environment variables as v29_ab.sh.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
N=$(powershell.exe -NoProfile -Command "@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'v2[123][0-9]*_ab[23]?\.sh|v212_run\.sh|v211_ab\.sh|v211_run\.sh|v210_ab2?\.sh|v210_run' -and \$_.CommandLine -notmatch 'ab_safe' }).Count" | tr -d '\r')
J="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/b2runner/jobs"
P=$(ls "$J"/*.py 2>/dev/null | wc -l)
if [ "$N" != "0" ] || [ "$P" != "0" ]; then echo "AB_SAFE_REFUSED: $N A/B processes, $P pending runner jobs"; exit 3; fi
exec bash Tools/SHME_V233_20261027/v233_ab.sh
