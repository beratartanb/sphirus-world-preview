#!/bin/bash
# run230_m2.sh : memory owner study 2 - editor with Unreal's Low Level Memory tracker (-LLM -LLMCSV writes per-tag CSV to
# Saved/Profiling/LLM), the same short PIE scenario 6x with a sample after every run.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; export O=$D/chain.out; source $D/lib230.sh
echo "M2 start $(date +%T)" >> $O
relaunch_llm() { export LR_LOG=$(basename "$(ls -t Saved/Logs/*.log | grep -v -i cef | head -1)"); export V219_EDARGS="-UseFixedTimeStep -FPS=30 -LLM -LLMCSV"; bash Tools/SHME_V2_20261014/v2_editor_launch.sh "shmv230_m2" 2>&1 | tail -2 >> $O; export LR_LOG="shmv230_m2.log"; echo "RELAUNCH m2 llm $(date +%T)" >> $O; }
if tasklist 2>/dev/null | grep -qi UnrealEditor.exe; then bash Tools/SHME_V2_20261014/run_v2.sh Tools/SHME_V21_20261014/revert_quit.py rq_m2 300 | grep -E "dirty after|QUIT|REFUSED" >> $O; for i in $(seq 1 90); do tasklist | grep -qi UnrealEditor.exe || break; sleep 2; done; fi
relaunch_llm
export WARM=0 MEMCAP_GB=50 MEMPROBE=1 MEMPROBE_GC=False
J=""; for i in 1 2 3 4 5 6; do J="$J j24_ph0:o:$i"; done
ab m2 "$J" $D/vars230.sh
echo "M2_DONE $(date +%T)" >> $O
