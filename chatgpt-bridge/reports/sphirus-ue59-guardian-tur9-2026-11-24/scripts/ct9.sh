# ct9.sh <label> <plan> "<pos>" [extra python] : contact scenario with the round-9 fall hook (CTHZ, VSHOT/VSIDE honoured); labels never reused
cd "/c/Users/berat/Documents/Unreal Projects/sphirus_UE59"
[ -f Saved/Codex/Grip_20261106/rec/$1.json ] && { echo "EXISTS $1"; exit 0; }
X="import builtins; builtins.CT_FAT=None; builtins.CT_CARRY=None; builtins.CT_SET=None; builtins.CT_PROP=None; builtins.CT_EXS=None; builtins.CT_EXM=None; builtins.CT_EXTRA=None; ${4:-pass}; exec(open(u.Paths.project_dir()+'Tools/UE59_20261124/hk_fall9.py',encoding='utf8').read())"
DFPS=${CTHZ:-60.0} POS="$3" bash Tools/UE59_20261120/seqP.sh $1 Saved/UE59Work/plan_ct_$2.txt "$X" | grep -E "VIDREC|Error|mp4" | cut -c1-120
