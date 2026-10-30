#!/bin/bash
# pub238.sh : assemble Saved/Codex/SHME_V238_20261030/pub (code copies, DSL / profile / harness diffs vs the pre-V2.36 checkpoint, manifests
# (JSON only, no binary backups), state records, tables, chain / gate logs, skills, sheets). Never copies content packages, raw animation data,
# checkpoint .uasset backups or vendor files.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V238_20261030; P=$D/pub; T=Tools/SHME_V238_20261030; C=$D/checkpoint
mkdir -p $P/code $P/data $P/state $P/manifests $P/skills $P/sheets
cp $T/*.py $T/*.sh $T/*.ps1 $P/code/ 2>/dev/null
for f in lib238.sh vars238.sh capblock238.sh notes238.md pub238.sh publish238.sh $(cd $D && ls run238_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
cp -r $D/research $P/ 2>/dev/null; cp $D/tables_*.md $P/data/ 2>/dev/null
cp $D/chain.out $D/*.out $D/*.txt $D/gen238_*.json $D/capsule*.json $P/data/ 2>/dev/null
cp Saved/Codex/SHME_V233_20261027/gate233.log $P/data/gate_runner.log
for f in $D/checkpoint/manifests/*.json; do cp "$f" $P/manifests/; done
for s in sphirus-natural-motion sphirus-camera-direction sphirus-safe-unreal-iteration sphirus-balance-recovery sphirus-motion-synthesis sphirus-game-dev-director; do mkdir -p $P/skills/$s; cp -r .agents/skills/$s/. $P/skills/$s/; done
cp CLAUDE.md $P/skills/CLAUDE_md_project.md
cp $D/sheets/*.png $P/sheets/ 2>/dev/null   # stick JSON (per-frame bone positions derived from paid source clips) is NOT published; the rendered sheets are
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v238[a-z0-9]+_.*_state.json$"); do cp $S/$l $P/state/; done
find $P -type f \( -name "*.uasset" -o -name "*.umap" -o -name "*.fbx" \) -printf "BINARY %p\n"
find $P -type f -size +95M -printf "TOO_BIG %p %s\n"
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
