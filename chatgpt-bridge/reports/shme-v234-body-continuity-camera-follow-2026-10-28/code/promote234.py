"""promote234.py (editor job, write manifest: ABP base + child + DA) - V2.34 production switch per group; builtins.V234_PROMO = {group:
True | {overrides}} or {'rollback': True}. Groups:
  loco       DA LocoFrameEnabled + LocoExploreEnabled + LocoExploreMaxSpeed 380 (the camera never changes direction / speed / facing; a
             calm walk / jog body decides to walk the held lateral direction, the camera follows the body)
  camfollow  DA CamRecMinSpeed 60 (walk follow on), CamRecWalkRate 45, CamRecFaceMax 40, CamRecTurnSide (recentre only behind a body that
             faces its travel), CamEnvEnabled (cinematic orbit tied to the brake / turn / reversal episode)
  revkeep    ABP SHM234_RevKeepOn 1 + DA RevGraceTime 0.4 (release-repress continues the reversal)
  sprintcalm ABP SHM211_DB_Sprint -> V233/SprintCalm/PSD_SHM233_SprintCalm (calmer sprint upper body)
builtins.V234_SAVE saves. Prints PROMO234 {...} incl. the rollback values."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V234_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
ABPG = {'revkeep': {'SHM234_RevKeepOn': (1.0, 0.0)},
        'sprintcalm': {'SHM211_DB_Sprint': ('/Game/GraceRanger/SHME/Animations/V233/SprintCalm/PSD_SHM233_SprintCalm', '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_SprintLoops')}}
DAG = {'loco': {'LocoFrameEnabled': (True, False), 'LocoExploreEnabled': (True, False), 'LocoExploreMaxSpeed': (380.0, 0.0)},
       'camfollow': {'CamRecMinSpeed': (60.0, 170.0), 'CamRecWalkRate': (45.0, 0.0), 'CamRecFaceMax': (40.0, 0.0), 'CamRecTurnSide': (True, False), 'CamEnvEnabled': (True, False)},
       'revkeep': {'RevGraceTime': (0.4, 0.0)}}
out = {'groups': P_, 'set': {}, 'rollback_values': {g: {k: v[1] for k, v in kv.items()} for g, kv in list(ABPG.items()) + list(DAG.items())}}
for g, kv in ABPG.items():
    if not (P_.get(g) or rb): continue
    ov = P_.get(g) if isinstance(P_.get(g), dict) else {}
    vals = {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on)
        vals[k] = u.load_asset(val) if isinstance(val, str) else val
    set_defaults(abp, vals); out['set'][g] = {k: str(v)[:90] for k, v in vals.items()}
for g, kv in DAG.items():
    if not (P_.get(g) or rb): continue
    ov = P_.get(g) if isinstance(P_.get(g), dict) else {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on); sda.set_editor_property(k, val); out['set'].setdefault(g, {})[k] = val
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k))[:90] for k in ('SHM234_RevKeepOn', 'SHM211_DB_Sprint', 'SHM233_StandBackOn')}
out['da_after'] = {k: str(sda.get_editor_property(k)) for k in ('LocoFrameEnabled', 'LocoExploreEnabled', 'LocoExploreMaxSpeed', 'CamRecEnabled', 'CamRecMinSpeed', 'CamRecMaxErr', 'CamRecWalkRate', 'CamRecFaceMax', 'CamRecTurnSide', 'CamEnvEnabled', 'RevGraceTime')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V234_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO234 ' + json.dumps(out, default=str))
