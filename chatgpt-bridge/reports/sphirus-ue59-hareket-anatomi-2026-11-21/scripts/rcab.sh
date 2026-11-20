cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"
HKF="$(cat Saved/UE59Work/r4/hkp2_line.txt)"; O=Saved/UE59Work/r4/rcab_$1.txt; : > $O
for c in $2; do
  n=${c%%=*}; v=${c#*=}
  echo "import builtins; builtins.RCV=$v" > Saved/UE59Work/r4/rcv_tmp.py; echo "exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261121/c_revclip_defaults.py',encoding='utf8').read())" >> Saved/UE59Work/r4/rcv_tmp.py
  SHME_OWNER=emb SHME_KIND=control bash Tools/SHME_V2_20261014/run_v2.sh "$PWD/Saved/UE59Work/r4/rcv_tmp.py" emb_rcv 60 | tail -1 | cut -c1-60
  for p in ${3:-R:planR1}; do l=$1_${n}_${p%%:*}; f=Saved/UE59Work/${p##*:}.txt
    DFPS=${4:-60.0} bash Tools/UE59_20261120/seqP.sh $l $f "$HKF" | grep -E "VIDREC|SLOT_CH"
    echo "#### $l $v" >> $O; "$PY" Tools/UE59_20261120/an_slide2.py $l $f 6 >> $O 2>&1
  done
done
echo RCAB_DONE >> $O
