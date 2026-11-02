#!/bin/bash
# pub250.sh : assemble Saved/Codex/SHME_V250_20261103/pub (code copies, DSL / profile / harness diffs vs the pre-V2.36 checkpoint, manifests
# (JSON only, no binary backups), state records, tables, chain / gate logs, skills, sheets). Never copies content packages, raw animation data,
# checkpoint .uasset backups or vendor files.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V250_20261103; P=$D/pub; T=Tools/SHME_V250_20261103; C=$D/checkpoint
mkdir -p $P/code $P/data $P/state $P/manifests $P/skills $P/sheets
cp Tools/SHME_V249_20261102/turn249.py Tools/SHME_V249_20261102/install249_*.py $P/code/ 2>/dev/null; cp $T/*.py $T/*.sh $T/*.ps1 $P/code/ 2>/dev/null
cp Tools/SHME_V212_20261017/v212_run.sh $P/code/v212_run_v250.sh; cp Tools/SHME_V1_20260925/qa_pie.py $P/code/qa_pie_v250.py
for f in lib250.sh vars248.sh vars248_cap.sh pub250.sh publish248.sh $(cd $D && ls run250_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
cp -r $D/research $P/ 2>/dev/null; cp $D/tables_*.md $P/data/ 2>/dev/null
cp $D/chain.out $D/*.out $D/*.txt $P/data/ 2>/dev/null
cp Saved/Codex/SHME_V233_20261027/gate233.log $P/data/gate_runner.log; cp Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v250_*.json $P/manifests/ 2>/dev/null; cp Tools/SHME_V242_20261101/gait242.py Tools/SHME_V242_20261101/cropstrip242.ps1 Tools/SHME_V231_20261026/contact231.py Tools/SHME_V21_20261014/pop_report.py Saved/Codex/SHME_V243_20261101/idlemet243.py Tools/SHME_V212_20261017/v212_run.sh $P/code/ 2>/dev/null
for f in $D/checkpoint/manifests/*.json; do cp "$f" $P/manifests/; done
for s in sphirus-safe-unreal-iteration sphirus-balance-recovery sphirus-motion-synthesis sphirus-human-motion-engine sphirus-natural-motion sphirus-camera-direction; do mkdir -p $P/skills/$s; cp -r .agents/skills/$s/. $P/skills/$s/; done
cp CLAUDE.md $P/skills/CLAUDE_md_project.md; cp $D/REPORT_V250*.md $D/CHANGES_V250.md $D/TABLES_V250.md $P/ 2>/dev/null; cp -r $D/data/. $P/data/ 2>/dev/null; mkdir -p $P/vid; cp $D/vid/*.avi $D/vid/*.gif $P/vid/ 2>/dev/null
cp $D/sheets/*.png $P/sheets/ 2>/dev/null   # stick JSON (per-frame bone positions derived from paid source clips) is NOT published; the rendered sheets are
mkdir -p $P/code/retention; cp Tools/Retention/retention.py Tools/Retention/protect.txt $P/code/retention/; cp Saved/Codex/Retention/*.txt $P/data/ 2>/dev/null
rm -f $P/data/footpath.out $P/data/blendfk.out $P/data/clipdump.json   # per-frame bone data derived from paid source clips is not published
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v250[a-z0-9]+_.*_state.json$"); do cp $S/$l $P/state/; done
find $P -type f \( -name "*.uasset" -o -name "*.umap" -o -name "*.fbx" \) -printf "BINARY %p\n"
find $P -type f -size +95M -printf "TOO_BIG %p %s\n"
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
