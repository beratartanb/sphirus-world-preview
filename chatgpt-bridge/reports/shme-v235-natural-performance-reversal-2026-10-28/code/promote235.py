"""promote235.py (editor job, write manifest: ABP base + child + DA + BP_GR_Player) - V2.35 production switch per group;
builtins.V235_PROMO = {group: True} or {'rollback': True}. Groups:
  rev    ABP SHM224_DB_JRFwd / JRFwdM -> V235/PSD_SHM235_JogRevFwd, SHM224_DB_JRBwd / JRBwdM -> V235/PSD_SHM235_JogRevBwdX (support-exchange
         jog reversal content, gen235_rev; continuing bias -0.5)
  route  DA RevOverHard (a real reversal request takes over a hard-turn episode at once)
  gap    DA RevGapKeep (a release shorter than RevGraceTime inside a reversal does not end the episode)
  mouse  BP_GR_Player GR233_RecMouseScale 0.35 -> 0.7 (mouse / keyboard walk follow settles in ~2.4 s instead of never)
The jog stop re-plan (gen235_stop r2-r6) was REJECTED: the V2.34 clip is restored (stop1 backup, sha1 checked by verify235).
builtins.V235_SAVE saves. Prints PROMO235 {...} incl. the rollback values."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V235_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default'); gp = u.load_asset('/Game/GraceRanger/BP_GR_Player')
F5 = '/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevFwd'; B5 = '/Game/GraceRanger/SHME/Animations/V235/PSD_SHM235_JogRevBwdX'
F4 = '/Game/GraceRanger/SHME/Animations/V226/PSD_SHM226_JogRevFwd'; B4 = '/Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX'
ABPG = {'rev': {'SHM224_DB_JRFwd': (F5, F4), 'SHM224_DB_JRFwdM': (F5, F4), 'SHM224_DB_JRBwd': (B5, B4), 'SHM224_DB_JRBwdM': (B5, B4)}}
DAG = {'route': {'RevOverHard': (True, False)}, 'gap': {'RevGapKeep': (True, False)}}
GRG = {'mouse': {'GR233_RecMouseScale': (0.7, 0.35)}}
out = {'groups': P_, 'set': {}, 'rollback_values': {g: {k: v[1] for k, v in kv.items()} for g, kv in list(ABPG.items()) + list(DAG.items()) + list(GRG.items())}}
for g, kv in ABPG.items():
    if not (P_.get(g) or rb): continue
    vals = {k: u.load_asset(off if rb else on) for k, (on, off) in kv.items()}
    set_defaults(abp, vals); out['set'][g] = {k: v.get_name() for k, v in vals.items()}
for g, kv in DAG.items():
    if not (P_.get(g) or rb): continue
    for k, (on, off) in kv.items(): sda.set_editor_property(k, off if rb else on); out['set'].setdefault(g, {})[k] = off if rb else on
for g, kv in GRG.items():
    if not (P_.get(g) or rb): continue
    vals = {k: (off if rb else on) for k, (on, off) in kv.items()}; set_defaults(gp, vals); out['set'][g] = vals
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]; st3 = compile_ok(gp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k).get_name()) for k in ('SHM224_DB_JRFwd', 'SHM224_DB_JRFwdM', 'SHM224_DB_JRBwd', 'SHM224_DB_JRBwdM')}
out['da_after'] = {'RevOverHard': sda.get_editor_property('RevOverHard'), 'RevGapKeep': sda.get_editor_property('RevGapKeep')}
out['gr_after'] = {'GR233_RecMouseScale': u.get_default_object(gp.generated_class()).get_editor_property('GR233_RecMouseScale'),
                   'child': u.get_default_object(u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class()).get_editor_property('GR233_RecMouseScale')}
ok = all('UP_TO_DATE' in str(s) for s in (st, st2, st3)) and not errs; out['ok'] = ok
if ok and getattr(builtins, 'V235_SAVE', False):
    save(abp, cp, gp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO235 ' + json.dumps(out, default=str))
