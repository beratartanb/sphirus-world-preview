#!/bin/bash
# lock233.sh acquire <owner> "<reason>" | release <owner> | status : single job owner for the project editor (Saved/Codex/EDITOR_LOCK.txt).
# acquire refuses when another owner holds the lock or when an A/B process / pending runner job exists; the gated runner (G3) refuses
# jobs of any other owner while the lock is held.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
L=Saved/Codex/EDITOR_LOCK.txt; J="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad/b2runner/jobs"
cur=$(grep -o "owner=[^ ]*" $L 2>/dev/null | head -1 | cut -d= -f2); locked=$(grep -c "^LOCKED" $L 2>/dev/null)
case "$1" in
  acquire)
    if [ "$locked" = "1" ] && [ -n "$cur" ] && [ "$cur" != "$2" ]; then echo "LOCK233_REFUSED held by $cur"; exit 3; fi
    n=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'v23[0-9]_ab\.sh|ab_safe23' }).Count" 2>/dev/null | tr -d '\r')
    p=$(ls $J/*.py 2>/dev/null | wc -l)
    if [ "${n:-0}" != "0" ] || [ "$p" != "0" ]; then echo "LOCK233_REFUSED busy: $n A/B processes, $p pending jobs"; exit 3; fi
    echo "LOCKED owner=$2 $(date '+%Y-%m-%d %H:%M') - $3" > $L; echo "LOCK233 acquired $2";;
  release)
    if [ -n "$cur" ] && [ "$cur" != "$2" ]; then echo "LOCK233_REFUSED release by $2, held by $cur"; exit 3; fi
    echo "UNLOCKED $(date '+%Y-%m-%d %H:%M') - released by $2" > $L; echo "LOCK233 released";;
  *) cat $L;;
esac
