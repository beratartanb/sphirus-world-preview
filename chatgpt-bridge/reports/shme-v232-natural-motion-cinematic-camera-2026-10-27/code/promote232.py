"""promote232.py (editor job): V2.32 production switch, one group at a time. builtins.V232_PROMO = {group: True | {overrides}, ...} (missing =
leave); {'rollback': True} = every V2.32 knob back to its V2.31 value. Groups:
  camera    DA CamOrbitEnabled + the orbit tuning (cinematic visual azimuth on the boom yaw: BP_GR_Player GR_SHM_CamOrbit)
  bfexit    ABP SHM224_DB_JRBwd / JRBwdM -> PSD_SHM232_JogRevBwdX, SHM231_DB_JRBwdS -> PSD_SHM232_SlowRevBwdX (B_F reversal DBs WITH the
            forward exit loop: no end-of-clip search into another B_F bin)
  loadedbf  ABP SHM230_DB_JRBwdL -> PSD_SHM232_LoadRevBwdX (loaded B_F catch-step family + exit loop; effort visible in both directions)
  startbind ABP SHM232_StartBind 1 (capsule bound to the designed speed of a start clip carrying the SHM232_SW witness while the backward
            intent holds)
  swingpelvis DA SwingPelvisComp (T6: swing target lowered by the pelvis lag after a step-up)
  floorguard  DA SwingFloorGuard (T7: a swing foot never under its planted height + guard)
Content changed in place in V2.32 (PSD_SHM231L_LoadRevFwd rebuilt with the P29 re-make + P21 / P30 production fallback; the idle-stance start
copies SHM232_IS_* in the start DBs; B_F X DBs = new assets) rolls back from Saved/Codex/SHME_V232_20261027/checkpoint/pre_v232/ (editor
closed) / by deleting the new assets. builtins.V232_SAVE saves. Prints PROMO232 {...}."""
import builtins, json, unreal as u
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
P = dict(getattr(builtins, 'V232_PROMO', {})); rb = bool(P.get('rollback'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
abp = u.load_asset(AP); cp = u.load_asset(CP); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
V = '/Game/GraceRanger/SHME/Animations/'
ABPG = {'bfexit': {'SHM224_DB_JRBwd': (V + 'V232/PSD_SHM232_JogRevBwdX', V + 'V226/PSD_SHM226_JogRevBwd'),
                   'SHM224_DB_JRBwdM': (V + 'V232/PSD_SHM232_JogRevBwdX', V + 'V226/PSD_SHM226_JogRevBwd'),
                   'SHM231_DB_JRBwdS': (V + 'V232/PSD_SHM232_SlowRevBwdX', V + 'V231/PSD_SHM231S_SlowRevBwd')},
        'loadedbf': {'SHM230_DB_JRBwdL': (V + 'V232/PSD_SHM232_LoadRevBwdX', V + 'V226/PSD_SHM226_JogRevBwd')},
        'startbind': {'SHM232_StartBind': (1.0, 0.0)}}
CAM = {'CamOrbitEnabled': (True, False), 'CamOrbitLagTau': (0.3, 0.8), 'CamOrbitFreq': (5.0, 4.0), 'CamOrbitMaxSprint': (16.0, 14.0),
       'CamOrbitMaxJog': (8.0, 8.0), 'CamOrbitMaxWalk': (2.0, 2.0), 'CamOrbitTravelW': (0.5, 0.5)}
DAG = {'camera': CAM, 'swingpelvis': {'SwingPelvisComp': (1.0, 0.0)}, 'floorguard': {'SwingFloorGuard': (1.5, 0.0)}}
out = {'groups': P, 'set': {}}
for g, kv in ABPG.items():
    if not (P.get(g) or rb): continue
    ov = P.get(g) if isinstance(P.get(g), dict) else {}
    vals = {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on)
        vals[k] = u.load_asset(val) if isinstance(val, str) else val
    set_defaults(abp, vals); out['set'][g] = {k: str(v)[:80] for k, v in vals.items()}
for g, kv in DAG.items():
    if not (P.get(g) or rb): continue
    ov = P.get(g) if isinstance(P.get(g), dict) else {}
    for k, (on, off) in kv.items():
        val = off if rb else ov.get(k, on)
        sda.set_editor_property(k, val); out['set'].setdefault(g, {})[k] = val
st, errs = compile_ok(abp); st2 = compile_ok(cp)[0]
cdo = u.get_default_object(abp.generated_class())
out['abp_after'] = {k: str(cdo.get_editor_property(k))[:70] for k in ('SHM224_DB_JRBwd', 'SHM224_DB_JRBwdM', 'SHM231_DB_JRBwdS', 'SHM230_DB_JRBwdL', 'SHM230_DB_JRFwdL', 'SHM232_StartBind', 'SHM230_LoadedOn')}
out['shm_after'] = {k: str(sda.get_editor_property(k)) for k in list(CAM) + ['SwingPelvisComp', 'SwingFloorGuard', 'IntentTickPrePhysics']}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in str(st2); out['ok'] = ok
if ok and getattr(builtins, 'V232_SAVE', False):
    save(abp, cp); sda.modify(True); u.EditorAssetLibrary.save_loaded_asset(sda, False)
    out['saved'] = True; out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PROMO232 ' + json.dumps(out, default=str))
