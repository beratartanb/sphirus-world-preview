import unreal as u, json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class())
out = {}
for k in dir(cdo):
    if not (k.startswith('shm2') or k.startswith('SHM2')): continue
for bv in u.BlueprintEditorLibrary.get_blueprint_variables(abp) if hasattr(u, 'BlueprintEditorLibrary') and hasattr(u.BlueprintEditorLibrary, 'get_blueprint_variables') else []:
    pass
names = []
try:
    gc = abp.generated_class()
    for p in ['SHM224_DB_JRFwd','SHM224_DB_JRFwdM','SHM224_DB_JRBwd','SHM224_DB_JRBwdM','SHM231_DB_JRBwdS','SHM231_DB_JRFwdS','SHM230_DB_JRFwdL','SHM230_DB_JRBwdL','SHM211_DB_Sprint','SHM233_DB_StandBack','SHM228_ClipSpeed','SHM227_RevHold','SHM227_HoldExit','SHM231_SlowOn','SHM230_LoadedOn','SHM234_RevKeepOn','SHM218_DB_JogPush','SHM212_DB_RevPush']:
        try:
            v = cdo.get_editor_property(p); out[p] = v.get_path_name() if hasattr(v, 'get_path_name') else v
        except Exception as e: out[p] = 'ERR ' + str(e)[:60]
except Exception as e: out['err'] = str(e)
print('PROBE235 ' + json.dumps(out, default=str))
