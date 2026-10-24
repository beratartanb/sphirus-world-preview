#!/bin/bash
# tables227.sh : report tables. A: worst planted-foot slip (height-only plant225 / contact-start plant227) prod | rv32 | rh (fixed 30).
# B: clip life (exit227) rv32 vs rh. C: posture rv32 vs rh. Labels: prod = V2.26/V2.25 production runs (fam Pivot), rv32/rh = newest tag.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; T7=Tools/SHME_V227_20261024; E=Saved/Codex/SHME_V1_20260925/Evidence
pick() { for c in "$@"; do [ -f $E/$c.json ] && { echo $c; return; }; done; echo ""; }
p25() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T5/plant225.py $2 $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
p27() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T7/plant227.py $2 $1 2>/dev/null | grep -o "contact-start worst *[0-9.]*" | grep -o "[0-9.]*$"; }
echo "A) worst planted-foot slip cm (height-only | contact-start), fixed 30 FPS"
printf "%-7s %-13s %-13s %-13s   labels\n" scen prod rv32 rh
for s in ph0 ph3 sw_ph0 sw_ph2 rel dbl ad_ph0 m180w; do
  P=$(pick v226fin_j24_${s}_o_r1 v226t1_j24_${s}_o_r1 v225t10_j24_${s}_o_r1 v225t1_j24_${s}_o_r1 v224t1c_j24_${s}_o_r1)
  V=$(pick v227t3_j24_${s}_rv32_r1 v227t2_j24_${s}_rv32_r1 v227t1_j24_${s}_rv32_r1 v226t4_j24_${s}_rv32_r1)
  H=$(pick v227t3_j24_${s}_rh_r1 v227t2_j24_${s}_rh_r1)
  printf "%-7s %5s | %5s %5s | %5s %5s | %5s   %s %s %s\n" $s "$(p25 "$P" --fam=Pivot)" "$(p27 "$P" --fam=Pivot)" "$(p25 "$V")" "$(p27 "$V")" "$(p25 "$H")" "$(p27 "$H")" "$P" "$V" "$H"
done
echo; echo "B) clip life (exit227): rv32 vs rh"
for s in ph0 ph3 sw_ph0 sw_ph2 rel dbl; do for v in rv32 rh; do l=$(pick v227t3_j24_${s}_${v}_r1 v227t2_j24_${s}_${v}_r1 v227t1_j24_${s}_${v}_r1); [ -n "$l" ] && "$PY" $T7/exitjump227.py $l | sed 's/ | pelvis excess.*next/ | next/; s/ | SWITCH.*//'; done; done
echo; echo "C) posture (window request..exit)"
for s in ph0 ph3 sw_ph2; do for v in rv32 rh; do l=$(pick v227t3_j24_${s}_${v}_r1 v227t2_j24_${s}_${v}_r1 v227t1_j24_${s}_${v}_r1); [ -n "$l" ] && "$PY" Tools/SHME_V226_20261024/posture226.py $l 4.9 7.5; done; done
