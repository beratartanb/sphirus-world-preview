#!/bin/bash
# tables227d.sh : final decision tables. Fixed 30 and FPS sweep: prod | rh pass e (t5/w*) | rhH hold-only (h*). cm, height-only | contact-start.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; T7=Tools/SHME_V227_20261024; E=Saved/Codex/SHME_V1_20260925/Evidence
pick() { for c in "$@"; do [ -f $E/$c.json ] && { echo $c; return; }; done; echo ""; }
p25() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T5/plant225.py $2 $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
p27() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T7/plant227.py $2 $1 2>/dev/null | grep -o "contact-start worst *[0-9.]*" | grep -o "[0-9.]*$"; }
row() { printf "%-7s %5s | %5s %5s | %5s %5s | %5s\n" "$1" "$(p25 "$2" --fam=Pivot)" "$(p27 "$2" --fam=Pivot)" "$(p25 "$3")" "$(p27 "$3")" "$(p25 "$4")" "$(p27 "$4")"; }
echo "fixed 30:  prod | rh (e) | rhH"
for s in ph0 ph3 sw_ph0 sw_ph2 rel dbl; do row $s "$(pick v226fin_j24_${s}_o_r1 v226t1_j24_${s}_o_r1)" "$(pick v227t5_j24_${s}_rh_r1)" "$(pick v227h30_j24_${s}_rhH_r1)"; done
for f in 20 60 120; do echo "-- $f FPS: prod | rh (e) | rhH"; for s in ph0 ph3 sw_ph2 ovl120 dbl; do row $s "$(pick v226s${f}_j24_${s}_o_r1 v227h${f}_j24_${s}_o_r1)" "$(pick v227w${f}_j24_${s}_rh_r1)" "$(pick v227h${f}_j24_${s}_rhH_r1)"; done; done
echo; echo "exit227 rhH"; for l in $(ls $E | grep -E '^v227h(30|60|120|20)_j24_.*_rhH_r1\.json$' | sed 's/\.json$//'); do "$PY" $T7/exitjump227.py $l | sed 's/ | pelvis excess.*next/ | next/; s/ | SWITCH.*//'; done
