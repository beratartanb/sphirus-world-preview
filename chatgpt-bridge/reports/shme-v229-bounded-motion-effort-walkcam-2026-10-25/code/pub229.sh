#!/bin/bash
# pub229.sh : assemble Saved/Codex/SHME_V229_20261025/pub (code copies, tool diffs vs the pre-V2.29 checkpoint, state records, tables, chain log).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V229_20261025; P=$D/pub; T=Tools/SHME_V229_20261025; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib229.sh vars229.sh vars229f.sh run229_t1.sh run229_t2.sh run229_t3.sh run229_t4.sh run229_t5.sh run229_t6.sh run229_t7.sh run229_build.sh run229_build2.sh run229_build3.sh run229_fin.sh run229_pc.sh run229_fin2.sh run229_fin3.sh run229_fin3b.sh run229_ems.sh run229_sm.sh run229_cap4.sh run229_captest.sh pub229.sh publish229.sh; do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py; do case "$f" in *pre_v229*|*pre_pc229*) ;; *) cp "$f" "$P/code/req_$(basename "$f")";; esac; done
diff -u $D/req/v212_run.pre_v229.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v229.diff
diff -u $D/req/qa_pie.pre_v229.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v229.diff
diff -u $D/checkpoint/pre_v229/tools/shm_src.py Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v229.diff
diff -u $D/checkpoint/pre_v229/tools/shm_profiles.py Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v229.diff
diff -u $D/checkpoint/pre_v229/tools/shm_component_vars.py Tools/SHME_V1_20260925/shm_component_vars.py > $P/code/shm_component_vars_v229.diff
cp $D/tables229*.txt $D/chain.out $D/rb229_*.json $P/data/ 2>/dev/null
for f in $D/verify_fin.out $D/verify_fin2.out $D/verify_fin3.out $D/promo_fin.out $D/promo_fin2.out $D/promo_fin3.out; do [ -f $f ] && cp $f $P/data/; done
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E '^v229(fin|fn2|fn3|h20|h60|h120|hrt|cap4|pre|v229pc|em|sm|t1)_.*_state\.json$'); do cp $S/$l $P/state/; done
ls $P/code | wc -l; ls $P/data; ls $P/state | wc -l
