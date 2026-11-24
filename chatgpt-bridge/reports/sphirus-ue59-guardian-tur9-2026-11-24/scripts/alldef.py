import builtins,unreal as u
for k in ("MOT7","FTV","R8V","BOBV","R9V"): setattr(builtins,k,None)
for f in ("c_mot7_defaults","c_bob7_defaults","c_foot7_defaults","c_contact7_defaults","c_posture7_defaults","c_r8_defaults","c_r9_defaults"):
    exec(open(u.Paths.project_dir()+"Tools/UE59_20261124/"+f+".py",encoding="utf8").read())
print("ALLDEF9")
