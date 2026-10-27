#!/bin/bash
# pub233.sh : assemble Saved/Codex/SHME_V233_20261027/pub (code copies, tool diffs vs the pre-V2.33 checkpoint, gated runner + its diff,
# manifests (JSON lists / state, no binary backups), state records, tables, chain log, gate log, skills). Never copies content packages,
# raw animation data or paid vendor files (only scripts, diffs, JSON/text measurements, our own captures).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V233_20261027; P=$D/pub; T=Tools/SHME_V233_20261027; C=$D/checkpoint/tools
SP="/c/Users/berat/AppData/Local/Temp/claude/C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS/5f49a232-b001-47ad-8881-1eb04d9cb1c5/scratchpad"
mkdir -p $P/code $P/code/gatetest $P/data $P/state $P/manifests $P/skills $P/sheets
cp $T/*.py $T/*.sh $T/*.ps1 $P/code/ 2>/dev/null; cp $T/gatetest/* $P/code/gatetest/ 2>/dev/null
for f in lib233.sh vars233.sh vars233_cap.sh vars233_capall.sh notes233.md pub233.sh publish233.sh $(cd $D && ls run233_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
for f in qa_pie.py shm_src.py shm_component_vars.py shm_evidence.py; do diff -u $C/$f Tools/SHME_V1_20260925/$f > $P/code/${f%.py}_v233.diff; done
for f in shm_profiles.py build_funcs.py build_comp_vars.py; do [ -f Tools/SHME_V1_20260925/$f ] && cp Tools/SHME_V1_20260925/$f $P/code/${f%.py}_v233_full.py; done
diff -u $C/revert_v21_quit.py Tools/SHME_V21_20261014/revert_v21_quit.py > $P/code/revert_v21_quit_v233.diff
cp Tools/SHME_V212_20261017/v212_run.sh $P/code/v212_run_v233_full.sh
cp $SP/b2runner/runner.py $P/code/runner_v233_gated.py; diff -u $SP/b2runner/runner_v2_pre233.py $SP/b2runner/runner.py > $P/code/runner_v233.diff
cp $D/chain.out $D/gate233.log $D/*.out $D/*.json $D/tables_*.txt $D/matrix_fin.txt $D/rec_k2.txt $D/rec_fin.txt $D/ep_d60.txt $P/data/ 2>/dev/null
for f in $D/checkpoint/manifests/*.json; do cp "$f" $P/manifests/; done
cp $D/sheets/*.png $P/sheets/ 2>/dev/null
for s in sphirus-natural-motion sphirus-camera-direction sphirus-safe-unreal-iteration; do mkdir -p $P/skills/$s; cp -r .agents/skills/$s/. $P/skills/$s/; done
cp CLAUDE.md $P/skills/CLAUDE_md_project.md
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v233(fin|f60|f120|f20|freal|cap|k2|s|d60)_.*_state.json$"); do cp $S/$l $P/state/; done
find $P -type f -size +95M -printf "TOO_BIG %p %s\n"
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
