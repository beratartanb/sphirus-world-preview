#!/bin/bash
# tables228.sh : A) fixed 30 slip (height | contact-start): prod (V2.26 fin) | V2.27 rh pass e | V2.28 rhC | rhCR. B) FPS sweep 20/60/120: prod | V2.27 rh | V2.28 rhC. C) real time.
cd "/c/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS" || exit 1
PY="/c/Program Files/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; T5=Tools/SHME_V225_20261023; T7=Tools/SHME_V227_20261024; E=Saved/Codex/SHME_V1_20260925/Evidence
pick() { for c in "$@"; do [ -f $E/$c.json ] && { echo $c; return; }; done; echo ""; }
p25() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T5/plant225.py $2 $1 2>/dev/null | grep -o "worst net *[0-9.]*" | grep -o "[0-9.]*$"; }
p27() { [ -n "$1" ] || { echo "-"; return; }; "$PY" $T7/plant227.py $2 $1 2>/dev/null | grep -o "contact-start worst *[0-9.]*" | grep -o "[0-9.]*$"; }
row() { printf "%-7s %5s | %5s %5s | %5s %5s | %5s %5s | %5s\n" "$1" "$(p25 "$2" --fam=Pivot)" "$(p27 "$2" --fam=Pivot)" "$(p25 "$3")" "$(p27 "$3")" "$(p25 "$4")" "$(p27 "$4")" "$(p25 "$5")" "$(p27 "$5")"; }
echo "A) fixed 30: prod | V2.27 rh (e) | V2.28 rhC | V2.28 rhCR"
for s in ph0 ph3 sw_ph0 sw_ph2 rel dbl; do row $s "$(pick v227fin_j24_${s}_o_r1 v226fin_j24_${s}_o_r1)" "$(pick v227t5_j24_${s}_rh_r1)" "$(pick v228t2_j24_${s}_rhC_r1)" "$(pick v228t4_j24_${s}_rhCR_r1)"; done
echo; echo "B) FPS: prod | V2.27 rh (e) | V2.28 rhC | V2.28 rhCR"
for f in 20 60 120; do echo "-- $f FPS"; for s in ph0 ph3 sw_ph2 ovl120 dbl rel; do row $s "$(pick v226s${f}_j24_${s}_o_r1 v227h${f}_j24_${s}_o_r1)" "$(pick v227w${f}_j24_${s}_rh_r1)" "$(pick v228w${f}_j24_${s}_rhC_r1)" "$(pick v228x${f}_j24_${s}_rhCR_r1)"; done; done
echo; echo "C) real time (cold first): prod finrt | V2.28 rt rhC"
for s in ph0 sw_ph2 dbl ph3; do row $s "$(pick v227finrt_j24_${s}_o_r1)" "" "$(pick v228rt_j24_${s}_rhC_r1)" ""; done
