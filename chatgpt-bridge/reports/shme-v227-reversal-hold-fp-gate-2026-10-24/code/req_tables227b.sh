#!/bin/bash
# tables227b.sh : pass-d (t4/u60/u120/u20) tables. A: fixed 30 prod | rv32 | rh(t3, pass c) | rh(t4, pass d). B: FPS sweep prod(v226s*) | rv32(v227s*) | rh pass c (v227s*) | rh pass d (v227u*).
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; T7=Tools/SHME_V227_20261024; E=Saved/Codex/SHME_V1_20260925/Evidence
pick() { for c in "$@"; do [ -f $E/$c.json ] && { echo $c; return; }; done; echo ""; }
p25() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T5/plant225.py $2 $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
p27() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T7/plant227.py $2 $1 2>/dev/null | grep -o "contact-start worst *[0-9.]*" | grep -o "[0-9.]*$"; }
echo "A) worst planted-foot slip cm (height-only | contact-start), fixed 30 FPS"
printf "%-7s %-13s %-13s %-13s %-13s\n" scen prod rv32 rh_c rh_d
for s in ph0 ph3 sw_ph0 sw_ph2 rel dbl; do
  P=$(pick v226fin_j24_${s}_o_r1 v226t1_j24_${s}_o_r1 v225t10_j24_${s}_o_r1)
  V=$(pick v227t4_j24_${s}_rv32_r1 v227t3_j24_${s}_rv32_r1 v227t2_j24_${s}_rv32_r1 v227t1_j24_${s}_rv32_r1)
  H=$(pick v227t3_j24_${s}_rh_r1 v227t2_j24_${s}_rh_r1); H4=$(pick v227t4_j24_${s}_rh_r1)
  printf "%-7s %5s | %5s %5s | %5s %5s | %5s %5s | %5s\n" $s "$(p25 "$P" --fam=Pivot)" "$(p27 "$P" --fam=Pivot)" "$(p25 "$V")" "$(p27 "$V")" "$(p25 "$H")" "$(p27 "$H")" "$(p25 "$H4")" "$(p27 "$H4")"
done
echo; echo "B) FPS sweep, worst slip cm (height-only | contact-start): prod | rv32 | rh pass c | rh pass d"
for f in 20 60 120; do echo "-- $f FPS"; for s in ph0 ph3 sw_ph2 ovl120; do
  P=$(pick v226s${f}_j24_${s}_o_r1); V=$(pick v227s${f}_j24_${s}_rv32_r1); H=$(pick v227s${f}_j24_${s}_rh_r1); H4=$(pick v227u${f}_j24_${s}_rh_r1)
  printf "%-7s %5s | %5s %5s | %5s %5s | %5s %5s | %5s\n" $s "$(p25 "$P" --fam=Pivot)" "$(p27 "$P" --fam=Pivot)" "$(p25 "$V")" "$(p27 "$V")" "$(p25 "$H")" "$(p27 "$H")" "$(p25 "$H4")" "$(p27 "$H4")"
done; done
echo; echo "C) exit227 pass d (t4 30 / u60 / u120)"
for l in $(ls $E | grep -E '^v227(t4|u60|u120|u20)_j24_.*_rh_r1\.json$' | sed 's/\.json$//'); do "$PY" $T7/exitjump227.py $l | sed 's/ | pelvis excess.*next/ | next/'; done
