#!/bin/bash
# pub232.sh : assemble Saved/Codex/SHME_V232_20261027/pub (code copies, tool diffs vs the pre-V2.32 checkpoint, state records, tables, chain
# log). Never copies content packages, raw animation data or paid vendor files (only scripts, diffs, JSON/text measurements, our own captures).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V232_20261027; P=$D/pub; T=Tools/SHME_V232_20261027; C=$D/checkpoint/pre_v232/tools/Tools; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib232.sh vars232.sh vars232_post.sh vars232_cap.sh notes232.md pub232.sh publish232.sh $(cd $D && ls run232_*.sh); do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do cp "$f" "$P/code/req_$(basename "$f")"; done
for f in qa_pie.py shm_src.py shm_profiles.py shm_component_vars.py build_funcs.py; do diff -u $C/SHME_V1_20260925/$f Tools/SHME_V1_20260925/$f > $P/code/${f%.py}_v232.diff; done
diff -u $C/SHME_V212_20261017/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v232.diff
cp $D/chain.out $D/*.out $D/*.json $D/tables_*.txt $P/data/ 2>/dev/null
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v232(fin|f60|f120|f20|freal|p2|p2c|iso|cap)_.*_state.json$"); do cp $S/$l $P/state/; done
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
