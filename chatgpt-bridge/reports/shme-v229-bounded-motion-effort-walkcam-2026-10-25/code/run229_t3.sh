#!/bin/bash
# V2.29 t3: RevTurn bake check (dry, buggy recompute vs current keys; dry fixed)
source "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V229_20261025/lib229.sh"
until grep -q "T2 DUMPS_DONE" $O; do sleep 15; done
echo "T3 START $(date +%T)" >> $O
bash $R Saved/Codex/SHME_V229_20261025/req/rb229_dry_buggy.py rb229_dry_buggy 1200 | grep -a "RB229\|Error\|Traceback" | cut -c1-600 >> $O
bash $R Saved/Codex/SHME_V229_20261025/req/rb229_dry_fixed.py rb229_dry_fixed 1200 | grep -a "RB229\|Error\|Traceback" | cut -c1-600 >> $O
echo "T3 DONE $(date +%T)" >> $O
