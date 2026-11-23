cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"; PY="/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe"; O=Saved/UE59Work/r8/sh8.txt; : > $O
t() { bash Saved/UE59Work/r8/ab8.sh $1 "{'GR_StopRel':80.0,'GR_StopLead':2000.0}" "{}" $2 $3 > /dev/null 2>&1; echo "#### $1 $2 $3" >> $O; "$PY" Tools/UE59_20261122/an_slide3.py $1 Saved/UE59Work/$2.txt 5 2>&1 | cut -c1-230 >> $O; }
t s8_30a planB8s 30; t s8_30b planB8s 30; t s8_60 planB8s 60
t s8_B30 planU_B 30; t s8_K30 planK1 30; t s8_B60 planU_B 60; t s8_Q60 planQt 60
echo SH8_DONE >> $O
