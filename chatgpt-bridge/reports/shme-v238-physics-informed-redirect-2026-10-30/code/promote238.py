"""promote238.py (editor job, write manifest: ABP base + child) - V2.38 production switch (ABP class defaults only; content = new assets,
graph patches = install238_yaw / fam / hold / gaze / gaze2, all installed OFF behind these knobs).
builtins.V238_PROMO = {'cut': True, 'gaze': True} or {'rollback': True}. Groups:
  cut   SHM210_JogCutMode 1 (jog lateral episodes routed), SHM_RedirectDB_JL -> V238/PSD_SHM238_JogCut (48 physics-planned cut bins),
        SHM238_Yaw 1 (clip-bound heading + route hold + recovery-family guard), SHM238_GuardS 1.6
        rollback: 0 / Redirect/PSD_SHM_Redirect_JogLateral / 0 / 0.8
  gaze  SHM238_Gaze 1 (travel gaze while the camera recentre is pending / active)                             rollback 0
builtins.V238_SAVE saves. Prints PROMO238 {...} incl. the rollback values."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P_ = dict(getattr(builtins, 'V238_PROMO', {})); rb = bool(P_.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
LS = u.EditorLoadingAndSavingUtils
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
dirty = list(LS.get_dirty_content_packages())                      # harness abp_flags dirty the ABP CDOs: reload from disk first
if dirty:
    assert all(p.get_name() in (AP, CP) or '/Profiles/' in p.get_name() or '/SHME/DA_' in p.get_name() or 'DA_PBI' in p.get_name() for p in dirty), [p.get_name() for p in dirty]
    LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
abp = u.load_asset(AP); cp = u.load_asset(CP)
V8 = '/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'; JL0 = '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogLateral'
G = {'cut': {'SHM210_JogCutMode': (1.0, 0.0), 'SHM_RedirectDB_JL': (V8, JL0), 'SHM238_Yaw': (1.0, 0.0), 'SHM238_GuardS': (1.6, 0.8)},
     'gaze': {'SHM238_Gaze': (1.0, 0.0)}}
out = {'groups': P_, 'set': {}, 'rollback_values': {g: {k: v[1] for k, v in kv.items()} for g, kv in G.items()}}
for g, kv in G.items():
    if not (P_.get(g) or rb): continue
    vals = {}
    for k, (on, off) in kv.items():
        v = off if rb else on; vals[k] = u.load_asset(v) if isinstance(v, str) else float(v)
        assert vals[k] is not None, (g, k)
    set_defaults(abp, vals); out['set'][g] = {k: (v.get_name() if hasattr(v, 'get_name') else v) for k, v in vals.items()}
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
def rd(k):
    v = cdo.get_editor_property(k); return v.get_name() if hasattr(v, 'get_name') else float(v)
out['abp_after'] = {k: rd(k) for kv in G.values() for k in kv}
out['status'] = [str(st), str(st2)]; out['errs'] = [str(e)[:200] for e in errs[:6]]
ok = all('UP_TO_DATE' in str(s) for s in (st, st2)) and not errs; out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False):
    save(abp, cp); out['saved'] = True
    out['dirty_after'] = [p.get_name() for p in LS.get_dirty_content_packages()]
print('PROMO238 ' + json.dumps(out, default=str))
