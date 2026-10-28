#!/bin/bash
# pub234.sh : assemble Saved/Codex/SHME_V234_20261028/pub (code copies, tool diffs vs the pre-V2.34 checkpoint, manifests (JSON only, no binary
# backups), state records, tables, chain / gate logs, skills, sheets). Never copies content packages, raw animation data or vendor files.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V234_20261028; P=$D/pub; T=Tools/SHME_V234_20261028; C=$D/checkpoint/tools
mkdir -p $P/code $P/data $P/state $P/manifests $P/skills
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib234.sh vars234.sh notes234.md pub234.sh publish234.sh $(cd $D && ls run234_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
for f in shm_src.py shm_profiles.py shm_component_vars.py build_comp_vars.py build_funcs.py qa_pie.py shm_evidence.py; do diff -u $C/$f Tools/SHME_V1_20260925/$f > $P/code/${f%.py}_v234.diff; done
diff -u $C/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v234.diff
cp $D/chain.out $D/*.out $D/*.json $D/*.txt $P/data/ 2>/dev/null
cp Saved/Codex/SHME_V233_20261027/gate233.log $P/data/gate_runner.log
for f in $D/checkpoint/manifests/*.json; do cp "$f" $P/manifests/; done
for s in sphirus-natural-motion sphirus-camera-direction sphirus-safe-unreal-iteration; do mkdir -p $P/skills/$s; cp -r .agents/skills/$s/. $P/skills/$s/; done
cp CLAUDE.md $P/skills/CLAUDE_md_project.md
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v234(fin|f60|f120|f20|freal|cap|b12|b10|b9pre|b9post|b11pre|b11post|b5)_.*_state.json$"); do cp $S/$l $P/state/; done
find $P -type f -size +95M -printf "TOO_BIG %p %s\n"
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
