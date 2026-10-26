#!/bin/bash
# pub231.sh : assemble Saved/Codex/SHME_V231_20261026/pub (code copies, tool diffs vs the pre-V2.31 checkpoint, state records, tables, chain log).
# Never copies content packages, raw animation data or paid vendor files (only scripts, diffs, JSON/text measurements, our own captures).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V231_20261026; P=$D/pub; T=Tools/SHME_V231_20261026; C=$D/checkpoint/pre_v231/tools/Tools; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib231.sh vars231.sh an_gslow.py pick_loaded.py notes231.md $D/run231_*.sh pub231.sh publish231.sh; do f=$(basename $f); [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do case "$f" in *pre_*|*.r1.py) ;; *) cp "$f" "$P/code/req_$(basename "$f")";; esac; done
diff -u $D/req/v212_run.pre231.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v231.diff
diff -u $C/SHME_V1_20260925/qa_pie.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v231.diff
diff -u $C/SHME_V1_20260925/qa.sh Tools/SHME_V1_20260925/qa.sh > $P/code/qa_sh_v231.diff
diff -u $C/SHME_V1_20260925/shm_src.py Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v231.diff
diff -u $C/SHME_V1_20260925/shm_profiles.py Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v231.diff
diff -u $C/SHME_V1_20260925/shm_component_vars.py Tools/SHME_V1_20260925/shm_component_vars.py > $P/code/shm_component_vars_v231.diff
diff -u $C/SHME_V1_20260925/build_tick.py Tools/SHME_V1_20260925/build_tick.py > $P/code/build_tick_v231.diff
cp $D/chain.out $D/mem231.txt $D/loaded_good.json $D/loaded_good2.json $D/verify_p0.out $D/retention_apply.out $P/data/ 2>/dev/null
cp $D/gen231_slow_dry.json $P/data/gen231_slow_dry_r2_rejected.json 2>/dev/null; cp $D/gen231_loaded_dry_r2.json $P/data/ 2>/dev/null
for f in $D/promo_fin.out $D/verify_fin.out $D/verify_fin2.out $D/slide_audit.out $D/gslow_dry.out $D/gslow_dry2.txt $D/inspect_install.out $D/exitpush_c.out $D/tipend.out $D/timing231.out; do [ -f $f ] && cp $f $P/data/; done
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E "^v231(fin|f20|f60|f120|frt|a3|b1|b2|s3|s3b|cap)_.*_state.json$"); do cp $S/$l $P/state/; done
rm -f $P/REPORT_BODY_DRAFT.md
ls $P/code | wc -l; ls $P/data | wc -l; ls $P/state | wc -l; du -sh $P
