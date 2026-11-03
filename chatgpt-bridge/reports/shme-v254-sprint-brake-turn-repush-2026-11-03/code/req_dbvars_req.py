import unreal as u, json
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'
bp = u.load_asset(AP + 'Base'); cdo = u.get_default_object(u.load_asset(AP).generated_class()); out = {}
for v in [str(x) for x in B.list_variables(bp)]:
    try: val = cdo.get_editor_property(v)
    except Exception: continue
    if isinstance(val, u.PoseSearchDatabase): out[v] = val.get_name()
    elif ('SHM238' in v or 'SHM228' in v or 'Rev' in v or 'Redirect' in v) and isinstance(val, (float, bool, int)): out[v] = val
print('DBVARS254 ' + json.dumps(out, default=str))
