#!/bin/bash
# pub226.sh : assemble Saved/Codex/SHME_V226_20261024/pub (code copies + diffs vs the pre-V2.26 checkpoint, verify output, state records, media)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
D=Saved/Codex/SHME_V226_20261024; P=$D/pub; T=Tools/SHME_V226_20261024; C=$D/checkpoint/tools; mkdir -p $P/code $P/img $P/vid $P/data
for f in $T/*.py $T/*.sh; do cp "$f" $P/code/; done
cp $D/vars226.sh $D/run_fin.sh $D/lib226.sh $P/code/ 2>/dev/null
for f in capterm.py entry_drift.py cmp_t11.sh dbbias226.py footspeed_nolock.py probes_r12.py probes_remove.py gen_write32.py revdbs32.py; do [ -f $D/req/$f ] && cp $D/req/$f $P/code/req_$f; done
cp $D/capsule_rev_profiles226.json $P/data/ 2>/dev/null; cp Saved/Codex/SHME_V225_20261023/capsule_rev_table.json $P/data/
diff -u $C/shm_src.py Tools/SHME_V1_20260925/shm_src.py > $P/code/shm_src_v226.diff
diff -u $C/shm_profiles.py Tools/SHME_V1_20260925/shm_profiles.py > $P/code/shm_profiles_v226.diff
diff -u $C/shm_component_vars.py Tools/SHME_V1_20260925/shm_component_vars.py > $P/code/shm_component_vars_v226.diff
diff -u $C/qa_pie.py Tools/SHME_V1_20260925/qa_pie.py > $P/code/qa_pie_v226.diff
diff -u $C/v212_run.sh Tools/SHME_V212_20261017/v212_run.sh > $P/code/v212_run_v226.diff
diff -u $C/gen225_rev.py $T/gen226_rev.py > $P/code/gen225_to_gen226.diff
cp $D/verify_fin.out $P/verify_prod226_final.txt 2>/dev/null; cp $D/promo_fin.out $P/promote226_final.txt 2>/dev/null
cp $D/run_fin.out $P/data/run_fin.out 2>/dev/null; cp $D/run_m5.out $P/data/run_m5.out 2>/dev/null
E=Saved/Codex/SHME_V1_20260925/Evidence
for lab in v226fin_j24_ph0_o_r1 v226fin_ins_ws_o_r1 v226fin_ter_drop_walk_o_r1 v226fin_map_r2_o_r1; do cp Saved/Codex/SHME_V1_20260925/${lab}_state.json $P/data/ 2>/dev/null; cp Saved/Codex/SHME_V1_20260925/${lab}_pie.json $P/data/ 2>/dev/null; done
bash $D/req/cmp_t11.sh > $P/data/slip_table_reversal.txt 2>/dev/null
"/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" $D/req/capterm.py v226t9_j24_ph3_rv32F_r1 v226t9_j24_ph3_rv32_r1 v226t9_j24_sw_ph0_rv32F_r1 > $P/data/capterm_ph3_sw_ph0.txt 2>/dev/null
# diffs are the only place with user-private paths? no - project-relative; vendor animations are NOT copied (names only)
du -sh $P; ls $P/code | wc -l
