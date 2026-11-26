cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; H="exec(open(u.Paths.project_dir()+'Tools/UE59_20261126/hk_imp.py',encoding='utf8').read())"
rec() { VSHOT=1 VSIDE="$3" bash Saved/UE59Work/p4/rec.sh $1 $2 - "" 30 "$4" | grep -a "VIDREC\|Error"; }
rec af_fwd Saved/UE59Work/b11/plan_idle14.txt "(700,60,0,-30)" "builtins.IMP_PLAN=[(1.0,'spine_02','spine_04',1,(700,0,0))]; builtins.FL_PLAN=[]; $H"
rec af_back Saved/UE59Work/b11/plan_idle14.txt "(700,60,0,-30)" "builtins.IMP_PLAN=[(1.0,'spine_02','spine_04',1,(-700,0,0))]; builtins.FL_PLAN=[]; $H"
rec af_tired Saved/UE59Work/b11/plan_idle14.txt "(700,60,0,-30)" "builtins.CT_FAT=0.9; builtins.IMP_PLAN=[(1.0,'spine_02','spine_04',1,(700,0,0))]; builtins.FL_PLAN=[]; $H"
echo "[('', 1.0, 0), ('W LeftShift', 2.5, 0), ('', 12.0, 0)]" > Saved/UE59Work/b11/plan_runfall.txt
rec af_run Saved/UE59Work/b11/plan_runfall.txt "(900,80,0,-30)" "builtins.IMP_PLAN=[]; builtins.FL_PLAN=[(3.0,(250,0,40))]; $H"
for n in af_fwd af_back af_tired; do for t in 0.95 1.2 1.45 1.7 2.1 3.0 5.0; do bash Saved/UE59Work/mr2/fr.sh $n $t | tail -1; done; done
for t in 2.9 3.2 3.45 3.7 4.1 5.0 7.0; do bash Saved/UE59Work/mr2/fr.sh af_run $t | tail -1; done
echo FALLSET_DONE
