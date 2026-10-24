#!/bin/bash
# worst planted-foot slip (plant225) per scenario: production (V2.24 pivot, fam Pivot) | t4 (rv32, no curves) | t9 (footspeed v2) | t11 (footspeed v2 + Disable_FootLock=1)
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; E=Saved/Codex/SHME_V1_20260925/Evidence
w() { [ -f $E/$1.json ] || { echo "-"; return; }; "$PY" $T5/plant225.py $2 $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
printf "%-8s %6s %6s %6s %6s\n" scen prod t4 t9 t11
for s in sw_ph0 sw_ph1 sw_ph2 sw_ph3 sw_ph4 ph0 ph1 ph2 ph3 ph4 rel dbl ad_ph0 m180w; do
  o=""; for c in v226t1_j24_${s}_o_r1 v225t10_j24_${s}_o_r1 v225t1_j24_${s}_o_r1 v224t1c_j24_${s}_o_r1; do [ -f $E/$c.json ] && { o=$(w $c --fam=Pivot); break; }; done
  printf "%-8s %6s %6s %6s %6s\n" $s "${o:--}" "$(w v226t4_j24_${s}_rv32_r1)" "$(w v226t9_j24_${s}_rv32_r1)" "$(w v226t11_j24_${s}_rv32_r1)"
done
echo; echo "t11 episodes:"; for s in sw_ph0 ph0 ph3 rel dbl ad_ph0 m180w; do "$PY" $T5/plant225.py v226t11_j24_${s}_rv32_r1 2>/dev/null | cut -c1-260; done
