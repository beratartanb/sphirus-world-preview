#!/bin/bash
P="/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS"; L="$P/Saved/Codex/CharacterFinal_20260929/outfit_jobs_log.txt"
for i in $(seq 1 900); do grep -q "recompiled" "$L" 2>/dev/null && break; sleep 10; done
cat "$L"
bash "$P/Tools/CharacterFinal_20260929/run_final_chain.sh" j4 setup_body audit_a6 body_dfm setup_final neutral closeups deform gameplay lods clay hair hairalts eval boards
