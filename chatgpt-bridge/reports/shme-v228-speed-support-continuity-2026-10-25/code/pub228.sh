#!/bin/bash
# pub227.sh : assemble Saved/Codex/SHME_V228_20261025/pub (code copies, tool diffs vs the pre-V2.27 checkpoint, state records, tables, chain log).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V228_20261025; P=$D/pub; T=Tools/SHME_V228_20261025; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib228.sh run228_t1.sh run228_t2.sh run228_t3.sh run228_t4d.sh run228_t5.sh run228_t6.sh run228_build.sh run228_build2.sh run228_gen4.sh run228_c5.sh run228_fin.sh pub228.sh publish228.sh; do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py $D/req/*.sh; do cp "$f" "$P/code/req_$(basename "$f")"; done
diff -u $D/checkpoint/tools/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v227.diff
diff -u $D/checkpoint/tools/qa_pie.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v227.diff; [ -s $P/code/qa_pie_v227.diff ] || rm -f $P/code/qa_pie_v227.diff
cp $D/tables228*.txt $D/chain.out $P/data/ 2>/dev/null; cp $D/probe_entry228.json $D/probe_gr228.json $D/probe_gr228b.json $D/probe_route228.json $D/probe_jr228.json $D/probe_look228.json $P/data/ 2>/dev/null
for f in $D/verify_fin.out $D/promo_fin.out; do [ -f $f ] && cp $f $P/data/; done
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E '^v228(fin|finrt|capfin|capter|capins)_.*_state\.json$'); do cp $S/$l $P/state/; done
cp $S/v228r2_j24_dbl_rhCR_r1_state.json $S/v228t2_j24_ph0_rhC_r1_state.json $S/v228t6_ter_drop_jog_te4b_r1_state.json $S/v228t6_ins_ws2_ins5_r1_state.json $P/state/ 2>/dev/null
ls $P/code | wc -l; ls $P/data; ls $P/state | wc -l
cp Tools/SHME_V1_20260925/shm_src.py $P/code/shm_src_v228.py; diff -u $D/checkpoint/tools/shm_src.pre_v228.py Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v228.diff; diff -u $D/checkpoint/tools/shm_profiles.pre_v228.py Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v228.diff; diff -u $D/checkpoint/tools/shm_component_vars.pre_v228.py Tools/SHME_V1_20260925/shm_component_vars.py > $P/code/shm_component_vars_v228.diff; cp $D/pub/notes228.md $P/data/ 2>/dev/null; rm -f $P/code/shm_src_v228.py
