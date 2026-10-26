#!/bin/bash
# pub230.sh : assemble Saved/Codex/SHME_V230_20261026/pub (code copies, tool diffs vs the pre-V2.30 checkpoint, state records, tables, chain log).
# Never copies content packages, raw animation data or paid vendor files (only scripts, diffs, JSON/text measurements, our own captures).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V230_20261026; P=$D/pub; T=Tools/SHME_V230_20261026; C=$D/checkpoint/pre_v230/tools; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib230.sh vars230.sh vars230c.sh gate230L.py $D/run230_*.sh pub230.sh publish230.sh; do f=$(basename $f); [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do case "$f" in *pre_*) ;; *) cp "$f" "$P/code/req_$(basename "$f")";; esac; done
diff -u $C/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v230.diff
diff -u $C/qa_pie.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v230.diff
diff -u $D/req/evidence.pre_ltp230.py Tools/SHME_V1_20260925/evidence.py > $P/code/evidence_v230.diff
diff -u $C/shm_src.py Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v230.diff
diff -u $C/shm_profiles.py Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v230.diff
diff -u Tools/SHME_V2_20261014/v2_editor_launch.sh $T/editor_launch230.sh > $P/code/editor_launch230.diff
cp $D/chain.out $D/mem230.jsonl $D/loaded_good.json $D/capsule_rev_table_loaded.json $D/integrity.out $D/verify_p0.out $P/data/ 2>/dev/null
for f in $D/promo_fin.out $D/verify_fin.out $D/verify_fin2.out $D/verify_fin3.out $D/promo_fin3.out $D/ra_write7.out $D/ra_measure3.out $D/tables230*.txt $D/timing230.out; do [ -f $f ] && cp $f $P/data/; done
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v230(fin|fin3|h20|h60|h120|t12|t13|t14|t15|t16|cap)_.*_state.json$"); do cp $S/$l $P/state/; done
ls $P/code | wc -l; ls $P/data; ls $P/state | wc -l
