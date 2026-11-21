cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
HKF="$(cat Saved/UE59Work/r5/hk3_line.txt)"; T=$1; export VSHOT=1 VKEEP=1
for v in ${2:-side:90 front:0 back:180}; do
  export VSIDE="(600,${v##*:},0,95,'pelvis')"
  bash Tools/UE59_20261120/seqP.sh ${T}${v%%:*} Saved/UE59Work/${3:-planV1}.txt "$HKF" | grep -E "VIDREC"
done
echo VIEWS_DONE_$T
