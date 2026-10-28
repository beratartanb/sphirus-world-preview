#!/bin/bash
# pub235.sh : assemble Saved/Codex/SHME_V235_20261028/pub (code copies, DSL / profile / harness diffs vs the pre-V2.35 checkpoint, manifests
# (JSON only, no binary backups), state records, tables, chain / gate logs, skills, sheets). Never copies content packages, raw animation data,
# checkpoint .uasset backups or vendor files.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V235_20261028; P=$D/pub; T=Tools/SHME_V235_20261028; C=$D/checkpoint
mkdir -p $P/code $P/data $P/state $P/manifests $P/skills $P/sheets
cp $T/*.py $T/*.sh $T/*.ps1 $P/code/ 2>/dev/null
for f in lib235.sh vars235.sh capblock235.sh notes235.md pub235.sh publish235.sh capsule_rev235.json $(cd $D && ls run235_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
diff -u $C/shm_src.py.pre235 Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v235.diff
diff -u $C/shm_profiles.py.pre235 Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v235.diff
diff -u $C/v212_run.sh.pre235 Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v235.diff
cp $D/chain.out $D/*.out $D/*.txt $D/stopbody235*.json $D/gen235_rev_*.json $P/data/ 2>/dev/null
cp Saved/Codex/SHME_V233_20261027/gate233.log $P/data/gate_runner.log
for f in $D/checkpoint/manifests/*.json; do cp "$f" $P/manifests/; done
for s in sphirus-natural-motion sphirus-camera-direction sphirus-safe-unreal-iteration; do mkdir -p $P/skills/$s; cp -r .agents/skills/$s/. $P/skills/$s/; done
cp CLAUDE.md $P/skills/CLAUDE_md_project.md
cp $D/sheets/*.png $P/sheets/ 2>/dev/null; rm -f $P/sheets/probe.png
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v235(fin|f60|f120|f20|freal|cap|b8|b7|b6|b4|b3|a1)_.*_state.json$"); do cp $S/$l $P/state/; done
find $P -type f \( -name "*.uasset" -o -name "*.umap" -o -name "*.fbx" \) -printf "BINARY %p\n"
find $P -type f -size +95M -printf "TOO_BIG %p %s\n"
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
