#!/bin/bash
# pub227.sh : assemble Saved/Codex/SHME_V227_20261024/pub (code copies, tool diffs vs the pre-V2.27 checkpoint, state records, tables, chain log).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V227_20261024; P=$D/pub; T=Tools/SHME_V227_20261024; mkdir -p $P/code $P/data $P/state
cp $T/*.py $T/*.sh $P/code/ 2>/dev/null
for f in lib227.sh run227_sweep.sh run227_t4.sh run227_t5.sh run227_fin.sh pub227.sh publish227.sh; do [ -f $D/$f ] && cp $D/$f $P/code/; done
for f in $D/req/*.py $D/req/*.sh; do cp "$f" "$P/code/req_$(basename "$f")"; done
diff -u $D/checkpoint/tools/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v227.diff
diff -u $D/checkpoint/tools/qa_pie.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v227.diff; [ -s $P/code/qa_pie_v227.diff ] || rm -f $P/code/qa_pie_v227.diff
cp $D/tables227*.txt $D/chain.out $P/data/ 2>/dev/null; cp $D/probe227.json $D/probe_fp227.json $P/data/ 2>/dev/null
for f in $D/verify_fin.out $D/promo_fin.out; do [ -f $f ] && cp $f $P/data/; done
S=Saved/Codex/SHME_V1_20260925
for l in $(ls $S | grep -E '^v227(fin|finrt|capfin)_.*_state\.json$'); do cp $S/$l $P/state/; done
cp $S/v227t5_j24_dbl_rh_r1_state.json $S/v227t5_j24_ph0_rh_r1_state.json $P/state/ 2>/dev/null
ls $P/code | wc -l; ls $P/data; ls $P/state | wc -l
