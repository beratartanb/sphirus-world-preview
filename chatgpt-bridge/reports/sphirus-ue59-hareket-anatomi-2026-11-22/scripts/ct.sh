# ct.sh <label> "<scene tuple or None>" <planfile> [fat] : one contact scenario (60 Hz data unless CTHZ is set, MoveTest map)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
X="import builtins; builtins.CT_SCENE=$2; builtins.CT_FAT=${4:-None}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261122/hk_ct.py',encoding='utf8').read())"
DFPS=${CTHZ:-60.0} POS="${CTPOS:--6000 -6000 92 0}" bash Tools/UE59_20261120/seqP.sh $1 $3 "$X" | grep -E "VIDREC|Error" | cut -c1-120
