"""promote233.py (editor job, write manifest: ABP base + child + DA) - V2.33 production switch per group; builtins.V233_PROMO = {group:
True | {overrides}} or {'rollback': True}. Groups:
  standback  ABP SHM233_StandBackOn 2 (entry override) + SHM233_DB_StandBack -> V233/PSD_SHM233_StandBackStart2 (true-stand backward start)
  camrec     DA CamRecEnabled true (auto recentre behind the stable travel + input frame latch; device profile in BP_GR_Player:
             gamepad 1.0, mouse / keyboard 0.35)
  sprintcalm ABP SHM211_DB_Sprint -> V233/SprintCalm/PSD_SHM233_SprintCalm (calmer sprint upper body)  [only if accepted]
builtins.V233_SAVE saves. Prints PROMO233 {...}."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V233_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
V = '/Game/GraceRanger/SHME/Animations/V233/'
cdo0 = u.get_default_object(abp.generated_class())
ABPG = {'standback': {'SHM233_StandBackOn': (2.0, 0.0), 'SHM233_DB_StandBack': (V + 'PSD_SHM233_StandBackStart2', V + 'PSD_SHM233_StandBackStart')},
        'sprintcalm': {'SHM211_DB_Sprint': (V + 'SprintCalm/PSD_SHM233_SprintCalm', None)}}
DAG = {'camrec': {'CamRecEnabled': (True, False), 'CamRecMaxErr': (110.0, 150.0), 'CamRecMinSpeed': (170.0, 60.0)}}   # MinSpeed 170: jog (>= 190) / sprint only - walk recentre costs a planted-foot slide (open 5C)   # 110: backward-diagonal travel (135 deg) never turns the view (f60 jback)
out = {'groups': P_, 'set': {}}
for g, kv in ABPG.items():
    if not (P_.get(g) or rb): continue
    ov = P_.get(g) if isinstance(P_.get(g), dict) else {}
    vals = {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on)
        if val is None: continue
        vals[k] = u.load_asset(val) if isinstance(val, str) else val
    if vals: set_defaults(abp, vals); out['set'][g] = {k: str(v)[:80] for k, v in vals.items()}
for g, kv in DAG.items():
    if not (P_.get(g) or rb): continue
    ov = P_.get(g) if isinstance(P_.get(g), dict) else {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on); sda.set_editor_property(k, val); out['set'].setdefault(g, {})[k] = val
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k))[:80] for k in ('SHM233_StandBackOn', 'SHM233_DB_StandBack', 'SHM211_DB_Sprint')}
out['da_after'] = {k: str(sda.get_editor_property(k)) for k in ('CamRecEnabled', 'CamOrbitEnabled', 'IntentTickPrePhysics')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V233_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO233 ' + json.dumps(out, default=str))
