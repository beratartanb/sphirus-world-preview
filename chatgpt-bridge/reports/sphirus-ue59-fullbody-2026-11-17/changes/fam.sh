#!/bin/bash
# fam.sh <suffix> <profile> [tests]: whole-family runs for one profile on the flat map (side camera): full gait, stop, crouch, jump.
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; . Tools/UE59_20261116/plans.sh; S=$1; PR=$2; shift; shift
for t in ${@:-full stop crouch jump}; do case $t in
 full)   LP=F  bash Tools/UE59_20261116/ab1.sh $S $PR;;
 stop)   PLAN="$PLAN_STOP" LP=FS bash Tools/UE59_20261116/ab1.sh $S $PR;;
 crouch) PLAN="$PLAN_CROUCH" LP=FC bash Tools/UE59_20261116/ab1.sh $S $PR;;
 jump)   PLAN="$PLAN_JUMP" LP=FJ bash Tools/UE59_20261116/ab1.sh $S $PR;;
 brake)  PLAN="$PLAN_BRAKE" LP=FB bash Tools/UE59_20261116/ab1.sh $S $PR;;
esac; done 2>&1 | grep -E "VIDREC|SLOT_CH"
