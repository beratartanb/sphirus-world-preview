#!/bin/bash
# gd14_memguard.sh [limit_GB=40] : restart the editor (lk_editor_restart) when its committed (private) memory exceeds the limit -
# the 2026-10-09 fit crash was an OOM at 63 GB committed (page file too small); heavy MHC fit / auto-rig jobs need headroom.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; LIM=${1:-24}
GB=$(powershell.exe -NoProfile -Command "\$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue; if (\$p) { [math]::Round(\$p.PrivateMemorySize64/1GB,1) } else { -1 }" | tr -d '\r')
GB=${GB/,/.}; echo "EDITOR_PRIVATE_GB $GB"
if [ "$GB" = "-1" ] || awk "BEGIN{exit !($GB > $LIM)}"; then bash Tools/CharacterLookdev_20260930/lk_editor_restart.sh gd14_$(date +%H%M%S) | tail -2; fi
