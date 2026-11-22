# ct6.sh <label> <plan> "<pos>" [extra python, e.g. "builtins.CT_FAT=0.9; builtins.CT_CARRY=True"] : one contact scenario (CTHZ, VSHOT/VSIDE honoured)
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
X="import builtins; builtins.CT_FAT=None; builtins.CT_CARRY=None; builtins.CT_SET=None; ${4:-pass}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261123/hk_ct6.py',encoding='utf8').read())"
DFPS=${CTHZ:-60.0} POS="$3" bash Tools/UE59_20261120/seqP.sh $1 Saved/UE59Work/plan_ct_$2.txt "$X" | grep -E "VIDREC|Error|mp4" | cut -c1-120
