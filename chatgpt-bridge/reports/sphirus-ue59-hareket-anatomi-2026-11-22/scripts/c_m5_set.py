# c_m5_set.py (control): A/B overrides for the round-5 motion defaults. Reads Saved/UE59Work/r5/m5v.json into builtins.M5V and runs c_motion5_defaults.py.
import json, builtins, os, unreal as u
D = u.Paths.convert_relative_path_to_full(u.Paths.project_dir())
P = os.path.join(D, 'Tools', 'UE59_20261122', 'c_motion5_defaults.py'); R = os.path.join(D, 'Saved', 'UE59Work', 'r5', 'm5v.json')
builtins.M5V = json.load(open(R)) if os.path.exists(R) else {}
exec(compile(open(P, encoding='utf8').read(), P, 'exec'))
print('M5SET', builtins.M5V)
