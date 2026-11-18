#!/bin/bash
# hip1.sh <suffix> <profile A|C> <gait W|J> [extra prelude]: one hip-swing turn run on the flat map (side camera), recorder hiprec.py.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh
S=$1; PR=$2; G=$3; X=${4:-pass}; case $G in J) PL="$PLAN_HIPJ";; S) PL="$PLAN_HIPS";; *) PL="$PLAN_HIPW";; esac
L=H_${PR}${G}_$S
PLAN="$PL" LP=H${G} XP="builtins.HR_LABEL='$L'; builtins.HR_TMAX=33.5; $X; exec(open(u.Paths.project_dir()+'Tools/UE59_20261116/hiprec.py',encoding='utf8').read())" bash Tools/UE59_20261116/ab1.sh $S $PR
ls -la Saved/UE59Work/rec/$L.json
